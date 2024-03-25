
from django.urls import path
from feedback.api.views import (FeedbackListAV, CommentCreate,FeedbackMarkResolved, FeedbackDetailAV, CommentDetail, CommentList)

urlpatterns = [
    path('list/', FeedbackListAV.as_view()),
    path('<int:pk>/', FeedbackDetailAV.as_view(), name='feedback-detail'),
    path('<int:pk>/comments/', CommentList.as_view(), name='comment-list'),
    path('comment/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('<int:pk>/comment-create/', CommentCreate.as_view(), name='comment-create'),
    path('<int:pk>/status/', FeedbackMarkResolved.as_view(), name='feedback-status'),
    


]
