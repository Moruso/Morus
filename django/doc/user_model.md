#### 自定义User Model的使用方法

* 获取当前使用model的方法

~~~ python
from django.contrib.auth import get_user_model

get_user_model()
~~~

* 使用自定义的User Model 需要修改setting 添加 AUTH_USER_MODEL

~~~ python
AUTH_USER_MODEL = "app.NewUser"
~~~

* 外键使用自定义 USER MODEL 不要使用get_user_model()

~~~
from django.conf import settings
from django.db import models

class Blog(model.Model):
	author = model.ForeignKey(settings.AUTH_USER_MODEL)
    
    ……
~~~

#####  扩展AbstractUser类

AbstractUser类默认提供了一些field，如果你对这些field觉得满意就可以直接扩展AbstractUser

~~~python 
from django.contrib.auth.models import AbstractUser
from django.db import models

class NewUser(AbstractUser):
    new_field = models.CharField(max_length=100)

~~~

##### 扩展 AbstractBaseUser类

如果你的AbstractUser提供的field不满意，使用AbstractBaseUser 只提供了3个field： password, last_login 和is_active.

~~~python 
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class NewUser(AbstractBaseUser):
    new_field = models.CharField(max_length=100)

~~~

##### 使用OneToOneField

~~~ python
from django.contrib.auth.models import User
class UserExt(models.Model):
    user = models.OneToOneField(User)

~~~






