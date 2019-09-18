from django.urls import path

from . import views

app_name = 'polls' # namespace 추가

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/',views.DetailView.as_view(), name='detail'), # DetailView 제너릭 뷰 사용 시 pk로 사용해야
    path('<int:pk>/results/',views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/',views.vote, name='vote'),
]
