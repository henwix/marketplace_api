from django.db.models import TextChoices


class SocialAccountProviders(TextChoices):
    GITHUB = 'github', 'GitHub'
    GOOGLE = 'google', 'Google'
