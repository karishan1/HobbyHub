from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
        self.main_content = (By.CLASS_NAME, "main-content")
        self.edit_button = (By.CLASS_NAME, "edit-btn")
        self.save_button = (By.CLASS_NAME, "save-btn")
        self.logout_button = (By.CLASS_NAME, "logout-btn")
        self.user_details = (By.CLASS_NAME, "user-details")

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


class UsersPage:
    def __init__(self, browser):
        self.browser = browser
        self.age_filter_min = (By.ID, "min_age")
        self.age_filter_max = (By.ID, "max_age")
        self.filter_button = (By.CLASS_NAME, "filter_button")

    def filter_users_by_age(self, min_age, max_age):
        self.browser.find_element(*self.age_filter_min).clear()
        self.browser.find_element(*self.age_filter_min).send_keys(min_age)
        self.browser.find_element(*self.age_filter_max).clear()
        self.browser.find_element(*self.age_filter_max).send_keys(max_age)
        self.browser.find_element(*self.filter_button).click()


class FriendRequestsPage:
    def __init__(self, browser):
        self.browser = browser
        self.send_request_button = (By.CLASS_NAME, "add_button")
        self.accept_request_button = (By.CLASS_NAME, "accept")

    def send_friend_request(self):
        self.browser.find_element(*self.send_request_button).click()

    def accept_friend_request(self):
        self.browser.find_element(*self.accept_request_button).click()


# Test Cases
class UserAccountTests(StaticLiveServerTestCase):
    def setUp(self):
        service = ChromeService(r"C:\Users\nisha\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Update path to chromedriver
        self.browser = WebDriver(service=service)
        self.wait = WebDriverWait(self.browser, 20)

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
        self.assertIn("http://localhost:5173/", self.browser.current_url)

    def test_login(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(username="testuser", password="Password123!")

        login_page = LoginPage(self.browser)
        login_page.load(f"{self.live_server_url}/")
        login_page.login("testuser", "Password123!")
        self.assertIn("http://localhost:5173/", self.browser.current_url)
