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

2019-06-01

- 为database封装了`order_by`方法
- 禁止删除处于`administrator`组中的用户
- 检查权限的装饰器改名为`require_permission`
- 添加检查登录状态的装饰器`require_login`, 使用时被装饰方法需要在第一个参数接收`current_user`对象
- 简化之前的方法

2019-05-31

- 添加了`view_users`方法, 修复了权限检查装饰器会替换原函数的bug
- 登录和注册以外的用户相关URL统一改为'users'
- 为database封装了`paginate`和`count`方法
- 为`view_users`方法添加了分页并优化了返回结果

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

## 演示

### 登录

```
$ http --session=flask-auth POST :5000/auth/login username=admin password=admin
HTTP/1.0 200 OK
Content-Length: 37
Content-Type: application/json
Date: Fri, 31 May 2019 15:59:25 GMT
Server: Werkzeug/0.15.4 Python/3.7.3
Set-Cookie: jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1dWlkIjoiZjM5Y2VmMzYtODJiZC0xMWU5LWE0ZGMtOTg1YWViZTFjNmFlIiwicGVybWlzc2lvbnMiOlsiQ2FuIGRlbGV0ZSB1c2VycyIsIkNhbiB2aWV3IHVzZXJzIl0sImV4cCI6MTU1OTQwNDc2NS44MzQ4NzU4fQ.eF1qnfWWqIo090F04-oJZbNGPlM8XvtndNdq6m1i3v8; Expires=Sat, 01-Jun-2019 15:59:25 GMT; Max-Age=86400; HttpOnly; Path=/; SameSite=Lax

{
    "message": "login successful."
}
```

#### 认证失败

```
$ http --session=flask-auth POST :5000/auth/login username=admin password=wrong_psw
HTTP/1.0 401 UNAUTHORIZED
Content-Length: 47
Content-Type: application/json
Date: Fri, 31 May 2019 16:01:12 GMT
Server: Werkzeug/0.15.4 Python/3.7.3

{
    "message": "Wrong username or password."
}
```

#### 缺少信息

```
$ http --session=flask-auth POST :5000/auth/login
HTTP/1.0 400 BAD REQUEST
Content-Length: 50
Content-Type: application/json
Date: Fri, 31 May 2019 16:00:41 GMT
Server: Werkzeug/0.15.4 Python/3.7.3

{
    "message": "Require username and password."
}
```

### 获取个人信息

```
$ http --session=flask-auth :5000/auth/users/me
HTTP/1.0 200 OK
Content-Length: 308
Content-Type: application/json
Date: Fri, 31 May 2019 16:04:40 GMT
Server: Werkzeug/0.15.4 Python/3.7.3

{
    "created_on": "Thu, 30 May 2019 09:33:55 GMT",
    "email": "admin@example.com",
    "groups": [
        "administrator"
    ],
    "nickname": "nickname",
    "permissions": [
        "Can delete users",
        "Can view users"
    ],
    "username": "admin",
    "uuid": "f39cef36-82bd-11e9-a4dc-985aebe1c6ae"
}
```

### 查看用户列表

```
$ http --session=flask-auth :5000/auth/users
HTTP/1.0 200 OK
Content-Length: 397
Content-Type: application/json
Date: Fri, 31 May 2019 15:56:25 GMT
Server: Werkzeug/0.15.4 Python/3.7.3

{
    "count": 2,
    "next": null,
    "prev": null,
    "result": [
        {
            "email": "admin@example.com",
            "url": "http://localhost:5000/auth/users/f39cef36-82bd-11e9-a4dc-985aebe1c6ae",
            "username": "admin"
        },
        {
            "email": "user2@example.com",
            "url": "http://localhost:5000/auth/users/a9e265fa-82be-11e9-82d8-985aebe1c6ae",
            "username": "user2"
        }
    ]
}
```

#### 没有认证

```
$ http :5000/auth/users
HTTP/1.0 401 UNAUTHORIZED
Content-Length: 48
Content-Type: application/json
Date: Fri, 31 May 2019 16:02:21 GMT
Server: Werkzeug/0.15.4 Python/3.7.3

{
    "message": "Missing verification letter."
}
```

#### 权限不足

```
$ http --session=flask-auth :5000/auth/users
HTTP/1.0 403 FORBIDDEN
Content-Length: 38
Content-Type: application/json
Date: Fri, 31 May 2019 16:03:23 GMT
Server: Werkzeug/0.15.4 Python/3.7.3

{
    "message": "Permission denied."
}
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

