from csv import reader, writer
import os


def read_local_file(file_name):
    if '.csv' in file_name:
        rdr = reader(open(file_name, 'rb'))
        return rdr
    return open(file_name, 'rb')


def write_local_file(file_name, data):
    with open(file_name, 'wb') as open_file:
        if type(data) is list:
            wr = writer(open_file)
            for line in data:
                wr.writerow(line)
        else:
            open_file.write(data)


def get_latest(folder):
    files = [os.path.join(folder, f) for f in os.listdir(folder)]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[0]
