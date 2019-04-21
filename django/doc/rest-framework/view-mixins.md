## mixins 
> mixin类提供用于基本视图行为的操作, 请注意，mixin类提供了操作方法，而不是定义处理程序的方法,例如.get（）和.post(),这允许更灵活的行为组合.
> 混合类 作用比较简单, 定义了特定的几个方法。
> 混合类 可以从rest_framework.mixins 导入

[toc]

### CreateModelMixin

    提供了.create(request, *args, **kwargs)方法，实现创建并保存一个新的model 实例。
    如果对象被创建返回201 Created 响应， 响应数据的主体为序列化后的对象。如果representation包含名为url的键，则响应的Location头将填充该值。 如果为创建对象而提供的请求数据无效，将返回400 Bad Request响应,响应的主体为错误详情。

~~~ python
class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # 获取serializer 对象
        serializer.is_valid(raise_exception=True) # 对数据进行验证
        self.perform_create(serializer) # 调用了serializer的save方法
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


~~~

> 实现了一个create方法, 调用serializer.save(),创建一个model实例,, 
> serializer.save()根据不同的参数对实现了对model实例的创建或更新

### ListModelMixin

    提供了.list(request, *args, **kwargs)方法，实现列出查询集。
    如果查询集存在,这会返回200 OK响应，响应的主体为序列化后的查询集,响应数据可以选择分页。

~~~ python
class ListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()) # 获取一个queryset

        page = self.paginate_queryset(queryset) 
        if page is not None:  # 判断是否分页
            serializer = self.get_serializer(page, many=True)  
            return self.get_paginated_response(serializer.data) # 返回分页数据

        serializer = self.get_serializer(queryset, many=True)  
        return Response(serializer.data) # 返回不分页
~~~

> 展示queryset中的所有对象
> get_serializer方法定义在 GenericAPIView 中

### RetrieveModelMixin

    提供了.retrieve(request, *args, **kwargs)方法，实现了在响应中返回现有的模型实例。
    如果对象可以被检索,那么将返回200ok 响应，并且相应的主体是序列化后的对象。如果无法被检索，将返回404 Not found.

~~~ python
class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object() # 获取实例对象
        serializer = self.get_serializer(instance) 
        return Response(serializer.data) 
~~~

### UpdateModelMixin

    提供了.update(request, *args, **kwargs)方法，实现了更新并保存一个现有的模型实例。
    也提供了.partial_update(request, *args, **kwargs)方法，这与update方法类似，除了更新的所有字段，剩下的都是可选的。也支持http PATCH请求.
    如果对象更新，则返回200 OK响应，使用序列化后的对象作为响应的主体。
    如果为更新对象而提供的请求数据无效，将返回400 Bad Request响应，响应主体为错误详情

~~~python
class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) # 部分更新
        instance = self.get_object() # 获取实例
        serializer = self.get_serializer(instance, data=request.data, partial=partial) # 获取序列化实例
        serializer.is_valid(raise_exception=True) # 验证数据
        self.perform_update(serializer) #更新

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

~~~

### DestroyModelMixin

    提供了.destroy(request, *args, **kwargs)方法，实现了删除现有的模型实例。
    如果对象被成功删除，则返回204 No Content响应。否则，返回404 Not Found.

~~~ python
class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # 获取实例
        self.perform_destroy(instance) # 销毁实例
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

~~~

