import unittest
import time
import os
import requests
import sys


class TestUserManagementApp(unittest.TestCase):
    """Simple HTTP-based integration tests (simulating Selenium functionality)"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
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
                    print(f"✓ Application is ready at {cls.base_url}")
                    return
            except requests.exceptions.RequestException:
                pass

            print(f"Waiting for application... attempt {i+1}/{max_retries}")
            time.sleep(2)

        raise Exception(f"Application at {cls.base_url} is not responding after {max_retries} attempts")

    def test_01_health_check_endpoint(self):
        """Test Case 1: Verify health check endpoint works"""
        print("Running Test Case 1: Health check endpoint")
        
        response = requests.get(f"{self.base_url}/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        
        print("✓ Health check endpoint works")

    def test_02_home_page_loads(self):
        """Test Case 2: Verify that the home page loads correctly"""
        print("Running Test Case 2: Home page loads")
        
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        
        # Check that response contains expected content
        content = response.text
        self.assertIn("User Management", content)
        
        print("✓ Home page loads correctly")

    def test_03_add_user_page_loads(self):
        """Test Case 3: Verify add user page loads"""
        print("Running Test Case 3: Add user page loads")
        
        response = requests.get(f"{self.base_url}/add_user")
        self.assertEqual(response.status_code, 200)
        
        # Check that response contains form elements
        content = response.text
        self.assertIn("form", content.lower())
        
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
