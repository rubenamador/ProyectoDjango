from django.contrib import admin

from apps.Links.models import Call, Meeting

# Register your models here.
admin.site.register(Call)
admin.site.register(Meeting)
