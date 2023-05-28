from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:project_id>/update/', views.project_update, name='project_update'),
    path('project/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('scenerisation/', views.scenerisation_services, name='scenerisation_services'),
    path('object3d/', views.object3d_service, name='object3d_service'),
    path('charte_graphique/', views.show_charte_graphique, name='show_charte_graphique'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('portfolio/<int:portfolio_id>/', views.portfolio_detail, name='portfolio_detail'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('contact/', views.contact, name='contact'),
    path('register/',views.register, name = 'register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
