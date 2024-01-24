from django.urls import path
from .views import home, quizes, quizHistory, activate, updateInfo, quiz_page, UserLoginView, UserLogoutView, RegistrationView, ProfileView, BlogView

urlpatterns = [
    path('', home, name='home'),
    path('quizes/', quizes, name='quizes'),
    path('quiz/history', quizHistory, name='quiz_history'),
    path('category/<slug:category_slug>/', quizes, name='category_slug_quizes'),
    path('category/<slug:category_slug>/', home, name='category_slug_home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('register/active/<uid64>/<token>/', activate, name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', updateInfo, name='update_info'),
    path('quiz/<int:quiz_id>/', quiz_page, name='quiz_page'),
    path('blog/', BlogView.as_view(), name='blog'),
]
