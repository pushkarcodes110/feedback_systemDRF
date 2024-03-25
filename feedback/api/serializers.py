from rest_framework import serializers
from feedback.models import Feedback_entries, FeedbackComment


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_entries
        fields = ['id', 'title', 'description', 'resolved', 'feedback_user', 'submission_date']
        read_only_fields = ['id', 'feedback_user', 'submission_date']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackComment
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['id', 'created_at'] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('user', None)
