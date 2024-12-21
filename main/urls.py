from django.urls import path
from .views import *

urlpatterns = [
      path('<int:id>/<str:username>/',HomePageListView.as_view(),name='home'),
      path('user/<str:username>/',UserPage,name = 'userpage'),
      path('verify/<str:username>/',Verify_email,name = 'verify'),
      path('sendcode/<str:username>/',SendCode,name='sendcode'),
      path('controler/<str:username>/',ControlPage,name = 'control'),
      path('register/',Register,name='register'),
      path('login/',LoginPage,name='login'),
      path('save-qr-data/', save_qr_data, name='save_qr_data'),
      path('for_user_login/<str:my_email>/',send_qr_email,name='send_qr'),
      path('qr_scanner/',WriteEmail,name='writeemail'),
      path('logout/',Logout,name = 'logout'),
      path('',HomePage,name = 'homepage'),      
              ]