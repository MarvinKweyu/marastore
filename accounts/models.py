from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Default custom user model for the store.
    """

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("customuser:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """Save user and create profile during registration."""
        super().save(*args, **kwargs)
        Profile.objects.get_or_create(user=self)


class Profile(models.Model):
    """
    User profile
    """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="user_profile"
    )

    CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("P", "Prefer not to say"),
    )
    gender = models.CharField(max_length=1, choices=CHOICES, default="P")
    # TODo: Add more fields
    # city = models.CharField(_("city"), max_length=250)
    # address = models.CharField(_("address"), max_length=250)
    # postal_code = models.CharField(_("postal code"), max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("profile:detail", kwargs={"username": self.user.username})
