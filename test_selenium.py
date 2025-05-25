import unittest
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests


class TestUserManagementApp(unittest.TestCase):
    """Selenium test cases for User Management Application"""

    @classmethod
    def setUpClass(cls):
        """Set up Chrome driver with options for headless testing"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # Use ChromeDriverManager to automatically manage driver
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(10)

        # Base URL - change this if your app runs on different port
        cls.base_url = os.getenv("APP_URL", "http://localhost:5000")

        # Wait for application to be ready
        cls.wait_for_app_ready()

    @classmethod
    def wait_for_app_ready(cls, max_retries=30):
        """Wait for the Flask application to be ready"""
        for i in range(max_retries):
            try:
                response = requests.get(f"{cls.base_url}/health", timeout=2)
                if response.status_code == 200:
                    print(f"Application is ready at {cls.base_url}")
                    return
            except requests.exceptions.RequestException:
                pass

            print(f"Waiting for application... attempt {i+1}/{max_retries}")
            time.sleep(2)

        raise Exception(f"Application at {cls.base_url} is not responding after {max_retries} attempts")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.driver.quit()

    def setUp(self):
        """Set up before each test"""
        self.driver.get(self.base_url)

    def test_01_home_page_loads(self):
        """Test Case 1: Verify that the home page loads correctly"""
        print("Running Test Case 1: Home page loads")

        # Check that the page title is correct
        self.assertIn("User Management System", self.driver.title)

        # Check for main heading
        main_title = self.driver.find_element(By.ID, "main-title")
        self.assertEqual(main_title.text, "User Management System")

        # Check for "Add New User" button
        add_user_btn = self.driver.find_element(By.ID, "add-user-btn")
        self.assertEqual(add_user_btn.text, "Add New User")

        print("✓ Home page loads correctly")

    def test_02_add_user_functionality(self):
        """Test Case 2: Verify that users can be added successfully"""
        print("Running Test Case 2: Add user functionality")

        # Navigate to add user page
        add_user_btn = self.driver.find_element(By.ID, "add-user-btn")
        add_user_btn.click()

        # Wait for the add user page to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "add-user-form")))

        # Check page title
        page_title = self.driver.find_element(By.ID, "page-title")
        self.assertEqual(page_title.text, "Add New User")

        # Fill in the form
        test_name = f"Test User {int(time.time())}"  # Unique name using timestamp
        test_email = f"test{int(time.time())}@example.com"  # Unique email

        name_input = self.driver.find_element(By.ID, "name")
        email_input = self.driver.find_element(By.ID, "email")

        name_input.clear()
        name_input.send_keys(test_name)

        email_input.clear()
        email_input.send_keys(test_email)

        # Submit the form
        submit_btn = self.driver.find_element(By.ID, "submit-btn")
        submit_btn.click()

        # Wait for redirect to home page
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "main-title")))

        # Check that we're back on the home page
        self.assertIn("User Management System", self.driver.title)

        # Verify the user appears in the table
        try:
            users_table = self.driver.find_element(By.ID, "users-table")
            user_rows = users_table.find_elements(By.CLASS_NAME, "user-row")

            # Check if our test user is in the table
            user_found = False
            for row in user_rows:
                name_cell = row.find_element(By.CLASS_NAME, "user-name")
                email_cell = row.find_element(By.CLASS_NAME, "user-email")

                if name_cell.text == test_name and email_cell.text == test_email:
                    user_found = True
                    break

            self.assertTrue(user_found, f"User {test_name} with email {test_email} not found in the table")

        except Exception as e:
            # If users table doesn't exist, check for no users message
            try:
                no_users_msg = self.driver.find_element(By.ID, "no-users-message")
                self.fail("Users table not found and no users message is displayed")
            except:
                self.fail(f"Could not verify user addition: {str(e)}")

        print(f"✓ User '{test_name}' added successfully")

    def test_03_form_validation(self):
        """Test Case 3: Verify form validation works"""
        print("Running Test Case 3: Form validation")

        # Navigate to add user page
        add_user_btn = self.driver.find_element(By.ID, "add-user-btn")
        add_user_btn.click()

        # Wait for the add user page to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "add-user-form")))

        # Try to submit empty form
        submit_btn = self.driver.find_element(By.ID, "submit-btn")
        submit_btn.click()

        # Check that required field validation prevents submission
        name_input = self.driver.find_element(By.ID, "name")
        email_input = self.driver.find_element(By.ID, "email")

        # HTML5 validation should prevent form submission
        # We check if we're still on the add user page
        current_url = self.driver.current_url
        self.assertIn("add_user", current_url)

        print("✓ Form validation works correctly")

    def test_04_navigation(self):
        """Test Case 4: Verify navigation between pages works"""
        print("Running Test Case 4: Navigation functionality")

        # Start at home page
        self.assertIn("User Management System", self.driver.title)

        # Navigate to add user page
        add_user_btn = self.driver.find_element(By.ID, "add-user-btn")
        add_user_btn.click()

        # Wait for add user page
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "page-title")))

        # Check we're on add user page
        page_title = self.driver.find_element(By.ID, "page-title")
        self.assertEqual(page_title.text, "Add New User")

        # Navigate back using back button
        back_btn = self.driver.find_element(By.ID, "back-btn")
        back_btn.click()

        # Wait for home page
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "main-title")))

        # Check we're back on home page
        main_title = self.driver.find_element(By.ID, "main-title")
        self.assertEqual(main_title.text, "User Management System")

        print("✓ Navigation works correctly")


def run_tests():
    """Run all test cases"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserManagementApp)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
