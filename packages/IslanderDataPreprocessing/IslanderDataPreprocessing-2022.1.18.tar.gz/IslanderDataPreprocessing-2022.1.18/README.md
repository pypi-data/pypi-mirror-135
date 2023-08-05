# IslanderDataPreprocessing

This python package was designed to help python developers
who want to get in to machine Learning have an easier way to do so.
currently there are 6 modules in this package, this number will grow
as the Islander Robotics Community works more and more with machine
Learning and Artificial Intelligence.

#DataBase

DataBase(API_command)
currently this module only works with downloading and installing
datasets from the Kagle website.

API_command: this is where you will insert the designated API command from the
Kagle website

datasets: this list is where all of the datasets you downloaded at the current
time of running the module will be stored as a pandas DataFrame
allowing you the ability to save time by not having to uploaded the datasets again.

filename: this module will allow you the ability to see what index each file is stored in
the datasets list. as well as you will have the ability to know what files where downloaded
from Kagle.

#DataCorrelation

DataCorrelation(df)
This module is designed to allow you the ability to see what parts of your data have high correlation between them
from there you will be able to use the information to combine those columns for the best results
