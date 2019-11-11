# cookbook

#### 过滤当前用户的数据

> 比如获取当前用户的recipient, 

###### 解决： 重写query_set()方法

~~~ python


~~~

### depth 无法添加
> serializers的时候使用了depth可以递归的显示相关信息，但是无法添加内容，

###### 解决: 定义2个serializers，一个用户depth参数用来展示内容,一个没有depth参数用来添加修改。

~~~ python


~~~

### ManyToManyField 当post添加时显示的主键而不是可读性的名字时

###### 解决：重写 Model 类__str__方法