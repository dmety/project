# 基于大模型的个性化资源生成与学习多智能体系统

采用前后端分离架构，基于科大讯飞大模型构建的智能学习系统。

## 技术栈

- **前端**: Vue3 + TypeScript + TailwindCSS + Vue Router + Pinia + Axios + ECharts
- **后端**: Python 3.11 + FastAPI + SQLAlchemy + Pydantic + JWT
- **数据库**: MySQL 8.0 + Milvus + Redis
- **部署**: Docker + Docker Compose
- **AI服务**: 科大讯飞星火大模型 V4.0 + 讯飞多模态API + 讯飞内容审核API

## 项目结构

```
project/
├── .trae/                  # 系统配置目录
├── frontend/               # Vue3前端工程
├── backend/                # FastAPI后端工程
├── database/               # 数据库初始化脚本
├── deploy/                 # 部署配置
├── docs/                   # 赛事交付文档
├── .env.example            # 环境变量模板
└── README.md               # 项目说明文档
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- MySQL 8.0+
- Docker (可选)

### 前端启动

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

### 后端启动

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件配置数据库和讯飞API
python app/main.py
# 或使用 uvicorn
uvicorn app.main:app --reload
# 访问 http://127.0.0.1:8000
```

### 数据库初始化

1. 执行数据库脚本：
   ```bash
   # 登录MySQL
   mysql -u root -p
   
   # 创建数据库
   CREATE DATABASE learning_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # 执行初始化脚本
   USE learning_system;
   source database/mysql_init.sql;
   source database/init_admin.sql;
   ```

2. 超级管理员账号：
   - 用户名：`admin`
   - 密码：`admin123`

### Docker部署

```bash
cd deploy
docker-compose up -d
```

## 核心功能模块

### 1. 对话式动态学生画像功能

**功能说明**：通过自然语言对话构建和更新学生学习画像，包含7维度能力评估。

**前端页面**：`/profile`
- 7维度能力雷达图
- 学习状态热力图
- 画像详情展示
- AI对话助手

**后端API**：
- `POST /api/profile/dialog` - 对话特征抽取
- `POST /api/profile/update` - 画像动态更新
- `GET /api/profile/visualization/{user_id}` - 画像可视化数据
- `POST /api/profile/agent/call` - 智能体调用入口

### 2. 多模态学习资源生成功能

**功能说明**：基于知识点和难度级别，生成6种类型的学习资源。

**前端页面**：`/resource`
- 资源生成配置
- 资源列表展示
- 资源类型筛选

**后端API**：
- `POST /api/resource/generate` - 资源生成
- `GET /api/resource/progress/{task_id}` - 生成进度查询
- `GET /api/resource/list` - 资源列表
- `GET /api/resource/detail/{resource_id}` - 资源详情
- `POST /api/resource/feedback` - 资源反馈
- `POST /api/resource/agent/call` - 多智能体协同调用入口

**资源类型**：
- `course_doc` - 课程讲解文档
- `mind_map` - 知识点思维导图
- `exercise` - 分难度练习题
- `code_case` - Python代码实操案例
- `extension_reading` - 拓展阅读材料
- `multimodal_diagram` - 多模态教学图解

### 3. 个性化学习路径规划与资源推送功能

**功能说明**：根据学生画像和学习目标，生成个性化学习路径，并推送相关学习资源。

**前端页面**：`/path`
- 路径生成配置
- 学习路径时间轴展示
- 路径节点状态管理
- 资源推送列表

**后端API**：
- `POST /api/path/generate` - 路径生成
- `GET /api/path/list/{user_id}` - 路径列表
- `GET /api/path/detail/{path_id}` - 路径详情
- `POST /api/path/node/update` - 节点状态更新
- `POST /api/path/push` - 资源推送
- `POST /api/path/agent/call` - 智能体调用入口

### 4. 多模态智能辅导功能

**功能说明**：提供实时答疑、代码运行调试、错题解析等智能辅导服务。

**前端页面**：`/tutor`
- 智能对话窗口
- Python代码编辑器
- 代码运行输出

**后端API**：
- `POST /api/tutor/dialog` - 实时答疑
- `POST /api/tutor/code/run` - 代码运行调试
- `POST /api/tutor/error/analysis` - 错题解析
- `POST /api/tutor/agent/call` - 智能体调用入口

### 5. 学习效果评估功能

**功能说明**：生成学习评估报告，展示学习效果数据看板。

**前端页面**：`/evaluation`
- 知识点掌握度趋势图
- 答题正确率趋势图
- 学习进度完成率趋势图
- 能力提升幅度趋势图
- 历史评估报告
- 知识漏洞定位

**后端API**：
- `POST /api/evaluation/generate` - 评估报告生成
- `GET /api/evaluation/dashboard/{user_id}` - 数据看板
- `POST /api/evaluation/agent/call` - 智能体调用入口

### 6. 防幻觉与内容安全管控功能

**功能说明**：集成讯飞内容安全API，实现内容安全检查和RAG检索。

**后端API**：
- `POST /api/evaluation/safety/check` - 内容安全检查
- `POST /api/evaluation/rag/retrieve` - RAG检索
- `POST /api/evaluation/safety/agent/call` - 智能体调用入口

## RBAC权限管理体系

**功能说明**：完整的基于角色的访问控制体系，支持细粒度权限管理。

**核心表结构**：
- `sys_role` - 系统角色表
- `sys_permission` - 系统权限表
- `sys_user_role` - 用户角色关联表
- `sys_role_permission` - 角色权限关联表
- `sys_operation_log` - 操作日志表

**预设角色**：
- 超级管理员 (super_admin)
- 学生 (student)
- 教师 (teacher)
- 审核员 (auditor)

**前端权限控制**：
- 路由守卫 - 自动鉴权
- 权限指令 - 按钮级权限控制
- 菜单动态渲染 - 基于角色权限

**后端权限控制**：
- JWT Token鉴权
- 接口级权限校验
- 操作日志记录

**权限指令**：
- `v-permission` - 单权限控制
- `v-role` - 单角色控制
- `v-any-permission` - 多权限任一控制
- `v-any-role` - 多角色任一控制

## API文档

**Swagger文档**：http://127.0.0.1:8000/docs
**健康检查**：http://127.0.0.1:8000/health
**路由列表**：http://127.0.0.1:8000/routes

## 智能体嵌入

所有核心功能模块均预留了智能体调用入口，支持：
- 多智能体协同工作
- 讯飞星火大模型集成
- 多模态能力调用
- 内容安全校验

## 开发规范

- 所有代码必须加中文注释
- 接口必须有入参校验和异常处理
- 所有开源依赖必须标注来源与协议
- 严格按照「框架搭建→功能开发→智能体嵌入」的顺序执行

## 依赖管理

### 前端依赖
- Vue3 + TypeScript
- TailwindCSS
- Vue Router + Pinia
- Axios
- ECharts + vue-echarts
- marked (Markdown渲染)

### 后端依赖
- FastAPI
- SQLAlchemy
- Pydantic
- JWT + Passlib
- Uvicorn
- Requests
- 讯飞SDK

## 安全配置

- JWT Token 认证
- 密码 bcrypt 加密
- 接口权限校验
- 内容安全检查
- 操作日志审计

## 联系方式

项目维护：系统开发团队
更新时间：2026-04-07