from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC



import os
import time


# Page Objects
class LoginPage:
    def __init__(self, browser):
        self.browser = browser
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CLASS_NAME, "btn")

    def load(self, url):
        self.browser.get(url)

    def login(self, username, password):
        self.browser.find_element(*self.username_input).send_keys(username)
        self.browser.find_element(*self.password_input).send_keys(password)
        self.browser.find_element(*self.login_button).click()


class MainPage:
    def __init__(self, browser):
        self.browser = browser
        self.edit_button = (By.CLASS_NAME, "edit-btn")
        self.save_button = (By.CLASS_NAME, "save-btn")
        self.logout_button = (By.CLASS_NAME, "logout-btn")

    def edit_profile(self, username, email):
        self.browser.find_element(*self.edit_button).click()
        username_field = self.browser.find_element(By.CSS_SELECTOR, "input[v-model='editedUser.username']")
        username_field.clear()
        username_field.send_keys(username)
        email_field = self.browser.find_element(By.CSS_SELECTOR, "input[v-model='editedUser.email']")
        email_field.clear()
        email_field.send_keys(email)
        self.browser.find_element(*self.save_button).click()

    def logout(self):
        self.browser.find_element(*self.logout_button).click()


# Test Cases
class UserAccountTests(StaticLiveServerTestCase):

    host = '127.0.0.1'  # Use 127.0.0.1 instead of localhost
    port = 8000  # Set the desired fixed port
    def setUp(self):
        # Use environment variable or default path for ChromeDriver
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH", r"C:\Users\nisha\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
        service = ChromeService(chromedriver_path)
        self.browser = WebDriver(service=service)
        self.wait = WebDriverWait(self.browser, 20)

        # Use environment variable to dynamically set base URL for redirection checks
        self.base_url = os.getenv("BASE_URL")  # Change default as needed

    def tearDown(self):
        self.browser.quit()
    
    def test_signup(self):
        self.browser.get(f"{self.live_server_url}/signup/")
        self.browser.find_element(By.ID, "username").send_keys("testuser")
        self.browser.find_element(By.ID, "email").send_keys("testuser@example.com")
        self.browser.find_element(By.ID, "DOB").send_keys("2000-01-01")
        self.browser.find_element(By.ID, "password1").send_keys("Password123!")
        self.browser.find_element(By.ID, "password2").send_keys("Password123!")
        self.browser.find_element(By.CLASS_NAME, "btn").click()

        logout_button = WebDriverWait(self.browser, 10).until(
            lambda browser: browser.find_element(By.CLASS_NAME, "logout-btn")
        )
        self.assertIsNotNone(logout_button)  # Ensure the logout button exists
        

    def test_login(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(username="testuser", password="Password123!",email = "testuser@example.com", DOB = "2000-01-01")

        login_page = LoginPage(self.browser)
        login_page.load(f"{self.live_server_url}/")
        login_page.login("testuser", "Password123!")

        logout_button = WebDriverWait(self.browser, 10).until(
            lambda browser: browser.find_element(By.CLASS_NAME, "logout-btn")
        )
        self.assertIsNotNone(logout_button)  # Ensure the logout button exists
        

    

    def test_edit_user_profile(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(username="testuser3", password="Password12345!",email = "testuser3@example.com", DOB = "2004-03-05")

        login_page = LoginPage(self.browser)
        login_page.load(f"{self.live_server_url}/")
        login_page.login("testuser3", "Password12345!")
        logout_button = WebDriverWait(self.browser, 10).until(
            lambda browser: browser.find_element(By.CLASS_NAME, "logout-btn")
        )
        
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "edit-btn"))
        ).click()

        username_field = self.browser.find_element(By.CSS_SELECTOR, "input[type='text']")
        username_field.clear()
        username_field.send_keys("newuser")

        email_field = self.browser.find_element(By.CSS_SELECTOR, "input[type='email']")
        email_field.clear()
        email_field.send_keys("newuser@example.com")

        dob_field = self.browser.find_element(By.CSS_SELECTOR, "input[type='date']")
        dob_field.clear()
        dob_field.send_keys("2000-01-01")
        

        self.browser.find_element(By.CLASS_NAME, "save-btn").click()

        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        print(f"Alert text: {alert.text}") 
        alert.accept()

        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "edit-btn"))
        ).click()

        self.browser.find_element(By.CLASS_NAME, "edit-btn-1").click()

        old_password_field = self.browser.find_element(By.CSS_SELECTOR, "input[type='password']:nth-of-type(1)")
        old_password_field.send_keys("Password12345!")

        new_password_field = self.browser.find_element(By.CSS_SELECTOR, "input[type='password']:nth-of-type(2)")
        new_password_field.send_keys("NewPassword123!")

        confirm_password_field = self.browser.find_element(By.CSS_SELECTOR, "input[type='password']:nth-of-type(3)")
        confirm_password_field.send_keys("NewPassword123!")

        self.browser.find_element(By.CLASS_NAME, "save-btn").click()

        try:
            WebDriverWait(self.browser, 5).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            print(f"Alert text: {alert.text}")  
            alert.accept()  
        except NoAlertPresentException:
            print("No alert was present after saving password.")

        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "logout-btn"))
        ).click()

        login_page.load(f"{self.live_server_url}/")
        login_page.login("newuser", "NewPassword123!")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "logout-btn"))
        )

        displayed_username = self.browser.find_element(By.XPATH, "//p[span[contains(text(), 'Username:')]]").text
        self.assertIn("newuser", displayed_username)


    def test_add_friendship(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(username="testuser", password="Password123!",email = "testuser@example.com", DOB = "2000-01-01")
        User.objects.create_user(username="testuser5", password="Password123456!",email = "testuser5@example.com", DOB = "2004-09-01")

        login_page = LoginPage(self.browser)
        login_page.load(f"{self.live_server_url}/")
        login_page.login("testuser", "Password123!")
        
        logout_button = WebDriverWait(self.browser, 10).until(
            lambda browser: browser.find_element(By.CLASS_NAME, "logout-btn")
        )

        other_page_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[href='/other/']"))
        )   

        other_page_link.click()

        add_friend_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "add_button"))
        )
        add_friend_button.click()

        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        print(f"Alert text: {alert.text}")
        alert.accept()

        main_page_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[href='/home']"))
        )
        main_page_link.click()

        logout_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "logout-btn"))
        )
        logout_button.click()

        login_page.load(f"{self.live_server_url}/")
        login_page.login("testuser5", "Password123456!")
        
        show_requests_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "show-requests"))
        )
        show_requests_button.click()

        accept_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "accept"))
        )
        accept_button.click()

        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        print(f"Alert text: {alert.text}")  # Debugging
        alert.accept()

        close_modal_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "close-request-modal"))
        )
        close_modal_button.click()

        other_page_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[href='/other/']"))
        )
        other_page_link.click()

        friend_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.add_button[disabled]"))
        )

        friend_button_text = friend_button.text
        self.assertIn("Friend", friend_button_text)


    def test_age_filter(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(
            username="testuser", 
            password="Password123!",
            email="testuser@example.com", 
            DOB="2000-01-01"
        )

        User.objects.create_user(
            username="user_age_20", 
            password="Password123!",
            email="user10@example.com", 
            DOB="2004-07-05"
        )
        User.objects.create_user(
            username="user_age_04", 
            password="Password123!",
            email="user20@example.com", 
            DOB="2020-07-05"
        )            

        login_page = LoginPage(self.browser)
        login_page.load(f"{self.live_server_url}/")
        login_page.login("testuser", "Password123!")


        other_page_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[href='/other/']"))
        )   

        other_page_link.click()
        min_age_field = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, "min_age")) 
        )
        min_age_field.clear()
        min_age_field.send_keys("15")

        max_age_field = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, "max_age")) 
        )
        max_age_field.clear()
        max_age_field.send_keys("30")  

        filter_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "filter_button"))
        )
        filter_button.click()    

        user_list = WebDriverWait(self.browser, 10).until(
        lambda browser: browser.find_elements(By.CLASS_NAME, "user-container")
        )

        self.assertEqual(len(user_list), 1) 
        displayed_username = user_list[0].find_element(By.CLASS_NAME, "name").text
        self.assertEqual(displayed_username, "user_age_20")  

