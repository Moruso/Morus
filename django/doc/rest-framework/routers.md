## Routers

某些Web框架（如Rails）提供了自动确定应用程序的URL应如何映射到处理传入请求的逻辑的功能。

REST框架增加了对Django自动URL路由的支持，并为您提供了一种简单，快速和一致的方法，将您的视图逻辑连接到一组URL。

#### Usage

这是一个使用SimpleRouter的简单URL conf的示例。

~~~ python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
~~~

register()方法有两个必需参数：

* prefix  - 用于此路由集的URL前缀。
* viewset  - 视图集类。

可选参数：

* basename  - 用于创建的URL名称的基础。如果未设置，将根据视图集的queryset属性自动生成基本名称（如果有）。请注意，如果视图集不包含queryset属性，则必须在注册视图集时设置basename。

上面的示例将生成以下URL模式：

* URL pattern: ^users/$ Name: 'user-list'
* URL pattern: ^users/{pk}/$ Name: 'user-detail'
* URL pattern: ^accounts/$ Name: 'account-list'
* URL pattern: ^accounts/{pk}/$ Name: 'account-detail'

> 注意：basename参数用于指定视图名称模式的初始部分。在上面的示例中，这是用户或帐户部分。

通常，您不需要指定basename参数，但如果您有一个viewset，您已经定义了自定义get_queryset方法，则视图集可能没有设置.queryset属性。如果您尝试注册该视图集，您将看到如下错误：

~~~ shell

'basename' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.

~~~

这意味着您需要在注册视图集时显式设置basename参数，因为它无法从模型名称自动确定。

#### Using include with routers

路由器实例上的.urls属性只是URL模式的标准列表。有关如何包含这些URL的方式有很多种。

例如，您可以将router.urls附加到现有视图列表中......

~~~ python

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
]

urlpatterns += router.urls

~~~

或者你可以使用Django的include函数，就像这样......
~~~ python

urlpatterns = [
    url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
    url(r'^', include(router.urls)),
]

~~

您可以在应用程序命名空间中使用include：

~~~ python

urlpatterns = [
    url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
    url(r'^api/', include((router.urls, 'app_name'))),
]

~~~

或者是应用程序和实例命名空间：
~~~ python
urlpatterns = [
    url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
    url(r'^api/', include((router.urls, 'app_name'), namespace='instance_name')),
]
~~~

---

注意：如果将命名空间与超链接序列化程序一起使用，则还需要确保序列化程序上的任何view_name参数都能正确反映命名空间。在上面的示例中，您需要为超链接到用户详细信息视图的序列化程序字段包含一个参数，例如view_name ='app_name：user-detail'。自动view_name生成使用类似％（model_name）-detail的模式。除非您的模型名称实际发生冲突，否则在使用超链接序列化程序时，最好不要命名Django REST Framework视图。

---

#### Routing for extra actions

视图集可以通过使用@action装饰器修饰方法来标记路由的额外操作。这些额外的操作将包含在生成的路由中。例如，给定UserViewSet类上的set_password方法：

~~~ python

from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action

class UserViewSet(ModelViewSet):
    ...

    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        ...

~~~

将生成以下路线：
* URL pattern: ^users/{pk}/set_password/$
* URL name: 'user-set-password'

默认情况下，URL模式基于方法名称，URL名称是ViewSet.basename和带连字符的方法名称的组合.如果您不想对这些值中的任何一个使用默认值，则可以为@action装饰器提供url_path和url_name参数。

例如，如果要将自定义操作的URL更改为^users/{pk}/change-password/$，则可以编写：

~~~ python

from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action

class UserViewSet(ModelViewSet):
    ...

    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf],
            url_path='change-password', url_name='change_password')
    def set_password(self, request, pk=None):
        ...

~~~

以上示例现在将生成以下URL模式：

* URL path: ^users/{pk}/change-password/$
* URL name: 'user-change_password'

### [API Guide](https://www.django-rest-framework.org/api-guide/routers/#api-guide)

##### SimpleRouter

此路由器包含标准列表，创建，检索，更新，部分更新和销毁操作的路由。视图集还可以使用@action装饰器标记要路由的其他方法。

