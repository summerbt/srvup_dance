from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

from accounts.models import MyUser
from notifications.signals import notify
from videos.models import Video

from .models import Comment
from .forms import CommentForm

# Create your views here.
@login_required
def comment_thread(request, id):
	comment = Comment.objects.get(id=id)
	form = CommentForm()
	context = {
	'form':form,
	'comment':comment,
	}
	return render(request, "comments/comment_thread.html", context)

def comment_create_view(request):
	if request.method == 'POST'and request.user.is_authenticated():
		# print '>>location: comments/Views.py/comment_create_view'
		# print '>> What is request'
		# print request
		# print ">>what is request.POST:"
		# print request.POST
		# print ">> request.POST.get('parent_id')"
		# print request.POST.get('parent_id')

		parent_id = request.POST.get('parent_id')
		# print ">>parent_id:"
		# print parent_id

		video_id = request.POST.get('video_id')
		# print ">>video_id"
		# print video_id

		origin_path = request.POST.get('origin_path')
		# print ">>origin_path"
		# print origin_path

		#try:
		# print '>>location: comments/Views.py/comment_create_view'
		# print '>>Video.object.get(id=video_id) is getting the video object with id = video_id'
		# print video_id
		# print Video.objects.get(id=video_id)

		video = Video.objects.get(id=video_id)
		#except:
			#video = None


		# print '>>location: comments/Views.py/comment_create_view'
		# print '>>printing video obj'
		# print video

		parent_comment = None
		if parent_id is not None:
			#try:
			parent_comment = Comment.objects.get(id=parent_id)
			# print ">>parent_comment @ given parent_id"
			# print parent_comment
			#except:
				#parent_comment = None
			if parent_comment is not None and parent_comment.video is not None:
				# print ">>Print video before video = parent_comment.video assignment:"
				# print video

				video = parent_comment.video
				# print ">>print video after video = parent_comment.video assignment:"
				# print video


		form = CommentForm(request.POST)
		# print">>print request.POST"
		# print request.POST
		# print ">>print CommentForm(request.POST)"
		# print CommentForm(request.POST)
		# print "print form after form = CommentForm(request.POST) assignment"
		# print form

		if form.is_valid():
			# print ">> print form.cleaned_data['comment']"
			# print form.cleaned_data['comment']
			comment_text = form.cleaned_data['comment']

			if parent_comment is not None:
				##################
				# print ">> print parent_comment"
				# print parent_comment
				# print """>> print Comment.objects.create_comment(
				# 	user=request.user, 
				# 	path=parent_comment.get_origin, 
				# 	text=comment_text,
				# 	video = video,
				# 	parent=parent_comment
				# 	)"""
				# print Comment.objects.create_comment(
				# 	user=request.user, 
				# 	path=parent_comment.get_origin, 
				# 	text=comment_text,
				# 	video = video,
				# 	parent=parent_comment
				# 	)
				# print"what is the difference between parent_comment.get_origin and origin_path"
				# print ">> print parent_comment.get_origin"
				# print parent_comment.get_origin
				# print ">> print origin_path"
				# print origin_path
				####################
				new_comment = Comment.objects.create_comment(
					user=request.user,
					text=comment_text,
					path=parent_comment.get_origin,
					video=video,
					parent=parent_comment)

				####################

				# print ">> print parent_comment.get_absolute_url()"
				# print parent_comment.get_absolute_url()
				# print "HttpResponseRedirect(parent_comment.get_absolute_url())"
				# print HttpResponseRedirect(parent_comment.get_absolute_url())

				####################
				affected_users = parent_comment.get_affected_users()
				notify.send(request.user,
					recipient_object=parent_comment.user,
					affected_users=affected_users,
					action='replied to',
					action_object=new_comment,
					target_object=parent_comment)
				messages.success(request, "Thank you for your response.", extra_tags='safe')
				return HttpResponseRedirect(parent_comment.get_absolute_url()) #comment origin
				####################

			else:
				# print ">> print origin_path"
				# print origin_path
				####################
				new_comment = Comment.objects.create_comment(
					user=request.user,
					text=comment_text,
					path=origin_path,
					video=video,)
				####################
				# print ">> print new_comment object"
				# print new_comment
				# print ">>print new_comment.get_absolute_url()"
				# print new_comment.get_absolute_url()
				# print ">> print HttpResponseRedirect(new_comment.get_absolute_url())"
				# print HttpResponseRedirect(new_comment.get_absolute_url())
				####################
				affected_users = MyUser.objects.get_admin()
				print "admin affected users"
				print affected_users
				notify.send(request.user,
					recipient_object=new_comment.user,
					affected_users=affected_users,
					action='commented on',
					action_object=new_comment,
					target_object=new_comment.video)
				messages.info(request, "Thank you for your comment.", extra_tags='safe')
				return HttpResponseRedirect(new_comment.get_absolute_url())
				####################
		else:
			# print ">> print origin_path"
			# print origin_path
			##################
			messages.error(request, "There was an error with your comment.")
			##################
			# print ">> print HttpResponseRedirect(origin_path)"
			# print HttpResponseRedirect(origin_path)
			##################
			return HttpResponseRedirect(origin_path)
	else:
		raise Http404



			# else:
			# 	new_comment = Comment.objects.create_comment(
			# 		user=request.user,
			# 		text=comment_text,
			# 		path=parent_comment.get_origin,
			# 		video=obj,
			# 		parent=parent_comment)

