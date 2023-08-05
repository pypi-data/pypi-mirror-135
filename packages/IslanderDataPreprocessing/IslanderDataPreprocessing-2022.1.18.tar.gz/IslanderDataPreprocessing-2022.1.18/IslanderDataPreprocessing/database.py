import os
import zipfile
import pandas as pd
class DataBase:
    '''DataBase(API_command)
    currently this module only works with downloading and installing
    datasets from the Kagle website.

    API_command: this is where you will insert the dessgnated API command fromt the
    Kagle website

    datasets: this list is where all of the datasets you downloaded at the current
    time of running the module will be stored as a pandas DataFrame
    allowing you the ability to save time by not having to uploaded the datasets again.

    filename: this module will allow you the ability to see what index each file is stored in
    the datasets list. as well as you will have the ability to know what files where downloaded
    from Kagle.'''
    def __init__(self,API_command):
        os.system(API_command)
        self.name = API_command.split('/')
        self.Open()
        os.remove(self.name[1]+".zip")
    def Open(self):
        self.dataset = []
        with zipfile.ZipFile(self.name[1]+".zip", "r") as zip:
            filenames = zip.namelist()
            zip.extractall()
        for i in filenames:
            self.dataset.append(pd.read_csv(i))
        self.filenames = filenames
