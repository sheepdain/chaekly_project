from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BookListSerializer, CustomCategorySerializer, BookSerializer, AuthorSerializer
from .models import Book, CustomCategory, Author
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F, Value
from django.db.models.functions import Replace
from django.db.models import CharField
from rest_framework.views import APIView
from django.conf import settings
from .serializers import BookSerializer
from .utils import fetch_titles_from_ai, fetch_and_save_books
from .utils2 import process_author_info_from_ai


from .utils_tts import generate_description_tts
@api_view(['GET'])
def generate_tts_audio(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
        print("📘 TTS 요청 도서:", book.title, "/", book.id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    path = generate_description_tts(book)
    if path:
        # return Response({"audio_url": settings.MEDIA_URL + str(path)})
        domain = request.build_absolute_uri('/')[:-1]  # ex) http://127.0.0.1:8000
        audio_url = f"{domain}{settings.MEDIA_URL}{str(path)}"
        return Response({"audio_url": audio_url})
    else:
        return Response({"error": "TTS 생성 실패"}, status=500)


class MoodRecommendView(APIView):
    def post(self, request):
        mood = request.data.get('mood', '').strip()
        if not mood:
            return Response({'detail': 'mood를 보내주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        collected_books = []
        seen_titles = set()
        max_attempts = 10 
        attempts = 0

        while len(collected_books) < 3 and attempts < max_attempts:
            titles = fetch_titles_from_ai(mood, n=3)
            titles = [t for t in titles if t not in seen_titles]
            seen_titles.update(titles)
            attempts += 1

            if not titles:
                continue  # 빈 배열이면 다시 시도 (무한루프 방지 위해 attempts 체크)

            books_raw = fetch_and_save_books(titles)
            new_books = [b for b in books_raw if isinstance(b, Book)]
            collected_books.extend(new_books)

            # isbn 기준 중복 제거
            unique = {}
            for b in collected_books:
                if b.isbn13 not in unique:
                    unique[b.isbn13] = b
            collected_books = list(unique.values())

            print(f"현재까지 수집된 책 개수: {len(collected_books)}")
            print(f"이번에 받은 추천: {titles}")

        # 응답은 3권만 (최소 3권이 모였을 때만 응답)
        if len(collected_books) < 3:
            return Response({'detail': '추천 결과가 충분하지 않습니다.'}, status=status.HTTP_204_NO_CONTENT)

        serializer = BookSerializer(collected_books[:3], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = CustomCategory.objects.all()
        serializer = CustomCategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def book_list(request):
    category_name = request.GET.get('category')
    keyword = request.GET.get('keyword', "").strip()
    cleaned_keyword = keyword.replace(" ", "")

    books = Book.objects.all()

    if category_name:
        books = books.filter(custom_category__name=category_name)

    if cleaned_keyword:
        books = books.annotate(
            title_nospace=Replace(F("title"), Value(" "), Value(""), output_field=CharField()),
            author_nospace=Replace(F("author"), Value(" "), Value(""), output_field=CharField()),
            publisher_nospace=Replace(F("publisher"), Value(" "), Value(""), output_field=CharField()),
            description_nospace=Replace(F("description"), Value(" "), Value(""), output_field=CharField()),
        ).filter(
            Q(title_nospace__icontains=cleaned_keyword) |
            Q(author_nospace__icontains=cleaned_keyword) |
            Q(publisher_nospace__icontains=cleaned_keyword) |
            Q(description_nospace__icontains=cleaned_keyword)
        )

    books = books.order_by('-pub_date')

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(books, request)
    serializer = BookListSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)  


@api_view(['GET'])
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    serializer = BookSerializer(book, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def author_detail(request, book_id):
    print(f"📥 작가 요청 들어옴: book_id={book_id}")
    book = Book.objects.get(id=book_id)
    
    full_name = book.author.strip()
    author, _ = Author.objects.get_or_create(name=full_name)

    if not author.info or not author.works:
        prompt = f"책 제목: {book.title}\n출판사: {book.publisher}\n도서 설명: {book.description}\n지은이: {book.author}"
        info, works= process_author_info_from_ai(prompt, full_name, book.title)

        author.info = info
        author.works = works
        print(f'새로 등록된 작가 정보 : {author.info}, {author.works}')
        author.save()
        

    serializer = AuthorSerializer(author, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user

    # 이미 위시리스트에 있으면 제거, 아니면 추가
    if book in user.wishlist.all():
        user.wishlist.remove(book)
        return Response({'wishlisted': False})
    else:
        user.wishlist.add(book)
        return Response({'wishlisted': True})


@api_view(['GET'])
def best_sellers(request):
    # best_rank가 있고 1~50위인 책만 추출, rank 오름차순 정렬
    books = Book.objects.filter(best_rank__isnull=False, best_rank__gte=1, best_rank__lte=100).exclude(best_rank=0).order_by('best_rank')[:50]
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)

