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

