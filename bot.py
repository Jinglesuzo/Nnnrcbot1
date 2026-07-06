from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import csv
import os
import sys
import random
import string

class NRCBot:
    def __init__(self):
        self.step = 0
        self.logins = []
        self.load_logins()
        self.setup_driver()

    def setup_driver(self):
        options = Options()
        
        # === TRACKING BLOCKED (JavaScript ENABLED) ===
        
        # 1. Hide automation flags
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # 2. Block cookies and tracking
        options.add_argument("--block-third-party-cookies")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.cookies": 2,  # Block all cookies
            "profile.default_content_setting_values.images": 1,   # Allow images
            "profile.default_content_setting_values.javascript": 1, # ✅ JavaScript ENABLED
            "profile.default_content_setting_values.plugins": 1,   # Allow plugins
            "profile.default_content_setting_values.popups": 2,    # Block popups
            "profile.default_content_setting_values.geolocation": 2, # Block geolocation
            "profile.default_content_setting_values.notifications": 2, # Block notifications
        })
        
        # 3. Disable tracking features (but keep JavaScript)
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-component-update")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-domain-reliability")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-prompt-on-repost")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-webrtc")
        
        # 4. Use realistic user-agent (without "Headless")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # 5. Additional privacy settings
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        
        # 6. Headless mode (remove if you want to see the browser)
        options.add_argument("--headless=new")
        
        print("🔄 Starting Chrome with tracking blocked...")
        try:
            service = Service('/usr/bin/chromedriver')
            self.driver = webdriver.Chrome(service=service, options=options)
        except:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver property (hide automation)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Chrome started with tracking blocked!")

    def screenshot(self, name):
        self.step += 1
        try:
            filename = f"bot_{self.step:03d}_{name}.png"
            self.driver.save_screenshot(filename)
            print(f"   📸 {filename}")
        except:
            pass

    def load_logins(self):
        try:
            with open('logins.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                self.logins = []
                for row in reader:
                    if len(row) >= 2:
                        self.logins.append({
                            'phone': row[0].strip(),
                            'password': row[1].strip()
                        })
            print(f"📋 Loaded {len(self.logins)} login(s)")
        except Exception as e:
            print(f"❌ Error loading logins.csv: {e}")
            self.logins = [{'phone': '08057536473', 'password': 'people56'}]

    def generate_password(self):
        """Generate a human-like password (letters + numbers)"""
        words = ['apple', 'banana', 'cherry', 'dragon', 'eagle', 'falcon', 
                 'garden', 'honey', 'island', 'jungle', 'knight', 'lion',
                 'magic', 'noble', 'ocean', 'piano', 'queen', 'river',
                 'star', 'tiger', 'uncle', 'victor', 'water', 'zebra']
        word = random.choice(words)
        number = random.randint(10, 999)
        if random.random() > 0.5:
            word = word.capitalize()
        return f"{word}{number}"

    def clear_field(self, element):
        try:
            element.click()
            time.sleep(0.1)
            element.clear()
            time.sleep(0.1)
            return True
        except:
            return False

    def type_text(self, element, text):
        self.clear_field(element)
        # Type like a human (with small random delays)
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        time.sleep(0.1)

    def click_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(random.uniform(0.3, 0.6))
        self.driver.execute_script("arguments[0].click();", element)

    def find_login_button(self):
        try:
            btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in now')]")
            return btn
        except:
            try:
                btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                return btn
            except:
                return None

    def remove_important_notice(self):
        try:
            news_btn = self.driver.find_element(By.XPATH, "//*[contains(text(), 'NEWS')]")
            if news_btn.is_displayed():
                self.click_element(news_btn)
                time.sleep(1)
                try:
                    close_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Got it')] | //*[text()='×']")
                    if close_btn.is_displayed():
                        self.click_element(close_btn)
                except:
                    pass
                return True
        except:
            pass
        return True

    def do_tasks(self):
        print("   📋 Doing tasks...")
        
        try:
            task_tab = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Task')]")
            self.click_element(task_tab)
            time.sleep(1)
        except:
            pass
        
        total = 0
        for i in range(6):
            try:
                read_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'read')]")
                if read_btn.is_displayed() and read_btn.is_enabled():
                    self.click_element(read_btn)
                    total += 1
                    print(f"   📖 Task {total} started")
                    time.sleep(20)
                    print(f"   ✅ Task {total} done")
            except:
                break
        
        print(f"   ✅ Completed {total} tasks")
        return total

    def login(self, phone, password):
        print(f"\n🔑 Logging in: {phone}")
        
        try:
            self.driver.get("https://nnnrc.com/#/login")
            time.sleep(2)
            self.screenshot("01_login_page")
            
            phone_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Please enter your phone number']"))
            )
            self.type_text(phone_field, phone)
            print(f"   ✅ Phone: {phone}")
            self.screenshot("02_phone_entered")
            
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Please enter login password']"))
            )
            self.type_text(password_field, password)
            print(f"   ✅ Password entered")
            self.screenshot("03_password_entered")
            
            login_btn = self.find_login_button()
            if login_btn:
                self.click_element(login_btn)
                print(f"   ✅ Clicked login")
                self.screenshot("04_after_login_click")
            else:
                print(f"   ❌ Login button not found")
                self.screenshot("04_login_button_not_found")
                return False
            
            time.sleep(5)
            self.screenshot("05_after_login_wait")
            
            page = self.driver.page_source.lower()
            if "important notice" in page or "cooperative wealth zone" in page:
                print(f"   ✅ Login success!")
                self.screenshot("06_login_success")
                return True
            else:
                print(f"   ❌ Login failed")
                self.screenshot("06_login_failed")
                return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.screenshot("06_login_error")
            return False

    def logout(self):
        try:
            self.driver.get("https://nnnrc.com/#/logout")
            time.sleep(2)
            print("   ✅ Logged out")
            self.screenshot("07_logged_out")
        except:
            pass

    def run(self):
        print("="*50)
        print("🤖 BOT WITH TRACKING BLOCKED")
        print("="*50)

        for login_data in self.logins:
            phone = login_data['phone']
            password = login_data['password']
            print(f"\n📱 Account: {phone}")
            
            if self.login(phone, password):
                self.remove_important_notice()
                self.do_tasks()
                self.logout()
            else:
                print(f"   ❌ FAILED for {phone}")
            
            time.sleep(2)

        self.driver.quit()
        print(f"\n✅ Done!")

if __name__ == "__main__":
    bot = NRCBot()
    bot.run()