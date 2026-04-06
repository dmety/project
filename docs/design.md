# 设计文档

## 系统架构

### 整体架构
系统采用前后端分离架构，包含以下主要组件：
- 前端：Vue3 + TypeScript + TailwindCSS
- 后端：Python FastAPI
- 数据库：MySQL 8.0 + Milvus + Redis
- AI服务：科大讯飞星火大模型

### 技术架构图

```
┌─────────────────┐
│   Vue3 前端     │
└────────┬────────┘
         │ HTTP/REST
┌────────▼────────┐
│  FastAPI 后端    │
├────────┬────────┤
│   MySQL  │Milvus│
└────────┴────────┘
         │
┌────────▼────────┐
│  讯飞大模型API   │
└─────────────────┘
```

## 模块设计

### 1. 用户认证模块
- 用户注册与登录
- JWT Token生成与验证
- 权限控制

### 2. 学生画像模块
- 多维度画像数据存储
- 画像动态更新
- 画像向量存储（Milvus）

### 3. 学习路径规划模块
- 个性化路径生成
- 路径节点管理
- 进度跟踪

### 4. 资源生成模块
- 大模型调用
- 内容安全审核
- 资源存储

### 5. 多智能体模块
- 教学指导智能体
- 练习辅导智能体
- 学习评估智能体

## 数据库设计

### 核心表说明

1. **user_info**: 用户基础信息
2. **student_profile**: 学生多维度画像
3. **course_knowledge**: 课程知识点体系
4. **learning_path**: 学习路径主表
5. **path_node**: 学习路径节点
6. **learning_resource**: 学习资源
7. **exercise_info**: 练习题
8. **learning_evaluation**: 学习评估报告

## 接口设计

### 统一响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 核心接口

1. `POST /api/auth/register` - 用户注册
2. `POST /api/auth/login` - 用户登录
3. `GET /api/learning/path` - 获取学习路径
4. `POST /api/resource/generate` - 生成学习资源
5. `POST /api/agent/chat` - 智能体对话
