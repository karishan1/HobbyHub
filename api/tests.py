from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

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

