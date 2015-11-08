from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'text','video']
	class Meta:
		model = Comment

admin.site.register(Comment,CommentAdmin)
# Register your models here.
