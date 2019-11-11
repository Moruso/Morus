## Views

[TOC]

### 继承关系图
![继承关系图](../../src/drf-views.png)
### APIView

> DRF提供的APIView 是Django View的子类，是所有DRF其他视图的基类，使用APIView几乎和使用Django的View一样

###### APIView 与django View的差别

* 传递给处理程序的请求是DRF的Request实例，而不是django的HttpRequest 
* 同样返回的是DRF的Response,来替换django的HttpResponse，该视图将管理内容协商并在响应上设置正确的渲染器。
* 任意的APIException将被捕获并给出相应的响应
* 将对传入的请求进行身份验证，并在将请求分派给处理程序方法之前运行适当的权限和throttle(函数节流)限制检查。

### 调用流程

根据用户请求的不同的URL和http方法来决定触发那些view函数

### [mixins](./view-mixins.md)

### Generic views

> 允许您快速构建与数据库模型紧密映射的API view, 如果通用视图不适合您的API的需要，你可以使用常规APIView类,或重用mixin和基类使用的通用视图来组成自己的组可重用通用视图

以下View是DRF预先定义了一些可以快速与数据库模型像映射的View.

###### GenericAPIView

DRF大多数view的基类，主要定义了一些通用的方法.

###### CreateAPIView

> 创建一个model实例，继承 GenericAPIView 和mixins中CreateModelMixin

使用HTTP POST放法调用自己的post方法,然后post方法调用CreateModelMixin中的create方法来创建一个model实例

###### ListAPIView

> 返回一个model的查询集, 继承 GenericAPIView 和mixins中ListModelMixin

使用HTTP GET方法调用自己的get方法, 然后get方法调用ListModelMixin的list方法来获取一个model查询集

###### RetrieveAPIView

> 检索一个model实例, 继承 GenericAPIView 和mixins中 RetrieveModelMixin

使用HTTP GET方法以及active调用自己的get方法，然后get方法调用RetrieveModelMixin的retrieve来检索一个实例对象

###### DestroyAPIView
    Concrete view for deleting a model instance
###### UpdateAPIView
    Concrete view for updating a model instance
###### ListCreateAPIView
    Concrete view for listing a queryset or creating a model instance.
###### RetrieveUpdateAPIView
    Concrete view for retrieving, updating a model instance
###### RetrieveDestroyAPIView
    Concrete view for retrieving or deleting a model instance
###### RetrieveUpdateDestroyAPIView
    Concrete view for retrieving, updating or deleting a model instance

### View Sets

> ViewSetMixin 重写了.as_view()方法，使其可以接收'action'参数并绑定到相应的HTTP方法实现对资源的操作, 其他的View 只是继承了相应的父类，并没有增加额外的操作

不同的action方法对应不同的ViewSet方法

* {'get': 'list'}  ===> list
* {'get': 'retrieve'}  ===> retrieve

###### ViewSetMixin
###### ViewSet
###### GenericViewSet
###### ReadOnlyModelViewSet
###### ModelViewSet


### decorator

###### api_view
###### API policy decorators
###### View schema decorator