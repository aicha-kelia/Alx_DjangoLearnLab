from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserSerializer
from .models import CustomUser

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserProfileSerializer(user).data,
                'token': token.key
            })
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class FollowUserView(generics.GenericAPIView):
    """Follow a user"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.all().get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': 'You are already following this user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.following.add(user_to_follow)
        
        # Create notification
        from notifications.models import Notification
        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb='started following you'
        )
        
        return Response(
            {'message': f'You are now following {user_to_follow.username}'},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    """Unfollow a user"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.all().get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': 'You are not following this user'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.following.remove(user_to_unfollow)
        return Response(
            {'message': f'You have unfollowed {user_to_unfollow.username}'},
            status=status.HTTP_200_OK
        )


class UserListView(generics.ListAPIView):
    """List all users"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]