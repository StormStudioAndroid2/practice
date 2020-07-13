from django.urls import path

# Create your views here.
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('view/<int:book_id>/', views.book_view, name='book_view'),
    path('pagination/', views.BookPagination.as_view(), name="pagination"),
    path('search/', views.BooksSearchView.as_view(), name="search"),
    path('search1/', views.BooksList.as_view(), name="search")

]


