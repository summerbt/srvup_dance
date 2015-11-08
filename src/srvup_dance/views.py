from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from accounts.forms import RegistrationForm
from accounts.models import MyUser
from videos.models import Video


#@login_required
#@login_required(login_url = '/enroll/login/')


def home (request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password1']
		#MyUser.objects.create_user(username=username, email=email, password=password)
		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		new_user.set_password(password)
		new_user.save()

		#Add message for success
		return redirect('login')


		print username, email, password



	# name = "Summer"
	# videos = Video.objects.all()
	# embeds = []
	# for vid in videos:
	# 	code = mark_safe(vid.embed_code)
	# 	embeds.append("%s" % code)
	context = {
	"form":form,
	"action_value":"",
	"submit_btn_value":"Register"
	# "the_name":name,
	# "number" :videos.count(),
	# "videos" :videos,
	# "embeds" :embeds,
	# "a_code" :mark_safe(videos[0].embed_code)
	}
	return render(request, "form.html", context)
		


	# def home (request):
# 	if request.user.is_authenticated():
# 		print request.user.is_authenticated()
# 		name = "Summer"
# 		videos = Video.objects.all()
# 		embeds = []
# 		for vid in videos:
# 			code = mark_safe(vid.embed_code)
# 			embeds.append("%s" % code)
# 		context = {
# 		"the_name":name,
# 		"number" :videos.count(),
# 		"videos" :videos,
# 		"embeds" :embeds,
# 		"a_code" :mark_safe(videos[0].embed_code)
# 		}
# 		return render(request, "home.html", context)
		
# 	else:
# 		return HttpResponseRedirect('/login/')

	
@login_required(login_url = '/staff/login/')
#@login_required(login_url = '/enroll/login/')
def staff_home (request):
	context = {
		
		}
	return render(request, "home.html", context)

