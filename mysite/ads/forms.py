from django import forms
from .models import Ad
from django.core.files.uploadedfile import InMemoryUploadedFile
from humanize import naturalsize


# Create the form class
class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    # Picture is manual
    class Meta:
        model = Ad
        fields = ['title', 'price', 'text', 'picture']

    # Override clean() to validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # Override save() to convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        # Make a copy
        f = instance.picture
        # Extract data from the form to the model
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            # Read the content type
            instance.content_type = f.content_type
            # Overwrite with the actual image data
            instance.picture = bytearr

        # We save the form data if commit=True
        if commit:
            instance.save()

        return instance

# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
