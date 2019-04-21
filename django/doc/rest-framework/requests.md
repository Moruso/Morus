## Requests
REST框架的Request类扩展了标准的HttpRequest，增加了对REST框架灵活的请求解析和请求认证的支持。

[TOC]

### Request parsing

REST框架的Request对象提供灵活的请求解析，允许您以与通常处理表单数据相同的方式处理具有JSON数据或其他媒体类型的请求。

###### .data

request.data返回请求正文的已解析内容。这类似于标准的request.POST和request.FILES属性，除了：

* 它包括所有已解析的内容，包括文件和非文件输入。
* 它支持解析除POST之外的HTTP方法的内容，这意味着您可以访问PUT和PATCH请求的内容。
* 它支持REST框架的灵活请求解析，而不仅仅支持表单数据。例如，您可以像处理传入表单数据一样处理传入的JSON数据。

###### .query_params

request.query_params是request.GET的更正确命名的同义词。
为清楚起见，我们建议使用request.query_params而不是Django的标准request.GET。这样做有助于保持代码库更加正确和明显 - 任何HTTP方法类型都可能包含查询参数，而不仅仅是GET请求。

###### .parsers

APIView类或@api_view装饰器将根据视图上设置的parser_classes或基于DEFAULT_PARSER_CLASSES设置，确保此属性自动设置为Parser实例列表。

> 您通常不需要访问此属性。
---

* 注意：如果客户端发送格式错误的内容，则访问request.data可能会引发ParseError。默认情况下，REST框架的APIView类或@api_view装饰器将捕获错误并返回400 Bad Request响应。
* 如果客户端发送的请求具有无法解析的内容类型，则将引发UnsupportedMediaType异常，默认情况下将捕获该异常并返回415 Unsupported Media Type响应。

---

### Content negotiation

该请求公开了一些允许您确定内容协商阶段结果的属性。这允许您实现诸如为不同媒体类型选择不同序列化方案之类的行为。

###### .accepted_renderer

内容协商阶段选择的渲染器实例。

###### .accepted_media_type

表示内容协商阶段接受的媒体类型的字符串。

### Authentication

REST框架提供灵活,按需的请求身份验证，使您能够执行以下操作:

* 对API的不同部分使用不同的身份验证策略。
* 支持使用多种身份验证策略。
* 提供与传入请求关联的用户和令牌信息。


###### .user

request.user通常返回django.contrib.auth.models.User的实例，但行为取决于所使用的身份验证策略。

如果请求未经身份验证，则request.user的默认值是django.contrib.auth.models.AnonymousUser的实例。

###### .auth

request.auth返回任何其他身份验证上下文。request.auth的确切行为取决于所使用的身份验证策略，但它通常可能是请求经过身份验证的令牌实例。

如果请求未经身份验证，或者没有其他上下文，则request.auth的默认值为None。

###### .authenticators

APIView类或@api_view装饰器将根据在视图上设置的authentication_classes或基于DEFAULT_AUTHENTICATORS设置，确保此属性自动设置为Authentication实例列表。

> 您通常不需要访问此属性。

---

注意：调用.user或.auth属性时，可能会看到引发WrappedAttributeError。这些错误源自身份验证器作为标准AttributeError，但是必须将它们重新引发为不同的异常类型，以防止它们被外部属性访问限制。Python不会识别来自身份验证器的AttributeError orginates，而是假设请求对象没有.user或.auth属性。验证者需要修复。

---

### Browser enhancements

REST框架支持一些浏览器增强功能，例如基于浏览器的PUT，PATCH和DELETE表单。

###### .method

request.method返回请求的HTTP方法的大写字符串表示形式。
基于浏览器的PUT，PATCH和DELETE表单是透明支持的。

###### .content_type

request.content_type，返回表示HTTP请求主体的媒体类型的字符串对象，如果未提供媒体类型，则返回空字符串。

您通常不需要直接访问请求的内容类型，因为您通常会依赖REST框架的默认请求解析行为。

如果确实需要访问请求的内容类型，则应优先使用.content_type属性，而不是使用request.META.get（'HTTP_CONTENT_TYPE'），因为它为基于浏览器的非表单内容提供透明支持。

###### .stream

request.stream返回表示请求正文内容的流。
您通常不需要直接访问请求的内容，因为您通常会依赖REST框架的默认请求解析行为。

### Standard HttpRequest attributes

由于REST框架的Request扩展了Django的HttpRequest，所有其他标准属性和方法也可用。例如，request.META和request.session词典可以正常使用。

请注意，由于实现原因，Request类不从HttpRequest类继承，而是使用composition扩展类。
