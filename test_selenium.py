import unittest
import time
import os
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestUserManagementApp(unittest.TestCase):
    """Simplified Selenium test cases for User Management Application"""

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

        # Check that the page title contains expected text
        self.assertIn("User Management", self.driver.title)

        # Check for main heading
        try:
            main_title = self.driver.find_element(By.ID, "main-title")
            self.assertEqual(main_title.text, "User Management System")
        except:
            # Fallback: check for any h1 element
            h1_elements = self.driver.find_elements(By.TAG_NAME, "h1")
            self.assertTrue(len(h1_elements) > 0, "No h1 elements found on page")

        print("✓ Home page loads correctly")

    def test_02_health_check_endpoint(self):
        """Test Case 2: Verify health check endpoint works"""
        print("Running Test Case 2: Health check endpoint")

        # Navigate to health endpoint
        self.driver.get(f"{self.base_url}/health")

        # Check that we get a response (should be JSON)
        page_source = self.driver.page_source
        self.assertIn("healthy", page_source)

        print("✓ Health check endpoint works")

    def test_03_add_user_page_loads(self):
        """Test Case 3: Verify add user page loads"""
        print("Running Test Case 3: Add user page loads")

        # Try to find and click add user button
        try:
            add_user_btn = self.driver.find_element(By.ID, "add-user-btn")
            add_user_btn.click()
        except:
            # Fallback: navigate directly to add_user page
            self.driver.get(f"{self.base_url}/add_user")

        # Wait for page to load and check for form elements
        WebDriverWait(self.driver, 10).until(lambda driver: "add" in driver.current_url.lower() or driver.find_elements(By.TAG_NAME, "form"))

        # Check that we have a form on the page
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        self.assertTrue(len(forms) > 0, "No forms found on add user page")

        print("✓ Add user page loads correctly")


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
