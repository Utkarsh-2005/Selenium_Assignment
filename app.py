import os
import time
import random
from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import uuid
from flask_cors import CORS

# Load environment variables
load_dotenv()
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
MONGO_URI = os.getenv("MONGO_URI")

if not TWITTER_USERNAME or not TWITTER_EMAIL or not TWITTER_PASSWORD or not MONGO_URI:
    raise ValueError("Ensure .env contains TWITTER_USERNAME, TWITTER_EMAIL, TWITTER_PASSWORD, and MONGO_URI.")

# Flask app setup
app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["stir_tech"]
collection = db["trending_topics"]

# List of proxy servers
PROXIES = ["https://52.35.240.119:1080",
           "https://47.251.122.81:8888"]

def get_driver():
    """Sets up ChromeDriver with a rotating proxy."""
    options = Options()

    # Randomly select a proxy from the list
    # proxy = random.choice(PROXIES)
    # options.add_argument(f'--proxy-server={proxy}')

    # Set up ChromeDriver
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def fetch_trending_topics():
    """Fetches top trending topics on Twitter using Selenium."""
    driver = get_driver()
    wait = WebDriverWait(driver, 10)
    ip_address = random.choice(PROXIES).split("//")[1]  # Extract IP address
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Open Twitter login page
        driver.get("https://x.com/i/flow/login")

        # Step 1: Enter username
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        username_field.send_keys(TWITTER_USERNAME)
        username_field.send_keys(Keys.RETURN)
        time.sleep(2)

        # Step 2: Enter email (if prompted)
        try:
            email_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
            email_field.send_keys(TWITTER_EMAIL)
            email_field.send_keys(Keys.RETURN)
            time.sleep(2)
        except Exception:
            print("Email prompt not required.")

        # Step 3: Enter password
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # Scroll to ensure the "Trending" section is loaded
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(3)

        # Wait for the "Timeline: Trending now" div to appear
        trending_section = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']")))

        # Find trend elements
        trend_elements = trending_section.find_elements(By.XPATH, ".//div[@role='link']/div/div[2]")

        # Extract text from the trend elements (top 5 trends)
        trends = [trend.text for trend in trend_elements if trend.text][:5]

        # Save data to MongoDB
        record = {
            "_id": unique_id,
            "trends": trends,
            "timestamp": timestamp,
            "ip_address": ip_address
        }
        collection.insert_one(record)

        return record
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script", methods=["GET"])
def run_script():
    data = fetch_trending_topics()
    if data:
        return jsonify({"success": True, "data": data})
    else:
        return jsonify({"success": False, "error": "Failed to fetch trends"})

if __name__ == "__main__":
    app.run(debug=True)
