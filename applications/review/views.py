from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.review.permissions import IsReviewAuthor
from applications.review.models import Review, Like
from applications.review.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'like':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsReviewAuthor, ]
        return [permission() for permission in permissions]

    @action(detail=True, methods=['POST'])
    def like(self, request, *arg, **kwargs):
        review = self.get_object()
        like_obj, _ = Like.objects.get_or_create(review=review, user=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})


    def ger_serializer_context(self):
        return {'request': self.request}
