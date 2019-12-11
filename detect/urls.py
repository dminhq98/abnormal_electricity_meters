
from django.urls import path,include
from .views import Screen1,Screen2,Screen3,Screen4
urlpatterns = [
    path('',Screen1.as_view(),name='Screen1' ),
    path('month',Screen2.as_view(),name='Screen2' ),
    path('<int:num>',Screen3.as_view(),name='Screen3' ),
    path('detal',Screen4.as_view(),name='Screen4' ),
    path('detal/<int:type>/<int:id>',Screen4.as_view(),name='Screen' ),
]
