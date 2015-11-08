from django.dispatch import Signal


notify = Signal(providing_args=['recipient_object','action','action_object','target_object', 'affected_users'])





"""sender_content_type = models.ForeignKey(ContentType, related_name = "notify_sending_object")
	sender_object_id = models.PositiveIntegerField()
	sender_object = GenericForeignKey('sender_content_type','sender_object_id')

	action=models.CharField(max_length=140)

	action_content_type = models.ForeignKey(ContentType, related_name = "notify_acting_object", null=True, blank=True)
	action_object_id = models.PositiveIntegerField()
	action_object = GenericForeignKey('action_content_type','action_object_id')

	target_content_type = models.ForeignKey(ContentType, related_name = "notify_targeted_object", null=True, blank=True)
	target_object_id = models.PositiveIntegerField()
	target_object = GenericForeignKey('target_content_type','target_object_id')

	# recipient_content_type = models.ForeignKey(ContentType)
	# recipient_object_id = models.PositiveIntegerField()
	# recipient_object = GenericForeignKey('recipient_content_type','recipient_object_id')

	recipient=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='notifications')
	
	timestamp=models.DateTimeField(auto_now_add=True, auto_now=False)
	"""