from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from .signals import notify
# Create your models here.

class NotificationQuerySet(models.query.QuerySet):
	def get_user_notes(self, recipient):
		return self.filter(recipient=recipient)

	def read(self):
		return self.filter(read=True)

	def unread(self):
		return self.filter(read=False)

	def mark_all_read(self, recipient):
		qs = self.unread().get_user_notes(recipient)
		qs.update(read=True)

	def mark_all_unread(self, recipient):
		qs = self.read().get_user_notes(recipient)
		qs.update(read=False)

	def mark_targetless(self, recipient):
		qs = self.get_user_notes(recipient).unread()
		qs_no_target = qs.filter(target_object_id=None)
		if qs_no_target:
			qs_no_target.update(read=True)

	def recent(self):
		return self.unread()[:5]





class NotificationManager(models.Manager):
	def get_queryset(self):
		return NotificationQuerySet(self.model, using=self._db)

	def get_user_unread(self, user):
		return self.get_queryset().get_user_notes(user).unread()

	def get_user_read(self, user):
		return self.get_queryset().get_user_notes(user).read()

	def get_all_user_notes(self, user):
		self.get_queryset().mark_targetless(user)
		return self.get_queryset().get_user_notes(user)

# class VideoQuerySet(models.query.QuerySet):
# 	def active(self):
# 		return self.filter(active=True)

# 	def featured(self):
# 		return self.filter(featured=True)

# class VideoManager(models.Manager):
# 	def get_queryset(self):
# 		return VideoQuerySet(self.model, using=self._db)

# 	def get_featured(self):
# 		return self.get_queryset().active().featured()
# 		#return super(VideoManager, self).filter(featured=True)

# 	def all(self):
# 		return self.get_queryset().active()


class Notification(models.Model):
	# tag = models.SlugField(choices=TAG_CHOICES)
	sender_content_type = models.ForeignKey(ContentType, related_name = "notify_sending_object",)
	sender_object_id = models.PositiveIntegerField()
	sender_object = GenericForeignKey('sender_content_type','sender_object_id')
	
	action=models.CharField(max_length=140)
	

	action_content_type = models.ForeignKey(ContentType, related_name = "notify_acting_object", null=True, blank=True)
	action_object_id = models.PositiveIntegerField(null=True, blank=True)
	action_object = GenericForeignKey('action_content_type','action_object_id')
	

	target_content_type = models.ForeignKey(ContentType, related_name = "notify_targeted_object", null=True, blank=True)
	target_object_id = models.PositiveIntegerField(null=True, blank=True)
	target_object = GenericForeignKey('target_content_type','target_object_id')
	
	# recipient_content_type = models.ForeignKey(ContentType)
	# recipient_object_id = models.PositiveIntegerField()
	# recipient_object = GenericForeignKey('recipient_content_type','recipient_object_id')

	recipient=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='notifications')
	
	timestamp=models.DateTimeField(auto_now_add=True, auto_now=False)
	
	read = models.BooleanField(default=False)


	objects = NotificationManager()
	
	@property
	def get_link(self):
		try:
			target_object_url = self.target_object.get_absolute_url()
		except:
			target_object_url = reverse('notifications_all')

		context = {
		"sender_object": self.sender_object,
		"action": self.action,
		"action_object": self.action_object,
		"target_object": self.target_object,
		"verify_read":reverse("notifications_read", kwargs={"id":self.id}),
		"target_object_url":target_object_url,
		}

		if self.target_object:
			if self.action_object:
				return "<a href='%(verify_read)s?next=%(target_object_url)s'> %(sender_object)s %(action)s %(target_object)s</a>" % context
			return "<a href='%(verify_read)s?next=%(target_object_url)s'> %(sender_object)s %(action)s %(target_object)s</a>" % context
		return "<a href='%(verify_read)s?next=%(target_object_url)s'> %(sender_object)s %(action)s</a>" % context

	def __unicode__(self):
		try:
			target_object_url = self.target_object.get_absolute_url()
		except:
			target_object_url = reverse('notifications_all')

		context = {
		"sender_object": self.sender_object,
		"action": self.action,
		"action_object": self.action_object,
		"target_object": self.target_object,
		"verify_read":reverse("notifications_read", kwargs={"id":self.id}),
		"target_object_url":target_object_url,
		}

		if self.target_object:
			if self.action_object and target_object_url:
				return "%(sender_object)s %(action)s <a href='%(verify_read)s?next=%(target_object_url)s'>%(target_object)s</a>" % context
			if self.action_object and not target_object_url:
				return "%(sender_object)s %(action)s %(target_object)s" % context
			return "%(sender_object)s %(action)s %(target_object_url)s %(target_object)s" % context
		return "%(sender_object)s %(action)s" % context



def new_notification(sender, **kwargs):
	#new_notification_create = Notification.objects.create(recipient=recipient, action=action)
	#'recipient_object','action','action_object','target_object'
	# print sender
	# print kwargs
	kwargs.pop('signal', None)
	recipient_object = kwargs.pop('recipient_object', None)
	action = kwargs.pop('action', None)
	target_object = kwargs.pop('target_object', None)
	action_object = kwargs.pop('action_object', None)
	affected_users = kwargs.pop('affected_users', None)
	# print "affected users are"
	# print affected_users
	# print "sender"
	# print sender
	if affected_users is not None:
		for user in affected_users:
			if user == sender:
				pass
			else:
				new_note = Notification(
					recipient=user,
					action = action,
					sender_content_type = ContentType.objects.get_for_model(sender),
					sender_object_id = sender.id,
					)
				print "user"
				print user
				if target_object is not None:
					new_note.target_content_type = ContentType.objects.get_for_model(target_object)
					new_note.target_object_id = target_object.id
				if action_object is not None:
					new_note.action_content_type = ContentType.objects.get_for_model(action_object)
					new_note.action_object_id = action_object.id
				new_note.save()
	else:
		new_note = Notification(
			recipient=recipient_object,
			action = action,
			sender_content_type = ContentType.objects.get_for_model(sender),
			sender_object_id = sender.id,
			)
		if target_object is not None:
			new_note.target_content_type = ContentType.objects.get_for_model(target_object)
			new_note.target_object_id = target_object.id
		if action_object is not None:
			new_note.action_content_type = ContentType.objects.get_for_model(action_object)
			new_note.action_object_id = action_object.id
		new_note.save()

notify.connect(new_notification)

# summer AUTH_USER_MODEL
# commented ("verb")
# on your comment Comment(id=12) targeted instance
# with a comment Comment(id=32) instance action_object #doing the commenting
# you should know AUTH_USER_MODEL

# <instance of a user>
# <takes action> #upon
# <instance of a model> #that targets
# <another instance of a model> #alert
# <another instance of a user>