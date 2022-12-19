from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.marketplace,name= 'marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail ,name= 'vendor_detail'),
    
    # add to card
    path('add_to_card/<int:food_id>', views.card_to_card, name= 'card_to_card'),
]
