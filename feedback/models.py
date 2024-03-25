from django.db import models
from django.contrib.auth.models import User

class Feedback_entries(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    submission_date = models.DateTimeField(auto_now_add=True)
    feedback_user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_date = models.DateTimeField(auto_now=True)
    resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.title) + " | " + str(self.feedback_user)
    
class FeedbackComment(models.Model):
    feedback = models.ForeignKey(Feedback_entries, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.feedback.title) + " | " + str(self.user)