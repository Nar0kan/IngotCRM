from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# For file upload validator
from .validators import validate_file
from django.core.exceptions import ValidationError


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    position = models.CharField(max_length=100, default="employee", null=True, blank=True)
    phone_number = models.CharField(max_length=100, default="unknown", null=True, blank=True)
    photo = models.ImageField(verbose_name="Photo", null=True, blank=True, upload_to="images/agents")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# class Rights(models.Model):
#     organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

#     level = models.CharField(default="free", max_length=100)
#     team_size = models.IntegerField(default=5)
#     individual_configuration = models.BooleanField(default=False)
#     premium_support = models.DateTimeField(auto_now_add=True)
#     price = models.FloatField(default=00.00, max_length=100)

#     def __str__(self):
#         return f"{self.level}"


# class Order(models.Model):
#     rights = models.ForeignKey(Rights, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.rights.level}, {self.rights.organisation}"


class Lead(models.Model):
    first_name = models.CharField(max_length=28)
    last_name = models.CharField(max_length=28)
    age = models.IntegerField(default=0)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    photo = models.ImageField(verbose_name="Photo", null=True, blank=True, upload_to="images/leads")

    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)    # Every lead has an agent
    category = models.ForeignKey("Category", related_name="lead_cat", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)             # Agent == User(AbstractUser)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # Organisation == UserProfile == User(AbstractUser)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=50)
    organisation = models.ForeignKey(UserProfile, on_delete = models.CASCADE)

    def __str__(self):
        return self.name
        

class Document(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    is_secret = models.BooleanField(default=False)
    file = models.FileField(validators=[validate_file, ], null=False, blank=False, upload_to="media/")
    date_added = models.DateTimeField(auto_now_add=True)

    lead = models.ForeignKey("Lead", null=False, blank=False, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class LeadComment(models.Model):
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    lead = models.ForeignKey("Lead", null=False, blank=False, related_name="lead_com", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lead.email} - {self.author.username}"


def postUserCreatedSignal(sender, instance, created, **kwargs):
    if created:
        user = UserProfile.objects.create(user=instance)

post_save.connect(postUserCreatedSignal, sender=User)


@receiver(post_save, sender=UserProfile)
def create_categories(sender, instance, created, **kwargs):
    if created:
        category_names = ['Unassigned', 'Contacted', 'Converted', 'Unconverted']
        for name in category_names:
            Category.objects.create(name=name, organisation=instance)
