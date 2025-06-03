from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserProfileSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from threads.models import Thread
from rest_framework import status

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    person = get_object_or_404(User, username=username)
    serializer = UserProfileSerializer(person, context={'request': request})
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_my_info(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        # 여기서 전체 프로필 정보 반환
        profile_serializer = UserProfileSerializer(user, context={'request': request})
        return Response(profile_serializer.data)
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    person = get_object_or_404(User, id=user_id)

    if person == request.user:
        return Response({'detail': '자기 자신은 팔로우할 수 없습니다.'}, status=400)

    if person.followers.filter(id=request.user.id).exists():
        person.followers.remove(request.user)
        is_follow = False
    else:
        person.followers.add(request.user)
        is_follow = True

    return Response({
        'is_follow': is_follow,
        'follower_count': person.followers.count(),
        'following_count': person.following.count()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_info(request):
    serializer = UserProfileSerializer(request.user, context={'request': request})
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_books_calendar(request, username):
    user = User.objects.get(username=username)
    threads = Thread.objects.filter(user=user, read_date__isnull=False).select_related('book')
    books_by_date = {}
    book_ids_by_date = {}

    for t in threads:
        date = t.read_date.strftime('%Y-%m-%d')
        if t.book and t.book.title:
            books_by_date.setdefault(date, []).append(str(t.book.title))
            book_ids_by_date.setdefault(date, []).append(t.book.id)

    result = [
        {
            'date': date,
            'titles': books_by_date[date],
            'book_ids': book_ids_by_date.get(date, [])
        }
        for date in books_by_date
    ]
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_password(request):
    user = request.user
    password = request.data.get('password')
    if password and user.check_password(password):
        return Response({"detail": "ok"})
    return Response({"detail": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response({'detail': '회원탈퇴가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)