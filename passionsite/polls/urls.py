from django.urls import path
from . import views


app_name = 'polls'

urlpatterns = [
    # basic views vs generic views, and I commented out all basic views.
    # basic polls view.
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # owner view
    path('owner', views.owner, name='owner'),
    # detail view function
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # results view function
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # vote view function
    path('<int:question_id>/vote/', views.vote, name= 'vote'),


]