from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.

from .models import Video, Category, TaggedItem

class TaggedItemInline (GenericTabularInline):
	model = TaggedItem

class VideoAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'slug')
	fields = ('title','order','share_message','embed_code', 'active',
	 	'featured', 'free_preview',
	 	'category')
	inlines = [TaggedItemInline,]
	# prepopulated_fields = {"slug":("title",)}
	# class Meta:
	# 	model = Video

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'slug')
	fields = ('title','image',
		'slug', 'active',
	 	'featured',)
	prepopulated_fields = {"slug":("title",)}
	inlines = [TaggedItemInline]

	class Meta:
		model = Category

admin.site.register(Video, VideoAdmin)

admin.site.register(Category, CategoryAdmin)

#admin.site.register(TaggedItem)
