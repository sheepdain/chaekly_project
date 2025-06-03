from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ThreadListSerializer, ThreadSerializer, CommentSerializer, ThreadListOfBookSerializer
from .models import Thread, Comment
from books.models import Book
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from django.db.models import Value, F, CharField, Count
from django.db.models.functions import Replace
from django.db.models import Q
from .threads_cover_generation_ai import generate_image, save_image_to_thread_cover


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def thread_list_of_book_or_create(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # 책에 작성된 쓰레드 조회
    if request.method == 'GET':
        threads = Thread.objects.filter(book=book).annotate(
            like_count=Count('like_users', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(threads, request)
        serializers = ThreadListOfBookSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializers.data)
    
    # 책에 쓰레드 작성
    if request.method == 'POST':
        serializer = ThreadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            # Thread 인스턴스 저장
            thread = serializer.save(user=request.user, book=book)

            # 1. 커버 이미지 생성
            image_info = generate_image(
                thread_title=thread.title,
                thread_content=thread.content,
                book_title=thread.book.title,
                book_description=thread.book.description,
            )

            # 2. 커버 이미지 저장
            save_image_to_thread_cover(image_info['url'], thread)

            annotated_thread = Thread.objects.annotate(
                like_count=Count('like_users', distinct=True),
                comment_count=Count('comments', distinct=True)
            ).get(id=thread.id)

            # 3. 새로 저장된 thread를 다시 직렬화
            refreshed = ThreadSerializer(annotated_thread, context={'request': request})
            return Response(refreshed.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thread_list(request):
    category_name = request.GET.get('category')
    keyword = request.GET.get('keyword', "").strip()
    cleaned_keyword = keyword.replace(" ", "")

    threads = Thread.objects.annotate(
        like_count=Count('like_users', distinct=True),
        comment_count=Count('comments', distinct=True)
    ).filter(is_public=True)

    if category_name:
        threads = threads.filter(book__custom_category__name=category_name)

    if cleaned_keyword:
        threads = threads.annotate(
            title_nospace=Replace(F("title"), Value(" "), Value(""), output_field=CharField()),
            content_nospace=Replace(F("content"), Value(" "), Value(""), output_field=CharField()),
            book_title_nospace=Replace(F("book__title"), Value(" "), Value(""), output_field=CharField()),
        ).filter(
            Q(title_nospace__icontains=cleaned_keyword) |
            Q(content_nospace__icontains=cleaned_keyword) |
            Q(book_title_nospace__icontains=cleaned_keyword)
        )

    threads = threads.order_by('-created_at')

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(threads, request)
    serializer = ThreadListSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])    
def thread_detail(request, thread_id):
    thread = get_object_or_404(
    Thread.objects.annotate(
            like_count=Count('like_users', distinct=True),
            comment_count=Count('comments', distinct=True)
        ),
        id=thread_id
    )

    if request.method == 'GET':
        if not thread.is_public and thread.user != request.user:
            return Response({'detail': '비공개 글에 접근할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ThreadSerializer(thread, context={'request': request})
        return Response(serializer.data)

    # 쓰레드 수정 & 삭제는 작성자만 가능
    if thread.user != request.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


    # 쓰레드 수정
    if request.method == 'PUT':
        serializer = ThreadSerializer(thread, data=request.data, partial = True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=thread.user, book=thread.book)
            return Response(serializer.data)

    # 쓰레드 삭제
    if request.method == 'DELETE':
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
       
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    # 쓰레드에 댓글 생성
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, thread=thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user != request.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    # 댓글 삭제
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#쓰레드 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likes(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.user in thread.like_users.all():
        thread.like_users.remove(request.user)
        is_liked = False
    else:
        thread.like_users.add(request.user)
        is_liked = True

    # thread 객체를 다시 새로 조회해서 최신 카운트 반영
    thread = Thread.objects.get(pk=thread_id)
    like_count = thread.like_users.count()

    return Response({
        'is_liked': is_liked,
        'like_count': like_count,
    }, status=status.HTTP_200_OK)
