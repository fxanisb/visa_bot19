from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

# =====================
# Telegram settings
# =====================

TOKEN = 8711953337:AAGsLQ1DgUGnwCKl4-mrcNnQAyLDCoRtw9Y
CHAT_ID = "5898450345"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

# =====================
# Chrome settings
# =====================

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 20)

# =====================
# Open mission page
# =====================

driver.get("https://appointment.mosaicvisa.com/mission/4")

wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# click Algiers
wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//*[contains(text(),'Algiers')]")
)).click()

wait.until(EC.url_contains("calendar"))

print("وصلنا صفحة المواعيد")

send_telegram("🤖 Bot started checking appointments")

# =====================
# checking loop
# =====================

while True:

    try:

        print("Checking...")

        html = driver.page_source

        found = False

        for number in range(1,200):

            if f">{number}<" in html:

                send_telegram(f"🚨 Appointment available: {number}")

                print("Appointment Found")

                found = True

                break

        if not found:
            print("No appointments")

        time.sleep(50)

        driver.refresh()

    except Exception as e:

        print("Error:", e)

        time.sleep(50)
