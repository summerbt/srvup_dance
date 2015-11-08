from django.contrib import admin

from .models import Notification

# class NotificationAdmin(admin.ModelAdmin):
# 	list_display = ('sender_object', 'recipient_object','recipient','__unicode__')
# 	# fields = ('recipient','action',)
# 	# prepopulated_fields = {"slug":("title",)}
# 	# class Meta:
# 	# 	model = Video




admin.site.register(Notification)
# Register your models here.
