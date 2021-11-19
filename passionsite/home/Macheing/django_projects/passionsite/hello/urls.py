from django.urls import path
from . import views



app_name = 'hello'

# urls patterns
urlpatterns = [
    # set_cookies view
    path('', views.set_cookies),
     # set_sessions view
    path('',views.set_sessions),


]
