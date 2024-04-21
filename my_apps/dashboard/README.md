# SQL to ORM

queryset to dict,
```
queryset[0].__dict__

from django.forms.models import model_to_dict
model_to_dict(queryset[0])
```

filter types,
```
iexact, contains, icontains, startswith, istartswith, endswith, iendswith
in, notin, isnull,
lt, lte, gt, gte,
```
here `i` make the column case-insensitive.
use `~` to make the filter opposite.


---
## and, or, order by, column filter

SQL:
```
SELECT * FROM dashboard_data
WHERE (LOWER(gender) = 'm' AND age > id) OR id <= 10
ORDER by age DESC, id ASC;
```

ORM:
```
from django.db.models import Q, F

queryset = Data.objects.filter(
    Q(gender__iexact='m', age__gt=F('id')) | Q(id__lte=10)
).order_by('-age', 'id')
```
Here `queryset` consist of list of models.


---
## select, between, in, limit, offset
SQL:
```
SELECT name, email, age FROM dashboard_data
WHERE age BETWEEN 18 AND 24 AND gender IN ('F', 'M')
LIMIT 100 OFFSET 50;
```

ORM:
```
queryset = Data.objects.filter(
    age__range=(18, 24), gender__in=['F', 'M']
)[50:150].values('name', 'email', 'age')
```
Here `queryset` consist of list of objects/dicts as `.values` is used.


---
## count, group by
SQL:
```
SELECT COUNT(*), gender FROM dashboard_data
WHERE age > 18
GROUP BY gender;
```

ORM:
```
from django.db.models import Count

queryset = Data.objects.filter(
    age__gt=18
).values('gender').annotate(count=Count('*'))
```


---
## alias, left join / one-to-one or many-to-one(foreign) relation
SQL:
```
SELECT fd.hair_color, d.email AS email, h.hair_length_cm AS hair_length
FROM dashboard_fulldata fd
LEFT JOIN dashboard_data d ON d.id = fd.data_id
LEFT JOIN dashboard_hair h ON h.id = fd.hair_id
WHERE d.age > 18 AND fd.duration > '200 days' AND h.is_hair_styled IS True;
```

ORM:
```
from django.db.models import F

queryset = FullData.objects.select_related('data', 'hair').filter(
    data__age__gt=18, duration__gt='200 days', hair__is_hair_styled=True
).annotate(
    email=F('data__email'), hair_length=F('hair__hair_length_cm')
).values('hair_color', 'email', 'hair_length')
```


---
## many-to-many, column as list of dict
SQL:
```
SELECT fd.id, fd.hair_color,
    JSON_AGG(JSON_BUILD_OBJECT(
        'id', c.id,
        'color', c.favorite_color
    )) as colors_list
FROM dashboard_fulldata fd
LEFT JOIN dashboard_fulldata_color fdc ON fd.id = fdc.fulldata_id
LEFT JOIN dashboard_color c ON fdc.color_id = c.id
GROUP BY fd.id, fd.hair_color;
```

ORM:
```
from django.db.models import OuterRef, F
from django.db.models.functions import JSONObject
from django.contrib.postgres.expressions import ArraySubquery

subquery = Color.objects.filter(fulldata=OuterRef("pk")).annotate(
    data=JSONObject(id=F("id"), favorite_color=F("favorite_color"))
).values_list("data")

queryset = FullData.objects.annotate(
    colors_list=ArraySubquery(subquery)
).values('id', 'hair_color', 'colors_list')
```


## one-to-many, many-to-one(foreign) relation

ORM:
```
queryset = Hair.objects.prefetch_related('fulldata_set').all()
queryset = FullData.objects.select_related('hair').all()
```
