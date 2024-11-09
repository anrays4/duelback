from django.db import models


class SocialForWebsite(models.Model):
    social_name = models.CharField(max_length=100)
    link = models.TextField(max_length=500)
    logo = models.ImageField(upload_to="social_logo/")

    def __str__(self):
        return self.social_name



