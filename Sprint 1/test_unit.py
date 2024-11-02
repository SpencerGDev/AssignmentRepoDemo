import unittest
from UserLogon import UserInfo, UserLogin  # Replace 'your_module' with the actual module name

class SimpleUserLoginTest(unittest.TestCase):
    
    def setUp(self):
        """Set up a basic UserLogin instance and a sample user for testing."""
        self.user_login = UserLogin()
        self.sample_user = UserInfo(
            firstName="John",
            lastName="Doe",
            email="john.doe@example.com",
            password="SecurePass123",
            phoneNumber="1234567890",
            SSN="123456789",
            symptom_list=["fever", "cough"],
            insurance=True
        )
        self.user_login.UserArray.append(self.sample_user)
    
    def test_user_creation(self):
        """Check if user info is set correctly when creating a UserInfo object."""
        user = UserInfo(
            firstName="Jane",
            lastName="Smith",
            email="jane.smith@example.com",
            password="password123",
            phoneNumber="0987654321",
            SSN="987654321",
            symptom_list=["headache"],
            insurance=False
        )
        self.assertEqual(user.firstName, "Jane")
        self.assertEqual(user.lastName, "Smith")
        self.assertEqual(user.email, "jane.smith@example.com")
    
    def test_is_in_database_email(self):
        """Test if an email is found in UserArray."""
        self.assertTrue(self.user_login.isInDataBase("john.doe@example.com", "email"))
        self.assertFalse(self.user_login.isInDataBase("not_in_database@example.com", "email"))
    
    def test_is_in_database_phone(self):
        """Test if a phone number is found in UserArray."""
        self.assertTrue(self.user_login.isInDataBase("1234567890", "phoneNumber"))
        self.assertFalse(self.user_login.isInDataBase("0000000000", "phoneNumber"))
    
    def test_login_correct_credentials(self):
        """Check login with correct email and password."""
        self.user_login.loggedinUser = None  # Ensure no user is logged in
        self.assertTrue(self.user_login.login("john.doe@example.com", "SecurePass123"))
        self.assertIsNotNone(self.user_login.loggedinUser)  # Logged-in user should be set
    
    def test_login_incorrect_credentials(self):
        """Check login with incorrect password."""
        self.assertFalse(self.user_login.login("john.doe@example.com", "wrongpassword"))
        self.assertIsNone(self.user_login.loggedinUser)  # Should remain None for failed login

if __name__ == '__main__':
    unittest.main()
