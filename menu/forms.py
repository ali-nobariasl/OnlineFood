from django import forms

from .models import Category ,FoodItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']
        
        

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['category','food_title','description','price', 'image', 'is_available']