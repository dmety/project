CREATE DATABASE IF NOT EXISTS learning_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE learning_system;

CREATE TABLE IF NOT EXISTS user_info (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码加密值',
    major VARCHAR(100) COMMENT '专业',
    grade VARCHAR(50) COMMENT '年级',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    last_login_at DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '最后登录时间',
    status INT DEFAULT 1 COMMENT '状态 1正常 0禁用',
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户基础信息表';

CREATE TABLE IF NOT EXISTS student_profile (
    profile_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '画像ID',
    user_id INT NOT NULL COMMENT '用户ID',
    knowledge_level VARCHAR(50) COMMENT '知识基础等级',
    cognitive_style_tags TEXT COMMENT '认知风格标签',
    weakness_tags TEXT COMMENT '薄弱点标签',
    error_prone_tags TEXT COMMENT '易错点标签',
    learning_goals TEXT COMMENT '学习目标',
    learning_pace_preference VARCHAR(50) COMMENT '学习节奏偏好',
    interest_directions TEXT COMMENT '兴趣方向',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生画像表';

CREATE TABLE IF NOT EXISTS course_knowledge (
    knowledge_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '知识点ID',
    course_id INT NOT NULL COMMENT '课程ID',
    knowledge_name VARCHAR(200) NOT NULL COMMENT '知识点名称',
    chapter_belong VARCHAR(100) COMMENT '章节归属',
    difficulty_level INT DEFAULT 1 COMMENT '难度等级 1-5',
    pre_knowledge TEXT COMMENT '前置知识点',
    post_knowledge TEXT COMMENT '后置知识点',
    knowledge_detail TEXT COMMENT '知识点详情',
    INDEX idx_course_id (course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程知识点表';

CREATE TABLE IF NOT EXISTS learning_path (
    path_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '路径ID',
    user_id INT NOT NULL COMMENT '用户ID',
    path_name VARCHAR(200) NOT NULL COMMENT '路径名称',
    learning_cycle VARCHAR(50) COMMENT '学习周期',
    total_milestones INT DEFAULT 0 COMMENT '总里程碑数',
    completed_milestones INT DEFAULT 0 COMMENT '已完成里程碑数',
    current_progress FLOAT DEFAULT 0.0 COMMENT '当前进度',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    status INT DEFAULT 1 COMMENT '状态 1进行中 0已完成',
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习路径表';

CREATE TABLE IF NOT EXISTS path_node (
    node_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '节点ID',
    path_id INT NOT NULL COMMENT '路径ID',
    knowledge_id INT NOT NULL COMMENT '知识点ID',
    learning_order INT NOT NULL COMMENT '学习顺序',
    is_milestone BOOLEAN DEFAULT FALSE COMMENT '是否里程碑',
    learning_content TEXT COMMENT '学习内容',
    completion_status INT DEFAULT 0 COMMENT '完成状态 0未开始 1进行中 2已完成',
    planned_completion_time DATETIME COMMENT '计划完成时间',
    actual_completion_time DATETIME COMMENT '实际完成时间',
    INDEX idx_path_id (path_id),
    INDEX idx_knowledge_id (knowledge_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习路径节点表';

CREATE TABLE IF NOT EXISTS learning_resource (
    resource_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '资源ID',
    user_id INT NOT NULL COMMENT '用户ID',
    knowledge_id INT NOT NULL COMMENT '知识点ID',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型',
    resource_content TEXT NOT NULL COMMENT '资源内容',
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
    usage_status INT DEFAULT 0 COMMENT '使用状态 0未使用 1已使用',
    user_feedback TEXT COMMENT '用户反馈',
    is_compliant BOOLEAN DEFAULT TRUE COMMENT '是否合规',
    INDEX idx_user_id (user_id),
    INDEX idx_knowledge_id (knowledge_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习资源表';

CREATE TABLE IF NOT EXISTS learning_behavior (
    behavior_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '行为ID',
    user_id INT NOT NULL COMMENT '用户ID',
    resource_id INT COMMENT '资源ID',
    behavior_type VARCHAR(50) NOT NULL COMMENT '行为类型',
    behavior_duration INT COMMENT '行为时长(秒)',
    operation_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    page_stay_duration INT COMMENT '页面停留时长(秒)',
    interaction_details TEXT COMMENT '交互详情',
    INDEX idx_user_id (user_id),
    INDEX idx_resource_id (resource_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习行为表';

CREATE TABLE IF NOT EXISTS exercise_info (
    exercise_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '题目ID',
    knowledge_id INT NOT NULL COMMENT '知识点ID',
    difficulty_level INT DEFAULT 1 COMMENT '难度等级 1-5',
    exercise_type VARCHAR(50) NOT NULL COMMENT '题目类型',
    exercise_content TEXT NOT NULL COMMENT '题目内容',
    answer TEXT NOT NULL COMMENT '答案',
    explanation TEXT COMMENT '解析',
    error_prone_tags TEXT COMMENT '易错点标签',
    INDEX idx_knowledge_id (knowledge_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='练习题信息表';

CREATE TABLE IF NOT EXISTS user_exercise_record (
    record_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    exercise_id INT NOT NULL COMMENT '题目ID',
    user_answer TEXT NOT NULL COMMENT '用户答案',
    is_correct BOOLEAN DEFAULT FALSE COMMENT '是否正确',
    answer_duration INT COMMENT '答题时长(秒)',
    answer_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '答题时间',
    is_error BOOLEAN DEFAULT FALSE COMMENT '错题标记',
    explanation_viewed BOOLEAN DEFAULT FALSE COMMENT '解析查看状态',
    INDEX idx_user_id (user_id),
    INDEX idx_exercise_id (exercise_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户答题记录表';

CREATE TABLE IF NOT EXISTS learning_evaluation (
    evaluation_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评估ID',
    user_id INT NOT NULL COMMENT '用户ID',
    evaluation_period VARCHAR(50) NOT NULL COMMENT '评估周期',
    knowledge_mastery FLOAT COMMENT '知识点掌握度',
    answer_accuracy FLOAT COMMENT '答题正确率',
    learning_progress_completion FLOAT COMMENT '学习进度完成率',
    ability_improvement FLOAT COMMENT '能力提升幅度',
    knowledge_gaps_tags TEXT COMMENT '知识漏洞标签',
    evaluation_report TEXT COMMENT '评估报告',
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习评估表';

CREATE TABLE IF NOT EXISTS sys_role (
    role_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '角色ID',
    role_name VARCHAR(50) NOT NULL COMMENT '角色名称',
    role_code VARCHAR(50) NOT NULL UNIQUE COMMENT '角色标识',
    role_type VARCHAR(20) NOT NULL DEFAULT 'custom' COMMENT '角色类型 system-系统 custom-自定义',
    role_desc VARCHAR(255) COMMENT '角色描述',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态 1正常 0禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_role_code (role_code),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统角色表';

CREATE TABLE IF NOT EXISTS sys_permission (
    permission_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '权限ID',
    permission_name VARCHAR(50) NOT NULL COMMENT '权限名称',
    permission_code VARCHAR(100) NOT NULL UNIQUE COMMENT '权限标识',
    permission_type VARCHAR(20) NOT NULL COMMENT '权限类型 menu-菜单 button-按钮 api-接口 data-数据 agent-智能体',
    parent_id INT DEFAULT 0 COMMENT '父级ID',
    route_path VARCHAR(200) COMMENT '路由地址',
    component_path VARCHAR(200) COMMENT '组件路径',
    icon VARCHAR(50) COMMENT '图标',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态 1正常 0禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_permission_code (permission_code),
    INDEX idx_parent_id (parent_id),
    INDEX idx_type (permission_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统权限表';

CREATE TABLE IF NOT EXISTS sys_user_role (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    user_id INT NOT NULL COMMENT '用户ID',
    role_id INT NOT NULL COMMENT '角色ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_user_role (user_id, role_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

CREATE TABLE IF NOT EXISTS sys_role_permission (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    role_id INT NOT NULL COMMENT '角色ID',
    permission_id INT NOT NULL COMMENT '权限ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_role_permission (role_id, permission_id),
    INDEX idx_role_id (role_id),
    INDEX idx_permission_id (permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

CREATE TABLE IF NOT EXISTS sys_operation_log (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    user_id INT COMMENT '用户ID',
    role_code VARCHAR(50) COMMENT '角色标识',
    module VARCHAR(50) COMMENT '操作模块',
    operation_type VARCHAR(20) COMMENT '操作类型 create-update-delete-query',
    request_url VARCHAR(255) COMMENT '请求地址',
    request_method VARCHAR(10) COMMENT '请求方法',
    request_params TEXT COMMENT '请求参数',
    response_result TEXT COMMENT '响应结果',
    operation_ip VARCHAR(50) COMMENT '操作IP',
    operation_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    duration INT COMMENT '耗时(毫秒)',
    status TINYINT DEFAULT 1 COMMENT '状态 1成功 0失败',
    error_msg TEXT COMMENT '错误信息',
    INDEX idx_user_id (user_id),
    INDEX idx_operation_time (operation_time),
    INDEX idx_module (module)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统操作日志表';

INSERT INTO sys_role (role_id, role_name, role_code, role_type, role_desc, sort_order, status) VALUES
(1, '超级管理员', 'super_admin', 'system', '拥有系统所有权限', 1, 1),
(2, '学生', 'student', 'system', '系统学生用户', 2, 1),
(3, '教师', 'teacher', 'system', '系统教师用户', 3, 1),
(4, '审核员', 'auditor', 'system', '内容审核人员', 4, 1);

INSERT INTO sys_permission (permission_id, permission_name, permission_code, permission_type, parent_id, route_path, component_path, icon, sort_order, status) VALUES
(1, '系统管理', 'system', 'menu', 0, '/system', NULL, 'setting', 1, 1),
(2, '用户管理', 'system:user', 'menu', 1, '/system/user', 'system/User', 'user', 1, 1),
(3, '角色管理', 'system:role', 'menu', 1, '/system/role', 'system/Role', 'team', 2, 1),
(4, '权限管理', 'system:permission', 'menu', 1, '/system/permission', 'system/Permission', 'key', 3, 1),
(5, '操作日志', 'system:log', 'menu', 1, '/system/log', 'system/Log', 'document', 4, 1),
(6, '学生画像', 'profile', 'menu', 0, '/profile', NULL, 'target', 2, 1),
(7, '学习资源', 'resource', 'menu', 0, '/resource', NULL, 'book', 3, 1),
(8, '学习路径', 'path', 'menu', 0, '/path', NULL, 'map', 4, 1),
(9, '智能辅导', 'tutor', 'menu', 0, '/tutor', NULL, 'robot', 5, 1),
(10, '学习评估', 'evaluation', 'menu', 0, '/evaluation', NULL, 'chart', 6, 1),
(11, '内容审核', 'audit', 'menu', 0, '/audit', NULL, 'shield', 7, 1),
(12, '用户查询', 'system:user:query', 'api', 2, NULL, NULL, NULL, 1, 1),
(13, '用户新增', 'system:user:add', 'api', 2, NULL, NULL, NULL, 2, 1),
(14, '用户编辑', 'system:user:edit', 'api', 2, NULL, NULL, NULL, 3, 1),
(15, '用户删除', 'system:user:delete', 'api', 2, NULL, NULL, NULL, 4, 1),
(16, '角色查询', 'system:role:query', 'api', 3, NULL, NULL, NULL, 1, 1),
(17, '角色新增', 'system:role:add', 'api', 3, NULL, NULL, NULL, 2, 1),
(18, '角色编辑', 'system:role:edit', 'api', 3, NULL, NULL, NULL, 3, 1),
(19, '角色删除', 'system:role:delete', 'api', 3, NULL, NULL, NULL, 4, 1),
(20, '画像查询', 'profile:query', 'api', 6, NULL, NULL, NULL, 1, 1),
(21, '画像更新', 'profile:update', 'api', 6, NULL, NULL, NULL, 2, 1),
(22, '资源查询', 'resource:query', 'api', 7, NULL, NULL, NULL, 1, 1),
(23, '资源生成', 'resource:generate', 'api', 7, NULL, NULL, NULL, 2, 1),
(24, '路径查询', 'path:query', 'api', 8, NULL, NULL, NULL, 1, 1),
(25, '路径生成', 'path:generate', 'api', 8, NULL, NULL, NULL, 2, 1),
(26, '辅导对话', 'tutor:chat', 'api', 9, NULL, NULL, NULL, 1, 1),
(27, '代码运行', 'tutor:code', 'api', 9, NULL, NULL, NULL, 2, 1),
(28, '评估查询', 'evaluation:query', 'api', 10, NULL, NULL, NULL, 1, 1),
(29, '评估生成', 'evaluation:generate', 'api', 10, NULL, NULL, NULL, 2, 1),
(30, '内容审核', 'audit:check', 'api', 11, NULL, NULL, NULL, 1, 1),
(31, '智能体调用', 'agent:invoke', 'agent', 0, NULL, NULL, NULL, 1, 1);

INSERT INTO sys_role_permission (role_id, permission_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11),
(1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21),
(1, 22), (1, 23), (1, 24), (1, 25), (1, 26), (1, 27), (1, 28), (1, 29), (1, 30), (1, 31),
(2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 20), (2, 21), (2, 22), (2, 23), (2, 24),
(2, 25), (2, 26), (2, 27), (2, 28), (2, 29), (2, 31),
(3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 20), (3, 21), (3, 22), (3, 23),
(3, 24), (3, 25), (3, 26), (3, 27), (3, 28), (3, 29), (3, 30), (3, 31),
(4, 11), (4, 30);
