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

### [mixins](./view-mixins.md)
> 混合类，作用比较简单

###### CreateModelMixin   
    创建一个model实例
###### ListModelMixin 
    List a queryset   
###### RetrieveModelMixin
    Retrieve a model instance
###### UpdateModelMixin
    Update a model instance
###### DestroyModelMixin
    Destroy a model instance

  
#### [GenericAPIView](./view-generics.md)

    允许您快速构建与数据库模型紧密映射的API view, 如果通用视图不适合您的API的需要，你可以使用常规APIView类,或重用mixin和基类使用的通用视图来组成自己的组可重用通用视图
    Base class for all other generic views
        
### Concrete View Classes

    * 以下类是具体的通用视图，如果您使用的是通用视图，这通常是您将要使用的级别，除非您需要大量自定义的行为。这些视图类，你可以从rest_framework.generics 引入。

###### CreateAPIView
> Concrete view for creating a model instance
    
    用于仅创建端点,
    提供了POST方法处理程序
    扩展: GenericAPIView, CreateModelMixin
    

###### ListAPIView

> Concrete view for listing a queryset

    用于只读端点以表示模型实例的集合。
    提供了GET方法处理程序
    扩展: GenericAPIView, ListModelMixin

###### RetrieveAPIView

> Concrete view for retrieving a model instance

    用于只读端点以表示单个模型实例。
    提供了GET方法处理程序
    扩展: GenericAPIView, RetrieveModelMixin

###### DestroyAPIView


> Concrete view for deleting a model instance

    用于单个模型实例的仅删除端点。
    提供了delete方法处理程序
    扩展: GenericAPIView, DestroyModelMixin

###### UpdateAPIView

>    Concrete view for updating a model instance
    
    用于单个模型实例的仅更新端点。
    提供了PUT和PATCH方法处理程序
    扩展: GenericAPIView, UpdateModelMixin 

###### ListCreateAPIView

> Concrete view for listing a queryset or creating a model instance.

    用于读写端点以表示模型实例的集合。
    提供GET和POST方法处理程序
    扩展: GenericAPIView, ListModelMixin, CreateModelMixin

###### RetrieveUpdateAPIView
    
> Concrete view for retrieving, updating a model instance

    用于读取或更新端点以表示单个模型实例。
    提供了GET，PUT和PATCH方法处理程序
    扩展: GenericAPIView, RetrieveModelMixin, UpdateModelMixin

###### RetrieveDestroyAPIView

>Concrete view for retrieving or deleting a model instance

    用于读取或删除端点以表示单个模型实例。
    提供了GET和DELETE方法处理程序
    扩展: GenericAPIView, RetrieveModelMixin, DestroyModelMixin

###### RetrieveUpdateDestroyAPIView
    
> Concrete view for retrieving, updating or deleting a model instance

    用于读-写-删除端点以表示单个模型实例。
    提供了 GET,PUT,PATCH和DELETE方法处理程序
    扩展: GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

### [View Sets](./view-sets.md)

> ViewSetMixin 重写了.as_view()方法，使其可以接收'action'参数并绑定到相应的HTTP方法实现对资源的操作, 其他的View 只是继承了相应的父类，并没有增加额外的操作


###### ViewSetMixin
###### ViewSet
###### GenericViewSet
###### ReadOnlyModelViewSet
###### ModelViewSet


### decorator

###### api_view
###### API policy decorators
###### View schema decorator
<!-- ### @api_view

> @api_view(http_method_names=['GET'])

DRF框架也允许您使用基于常规函数的视图。它提供了一组简单的装饰器来包装基于函数的视图来确保他们能够收到Request,也允许他们返回一个Response,允许您配置请求的处理方式。

这个功能的核心是api_view装饰器, 需要提供一组你的函数能够处理的http 方法

### API policy decorators

> 覆盖默认设置，DRF 提供了一组额外的装饰器，可以添加到您的视图

* @renderer_classes(...)
* @parser_classes(...)
* @authentication_classes(...)
* @throttle_classes(...)
* @permission_classes(...)

    > **这些必须使用在@api_view之后**
    > 这些装饰器中的每一个都接受一个参数，该参数必须是类的列表或元组。

### View schema decorator

> 要覆盖基于函数的视图的默认schema生成,可以使用@schema装饰器
> **必须使用在@api_view之后**

    @api_view(['GET'])
    @schema(None) -->

#### Customizing the generic views

    通常，您会想要使用现有的通用视图，但使用一些略微自定义的行为。如果您发现自己在多个位置重复使用某些自定义行为，则可能需要将该行为重构为一个公共类，然后您可以根据需要将其应用于任何视图或视图集。

##### Creating custom mixins

    例如，如果您需要根据URL提供的多个字段查找对象，则可以创建如下所示的mixin类:

~~~ python

class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
~~~

    然后，只要您需要应用自定义行为，就可以将此mixin简单地应用于视图或视图集。

~~~ python

class RetrieveUserView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ('account', 'username')

~~~

##### Creating custom base classes

    如果您在多个视图中使用mixin，则可以更进一步，创建自己的一组基本视图，然后可以在整个项目中使用。例如：

~~~ python
class BaseRetrieveView(MultipleFieldLookupMixin,
                       generics.RetrieveAPIView):
    pass

class BaseRetrieveUpdateDestroyView(MultipleFieldLookupMixin,
                                    generics.RetrieveUpdateDestroyAPIView):
    pass

~~~

> 如果您的自定义行为始终需要在整个项目中的大量视图中重复，那么使用自定义基类是一个不错的选择。

#### PUT as create

    在3.0版之前，REST框架将处理后的PUT混合为更新或创建操作，具体取决于对象是否已存在。
    允许PUT作为创建操作是有问题的，因为它必然暴露有关对象存在或不存在的信息。透明地允许重新创建先前删除的实例也不一定是比仅返回404响应更好的默认行为。
    两种样式“PUT as 404”和“PUT as create”在不同情况下都可以有效，但从版本3.0开始，我们现在使用404行为作为默认值，因为它更简单，更明显。如果您需要通用的PUT-as-create行为，您可能希望将类似此类的AllowPUTAsCreateMixin类作为mixin包含在您的视图中。
