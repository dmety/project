USE learning_system;

INSERT INTO user_info (user_id, username, password_hash, major, grade, status) VALUES
(1, 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyWqKqKqKqK', '计算机科学与技术', '大三', 1);

INSERT INTO sys_user_role (user_id, role_id) VALUES
(1, 1);

