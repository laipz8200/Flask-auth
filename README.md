# Flask用户验证组件

基于JWT的用户验证和权限管理组件

```
.
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── app
│   ├── __init__.py
│   ├── app.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── views.py
│   ├── database.py
│   ├── extensions.py
│   └── settings.py
├── autoapp.py
├── db.sqlite3
└── requirement.txt
```

## 更新

2019-05-28

- 添加了基于RBAC模式的权限管理
- 从github上移除了migrations目录

## 使用

### 安装依赖

```
pip install -r requirement.txt
```

### 数据库模型和迁移文件初始化

```
flask db init
flask db migrate
flask db upgrade
```

### 配置初始化

在根目录下创建`.env`文件并在其中设置基本信息:

```
FLASK_APP=autoapp.py
DATABASE_URL=<your-database-url>
SECRET_KEY=<your-secret-key>
```

### 运行服务

```
flask run
```

