from django.contrib import admin
from .models import Category, Recipe, Ingredient, Step, Review
 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
 
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
 
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'name')
    list_display_links = ('id', 'recipe', 'name')
 
class StepAdmin(admin.ModelAdmin):
    list_display = ('id','recipe' , 'step_number')
    list_display_links = ('id', 'recipe', 'step_number')
 
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'rating')
    list_display_links = ('id', 'recipe', 'rating')
 
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Review, ReviewAdmin)
