from django.contrib import admin

from apps.Nodes.models import Person, Phone, MeetingPoint

# Register your models here.
admin.site.register(Person)
admin.site.register(Phone)
admin.site.register(MeetingPoint)
