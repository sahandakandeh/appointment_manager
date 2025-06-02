from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class UserDoctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='user_profile', default='default_profile_picture.png')
    
    def get_absolute_url(self):
        return reverse('appointments:doctors')
    
    def __str__(self):
        return self.user.username


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    doctor = models.ForeignKey(UserDoctor, on_delete=models.CASCADE, related_name='bookings')
    patient_name = models.CharField(max_length=100 , null=True,blank=True)
    phone_number = models.CharField(max_length=100 , null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"{self.user.username} -> {self.doctor.user.username} @ {self.date} {self.time}"


class Post(models.Model):
    author = models.ForeignKey(UserDoctor,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User,related_name="post_like",null=True,blank=True)
    dislike = models.ManyToManyField(User,related_name="post_dislike",null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"title = {self.title}"
    
    def get_absolute_url(self):  
        return reverse("doctors", kwargs={"pk": self.pk})
    
class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    body = models.TextField(max_length=400)
    is_validate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.author} - {self.body[:30]}"
    
class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.from_user} following {self.to_user}'