from django.contrib import admin
from .models import Reg
class Regadmin(admin.ModelAdmin):
    list_display = ['username','fname','lname','dob','mobno']
    list_filter = ['dob']
    class meta:
     model=Reg
admin.site.register(Reg,Regadmin)

# Register your models here.
