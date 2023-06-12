from django.contrib import admin

from .models import Topic, Entry

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Topic, TopicAdmin)
admin.site.register(Entry, EntryAdmin)