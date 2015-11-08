from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'srvup_dance.views.home', name='home'),
    url(r'^staff/$', 'srvup_dance.views.staff_home', name='staff'),
    
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', TemplateView.as_view(template_name="base.html"), name='home'),
    url(r'^courses/$', 'videos.views.category_list', name='courses'),
    url(r'^courses/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail', name='course_detail'),
    url(r'^courses/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'videos.views.video_detail', name='video_detail'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += patterns('',) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('accounts.views',
	url(r'^login/$', 'auth_login', name='login'),
    url(r'^logout/$', 'auth_logout', name='logout'),
    )

#Comment Thread
urlpatterns += patterns('comments.views',
    url(r'^comment/(?P<id>\d+)$', 'comment_thread', name='comment_thread'),
    url(r'^comment/create/$', 'comment_create_view', name='comment_create'),
    )

#Notifications
urlpatterns += patterns('notifications.views',
    url(r'^notifications/$', 'all', name='notifications_all'),
    url(r'^notifications/unread$', 'unread', name='notifications_uread'),
    url(r'^notifications/read/(?P<id>\d+)$', 'read', name='notifications_read'),
    url(r'^notifications/ajax$', 'get_notifications_ajax', name='get_notifications_ajax')
    )