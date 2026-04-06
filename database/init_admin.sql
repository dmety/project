
USE learning_system;

-- 更新超级管理员密码为 admin123
UPDATE user_info 
SET password_hash = '$2b$12$NjJdcAg9ft.pZdbSKbvncuXG.JZWDVjfTabvDv4h2v2IjrEi0A8tu'
WHERE username = 'admin';

-- 确保管理员有超级管理员角色
REPLACE INTO sys_user_role (user_id, role_id) VALUES (1, 1);
