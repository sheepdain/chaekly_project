from django.urls import path
from . import views
from threads import views as thread_views


urlpatterns = [
    path('', views.book_list),
    path('categories/', views.category_list),
    path('<int:book_id>/threads/', thread_views.thread_list_of_book_or_create),
    path('<int:book_id>/', views.book_detail),
    # path('save_popular_books/', views.save_popular_books, name='save_popular_books'),
    path('recommend/', views.MoodRecommendView.as_view()),
    path('<int:book_id>/author/', views.author_detail), 
    path('<int:book_id>/tts/', views.generate_tts_audio),
    path('<int:book_id>/wishlist/', views.wishlist),
    path('bestsellers/', views.best_sellers),
]
