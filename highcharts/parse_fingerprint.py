import csv
from io import StringIO


def parse_csv_fingerprint(csvfile):
    """Open, read, parse the CSV file and return the proper data.

    Get the CSV file, read and decode it to String. Call csv.reader() with the proper delimiter. Skip the first
    line. Obviously all of this will depend on CSV file format.

    Args:
        request
        csvfile_name: This is the name of the uploaded & validated CSV file (default = False).

    Returns:
        x-axis values, y-axis values, grid-data values, minimum z-axis value, maximum z-axis value.
        Grid-data values is a list of lists comprised of x-axis value, z-axis values and row index.

    """
    csvfile_string = StringIO(csvfile.read().decode())
    data_reader = csv.reader(csvfile_string, delimiter=',')
    next(csvfile_string)

    x_cv = []   # X-axis values
    grid_data = []  # Z-grid values
    z_min = 0   # min Z-grid value
    z_max = 0   # max Z-grid value

    for row in data_reader:
        x_cv.append(row[0])
        grid_data = data_generator(grid_data, row)
        [z_min, z_max] = row_min_max(row[1:], z_min, z_max)

    y_dv = list(range(1, len(row[1:])+1))   # Y-axis values

    return x_cv, y_dv, grid_data, z_min, z_max


def data_generator(grid_data, row):
    """Update the grid_data list with the new row data.

    Given the current read CSV file row and the grid_data list, append to the list a list of: x-axis value, z-axis
    values and row index.

    Args:
        grid_data: This is the grid_data list.
        row: This is the current read CSV file line.

    Returns:
        The updated grid_data list.

    """
    index = 1
    for z_values in row[1:]:
        grid_data.append([row[0], z_values, str(index)])
        index += 1
    return grid_data


def row_min_max(row, z_min, z_max):
    """Return the minimum and the maximum value given a row.

    Given a row, and the last minimum and maximum values, sort the row values and compare the ends with the reference
    values.

    Args:
        row: A CSV file line. Starts at second field, ends at last field.
        z_min: This is the current minimum z-axis value since first CSV file row.
        z_max: This is the current maximum z-axis value since first CSV file row.

    Returns:
        The updated minimum and the maximum z-axis value given a new row.

    """
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
# Main
if __name__ == "__main__":
    data = {}

    csvfile = "" # a Django FileField, If is used a CSV file path instead, modify the parse_csv_fingerprint
    [x_cv, y_dv, grid_data, z_min, z_max] = parse_csv_fingerprint(csvfile)
    data['x_cv'] = x_cv
    data['y_dv'] = y_dv
    data['grid_data'] = grid_data
    data['z_min'] = z_min
    data['z_max'] = z_max
'''

