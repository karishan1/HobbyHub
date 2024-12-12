from django.contrib import admin
from .models import User, Hobby, UserHobby, Friendship, FriendRequest

admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(UserHobby)
admin.site.register(Friendship)
admin.site.register(FriendRequest)
