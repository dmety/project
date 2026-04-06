from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "admin123"
hashed = pwd_context.hash(password)

print(f"密码: {password}")
print(f"哈希值: {hashed}")
