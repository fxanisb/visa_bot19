from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# =========================
# Telegram Settings
# =========================
TOKEN = "8711953337:AAGsLQ1DgUGnwCKl4-mrcNnQAyLDCoRtw9Y"
CHAT_ID = "5898450345"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

# =========================
# Start Browser
# =========================
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

# =========================
# Step 1: Open Main Website
# =========================
driver.get("https://mosaicvisa.com/")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Step 2: Click "Select Office"
wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//*[contains(text(),'Select Office')]")
)).click()

# Step 3: Choose "Algiers"
wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//*[contains(text(),'Algiers')]")
)).click()

# Wait page load
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Scroll down
driver.execute_script("window.scrollBy(0, 600);")

# Go directly to appointment mission page
driver.get("https://appointment.mosaicvisa.com/mission/4")

wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Wait mission page
wait.until(EC.url_contains("appointment.mosaicvisa.com"))

# Step 5: Click "Algiers" on mission page
wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//*[contains(text(),'Algiers')]")
)).click()

# Wait calendar page
wait.until(EC.url_contains("calendar"))

print("✅ Reached calendar page")
send_telegram("TEST MESSAGE 🚀")

# =========================
# Appointment Checking Loop
# =========================
while True:
    try:
        time.sleep(5)

        # Find all elements that contain the word "Reserved"
        reserved_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'Reserved')]")
        appointment_found = False

        for element in reserved_elements:
            text = element.text.strip()   # Example: "Reserved 0"

            # Split text into words
            parts = text.split()

            for part in parts:
                # Check if part is a number
                if part.isdigit():
                    number = int(part)

                    # If number is greater than 0 → Appointment available
                    if number > 0:
                        send_telegram("🚨 Appointment Available in Algiers!")
                        print("🚨 Appointment Found!")
                        appointment_found = True
                        break

        if not appointment_found:
            print("No appointments available...")

        # Refresh every 50 seconds
        time.sleep(50)
        driver.refresh()


    except Exception as e:
        print("Error:", e)

        time.sleep(50)