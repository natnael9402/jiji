import ssl
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from typing import List, Dict

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

def scrape_jiji(car_model: str) -> List[Dict]:
    url = f"https://jiji.com.et/search?query={car_model}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    session = requests.Session()
    session.mount("https://", TLSAdapter())
    
    try:
        response = session.get(url, headers=headers)
    except requests.exceptions.SSLError as e:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []
    
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
        
        image_elem = element.find("img")
        image_url = image_elem.get("src") if image_elem else "N/A"
        
        listings.append({
            "title": title,
            "price": price,
            "url": listing_url,
            "image": image_url,
            "source": "jiji.com.et"
        })
    
    return listings

def scrape_mekina(car_model: str) -> List[Dict]:
    url = f"https://www.mekina.net/cars/search?q={car_model}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []
    
    # Find all car listing cards
    listing_elements = soup.find_all("a", class_="cur")
    
    for element in listing_elements:
        # Extract title
        title_elem = element.find("div", class_="text-sm sm:text-md")
        title = title_elem.text.strip() if title_elem else "N/A"
        
        # Extract price
        price_elem = element.find("div", class_="flex flex-col justify-between bg-primary-main")
        if price_elem:
            price_text = price_elem.text.strip()
            price = price_text.split("(")[0].strip()  # Remove the (Negotiable) part
        else:
            price = "N/A"
        
        # Extract URL
        listing_url = f"https://www.mekina.net{element.get('href')}" if element.get('href') else "N/A"
        
        # Extract image
        image_elem = element.find("img")
        if image_elem and image_elem.get("src"):
            image_url = f"https://www.mekina.net{image_elem.get('src')}"
        else:
            image_url = "N/A"
        
        # Extract phone number
        phone_elem = element.find("div", class_="mt-3 text-sm")
        phone = phone_elem.text.strip() if phone_elem else "N/A"
        
        listings.append({
            "title": title,
            "price": price,
            "url": listing_url,
            "image": image_url,
            "phone": phone,
            "source": "mekina.net"
        })
    
    return listings

@app.get("/car-prices/{car_model}")
def get_car_price(car_model: str):
    # Scrape from both websites
    jiji_listings = scrape_jiji(car_model)
    mekina_listings = scrape_mekina(car_model)
    
    # Combine results
    all_listings = jiji_listings + mekina_listings
    
    return JSONResponse(content={
        "car_model": car_model,
        "total_listings": len(all_listings),
        "listings": all_listings
    })
