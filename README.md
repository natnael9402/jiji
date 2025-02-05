# Car Price Scraper API

## Overview
The **Car Price Scraper API** is a FastAPI-based web service that scrapes car listings from **Jiji Ethiopia** in real time. It allows users to search for car models and retrieve key details such as:
- **Car Title**
- **Price**
- **Listing URL**
- **Image URL**

This API is designed for research and informational purposes. Please ensure compliance with web scraping policies and ethical guidelines.

---

## Features
✅ **Real-time Car Listing Search**  
✅ **Extracts Key Listing Details**  
✅ **Returns JSON-formatted Data**  
✅ **Fast & Lightweight API**  

---

## Technologies Used
- **FastAPI** - Modern web framework for building APIs.
- **Uvicorn** - High-performance ASGI server.
- **BeautifulSoup4** - HTML parsing for web scraping.
- **Requests** - Handling HTTP requests.
- **Python 3.7+** - Required for running the API.

---

## Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/natnael9402/jiji.git
cd jiji
cd car-price-scraper
```

### 2️⃣ Create and Activate a Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the API Server
```bash
python -m uvicorn main:app --reload
```
The server will start at: **http://127.0.0.1:8000**

---

## API Usage
### Endpoint: **Search for Car Prices**
```http
GET /car-prices/{car_model}
```
- **Path Parameter:** `car_model` (e.g., `tesla`, `toyota`)

### Example Request
```http
GET http://127.0.0.1:8000/car-prices/tesla
```

### Example JSON Response
```json
{
  "car_model": "tesla",
  "listings": [
    {
      "title": "New Tesla Model Y 2024 White",
      "price": "ETB 8,400,000",
      "url": "https://jiji.ethiopia.com/bole/cars/tesla-model-y-2024.html",
      "image": "https://pictures-ethiopia.jijistatic.com/sample-image.jpg"
    }
  ]
}
```

---

## SSL Certificate Handling
This API includes a custom **TLS adapter** to bypass SSL verification issues when scraping Jiji Ethiopia. However, **this is not recommended for production environments**.

---

## Contributing 🤝
Want to improve this project? Feel free to **fork** it and submit a **pull request**! 🚀

---

