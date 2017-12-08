#### 安装

	pip install django

#### 安装测试

	python -c "import django; print(django.get_version());"

#### 创建项目

	django-admin startproject project_name
		
> project_name 你的项目名

#### 创建app

	cd project_name
	python manage.py startapp app_name
	
> app_name  app名称
    
#### 配置启动APP

* 添加app到project_name/settings.py

	~~~shell
	INSTALLED_APPS = [
	    ......
	'app_name.apps.App_nameConfig'
	]
	~~~
	
	> 在INSTALLED_APPS = [ ]行添加配置

* 创建app urls映射文件

	> 创建```app_name/urls.py```

	~~~ python
	#encoding: utf-8
	from django.conf.urls import url
	
	urlpatterns = []
	
	~~~

	
* 添加app urls 映射到project urls

	> 修改project_name/urls.py	

	~~~python
	from django.conf.urls import url, include
	from django.contrib import amdin
	
	urlpatterns = [
	    url(r'^admin/', admin.site.urls),
	    url(r'^online/', include('app_name.urls', namespace='app_name')),
	]
	~~~
	
	
#### 配置项目(`project_name/project_name/settings.py`)
 
* 允许访问的主机名
	
		ALLOWED_HOSTS = ['*']
	
* 设置debug模式

		DEBUG = True

#### 启动服务
~~~shell
python manage.py runserver IP:PORT
~~~

#### 额外配置(修改`project_name/project_name/settings.py`)

* 配置模板目录

	~~~python
	TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [os.path.join(BASE_DIR, 'templates')],
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                'django.template.context_processors.debug',
	                'django.template.context_processors.request',
	                'django.contrib.auth.context_processors.auth',
	                'django.contrib.messages.context_processors.messages',
	            ],
	        },
	    },
	]
	~~~
	
* 配置数据库

	~~~python
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'data_name',
	        'USER': 'root',
	        'PASSWORD': '123123',
	        'HOST': '127.0.0.1',
	        'PORT': 3306,
	        'CHARSET' : 'utf8',
	    }
	}
	~~~
	
* 配置静态文件

	~~~ python
	STATIC_URL = '/static/'
	
	STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')
	
	STATICFILES_DIRS = [
	    os.path.join(BASE_DIR, 'static'),
	]
	
	MEDIA_URL = '/media/'
	MEDIA_ROOT= os.path.join(BASE_DIR, 'media')
	~~~

#### django shell

* modesl DDL修改同步
	
	~~~shell
	python manager.py makemigrations
	python manager.py migrate
	~~~
