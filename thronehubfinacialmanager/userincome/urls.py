from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

# URL patterns for the income app
urlpatterns = [
    # Maps the root URL to the index view
    path('', views.index, name="income"),
    
    # Maps the 'add-income' URL to the add_income view
    path('add-income', views.add_income, name="add-income"),
    
    # Maps the 'edit-income/<int:id>' URL to the income_edit view, expecting an integer ID
    path('edit-income/<int:id>', views.income_edit, name="income-edit"),
    
    # Maps the 'income-delete/<int:id>' URL to the delete_income view, expecting an integer ID
    path('income-delete/<int:id>', views.delete_income, name="income-delete"),
    
    # Maps the 'search-income' URL to the search_income view, exempting it from CSRF protection
    path('search-income', csrf_exempt(views.search_income), name="search_income")
]
