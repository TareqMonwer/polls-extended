from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/results/', views.ResultslView.as_view(), name='results'),
    # path('<int:pk>/vote/', views.VoteView.as_view(), name='vote'),
    path('<int:pk>/vote/', views.SwitchboardView.as_view(), name='vote_result'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
]