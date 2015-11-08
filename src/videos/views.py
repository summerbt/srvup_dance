from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, Http404, HttpResponseRedirect
from .models import Video, Category, TaggedItem
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def video_detail(request, cat_slug, vid_slug):
	obj = Video.objects.get(slug=vid_slug)
	comments = obj.comment_set.all()
	# content_type = ContentType.objects.get_for_model(obj)
	# tags = TaggedItem.objects.filter(content_type=content_type, object_id=obj.id)
	# print obj.tags.all()
	# for genrel in obj.tags.all():
	# 	print genrel.tag
	# print content_type
	#try:
	cat = Category.objects.get(slug=cat_slug)
	#except:
	#raise Http404

	#try:	
	comment_form = CommentForm(request.POST or None)
	return render(request, "videos/video_detail.html", {"obj":obj,"comments":comments,"comment_form":comment_form,})
	#except:
	#raise Http404

def category_list(request):
	queryset = Category.objects.all()

	context = {
	"queryset":queryset,
	}
	return render(request, "videos/category_list.html", context)

@login_required
def category_detail(request, cat_slug):
	try:
		obj = Category.objects.get(slug=cat_slug)
		queryset = obj.video_set.all()
		return render(request, "videos/video_list.html", {"obj":obj, "queryset": queryset})
	except:
		raise Http404
# def video_edit(request):
# 	context = {}
# 	return render(request, "videos/video_single.html", {})

# def video_create(request):
# 	context = {}
# 	return render(request, "videos/video_single.html", {})
