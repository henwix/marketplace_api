from django.db.models import TextChoices


class SupportedOAuthProviders(TextChoices):
    """All providers through which authentication can occur using the OAuth protocol"""

    GITHUB = 'github', 'GitHub'
    GOOGLE = 'google', 'Google'


class SupportedAuthProviders(TextChoices):
    """All providers/authentication methods that can be associated with a User via AuthProvider"""

    GITHUB = 'github', 'GitHub'
    GOOGLE = 'google', 'Google'
