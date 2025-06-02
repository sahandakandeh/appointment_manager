from django.contrib import admin
from .models import UserDoctor,Booking,Post,Comment
# Register your models here.
admin.site.register(UserDoctor)
admin.site.register(Booking)
admin.site.register(Post)
admin.site.register(Comment)