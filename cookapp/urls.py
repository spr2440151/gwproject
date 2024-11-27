from django.urls import path
from . import views

app_name = 'cook'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('post_recipe/', views.CreateRecipeView.as_view(), name = 'post_recipe'),
    path('post_ingredient/', views.CreateIngredientView.as_view(), name='post_ingredient'),
    path('post_step/', views.CreateStepView.as_view(), name = 'post_step'),
    path('post_success', views.PostSuccessView.as_view(), name = 'post_success'),
    path('cooks_list/', views.RecipeListView.as_view(), name = 'cooks_list'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    path('contact/', views.ContactView.as_view(), name ='contact'),
    path('recipe-detail/<int:pk>', views.DetailView.as_view(), name = 'recipe_detail'),
    path('recipes/<int:category>/', views.CategoryView.as_view(), name = 'recipes_cat'),
    path('recipe/<int:recipe_id>/review/', views.write_review, name='write_review'),
]
