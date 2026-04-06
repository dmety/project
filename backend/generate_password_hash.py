
import bcrypt

password = b"admin123"

# 生成盐并哈希密码
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password, salt)

print(f"密码: admin123")
print(f"哈希值: {hashed.decode('utf-8')}")
print()
print("请在MySQL中执行以下SQL:")
print(f"""
USE learning_system;

UPDATE user_info 
SET password_hash = '{hashed.decode('utf-8')}'
WHERE username = 'admin';
""")
