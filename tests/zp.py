import os
import uuid

def file_name(file_dir):  
	for root, dirs, files in os.walk(file_dir):
		return files


def change_name(file_dir):
	lj = file_name(file_dir)
	change_list = []
	for x in lj:
		file_name = uuid.uuid4()
		a = "mv /" + x + " " + "/" + file_name

		change_list.append(a)

	for x in change_list:

		os.system(x)

change_name("/Users/lucy/Desktop/test")
