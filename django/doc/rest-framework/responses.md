## Responses

REST框架通过提供Response类来支持HTTP内容协商，该类允许您返回可以呈现为多种类型的内容，具体取决于客户端请求。

Response类是Django的SimpleTemplateResponse的子类。响应对象使用数据初始化，数据应包含原生Python原语。然后，REST框架使用标准HTTP内容协商来确定它应如何呈现最终响应内容。

您无需使用Response类，如果需要，您还可以从视图中返回常规HttpResponse或StreamingHttpResponse对象。使用Response类只是为返回内容协商的Web API响应提供了一个更好的界面，可以将其呈现为多种格式。

除非您出于某种原因想要大量自定义REST框架，否则应始终对返回Response对象的视图使用API​​View类或@api_view函数。这样做可确保视图可以在从视图返回之前执行内容协商并为响应选择适当的渲染器。

[TOC]

### Creating responses

###### Response()

Response(data, status=None, template_name=None, headers=None, content_type=None)

与常规HttpResponse对象不同，您不会使用呈现的内容实例化Response对象。而是传入未呈现的数据，这些数据可能包含任何Python原语。

Response类使用的渲染器本身不能处理复杂的数据类型，例如Django模型实例，因此在创建Response对象之前，需要将数据序列化为原始数据类型。

您可以使用REST框架的Serializer类来执行此数据序列化，或使用您自己的自定义序列化。

Arguments:

* data：响应的序列化数据。
* status：响应的状态代码。默认为200。
* template_name：如果选择了HTMLRenderer，则使用的模板名称。
* headers：要在响应中使用的HTTP标头的字典。
* content_type：响应的内容类型。通常，这将由内容协商确定的渲染器自动设置，但在某些情况下您可能需要明确指定内容类型。

### Attributes

###### .data

响应的未呈现的序列化数据。

###### .status_code

HTTP响应的数字状态代码。

###### .content

呈现的响应内容。必须先调用.render（）方法才能访问.content。

###### .template_name

template_name（如果提供）。仅当HTMLRenderer或某些其他自定义模板渲染器是响应的接受渲染器时才需要。

###### .accepted_renderer

将用于呈现响应的呈示器实例。

在从视图返回响应之前，立即由APIView或@api_view自动设置。

###### .accepted_media_type

内容协商阶段选择的媒体类型。

在从视图返回响应之前，立即由APIView或@api_view自动设置。

###### .renderer_context

将传递给渲染器的.render（）方法的其他上下文信息的字典。

在从视图返回响应之前，立即由APIView或@api_view自动设置。

### Standard HttpResponse attributes

Response类扩展了SimpleTemplateResponse，并且响应中也提供了所有常用属性和方法。例如，您可以按标准方式在响应上设置标题：

~~~python

response = Response()
response['Cache-Control'] = 'no-cache'

~~~

###### .render()

与任何其他TemplateResponse一样，调用此方法可将响应的序列化数据呈现到最终响应内容中。

调用.render（）时，响应内容将设置为在accepted_renderer实例上调用.render（data，accepted_media_type，renderer_context）方法的结果。

您通常不需要自己调用.render（），因为它是由Django的标准响应周期处理的。