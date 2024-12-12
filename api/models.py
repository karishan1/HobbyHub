from django.db import models
from django.contrib.auth.models import AbstractUser


class Hobby(models.Model):
    # Uniquely identifies each hobby to avoid duplicate hobbies
    hobby_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.hobby_name

class User(AbstractUser):
    # User model inherits from AbstractUser
    DOB = models.DateField(null=True,blank=True)
    Hobbies = models.ManyToManyField(Hobby)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="user_groups",
        blank=True,
        help_text=("The groups this user belongs to."),
        verbose_name=("groups"),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="user_permissions",
        blank=True,
        help_text=("Specific permissions for this user."),
        verbose_name=("user permissions"),
    )

    def __str__(self):
        return self.first_name


class Friendship(models.Model):
    # Establishes a friendship between two users (Many to Many)
    user = models.ForeignKey(User,on_delete = models.CASCADE, related_name='friendship_intiated')
    friend = models.ForeignKey(User,on_delete = models.CASCADE, related_name='friendship_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Establishes uniqueness between combination of User and Friend
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} is friends with {self.friend}"
    
class FriendRequest(models.Model):
    # Allows Friend requests to be sent from one user to another
    from_user = models.ForeignKey(User,on_delete = models.CASCADE, related_name='friend_request_sent')
    to_user = models.ForeignKey(User,on_delete = models.CASCADE, related_name='friend_request_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"Friend Request from {self.from_user} to {self.to_user}"








# idk what this is it was created before 

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
