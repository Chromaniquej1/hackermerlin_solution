from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from config import HEADLESS_MODE

class HackMerlinBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        if HEADLESS_MODE:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://hackmerlin.io/")
        self.wait = WebDriverWait(self.driver, 15)
        time.sleep(3)  # Wait for JS to load

    def send_prompt(self, prompt):
        try:
            # Assuming input is a textarea or input with placeholder "Ask me anything..."
            input_selector = "textarea[placeholder*='Ask'] or input[placeholder*='Ask']"
            input_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, input_selector)))
            input_field.clear()
            input_field.send_keys(prompt)
            input_field.submit()
            
            # Wait for response (look for new message div)
            time.sleep(5)  # Adjust based on response time
            response_selector = ".message:last-child, .response, div[role='log'] > div:last-child"
            response_elem = self.driver.find_element(By.CSS_SELECTOR, response_selector)
            response = response_elem.text
            return response
        except TimeoutException:
            raise Exception("Timeout waiting for input/response")

    def enter_password(self, password):
        try:
            # After revealing, a password input appears; assume ID or class
            pass_selector = "input[type='password'], #password-input"
            pass_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, pass_selector)))
            pass_input.clear()
            pass_input.send_keys(password)
            pass_input.submit()
            time.sleep(3)
            # Check if level advanced (e.g., URL change or text)
            if "Level" in self.driver.page_source and str(int(self.get_current_level()) + 1) in self.driver.page_source:
                return True
            return False
        except NoSuchElementException:
            raise Exception("Password input not found")

    def get_current_level(self):
        try:
            level_selector = "h1:contains('Level'), .level-header"
            level_elem = self.driver.find_element(By.CSS_SELECTOR, level_selector)
            level_text = level_elem.text
            return int(level_text.split()[1]) if "Level" in level_text else 1
        except:
            return 1

    def close(self):
        self.driver.quit()