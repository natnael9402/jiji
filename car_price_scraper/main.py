import ssl
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        # Create a default SSL context.
        context = ssl.create_default_context()
        # Disable hostname checking so we can set verify_mode to CERT_NONE.
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=context
        )

app = FastAPI()

@app.get("/car-prices/{car_model}")
def get_car_price(car_model: str):
    url = f"https://jiji.com.et/search?query={car_model}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    session = requests.Session()
    session.mount("https://", TLSAdapter())
    
    try:
        response = session.get(url, headers=headers)
    except requests.exceptions.SSLError as e:
        return JSONResponse(
            content={"error": f"SSL Error: {e}"},
            status_code=500
        )
    
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []
    
    # Find listing anchor tags by their class.
    listing_elements = soup.find_all("a", class_="qa-advert-list-item")
    
    for element in listing_elements:
        relative_url = element.get("href")
        listing_url = (
            f"https://jiji.com.et{relative_url}"
            if relative_url and relative_url.startswith("/")
            else relative_url
        )
        
        price_elem = element.find("div", class_="qa-advert-price")
        price = price_elem.text.strip() if price_elem else "N/A"
        
        title_elem = element.find("div", class_="b-advert-title-inner")
        title = title_elem.text.strip() if title_elem else "N/A"
        
        # Extract the first image found within the listing.
        image_elem = element.find("img")
        image_url = image_elem.get("src") if image_elem else "N/A"
        
        listings.append({
            "title": title,
            "price": price,
            "url": listing_url,
            "image": image_url
        })
    
    return JSONResponse(content={"car_model": car_model, "listings": listings})
