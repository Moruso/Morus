## Generic views
> Base class for all other generic views
> 允许您快速构建与数据库模型紧密映射的API view, 如果通用视图不适合您的API的需要，你可以使用常规APIView类,或重用mixin和基类使用的通用视图来组成自己的组可重用通用视图

[TOC]

### Attributes

#### Basic settings:

> 以下属性控制的基本视图的行为

###### queryset

    视图返回对象, 必须设置这个属性或者重写get_queryset()方法。
    如果你要重写这个视图函数, 获取该属性可以通过get_queryset()方法来替代直接访问。queryset 将评估一次,这些结果将为所有后续请求被缓存。

###### serializer_class
    
    序列化类，将用于对输入进行验证和反序列化以及对输出内容序列化, 你必须设置这个属性,或覆盖get_serializer_class()方法。

###### lookup_field

    模型的字段，被用来执行单个模型实例对象查找。默认是'pk'.注意,当使用超链接API, 如果需要使用自定义值,需要确保 API视图 和 序列化类设置了查找字段。

###### lookup_url_kwarg

    URL关键字参数用来对象查找，URL配置应包括一个关键字参数对应于这个值，如果没有设置，默认值将和lookup_filed使用相同的值

#### Pagination 

> 以下属性是用来控制分页时用于列表视图。

###### pagination_class

    分页类 当一个list views 需要分页的时候被使用，默认将和DEFAULT_PAGINATION_CLASS设置值一样。设置pagination_class=None将禁用分页。

#### Filtering

###### filter_backends
    
    过滤后端类的列表, 应该用于过滤queryset. 默认和 DEFAULT_FILTER_BACKENDS 设置一样

### Methods

###### get_queryset(self)

    返回用于list views 的queryset. 也被用作详细视图中查找的基础, 默认返回queryset属性指定的查询集。
    应始终使用此方法，而不是直接访问self.queryset，因为self.queryset只被评估一次，并且所有后续请求都会缓存这些结果。
    可以重写以提供动态行为，例如返回查询集，该查询集特定于发出请求的用户。

For example:：

~~~ python

def get_queryset(self):
    user = self.request.user
    return user.accounts.all()

~~~


######  get_object(self)

    返回用于detail views 的实例对象，默认使用lookup_field参数来过滤queryset.
    可以被重写以提供更复杂的行为, 例如基于多个URL kwarg的对象查找

For example:

~~~ python
def get_object(self):
    queryset = self.get_queryset()
    filter = {}
    for field in self.multiple_lookup_fields:
        filter[field] = self.kwargs[field]

    obj = get_object_or_404(queryset, **filter)
    self.check_object_permissions(self.request, obj)
    return obj
~~~

> 如果您的API不包含任何对象级权限,您可以选择排除self.check_object_permissions, 并简单地从get_object_or_404查找返回该对象。

###### filter_queryset(self, queryset)

    给定一个queryset，使用任何过滤后端过滤它，返回一个新的queryset.

For example:

~~~ python 

def filter_queryset(self, queryset):
    filter_backends = (CategoryFilter,)

    if 'geo_route' in self.request.query_params:
        filter_backends = (GeoRouteFilter, CategoryFilter)
    elif 'geo_point' in self.request.query_params:
        filter_backends = (GeoPointFilter, CategoryFilter)

    for backend in list(filter_backends):
        queryset = backend().filter_queryset(self.request, queryset, view=self)

    return queryset
~~~

###### get_serializer_class(self)

    返回一个序列化的类, 默认返回serializer_class属性。
    可以被重写以提供动态行为,例如使用不同的serializers进行读写操作，或者为不同类型的用户提供不同的serializers。

For example:

~~~ python

def get_serializer_class(self):
    if self.request.user.is_staff:
        return FullAccountSerializer
    return BasicAccountSerializer

~~~

#### Save and deletion hooks

    mixin类提供了以下方法，并提供对象保存或删除行为的轻松覆盖。

* perform_create(self，serializer) - 在保存新对象实例时由CreateModelMixin调用。
* perform_update(self，serializer) - 在保存现有对象实例时由UpdateModelMixin调用。
* perform_destroy(self，instance) - 在删除对象实例时由DestroyModelMixin调用.

> 这些钩子对于设置隐含在请求中的的属性特别的有用,但不是请求数据的一部分.

    例如: 
    您可以根据请求用户在对象上设置属性,或基于URL关键字参数。

~~~ python
def perform_create(self, serializer):
    serializer.save(user=self.request.user)
~~~ 

> 这些覆盖点也特别有用,当保存一个对象之前或之后添加一些特性，例如通过电子邮件发送确认或审计更新。

~~~ python
def perform_update(self, serializer):
    instance = serializer.save()
    send_email_confirmation(user=self.request.user, modified=instance)
~~~ 

    你还可以使用这些钩子来提供额外的验证，通过抛出ValidationError()，如果您需要在数据库保存时应用某些验证逻辑，这可能很有用。例如：

~~~ python

def perform_create(self, serializer):
    queryset = SignupRequest.objects.filter(user=self.request.user)
    if queryset.exists():
        raise ValidationError('You have already signed up')
    serializer.save(user=self.request.user)

~~~
> 这些方法取代了旧版本的2.x pre_save，post_save，pre_delete和post_delete方法，这些方法已不再可用。

#### Other methods:
    您通常不需要覆盖以下方法，但如果您使用GenericAPIView编写自定义视图，则可能需要调用它们。

###### get_serializer_context（self）

    返回一个字典，其中包含应提供给序列化程序的任何额外上下文。默认包括'request','view', 'format' keys。

###### get_serializer(self, instance=None, data=None, many=False, partial=False)

    返回一个 serializer 实例

###### get_paginated_response（self，data）
    
    返回分页样式的Response对象。

###### paginate_queryset（self，queryset）

    如果需要，可以返回查询集，返回页面对象;如果没有为此视图配置分页，则为“None”。

###### filter_queryset（self，queryset） 

    给定一个查询集，使用正在使用的过滤后端进行过滤，返回一个新的查询集。
