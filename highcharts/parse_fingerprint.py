import csv
from io import StringIO


def parse_csv_fingerprint(csvfile):
    '''
    This function opens a spectrometer-based CSV file, parse it and returns three variables.
    x_cv is a list with CV values.
    y_dv is a list with DV values.
    z_ic is a dictionary with the Ion Current measured at a specific CV & DV.
    '''

    csvfile_string = StringIO(csvfile.read().decode())
    data_reader = csv.reader(csvfile_string, delimiter=',')
    next(csvfile_string)

    x_cv = []
    grid_data = []
    z_min = 0
    z_max = 0
    #index = 1

    for row in data_reader:
        x_cv.append(row[0])
        #z_ic[index] = row[1:]
        #z_ic.append(row[1:])
        grid_data = data_generator(grid_data, row)
        # call min-max
        [z_min, z_max] = row_min_max(row[1:], z_min, z_max)
        #index += 1

    y_dv = list(range(1, len(row[1:])+1))

    return x_cv, y_dv, grid_data, z_min, z_max


def data_generator(grid_data, row):
    index = 1
    for i in row[1:]:
        grid_data.append([row[0], i, str(index)])
        index += 1
    return grid_data


def row_min_max(row, z_min, z_max):
    float_row = [float(i) for i in row]
    float_row.sort()
    row_min = float_row[0]
    row_max = float_row[-1]

    if float(row_max) >= float(z_max):
        z_max = row_max

    if float(row_min) <= float(z_min):
        z_min = row_min

    return z_min, z_max

'''
if __name__ == "__main__":
    file_path = "/home/coals/Documents/test_matrix.csv"
    x_cv = []
    y_dv = []
    z_ic = {}
    x_cv, y_dv, z_ic = parse_csv(file_path)
'''

