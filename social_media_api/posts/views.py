from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

User = get_user_model()


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit or delete their own posts/comments.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    
    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author (if not commenting on own post)
        if comment.post.author != self.request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=comment.post
            )


class FeedView(generics.ListAPIView):
    """
    Feed view that shows posts from users that the current user follows.
    This view returns posts ordered by creation date, showing the most recent posts at the top.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination
    
    def get_queryset(self):
        # Get the list of users the current user is following
        following_users = self.request.user.following.all()
        # Return posts from those users, ordered by creation date (most recent first)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """Like a post"""
    post = generics.get_object_or_404(Post, pk=pk)
    
    # Use get_or_create to handle like creation
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        return Response(
            {'error': 'You have already liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create notification for post author (if not liking own post)
    if post.author != request.user:
        from notifications.models import Notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )
    
    return Response(
        {'message': 'Post liked successfully'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """Unlike a post"""
    post = generics.get_object_or_404(Post, pk=pk)
    
    # Check if user has liked the post
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response(
            {'message': 'Post unliked successfully'},
            status=status.HTTP_200_OK
        )
    except Like.DoesNotExist:
        return Response(
            {'error': 'You have not liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )