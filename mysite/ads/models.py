from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


# Class for Ads
class Ad(models.Model) :

    # Actual data
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()

    # This field is used to check the owner of the data entry
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Ads picture as binary field
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text='The MIMEType of the file'
    )

    # Date/time of creation and modification - autofields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the model
    def __str__(self):
        return self.title

