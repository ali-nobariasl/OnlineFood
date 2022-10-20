from django.contrib import admin
from verndor.models import Vender



class VenderAdmin(admin.ModelAdmin):
    list_display = ('user','vender_name','is_approved','created_at')
    list_display_links = ('user','vender_name')
    list_editable= ('is_approved',)
    
admin.site.register(Vender, VenderAdmin)