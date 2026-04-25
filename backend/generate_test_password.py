from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate hashed password for test account
test_password = "Test123!"
hashed = pwd_context.hash(test_password)

print("=== Test Account Credentials ===")
print(f"Email: test@example.com")
print(f"Username: test_student")
print(f"Password: {test_password}")
print(f"\nHashed Password (for SQL):")
print(hashed)
