# 用户手册

## 快速开始

### 环境准备

1. 安装 Node.js 18+
2. 安装 Python 3.11+
3. 安装 MySQL 8.0+
4. （可选）安装 Docker

### 项目启动

#### 方式一：本地开发启动

**前端启动：**
```bash
cd frontend
npm install
npm run dev
```

**后端启动：**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件，配置数据库连接和讯飞API
uvicorn app.main:app --reload
```

#### 方式二：Docker 部署

```bash
cd deploy
docker-compose up -d
```

### 数据库初始化

**MySQL初始化：**
```bash
mysql -u root -p < database/mysql_init.sql
```

**Milvus初始化：**
```bash
cd database
python milvus_init.py
```

## 功能使用指南

### 1. 用户注册与登录

1. 访问系统首页
2. 点击「注册」按钮，填写用户名和密码
3. 注册成功后，使用账号密码登录

### 2. 个性化学习路径

1. 登录系统后，进入「学习路径」页面
2. 系统会根据您的画像自动生成个性化学习路径
3. 按照路径节点顺序进行学习
4. 完成学习后，系统会自动更新进度

### 3. 学习资源生成

1. 在学习路径中选择某个知识点
2. 点击「生成资源」按钮
3. 系统会基于大模型为您生成个性化学习资源
4. 资源生成后，可查看和学习

### 4. 多智能体助手

1. 进入「智能助手」页面
2. 选择对应的智能体类型：
   - 教学指导智能体：解答学习疑问
   - 练习辅导智能体：提供练习指导
   - 学习评估智能体：评估学习效果
3. 与智能体进行对话交互

## 常见问题

### Q: 如何配置讯飞API？

A: 在后端 `.env` 文件中配置以下参数：
```
XFYUN_SPARK_APP_ID=your-app-id
XFYUN_SPARK_API_SECRET=your-api-secret
XFYUN_SPARK_API_KEY=your-api-key
```

### Q: 系统支持哪些浏览器？

A: 推荐使用 Chrome、Firefox、Edge 等现代浏览器。

### Q: 如何重置学习进度？

A: 请联系管理员，在数据库中删除对应的学习路径记录。
