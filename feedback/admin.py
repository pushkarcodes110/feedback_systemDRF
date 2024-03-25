from django.contrib import admin
from feedback.models import Feedback_entries, FeedbackComment

admin.site.register(Feedback_entries)
admin.site.register(FeedbackComment)
