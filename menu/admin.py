from django.contrib import admin

from .models import Category ,FoodItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'sluge':('category_name',)}
    list_display= ('category_name','vendor','updated')
    search_fields = ('category_name','vendor__vendor_name')
                          
class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'sluge':('food_title',)}
    list_display= ('food_title','category','vendor','price','is_available','updated')
    search_fields = ('food_title','category__category_name','vendor__vendor_name','price')         
    list_filter =('is_available',)                                   
                          
admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
