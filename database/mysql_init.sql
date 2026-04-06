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
