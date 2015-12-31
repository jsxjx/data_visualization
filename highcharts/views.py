from django.http import JsonResponse
from django.shortcuts import render
from highcharts.form import FingerprintForm
from highcharts.models import Fingerprint
from highcharts.parse_fingerprint import parse_csv_fingerprint


def home(request):
    context_dict = {}
    data = {}

    if request.method == 'POST':
        form = FingerprintForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            context_dict['form_fingerprint'] = FingerprintForm()
            context_dict['csvfile_name'] = form.cleaned_data['title']
        else:
            context_dict['form_fingerprint'] = form
            context_dict['csvfile_name'] = False
    else:
        context_dict['form_fingerprint'] = FingerprintForm()
        context_dict['csvfile_name'] = False
        
    return render(request, 'highcharts/home.html', context_dict)


def chart_data_json(request, csvfile_name):
    data = {}
    context_dict = {}

    if csvfile_name is not False:
        try:
            csvfile = Fingerprint.objects.get(title=csvfile_name)
            [x_cv, y_dv, grid_data, z_min, z_max] = parse_csv_fingerprint(csvfile.file)
            data['x_cv'] = x_cv
            data['y_dv'] = y_dv
            data['grid_data'] = grid_data
            data['z_min'] = z_min
            data['z_max'] = z_max

        except Fingerprint.DoesNotExist:
            csvfile = None

    return JsonResponse(data)
