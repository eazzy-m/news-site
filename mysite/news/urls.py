from django.urls import path
from .views import HomeNews, NewsByCategory, ViewNews, CreateNews, contact, user_login, register, user_logout
# from django.views.decorators.cache import cache_page
# from .views import index, get_category, view_news, add_news


urlpatterns = [
    # path('', index, name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    # path('news/add_news/', add_news, name='add_news'),
    # path('', cache_page(10)(HomeNews.as_view()), name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(extra_context={'title': 'Категории'}), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
    path('contact/', contact, name='contact')
]
