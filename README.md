# Flask-auth

A user and permissions manager based on jwt

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

## Installation

### Install Requirements

```
pip install -r requirement.txt
```

### Initialize database

```
flask db init
flask db migrate
flask db upgrade
```

### Create Env

create a `.env` file with the following settings.

```
FLASK_APP=autoapp.py
DATABASE_URL=<your-database-url>
SECRET_KEY=<your-secret-key>
```

### Start Server

```
flask run
```

## Examples

### Login

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

#### Login failed

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

#### Loss information

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

### Get user info

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

### view user list

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

#### Have no verification

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

#### Have no permission

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

## Design

### Route

```
Endpoint          Methods  Rule
----------------  -------  -----------------------
auth.create_user  POST     /auth/users
auth.delete_user  DELETE   /auth/users/<uuid>
auth.get_myself   GET      /auth/users/me
auth.index        GET      /auth/
auth.login        POST     /auth/login
auth.logout       POST     /auth/logout
auth.update_user  PUT      /auth/users/<uuid>
auth.view_user    GET      /auth/users/<uuid>
auth.view_users   GET      /auth/users
```

### Permissions

#### Usergroup

| Group | Name          |
| ---   | ---           |
| admin | administrator |

#### Permissions

| Permission     | text             |
| ---            | ---              |
| delete user    | Can delete users |
| view user list | Can view users   |

