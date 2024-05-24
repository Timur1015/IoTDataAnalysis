import os
import zipfile


# extract and load the content of zipped folder into the project
def extract_files(directory):
    file = os.path.basename(directory)
    folder_name = (os.path.splitext(file)[0]).lower()
    # create new directory to keep the data structure
    os.makedirs(folder_name, exist_ok=True)

    with zipfile.ZipFile(directory, 'r') as zip_ref:
        zip_ref.extractall(folder_name)
        working_dir = os.getcwd()
        data_path = os.path.join(working_dir, folder_name)
        for file in os.listdir(data_path):
            path_old = os.path.join(data_path, file)
            os.rename(path_old, path_old.lower())


path = r"C:\Users\timur\privat\Jobs\Praxisnahe_Aufgabe.zip"
extract_files(path)
