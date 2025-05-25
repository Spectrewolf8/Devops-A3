import unittest
import tempfile
import os
import json
from app import app, init_db, DATABASE


class TestUserManagementApp(unittest.TestCase):
    """Unit tests for the Flask application"""

    def setUp(self):
        """Set up test client and temporary database"""
        # Create a temporary database file
        self.db_fd, app.config["DATABASE"] = tempfile.mkstemp()
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        # Override the DATABASE constant for testing
        global DATABASE
        DATABASE = app.config["DATABASE"]

        self.app = app.test_client()

        with app.app_context():
            init_db()

    def tearDown(self):
        """Clean up after each test"""
        os.close(self.db_fd)
        os.unlink(app.config["DATABASE"])

    def test_home_page(self):
        """Test that home page loads correctly"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Management System", response.data)
        self.assertIn(b"Add New User", response.data)

    def test_add_user_get(self):
        """Test GET request to add user page"""
        response = self.app.get("/add_user")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add New User", response.data)
        self.assertIn(b"Name:", response.data)
        self.assertIn(b"Email:", response.data)

    def test_add_user_post_valid(self):
        """Test POST request with valid user data"""
        response = self.app.post("/add_user", data={"name": "Test User", "email": "test@example.com"}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User added successfully!", response.data)
        self.assertIn(b"Test User", response.data)
        self.assertIn(b"test@example.com", response.data)

    def test_add_user_post_empty_fields(self):
        """Test POST request with empty fields"""
        response = self.app.post("/add_user", data={"name": "", "email": ""}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Name and email are required!", response.data)

    def test_add_user_post_duplicate_email(self):
        """Test POST request with duplicate email"""
        # Add first user
        self.app.post("/add_user", data={"name": "First User", "email": "duplicate@example.com"})

        # Try to add second user with same email
        response = self.app.post("/add_user", data={"name": "Second User", "email": "duplicate@example.com"}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email already exists!", response.data)

    def test_delete_user(self):
        """Test user deletion"""
        # First add a user
        response = self.app.post("/add_user", data={"name": "Delete Me", "email": "delete@example.com"}, follow_redirects=True)

        # Extract user ID from the response (this is a simple approach)
        # In a real app, you might want to query the database directly
        self.assertIn(b"Delete Me", response.data)

        # For testing purposes, we'll assume the user ID is 1 (first user)
        response = self.app.get("/delete_user/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User deleted successfully!", response.data)
        self.assertNotIn(b"Delete Me", response.data)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)

        # Parse JSON response
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)


if __name__ == "__main__":
    unittest.main()
