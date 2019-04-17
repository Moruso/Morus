## mixins 

> 混合类，作用比较简单, 定义了特定的几个方法。

[toc]

### CreateModelMixin

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

