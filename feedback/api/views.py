from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from feedback.models import Feedback_entries, FeedbackComment
from .serializers import FeedbackSerializer, CommentSerializer
from feedback.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

class CommentViewSet(viewsets.ModelViewSet):
    queryset = FeedbackComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema(responses=FeedbackSerializer)
class FeedbackListAV(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=FeedbackSerializer)
    def get(self, request):
        list = Feedback_entries.objects.all()
        serializer = FeedbackSerializer(list, many=True)
        return Response(serializer.data)

    @extend_schema(responses=FeedbackSerializer)
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(feedback_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(responses=FeedbackSerializer)
    def get(self, request, pk):
        try:
            feedback = Feedback_entries.objects.get(pk=pk)
        except Feedback_entries.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)

    @extend_schema(responses=FeedbackSerializer)
    def put(self, request, pk):
        feedback = Feedback_entries.objects.get(pk=pk)
        serializer = FeedbackSerializer(feedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        feedback = Feedback_entries.objects.get(pk=pk)
        feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        movie = Feedback_entries.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(responses=FeedbackSerializer)
class FeedbackMarkResolved(generics.UpdateAPIView):
    queryset = Feedback_entries.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.resolved = True 
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return FeedbackComment.objects.filter(feedback_id=pk)

@extend_schema(responses=CommentSerializer)
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeedbackComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsReviewUserOrReadOnly]

@extend_schema(responses=CommentSerializer)
class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        feedback_id = self.kwargs.get('pk')

        try:
            feedback_entry = Feedback_entries.objects.get(pk=feedback_id)
        except Feedback_entries.DoesNotExist:
            raise ValidationError("Invalid feedback entry ID")

        serializer.save(user=self.request.user, feedback=feedback_entry)
