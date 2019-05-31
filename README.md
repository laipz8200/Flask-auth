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

2019-05-31

- 添加了`view_users`方法, 修复了权限检查装饰器会替换原函数的bug
- 登录和注册以外的用户相关URL统一改为'users'

2019-05-30

- 添加了`SurrogateBaseKey`Mixin自动为模型添加主键`id`和删除标志`is_deleted`
- 修改数据库方法`delete()`为**将`is_deleted`修改为`True`**
- 添加新方法`remove()`实现原来`delete()`方法的功能
- 新增了两个类方法`filter_by`和`filter`, 用法与SQLAlchemy原方法类似, 但不会包含被标记为`is_deleted`的结果
- 添加删除用户接口
- 编写了权限验证装饰器

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

## 设计

### 路由设计

```
Endpoint          Methods  Rule
----------------  -------  -----------------------
auth.create_user  POST     /auth/users
auth.delete_user  DELETE   /auth/users/<uuid>
auth.get_myself   GET      /auth/users/me
auth.login        POST     /auth/login
auth.logout       POST     /auth/logout
auth.update_user  PUT      /auth/users/<uuid>
auth.view_user    GET      /auth/users/<uuid>
auth.view_users   GET      /auth/users
```

### 权限设计

| 权限         | 名称             | 注释                                                       |
| ---          | ---              | ---                                                        |
| 删除用户     | Can delete users |                                                            |
| 查看用户列表 | Can view users   | 该权限是指列出所有用户的列表, 不是通过uuid访问单个用户信息 |

