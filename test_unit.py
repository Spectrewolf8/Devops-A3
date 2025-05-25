import unittest
import tempfile
import os
import json
import sqlite3
from app import app, init_db


class TestUserManagementApp(unittest.TestCase):
    """Unit tests for the Flask application"""

    def setUp(self):
        """Set up test client and temporary database"""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config["DATABASE"] = self.db_path
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.app = app.test_client()

        with app.app_context():
            # Close any existing connections
            try:
                conn = sqlite3.connect(self.db_path)
                conn.execute("DROP TABLE IF EXISTS users")
                conn.commit()
                conn.close()
            except:
                pass
            
            init_db()

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.close(self.db_fd)
            os.unlink(self.db_path)
        except:
            pass

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
        self.app.post("/add_user", data={"name": "Delete Me", "email": "delete@example.com"})

        # Get the user ID from database
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.execute("SELECT id FROM users WHERE email = ?", ("delete@example.com",))
        user_row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(user_row, "User was not created")
        user_id = user_row[0]

        # Delete the user
        response = self.app.get(f"/delete_user/{user_id}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User deleted successfully!", response.data)
        
        # Verify user is deleted from database
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        deleted_user = cursor.fetchone()
        conn.close()
        
        self.assertIsNone(deleted_user, "User was not deleted from database")

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
