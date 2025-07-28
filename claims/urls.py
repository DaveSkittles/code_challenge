from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('claims/', views.claim_list, name='claim_list'),
    path('claims/<int:claim_id>/', views.claim_detail, name='claim_detail'),
    path('claims/<int:claim_id>/flag/', views.toggle_flag, name='toggle_flag'),
    path('claims/<int:claim_id>/annotations/', views.add_annotation, name='add_annotation'),
    path('claims/<int:claim_id>/annotations/list/', views.get_annotations, name='get_annotations'),
    path('annotations/<int:annotation_id>/delete/', views.delete_annotation, name='delete_annotation'),
] 