from django.urls import path
from . import views

app_name = 'appointments'
urlpatterns = [
    path('', views.Home, name = 'home'),
    path('booking/', views.booking, name = 'booking'),
    path('booking/success/', views.booking_success , name = 'booking_success'),
    path('doctors/', views.UserDoctoreView.as_view(), name = "doctors")   , 
    path('medicines/', views.medicines, name = "medicines") ,   
    path('login/', views.UserLoginView.as_view(), name = "login")   , 
    path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
    path('register/', views.UserRegisterView.as_view(), name = "register")   , 
    path('doctors_detail/<slug:slug>', views.doctors_detail, name = 'doctors_detail'),
    path('reset', views.UserPasswordResetView.as_view(), name = 'reset'),
    path('reset/done', views.UserPasswordResetDoneView.as_view(), name = 'password_reset'),
    path('confrim/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('confrim/complete/', views.UserPasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('follow/<int:user_id>', views.UserFollowView.as_view(), name = "follow"),
    path('unfollow/<int:user_id>', views.UserUnfollowView.as_view(), name = "unfollow"),
    path('post/<int:post_id>/<int:post_slug>/', views.PostDetailView.as_view(), name = "post_detail"),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name = 'post_delete'),
    path('post/update/<int:post_id>/', views.PostUpdateView.as_view(), name = 'post_update'),
    path('post/create/', views.PostCreateView.as_view(), name = 'post_create'),
]


