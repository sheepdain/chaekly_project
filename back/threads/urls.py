from django.urls import path
from . import views

urlpatterns = [
    path('', views.thread_list),
    path('<int:thread_id>/', views.thread_detail),
    path('<int:thread_id>/comments/', views.comment_create),
    path('comments/<int:comment_id>/', views.comment_delete),
    path('<int:thread_id>/likes/', views.likes),
]
