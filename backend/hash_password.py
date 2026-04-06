
import bcrypt

password = b"admin123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(f"Password: admin123")
print(f"Hash: {hashed.decode('utf-8')}")
