from django.db import models
from django.contrib.auth.models import AbstractUser # type: ignore



class Hobby(models.Model):
    # Uniquely identifies each hobby to avoid duplicate hobbies
    hobby_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.hobby_name

class User(AbstractUser):
    # User model inherits from AbstractUser
    DOB = models.DateField(null=True,blank=True)
    Hobbies = models.ManyToManyField(Hobby,blank=True)

    def __str__(self):
        return self.username
    
    def to_dict(self):
        return{
            'id' : self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'DOB': self.DOB,
            'hobbies': self.get_hobbies()
        }
    
    def to_dict_user_list(self):
        return{
            'id' : self.id,
            'username': self.username,
            'DOB': self.DOB,
            'hobbies': self.get_hobbies()
        }
    
    
    def get_hobbies(self):
        return [x.hobby_name for x in self.Hobbies.all()]




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
    status = models.CharField(max_length=10, choices=[('pending','Pending'),('accepted','Accepted')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"Friend Request from {self.from_user} to {self.to_user}"
    
    def to_dict(self):
        return {
            "id" : self.id,
            "from_user_id": self.from_user.id,
            "from_user_username": self.from_user.username,
            "status": self.status,
            "to_user_username" : self.to_user.username
            }
    


# idk what this is it was created before 

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
