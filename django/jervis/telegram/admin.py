from django.contrib import admin
from .models import *

class ImageAdmin(admin.ModelAdmin):
    pass

class ChatAdmin(admin.ModelAdmin):
    pass

admin.site.register(Chat, ChatAdmin)
admin.site.register(Image, ImageAdmin)
