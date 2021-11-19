
from django.contrib import admin
from ads.models import Ad,Comment,Fav

# Register your models here.

# don't show picture and content_type in admin ui
class AdAdmin(admin.ModelAdmin):
    exclude = ('picture','content_type')

# Ad database
admin.site.register(Ad, AdAdmin)
admin.site.register(Comment)
admin.site.register(Fav)
