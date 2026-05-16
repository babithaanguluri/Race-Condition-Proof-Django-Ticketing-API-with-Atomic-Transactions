from django.contrib import admin
from django.urls import path
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/events/<int:event_id>/book_vulnerable/', views.book_vulnerable, name='book_vulnerable'),
    path('api/events/<int:event_id>/book_pessimistic/', views.book_pessimistic, name='book_pessimistic'),
    path('api/events/<int:event_id>/book_optimistic/', views.book_optimistic, name='book_optimistic'),
    path('api/events/<int:event_id>/book_pessimistic_fail/', views.book_pessimistic_fail, name='book_pessimistic_fail'),
    path('api/events/<int:event_id>/status/', views.event_status, name='event_status'),
    path('api/events/<int:event_id>/reset/', views.reset_event, name='reset_event'),
]
