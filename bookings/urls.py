from django.urls import path

from . import views


app_name = "bookings"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('<int:year>/<int:month>/<int:day>', views.IndexView.as_view(), name="index"),
    path('add/', views.AddReservation.as_view(), name="add"),
    path('confirm/<str:code>/', views.ConfirmReservation.as_view(), name="confirm"),
]
