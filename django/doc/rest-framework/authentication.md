## Authentication

[TOC]

身份验证是将传入请求与一组标识凭据相关联的机制，例如请求来自的用户或使用该协议签名的令牌。然后，权限和限制策略可以使用这些凭据来确定是否应该允许该请求。

REST框架提供了许多开箱即用的身份验证方案，还允许您实现自定义方案.

身份验证始终在视图的最开始，在发生权限和限制检查之前，以及允许任何其他代码继续之前运行。

request.user属性通常设置为contrib.auth包的User类的实例。

request.auth属性用于任何其他身份验证信息，例如，它可用于表示请求已签名的身份验证令牌。

注意：不要忘记，身份验证本身不允许或禁止传入请求，它只是标识请求所使用的凭据。

### How authentication is determined

身份验证方案始终定义为类列表, REST框架将尝试对列表中的每个类进行身份验证, 并将使用成功进行身份验证的第一个类的返回值设置request.user和request.auth

如果没有类进行身份验证，则request.user将设置为django.contrib.auth.models.AnonymousUser的实例，request.auth将设置为None。

可以在django的配置中设置UNAUTHENTICATED_USER和UNAUTHENTICATED_TOKEN设置修改request.user和request.auth对未经身份验证的请求的值。

### Setting the authentication scheme

可以使用DEFAULT_AUTHENTICATION_CLASSES设置全局设置默认身份验证方案。例如。

~~~ python

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

~~~

您还可以使用基于APIView类的视图在每个视图或每个视图集的基础上设置身份验证方案。

~~~ python

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

~~~

或者，如果您将@api_view装饰器与基于功能的视图一起使用。

~~~ python

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)

~~~

### Unauthorized and Forbidden responses

当未经身份验证的请求被拒绝时，有两个不同的错误代码可能是合适的。

* HTTP 401 Unauthorized
* HTTP 403 Permission Denied

HTTP 401响应必须始终包含WWW-Authenticate标头，该标头指示客户端如何进行身份验证。HTTP 403响应不包括WWW-Authenticate标头。

将使用的响应类型取决于身份验证方案。尽管可以使用多种认证方案，但是可以仅使用一种方案来确定响应的类型。***在确定响应类型时，将使用视图上设置的第一个身份验证类。***

请注意，当请求可能成功进行身份验证但仍被拒绝执行请求的权限时，在这种情况下，无论身份验证方案如何，都将始终使用403 Permission Denied响应。


### Apache mod_wsgi specific configuration

请注意，如果使用mod_wsgi部署到Apache，则默认情况下不会将授权标头传递给WSGI应用程序，因为假定认证将由Apache处理，而不是在应用程序级别处理。如果要部署到Apache，并使用任何非基于会话的身份验证，则需要显式配置mod_wsgi以将所需的标头传递给应用程序。这可以通过在适当的上下文中指定WSGIPassAuthorization指令并将其设置为“On”来完成。

~~~ shell

WSGIPassAuthorization On

~~~

### API Reference

#### BasicAuthentication

此身份验证方案使用HTTP基本身份验证,根据用户的用户名和密码签名。基本身份验证通常仅适用于测试。

如果成功通过身份验证，BasicAuthentication将提供以下凭据:

* request.user will be a Django User instance.
* request.auth will be None.

拒绝许可的未经身份验证的响应将导致HTTP 401 Unauthorized响应，并具有相应的WWW-Authenticate标头。例如：

~~~ shell
WWW-Authenticate: Basic realm="api"
~~~

注意：如果您在生产中使用BasicAuthentication，则必须确保您的API仅通过https提供。您还应确保您的API客户端始终在登录时重新请求用户名和密码，并且永远不会将这些详细信息存储到持久存储中。

#### TokenAuthentication

此身份验证方案使用简单的基于令牌的HTTP身份验证方案。令牌认证适用于客户端 - 服务器设置，例如本机桌面和移动客户端。

