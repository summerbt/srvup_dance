import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, Http404, HttpResponseRedirect
from .models import Notification

@login_required
def all (request):
	print request
	notifications = Notification.objects.get_all_user_notes(request.user)
	context = {'notifications':notifications,}

	return render(request, 'notifications/all.html', context)

@login_required
def unread (request):
	notifications = Notification.objects.get_user_unread(request.user)
	context = {'notifications':notifications,}

	return render(request, 'notifications/unread.html', context)

@login_required
def read (request, id):
	try:	
		next = request.GET.get('next', None)
		notification = Notification.objects.get(id=id)
		if notification.recipient == request.user:
			notification.read = True
			notification.save()
			if next is not None:
				return HttpResponseRedirect(next)
			else:
				return HttpResponseRedirect(reverse("notifications_all"))
			raise Http404
	except:
		raise HttpResponseRedirect(reverse("notifications_all"))

@login_required
def get_notifications_ajax(request):
	if request.is_ajax() and request.method == "POST":	
		notifications = Notification.objects.get_all_user_notes(request.user).recent()
		count = notifications.count()
		notes = []
		for note in notifications:
			notes.append(str(note.get_link))
		data = {
		"notifications":notes,
		"count":count
		}
		print data
		json_data = json.dumps(data)
		print json_data
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404