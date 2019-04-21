## ViewSets
    
> * Django REST框架允许您将一组相关视图的逻辑组合在一个类中，称为ViewSet。在其他框架中，您还可以找到类似“资源”或“控制器”之类的概念上类似的实现。
> * ViewSet类只是一种基于类的View，它不提供任何方法处理程序，如.get（）或.post（），而是提供诸如.list（）和.create（）之类的操作。
> * ViewSet的方法处理程序仅使用.as_view（）方法绑定到最终化视图时的相应操作。通常，您不是在urlconf中的视图集中显式注册视图，而是使用路由器类注册视图集，该类会自动为您确定urlconf。

[TOC]

### Example

    让我们定义一个简单的视图集，可用于列出或检索系统中的所有用户。

~~~ python

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

~~~

    如果需要，我们可以将此视图集绑定到两个单独的视图中，如下所示：

~~~ python
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
~~~

    通常我们不会这样做，而是使用路由器注册视图集，并允许自动生成urlconf。

~~~ python

from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls

~~~
    
    您通常希望使用提供默认行为集的现有基类,而不是自己编写的视图集。例如：

~~~ python
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
~~~

###### 使用ViewSet类比使用View类有两个主要优点。

* 重复逻辑可以组合成一个类。在上面的示例中，我们只需要指定一次查询集，它将在多个视图中使用。
* 通过使用路由器，我们不再需要处理自己的URL连接。

> 这两者都需要权衡。使用常规视图和URL confs更明确，并为您提供更多控制。如果您希望快速启动并运行，或者您拥有大型API并希望在整个过程中强制执行一致的URL配置，则ViewSet非常有用。


### ViewSet actions

    REST框架中包含的默认路由器将为一组标准的create / retrieve / update / destroy样式操作提供路由，如下所示：

~~~ python
class UserViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass    

~~~

### Introspecting ViewSet actions

> 在调度期间，ViewSet上提供了以下属性:

* basename  -  用于创建的URL名称的基础。
* action  -  当前操作的名称（例如，list，create)
* detail  -  布尔值，指示是否为列表或详细信息视图配置了当前操作。
* suffix  -  视图集类型的显示后缀 - 镜像详细信息属性。
* name  - 视图集的显示名称。该参数与后缀互斥。
* description  - 视图集的单个视图的显示描述。

您可以检查这些属性以根据当前操作调整行为。例如，您可以限制除list操作之外的所有内容的权限，类似于：

~~~ python 
def get_permissions(self):
    """
    Instantiates and returns the list of permissions that this view requires.
    """
    if self.action == 'list':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdmin]
    return [permission() for permission in permission_classes]

~~~

### Marking extra actions for routing

> 如果你有可以路由的临时方法，你可以用@action装饰器标记它们。与常规操作一样，可以针对单个对象或整个集合执行额外操作。要指明这一点，请将detail参数设置为True或False。路由器将相应地配置其URL模式。例如，DefaultRouter将配置详细操作以在其URL模式中包含pk。

###### 额外操作的更完整示例：

~~~ python
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from myapp.serializers import UserSerializer, PasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
~~~

装饰器还可以采用仅为路由视图设置的额外参数。例如：

~~~ python 
@action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
def set_password(self, request, pk=None):
    ...
~~~

操作装饰器将默认路由GET请求，但也可以通过设置methods参数来接受其他HTTP方法。例如：

~~~ python

@action(detail=True, methods=['post', 'delete'])
    def unset_password(self, request, pk=None):
       ...

~~~

然后，两个新的行动将在网址上提供^users/{pk}/set_password/$和^users/{pk}/unset_password/$。要查看所有额外操作，请调用.get_extra_actions（）方法。

### Routing additional HTTP methods for extra actions

> 额外的操作可以将其他HTTP方法映射到单独的ViewSet方法。例如，上述密码设置/未设置方法可以合并为单个路由。请注意，其他映射不接受参数。

~~~ python
@action(detail=True, methods=['put'], name='Change Password')
def password(self, request, pk=None):
    """Update the user's password."""
    ...

@password.mapping.delete
def delete_password(self, request, pk=None):
    """Delete the user's password."""
    ...
~~~


### Reversing action URLs

如果需要获取操作的URL，请使用.reverse_action（）方法。这是reverse（）的便捷包装器，自动传递视图的请求对象，并在url_name前加上.basename属性。
请注意，在ViewSet注册期间，路由器会提供基本名称。如果您不使用路由器，则必须为.as_view（）方法提供basename参数。
使用上一节中的示例：

~~~python
>>> view.reverse_action('set-password', args=['1'])
'http://localhost:8000/api/users/1/set_password'

~~~

或者，您可以使用@action装饰器设置的url_name属性。

~~~ python 
>>> view.reverse_action(view.set_password.url_name, args=['1'])
'http://localhost:8000/api/users/1/set_password'
~~~

.reverse_action（）的url_name参数应该与@action装饰器的相同参数匹配。此外，此方法可用于反转默认操作，例如list和create。

### API Reference

##### ViewSet

ViewSet类继承自APIView。您可以使用任何标准属性（例如permission_classes，authentication_classes）来控制视图集上的API策略。ViewSet类不提供任何操作实现。为了使用ViewSet类，您将覆盖该类并显式定义动作实现。

##### GenericViewSet

GenericViewSet类继承自GenericAPIView，并提供默认的get_object，get_queryset方法和其他通用视图基本行为集，但默认情况下不包含任何操作。为了使用GenericViewSet类，您将覆盖该类并混合所需的mixin类，或者显式定义动作实现。

##### ModelViewSet

ModelViewSet类继承自GenericAPIView，并通过混合各种mixin类的行为来包含各种操作的实现。ModelViewSet类提供的操作是.list(), .retrieve(), .create(), .update(), .partial_update(), 和 .destroy().

Example:
因为ModelViewSet扩展了GenericAPIView，所以通常需要至少提供queryset和serializer_class属性。例如：    

~~~ python
class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]

~~~

请注意，您可以使用GenericAPIView提供的任何标准属性或方法覆盖。例如，要使用动态确定它应该操作的查询集的ViewSet，您可能会执行以下操作：

~~~ python

class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return self.request.user.accounts.all()

~~~

但请注意，从ViewSet中删除queryset属性后，任何关联的路由器都将无法自动派生模型的基本名称，因此您必须在路由器注册中指定basename kwarg。另请注意，虽然此类默认提供完整的create/list/retrieve/update/destroy操作集，但您可以使用标准权限类来限制可用操作。

##### ReadOnlyModelViewSet

ReadOnlyModelViewSet类也继承自GenericAPIView。与ModelViewSet一样，它还包括各种操作的实现，但与ModelViewSet不同，它只提供“只读”操作，.list（）和.retrieve（）。
Example

与ModelViewSet一样，您通常需要至少提供queryset和serializer_class属性。例如：

~~~ python
class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
~~~

##### Custom ViewSet base classes

您可能需要提供自定义ViewSet类，这些类没有完整的ModelViewSet操作集，或者以其他方式自定义行为。

Example
要创建提供crate，list和retrieve操作的基本视图集类，继承GenericViewSet，并混合所需的操作：

~~~ python

from rest_framework import mixins

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


~~~

通过创建自己的基础ViewSet类，您可以提供可在API中的多个视图集中重用的常见行为。