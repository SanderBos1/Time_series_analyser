import os


#reads all files from given directory and puts the names in a list
def get_files(target):
    for file in os.listdir(target):
        path = os.path.join(target, file)
        if os.path.isfile(path):
            yield (
                file
            )