from django.contrib import admin
from highcharts.models import Fingerprint


class FingerprintAdmin(admin.ModelAdmin):
    list_display = ('title', 'file',)

# Register models
admin.site.register(Fingerprint, FingerprintAdmin)