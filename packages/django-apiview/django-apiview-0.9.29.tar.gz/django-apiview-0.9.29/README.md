# django-apiview

## 项目描述

## 项目特性

1. 以注解形式定义接口。
1. 可自由定义响应包封装格式。
1. 提供快捷方法获取请求参数。
1. 提供丰富的参数检验器。

## 安装

```
pip install django-apiview
```

## 使用

1. 在项目settings.py文件中引入`django_apiview`包。
1. 在项目urls.py文件中引入`django_apiview.urls`，可实现swagger调试页面的加载。
1. 在应用视图中，使用注解`@apiview`定义视图函数，视图函数参数类型使用python的typing机制定义。
1. `django-apiview`默认使用`简易json格式`对结果进行封闭（详见`简易json格式`章节），也可以自行定义包装类。

*pro/settings.py*

```
INSTALLED_APPS = [
    "django_apiview",
]
```

*pro/urls.py*

```
from django.urls import path
from django.urls import include

urlpatterns = [
    ...
    path('django-apiview/', include("django_apiview.urls")),
    path('app/', include("app.urls")),
    ...
]
```

*app/views.py*

```
@apiview
def ping():
    return "pong"


@apiview
def echo(msg: str):
    return msg
```

*app/urls.py*

```
from django.urls import path
from . import views

urlpatterns = [
    ...
    path('ping', views.ping),
    path('echo', views.echo),
    ...
]
```

### 客户端请求

*请求：*

curl http://localhost:8000/app/ping

*响应：*

OK 200

{
    "result": "pong",
    "success": True
}


## 简易json格式

1. 正确响应由success字段和result字段组成，且success字段为True，result为应用响应内容。
1. 错误响应由success字段和error字段组成，且success字段为False，error.code为应用的错误代码，error.message为应用的错误消息。

- 正确响应体

    ```
    {
        "success": true,
        "result": result(typing.Any)
    }
    ```

- 错误响应体

    ```
    {
        "success": false,
        "error": {
            "code": error_code(int),
            "message": error_message(str)
        }
    }
    ```

