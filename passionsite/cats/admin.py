
from django.contrib import admin
from cats.models import Cat, Breed



# Register your models here.

# cat database
admin.site.register(Cat)
# Breed database
admin.site.register(Breed)