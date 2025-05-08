import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

#Get your email credentials
load_dotenv()
EMAIL = os.getenv('EMAIL')
PW = os.getenv('PW')
GMAIL_PW = os.getenv('GMAIL_PW')
first_name = "Mona"

#Drive to the website
driver = webdriver.Chrome()
driver.get("https://ticketsale.wimbledon.com/content")

#Wait for the "Accept Cookies" button to be clickable and click it
try:
    accept_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
    )
    accept_btn.click()
except:
    print("No cookie popup appeared, or it was already dismissed.")


#username_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username")))
time.sleep(5)
driver.execute_script("""
    const email = document.getElementById('loginID');
    email.value = arguments[0];
    email.dispatchEvent(new Event('input', { bubbles: true }));
""", EMAIL)

time.sleep(5)
driver.execute_script("""
    const pw = document.getElementById('password');
    pw.value = arguments[0];
    pw.dispatchEvent(new Event('input', { bubbles: true }));
""", PW)

#Click enter
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
time.sleep(5)

#Manually solve captcha while in dev
input("Please log in manually and solve the captcha. Press Enter to continue...")
time.sleep(5)

#Now that we're on the page, let's go through it
#Want to find by court heading and card heading
elements = driver.find_elements(By.XPATH,
    "//h2[contains(@class, 'stx-SectionHeading')] | //div[contains(@class, 'stx-ProductCard')]"
)

current_court = None

for element in elements:
    if element.tag_name == "h2":
        current_court = element.text
        print(f"Searching for tickets on {current_court}")
    elif "stx-ProductCard" in element.get_attribute("class"):
        #If there is no sold out indicator, the ticket is assumed to be available
        try:
            element.find_element(By.CLASS_NAME, "stx-SoldOutIndicator")
            print(f"No tickets found on {current_court}")
        except NoSuchElementException:
            available_date_time = element.find_element(By.XPATH, '//*[@id="catalog"]/div/div[1]/div/div/div[3]/div/div/div[3]/div/div/div/p').text
            print(f"Available ticket on {current_court} at {available_date_time}")


