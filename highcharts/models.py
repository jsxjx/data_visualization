from django.db import models


class Fingerprint(models.Model):
    """Stores a CSV Fingerprint entry.

    Attributes:
        title: The name of the CSV file.
        file: The CSV file.

    """
    title = models.CharField(max_length=128, unique=True)
    # file will be uploaded to MEDIA_ROOT/uploads
    file = models.FileField(upload_to='fingerprints/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Fingerprint'
        verbose_name_plural = 'Fingerprints'