要使用TokenAuthentication方案，您需要将身份验证类配置为包含TokenAuthentication，并在INSTALLED_APPS设置中另外包含rest_framework.authtoken：

~~~ python
INSTALLED_APPS = (
    ...
    'rest_framework.authtoken'
)

~~~

> 注意：确保在更改设置后运行manage.py migrate。rest_framework.authtoken应用程序提供Django数据库迁移。

您还需要为用户创建令牌:
~~~ python

from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)

~~~

要使客户端进行身份验证，令牌密钥应包含在Authorization HTTP标头中。密钥应以字符串文字“Token”为前缀，空格分隔两个字符串。例如：

~~~

Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

~~~

> 注意：如果要在标头中使用不同的关键字，例如Bearer，只需将TokenAuthentication子类化并设置关键字类变量。

如果成功通过身份验证，TokenAuthentication将提供以下凭据:

* request.user will be a Django User instance.
* request.auth will be a rest_framework.authtoken.models.Token instance.

拒绝许可的未经身份验证的响应将导致HTTP 401 Unauthorized响应，并具有相应的WWW-Authenticate标头。例如：

~~~ python

WWW-Authenticate: Token

~~~

curl命令行工具可用于测试令牌认证API。例如：

~~~ shell

curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

~~~
注意：如果您在生产中使用TokenAuthentication，则必须确保您的API仅通过https提供。

###### Generating Tokens

***By using signals***

如果您希望每个用户都拥有自动生成的令牌，您只需捕获用户的post_save信号即可。

~~~ python

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

~~~

请注意，您需要确保将此代码段放在已安装的models.py模块中，或者在启动时由Django导入的其他位置。

如果您已经创建了一些用户，则可以为所有现有用户生成令牌，如下所示：

~~~ python

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)

~~~

***By exposing an api endpoint***
使用TokenAuthentication时，您可能希望为客户端提供一种机制，以获取给定用户名和密码的令牌。REST框架提供了一个内置视图来提供此行为。要使用它，请将obtain_auth_token视图添加到您的URLconf：

~~~ python
from rest_framework.authtoken import views
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]
~~~

> 请注意，请求的URL部分,可以使用任何内容。

当使用表单数据或JSON将有效的用户名和密码字段POST到视图时，obtain_auth_token视图将返回JSON响应：

~~~ shell
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
~~~

请注意，默认的obtain_auth_token视图显式使用JSON请求和响应，而不是在您的设置中使用默认的渲染器和解析器类。

默认情况下，没有应用于obtain_auth_token视图的权限或限制。如果您确实希望应用限制，则需要覆盖视图类，并使用throttle_classes属性包含它们。

如果您需要creation_auth_token视图的自定义版本，则可以通过继承ObtainAuthToken视图类并在您的url conf中使用它来实现。

例如，您可以返回令牌值之外的其他用户信息：

~~~ python

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

~~~

添加你的url：

~~~ python
urlpatterns += [
    url(r'^api-token-auth/', CustomAuthToken.as_view())
]

~~~

***With Django admin***

也可以通过管理界面手动创建令牌。如果您使用的是大型用户群，我们建议您修补TokenAdmin类以根据需要对其进行自定义，更具体地说，将用户字段声明为raw_field。

your_app/admin.py:

~~~python

from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)

~~~

***Using Django manage.py command***

从版本3.6.4开始，可以使用以下命令生成用户令牌：

~~~ shell
./manage.py drf_create_token <username>
~~~

此命令将返回给定用户的API令牌，如果它不存在则创建它：
~~~ shell
Generated token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b for user user1
~~~
如果您想重新生成令牌（例如，如果它已被泄露或泄露），您可以传递一个额外的参数：
~~~ shell
./manage.py drf_create_token -r <username>
~~~

#### SessionAuthentication

此身份验证方案使用Django的默认会话后端进行身份验证。会话身份验证适用于与您的网站在同一会话上下文中运行的AJAX客户端。

如果成功通过身份验证，则SessionAuthentication将提供以下凭据:

