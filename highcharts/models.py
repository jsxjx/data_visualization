from django.db import models


class Fingerprint(models.Model):
    title = models.CharField(max_length=128, unique=True)
    # file will be uploaded to MEDIA_ROOT/uploads
    file = models.FileField(upload_to='fingerprints/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Fingerprint'
        verbose_name_plural = 'Fingerprints'