from django.urls import path
from . import views

urlpatterns = [
    path('<username>/profile/', views.profile),
    path('<username>/calendar/', views.read_books_calendar),
    path('<int:user_id>/follow/', views.follow),
    path('my_info/', views.get_my_info),
    path('update/', views.update_my_info),
    path('check_password/', views.check_password),
    path('delete/', views.delete_account,),
]