* request.user will be a Django User instance.
* request.auth will be None.

未经许可的未经身份验证的响应将导致HTTP 403 Forbidden响应。

如果您使用带有SessionAuthentication的AJAX样式API，则需要确保为任何“不安全”的HTTP方法调用（例如PUT，PATCH，POST或DELETE请求）包含有效的CSRF令牌。有关更多详细信息，请参阅Django CSRF文档。

警告：创建登录页面时始终使用Django的标准登录视图。这将确保您的登录视图得到适当保护。

REST框架中的CSRF验证与标准Django的工作方式略有不同，因为需要同时支持基于会话和非会话的身份验证。这意味着只有经过身份验证的请求才需要CSRF令牌，并且可以在没有CSRF令牌的情况下发送匿名请求。此行为不适用于登录视图，登录视图应始终应用CSRF验证。

#### RemoteUserAuthentication

此身份验证方案允许您将身份验证委派给Web服务器，该服务器设置REMOTE_USER环境变量。

要使用它，您必须在AUTHENTICATION_BACKENDS设置中使用django.contrib.auth.backends.RemoteUserBackend（或子类）。默认情况下，RemoteUserBackend为尚不存在的用户名创建User对象。要更改此行为和其他行为，请参阅Django文档。

如果成功通过身份验证，RemoteUserAuthentication将提供以下凭据：

* request.user will be a Django User instance.
* request.auth will be None.

有关配置身份验证方法的信息，请参阅Web服务器的文档，例如：

[Apache Authentication How-To](https://httpd.apache.org/docs/2.4/howto/auth.html)
[NGINX (Restricting Access)](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)

#### Custom authentication

要实现自定义身份验证方案，请继承BaseAuthentication并覆盖.authenticate（self，request）方法。如果验证成功，该方法应返回（user，auth）的两元组，否则返回None。

在某些情况下，您可能希望从.authenticate（）方法中引发AuthenticationFailed异常，而不是返回None。

通常，您应采取的方法是：

* 如果未尝试验证，则返回None。仍将使用任何其他正在使用的身份验证方案。
* 如果尝试进行身份验证但失败，则引发AuthenticationFailed异常。无论是否进行任何权限检查，都将立即返回错误响应，并且不会检查任何其他身份验证方案。

您还可以覆盖.authenticate_header（self，request）方法。如果实现，它应返回一个字符串，该字符串将用作HTTP 401 Unauthorized响应中的WWW-Authenticate标头的值。

如果未覆盖.authenticate_header（）方法，则在拒绝未经身份验证的请求访问时，身份验证方案将返回HTTP 403 Forbidden响应。

---

注意：当请求对象的.user或.auth属性调用自定义身份验证器时，您可能会看到将AttributeError重新引发为WrappedAttributeError。这是防止外部属性访问抑制原始异常所必需的。Python不会识别来自自定义身份验证器的AttributeError orginates，而是假设请求对象没有.user或.auth属性。这些错误应由您的验证者修复或以其他方式处理。

---

##### Example

以下示例将验证任何传入请求，作为用户在名为“X_USERNAME”的自定义请求标头中提供的用户。

~~~ python

from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)

~~~
### Third party packages

[第三方包查看官方文档](https://www.django-rest-framework.org/api-guide/authentication/#third-party-packages)

<!-- 还提供以下第三方软件包。

#### Django OAuth Toolkit

Django OAuth Toolkit包提供OAuth 2.0支持，可与Python 2.7和Python 3.3+一起使用。该软件包由Evonove维护，并使用优秀的OAuthLib。该软件包已有详细记录，并且得到了很好的支持，目前是我们推荐的OAuth 2.0支持包。

***Installation & configuration***

~~~ python
pip install django-oauth-toolkit
~~~

Add the package to your INSTALLED_APPS and modify your REST framework settings.

~~~python

INSTALLED_APPS = (
    ...
    'oauth2_provider',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    )
}

~~~ -->
