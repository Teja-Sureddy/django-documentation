# Django REST framework

You can put most of the config in the settings.


## Table of Contents

- [Request](#request)
- [Response](#response)
- [Class Based Views](#class-based-views)
- [Function Based Views](#function-based-views)
- [Generic Views](#generic-views)
- [Viewset](#viewset)
- [Routers](#routers)
- [Parsers](#parsers)
- [Renderers](#renderers)
- [Serializers](#serializers)
- [Authentication](views/authentication.py)
- [Cache](#cache)
- [Throttling](#throttling)
- [Filtering](#filtering)
- [Pagination](#pagination)
- [Versioning](#versioning)
- [Others](#others)



----
## <u>Request</u>
<a id="request"></a>

| request.          | Description                                                  |
|-------------------|--------------------------------------------------------------|
| data              | It has request body (Same as request.POST and request.FILES) |
| query_params      | Same as request.GET                                          |
| user              | User instance                                                |   
| method            | Displays the method like GET, POST, PUT, PATCH, DELETE, ...  |
| content_type      | Display the content type (Ex: application/json, text/plain)  | 
| parsers           | Lists the parsers used (Default: JSON, Form, MultiPart)      |
| accepted_renderer | Display the Renderer used (Default: JSON, BrowsableAPI)      |   
| auth              | Displays any additional authentication context (Like Token)  |  
| authenticators    | Lists the authenticators used (Ex: Token, Session)           |   



----
## <u>Response</u>
<a id="response"></a>

Signature: `Response(data, status=None, template_name=None, headers=None, content_type=None)`
 - data: The serialized data for the response.
 - status: A status code for the response. Defaults to 200.
 - template_name: A template name to use if HTMLRenderer is selected.
 - headers: A dictionary of HTTP headers to use in the response.
 - content_type: The content type of the response.

There are others too `HttpResponse, JsonResponse, Http404, HttpResponseNotAllowed, ...`



----
## <u>Class Based Views</u>
<a id="class-based-views"></a>

All views will use the default attributes (renderers, parsers, authentication, etc.) specified in the settings.


### Attributes
renderer_classes - `JSON, BrowsableAPI, StaticHTML, ...`  
parser_classes - `JSON, Form, MultiPart and FileUpload`  
authentication_classes - `Basic, Session and Token`  
throttle_classes - `SimpleRate, AnonRate, UserRate and ScopedRate`  
permission_classes - `AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions, ...`  
content_negotiation_class - `DefaultContent` [More..](#content-negotiation)  

metadata_class - `SimpleMetadata` [More..](#metadata)      
versioning_class - `AcceptHeaderVersioning, URLPathVersioning, ...`  

### Methods
 - You can check the attribute values by calling `self.get_<attribute>()`.
 - In the view, when a request is received, first it calls
   1. `dispatch()` Start
   2. `initialize_request()`
   3. `initial()` Start
   4. `Classes: authentication, permission, throttle, ...`
   5. `initial()` Ends
   6. `get(), post(), put(), patch() and delete()`
   7. `finalize_response()`
   8. `dispatch()` Ends
 - When any exception is raised from anywhere `handle_exception()` will get called.
 - Usually `dispatch()` method is used to perform any actions that need to occur before or after calling get(), post(), put(), patch() and delete().



----
## <u>Function Based Views</u>
<a id="function-based-views"></a>

It is same as Class Based Views but instead of attributed we use decorators and doesn't have any in-built methods.


### Decorators
api_view - Converts a function-based view into an APIView subclass.  
renderer_classes - `JSON, BrowsableAPI, StaticHTML, ...`  
parser_classes - `JSON, Form, MultiPart and FileUpload`  
authentication_classes - `Basic, Session and Token`  
throttle_classes - `SimpleRate, AnonRate, UserRate and ScopedRate`  
permission_classes - `AllowAny, IsAuthenticated, IsAdminUser, ...`  
schema - `Auto, Manual` it is for documentation.



---
## <u>Generic Views</u>
<a id="generic-views"></a>

It is the extension of APIView, You can use all the attributes, methods present in APIView.  
Simple case, `path('', ListCreateAPIView.as_view(queryset=Model.objects.all(), serializer_class=ModelSerializer), name='')`.


### Attributes
queryset - `Model.objects.all()` You can set this attribute or override the get_queryset() by returning queryset.  
serializer_class - `ModelSerializer` It is used for validating and deserializing input and serializing output. 
lookup_field - It is used for performing object lookup of individual model instances. Defaults to `pk`.   
lookup_url_kwarg - The queryset will be `queryset.get(pk=self.kwargs[self.lookup_url_kwarg])`.
pagination_class - `PageNumber, LimitOffset, Cursor`  
filter_backends - `Search, Ordering`  


### Methods
 - You can get or override the queryset by `get_queryset()`.
 - You can get or override the serializer_class by `get_serializer_class()`.
 - `get_object()` used to get a single object by lookup_field.
 - `filter_queryset()` uses filter_backends, or you can have a custom filters.
 - Save and deletion hooks `perform_create(), perform_update(), perform_destroy()`.


### Views

* CreateAPIView - 'post' - create new instances of a model
* ListAPIView - 'get' - retrieve a list of objects from a queryset
* RetrieveAPIView - 'get' - retrieve a single object from a queryset
* DestroyAPIView - 'delete' - delete an instance from a model
* UpdateAPIView - 'update' - update a model instance
* ListCreateAPIView - 'get', 'post'
* RetrieveUpdateAPIView - 'get', 'put', 'patch'
* RetrieveDestroyAPIView - 'get', 'delete'
* RetrieveUpdateDestroyAPIView - 'get', 'put', 'patch', 'delete'



---
## <u>Viewset</u>
<a id="viewset"></a>

It is the extension of APIView, You can use all the attributes, methods present in APIView.  

You can register the viewset with a router class. else you need to mention urlconf inside the as_view() like 
`ModelViewSet.as_view({'get': 'list'})`.

Usually PUT or `update()` method replaces all the data, 
Where PATCH or `partial_update()` method replaces the provided data.


### Attributes that are available
basename - the basename that you have mentioned in the url path.  
action - list, create, retrieve, ...  
detail - If pk is used in the queryset, then detail will be True else False.   
suffix  
name  
description  

You can access the attributes anywhere. Ex: In the permissions function to allow based on the basename, action, ...


### Methods
 - Instead of `get()` or `post()`, It provides actions such as `list()` and `create()`.
 - Actions: `list()`, `create()`, `retrieve()`, `update()`, `partial_update()` and `destroy()`.
 - To set name and description attributes, You can override the `get_view_name()` and `get_view_description()` methods to return the desired values.


### Action Decorator
If you want to add additional methods to the same ViewSet but with a custom path, 
You can create a custom method within the ViewSet and decorate it with the `@action()` decorator.

By default, all the attributes mentioned in the ViewSet will be set for the `@action()` decorator unless you explicitly specify an attribute.  
In addition to that, There are `methods`, `detail`, `url_path`, `url_name`, `name` attributes.

If you want each method for each get, post, put ..., with common `@action()` decorator and a path,  
You need to have a method (Ex: `action_get()`) with `@action` decorator, then for other methods, use `@action_get.mapping.post`, `@action_get.mapping.put`, ...


### Views

* GenericViewSet
* ModelViewSet
* ReadOnlyModelViewSet



---
## <u>Routers</u>
<a id="routers"></a>

For simple/default router which is used in urls, You can add regex to the lookup_field's (lookup_field defaults to pk) value by
defining `lookup_value_regex = '[0-9a-z]{32}'` attribute in the viewset class.

Simple and Default router are same, Where default router does have `[.format]` at the end which can support `.json`, `.api`, ...



---
## <u>Parsers</u>
<a id="parsers"></a>

When `request.data` is accessed, REST framework will examine the `Content-Type` header on the incoming request, 
and determine which parser to use to parse the request content.

| Parser     | Parses                      | Description                                                                                               | media_type                        |
|------------|-----------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------|
| JSON       | JSON request content        | `request.data` will be populated with a `dictionary` of data                                              | application/json                  |
| Form       | HTML form content           | `request.data` will be populated with a `QueryDict` of data                                               | application/x-www-form-urlencoded |
| MultiPart  | Multipart HTML form content | `request.data` and `request.FILES` will be populated with a `QueryDict` and `MultiValueDict` respectively | multipart/form-data               |
| FileUpload | Raw file upload content     | `request.data` property will be a `dictionary` with a single key 'file' containing the uploaded file      | \*/\*                             |

You will typically want to use both `Form` and `MultiPart` Parser together in order to fully support `HTML form data`.

For `FileUpload`, The client can set the `filename` in the `Content-Disposition` HTTP header.



---
## <u>Renderers</u>
<a id="renderers"></a>

| Renderer     | Description (charset: utf-8)                                                                              | media_type          |
|--------------|-----------------------------------------------------------------------------------------------------------|---------------------|
| JSON         | You need to pass the `data` to the _Response_ which renders into `JSON`.                                  | application/json    |
| TemplateHTML | You need to pass the `data` and a `template_name` to the _Response_ which renders a `HTML with the data`. | text/html           |
| StaticHTML   | You need to pass the `static HTML as text` to a _Response_ as data renders into `HTML`.                   | text/html           |
| BrowsableAPI | It renders data into HTML (Does have a form). Default template: `rest_framework/api.html`.                | text/html           |
| Admin        | It Renders data into HTML (Doesn't have a form) for an table-like display.                                | text/html           |
| HTMLForm     | You can render a form by passing `serializer` into an custom HTML form using `render_form `.              | text/html           |

You can have a custom renderer like ImageRenderer to render only Images.


### Render to Parse
```
content = JSONRenderer().render(serializer.data)
stream = io.BytesIO(content)
data = JSONParser().parse(stream)
```


---
## <u>Serializers</u>
<a id="serializers"></a>

It converts complex data such as `querysets` and `model instances` to `Python datatypes` that can then be easily rendered into `JSON`, `XML`,...

Serializers also provide deserialization, allowing parsed data to be converted back into complex types.

Serialization:
```
queryset = MyModel.objects.all()
serializer = MyModelSerializer(queryset, many=True)
```

deserialization:
```
serializer = MyModelSerializer(data=data)  # to create
serializer = MyModelSerializer(instance, data=data)  # to update

serializer.is_valid()  # returns True/False
serializer.errors  # returns error in dict

serializer.save()  # Will actually create/update
```

By default, All required fields needs to be passed to the serializers else it will raise validation errors. 
You can use `partial=True` in the `ModelSerializer()` to allow partial updates.


### Attributes
initial_data  
validated_data - Returns validated incoming data. Only available after calling `is_valid()`.  
errors - Returns any errors during validation. Only available after calling `is_valid()`.  
data - Returns dict representation of the serialized data. Only available after calling `is_valid()`.  

All the attributes are available in Deserialization. Only `data` attribute is available in Serialization.


### Methods
to_internal_value - Deserialization, for write operations.  
to_representation - Serialization, for read operations.  
create  
update  
save - It calls `update` if instance argument is present else `create`.  
is_valid - Deserializes and validates incoming data.  


### Validation
It is similar to the django form validators/clean.

```
# Field validator
def field_validator(value):
   if not value:
      raise serializers.ValidationError('Invalid field my_field.')

my_field = serializers.IntegerField(validators=[field_validator])

# Field level validator
def validate_my_field(self, value):
   if not value:
      raise serializers.ValidationError('Invalid field my_field.')

# Object level validator
def validate(self, data):
   if not data['value']:
      raise serializers.ValidationError('Invalid field my_field.')
```


### Meta
```
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__' (or) ['id', 'name', 'email']
        exclude = ['phone']
        depth = 1
        read_only_fields = ['gender']
        extra_kwargs = {'password': {'write_only': True}}
        unique_together = ['name', 'email']
        ordering = ['name']
        validators = []
```

 - You can add extra fields or override the default fields.
 - `model` and one of the attributes `fields` or `exclude` are required.
 - `depth` indicates the depth of the primary keys for relationships.


### Types
1. **ModelSerializer**  

2. **HyperlinkedModelSerializer**  
It is same as ModelSerializer but has `HyperlinkedIdentityField` and `HyperlinkedRelatedField`.  
Including a `url` field with a `view_name` and a `lookup_field` will generate a link directing to that specific view.
Need to pass `context={'request': request}` when instantiating a serializer.

3. **ListSerializer**  
It can validate multiple objects at once. 
You can simply pass `many=True` when instantiating any serializer which will create a `ListSerializer` instance.


### Serializer field
| Types            | Fields                                                                                                                |
|------------------|-----------------------------------------------------------------------------------------------------------------------|
| Boolean          | `BooleanField`                                                                                                        | 
| String           | `CharField` `EmailField` `RegexField` `SlugField` `URLField` `UUIDField` `FilePathField` `IPAddressField`             |
| Numeric          | `IntegerField` `FloatField` `DecimalField`                                                                            | 
| Date and Time    | `DateTimeField` `DateField` `TimeField` `DurationField`                                                               |
| Choice selection | `ChoiceField` `MultipleChoiceField`                                                                                   |
| File upload      | `FileField` `ImageField`                                                                                              |
| Composite        | `ListField` `DictField` `HStoreField` `JSONField`                                                                     |
| Relation         | `StringRelatedField` `PrimaryKeyRelatedField` `HyperlinkedRelatedField` `SlugRelatedField` `HyperlinkedIdentityField` |


#### Arguments
 - `read_only`, `write_only`, `required`, `allow_null`  
 - `default` - When serializing the instance, default will be used if the object attribute or dictionary key is not present in the instance.  
 - `initial` - Used for pre-populating the value of HTML form fields.  
 - `source` - URLField(source='get_absolute_url') or EmailField(source='user.email').  
 - `validators`, `error_messages`, `label`, `help_text`, `style`.  


#### Relations
 - StringRelatedField - It gets the __str__ method value for each.  
 - PrimaryKeyRelatedField - It will have the primary key value for each.  
 - HyperlinkedRelatedField - It has the url of the mentioned view for each.  
 - SlugRelatedField - It gets the column value that we mentioned for each.  
 - HyperlinkedIdentityField - It is similar to HyperlinkedRelatedField but will have only one url.  

If you are fetching data along with relation data use
`Model.objects.prefetch_related('serialize_field_name')` to avoid additional database hits.


#### Nested relationships
You can have Serializer as field in another serializer for nested relationships.  

By default, nested serializers are read-only. 
you'll need to have custom create() and update() methods in order to save the child relationships.



---
## <u>Cache</u>
<a id="cache"></a>


|                 |                                                        |
|-----------------|--------------------------------------------------------|
| cache_page      | Temporarily stores a response.                         |
| vary_on_headers | Responses stored separately based the request headers. |
| vary_on_cookie  | Responses stored separately based the cookie.          |


```
@method_decorator(cache_page(60 * 60 * 2))
@method_decorator(vary_on_cookie)
@method_decorator(vary_on_headers("Authorization"))
def list(self, request, format=None):
    ...
```



---
## <u>Throttling</u>
<a id="throttling"></a>

It refers to the process of limiting the number of requests that a user can make to an API within a certain period of time.


|                    |                                                                                                                   |
|--------------------|-------------------------------------------------------------------------------------------------------------------|
| AnonRateThrottle   | Limits the number of requests that can be made by anonymous users.                                                |
| UserRateThrottle   | Limits the number of requests that can be made by authenticated users.                                            |
| ScopedRateThrottle | Allows to set different throttling rates for different scopes, such as per user, per IP address, or per endpoint. |



---
## <u>Filtering</u>
<a id="filtering"></a>


|                     |                                                                                                                                                                                                                                            |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DjangoFilterBackend | Add this to the `filter_backends` and set the `filterset_fields` will give you the HTML form with fields mentioned to search. <br>`django-filter` needs to be installed, and you can directly implement it on generics views and viewsets. |
| SearchFilter        | Add this to the `filter_backends` and set the `search_fields` will give you one field to search all the mentioned fields. Default: `None`                                                                                                  | 
| OrderingFilter      | Add this to the `filter_backends` and set the `ordering_fields` will give you the buttons to order the list. Default: `'__all__'`                                                                                                          |



---
## <u>Pagination</u>
<a id="pagination"></a>


|                       |                         |
|-----------------------|-------------------------|
| PageNumberPagination  | `?page=4&page_size=100` |
| LimitOffsetPagination | `?offset=400&limit=100` |
| CursorPagination      |                         |



---
## <u>Versioning</u>
<a id="versioning"></a>

When API versioning is enabled, the `request.version` attribute will contain a string that corresponds to the version requested in the incoming client request.

You can assign the version class to `versioning_class` attribute. 


|                          |                                                                                                             |
|--------------------------|-------------------------------------------------------------------------------------------------------------|
| AcceptHeaderVersioning   | Specify the version as part of the media type in the Accept header. `Accept: application/json; version=1.0` |
| URLPathVersioning        | Specify the version as part of the URL path. `re_path(r'^(?P<version>(v1&#124;v2))/')`                      |
| NamespaceVersioning      | It checks URL namespacing for the version. `namespace='v1'`                                                 |
| HostNameVersioning       | Specify the requested version as part of the hostname in the URL. `Host: v1.example.com`                    |
| QueryParameterVersioning | Include the version as a query parameter in the URL. `?version=1.0`                                         |



---
## <u>Others</u>
<a id="others"></a>

### Content negotiation

It is the process of determining the appropriate content type (e.g., JSON, XML, HTML) for a response based on the client's preferences.  

It allows clients to specify the desired content type using HTTP headers like Accept and Content-Type, and the server responds with the appropriate content type.

`content_negotiation_class  = DefaultContentNegotiation`


### Metadata

It determines how your API should respond to OPTIONS requests.

`metadata_class = SimpleMetadata`

### Exceptions and Status

Check `rest_framework.exceptions` and `rest_framework.status`.


### Settings

Default API settings:
```
REST_FRAMEWORK = {
   'DEFAULT_RENDERER_CLASSES': [
      'rest_framework.renderers.JSONRenderer',
      'rest_framework.renderers.BrowsableAPIRenderer'
   ],
   
   'DEFAULT_PARSER_CLASSES': [
      'rest_framework.parsers.JSONParser',
      'rest_framework.parsers.FormParser',
      'rest_framework.parsers.MultiPartParser'
   ],
   
   'DEFAULT_AUTHENTICATION_CLASSES': [
      'rest_framework.authentication.SessionAuthentication',
      'rest_framework.authentication.BasicAuthentication'
   ],
   
   'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.AllowAny'
   ],
   
   'DEFAULT_THROTTLE_CLASSES': [],
   
   'DEFAULT_CONTENT_NEGOTIATION_CLASS': [
      'rest_framework.negotiation.DefaultContentNegotiation'
   ],
   
   'DEFAULT_SCHEMA_CLASS': [
      'rest_framework.schemas.openapi.AutoSchema'
   ],
}
```

Default Generic view settings:
```
REST_FRAMEWORK = {
   'DEFAULT_FILTER_BACKENDS': None,
   'DEFAULT_PAGINATION_CLASS': None,
   'PAGE_SIZE': None,
   'SEARCH_PARAM': 'search',
   'ORDERING_PARAM': 'ordering'
}
```

[More Settings](https://www.django-rest-framework.org/api-guide/settings)



