from django.http import JsonResponse
from django.shortcuts import render
from highcharts.form import FingerprintForm
from highcharts.models import Fingerprint
from highcharts.parse_fingerprint import parse_csv_fingerprint


def home(request):
    """Render and manage FingerprintForm form.

    If POST read the FingerprintForm form, validate it and retrieve the title for csv_file_name. If form is not valid,
    return FingerprintForm form and set csv_file_name to False.
    If !POST return FingerprintForm form, where csv_file_name is False.

    Args:
        request

    Returns:
        A dict mapping keys to the corresponding FingerprintForm form and csv_file_name variable.

    """
    context_dict = {}
    data = {}

    if request.method == 'POST':
        form = FingerprintForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            context_dict['form_fingerprint'] = FingerprintForm()
            context_dict['csv_file_name'] = form.cleaned_data['title']
        else:
            context_dict['form_fingerprint'] = form
            context_dict['csv_file_name'] = False
    else:
        context_dict['form_fingerprint'] = FingerprintForm()
        context_dict['csv_file_name'] = False
        
    return render(request, 'highcharts/home.html', context_dict)


def chart_data_json(request, csv_file_name):
    """Retrieve the CSV file, parse it and return the data in a JSON object.

    Retrieve the CSV file from DB by its name, call the parse method and return the data dict a JSON object.
    By default the CSV file name is False.

    Args:
        request
        csv_file_name: This is the name of the uploaded & validated CSV file (default = False).

    Returns:
        JSON object of data dict. Data dict contains: x-axis values, y-axis values, grid-data values, minimum z-axis
        value, maximum z-axis value.

    """
    data = {}
    context_dict = {}

    if csv_file_name is not False:
        try:
            csvfile = Fingerprint.objects.get(title=csv_file_name)
            [x_cv, y_dv, grid_data, z_min, z_max] = parse_csv_fingerprint(csvfile.file)
            data['x_cv'] = x_cv
            data['y_dv'] = y_dv
            data['grid_data'] = grid_data
            data['z_min'] = z_min
            data['z_max'] = z_max

        except Fingerprint.DoesNotExist:
            csvfile = None

    return JsonResponse(data)
