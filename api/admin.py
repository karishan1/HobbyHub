from django.contrib import admin
from .models import User, Hobby, Friendship, FriendRequest

admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(Friendship)
admin.site.register(FriendRequest)
