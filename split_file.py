import os
import sys
import math
from functools import reduce

# To split file     : $ python split_file.py SPLIT PATH_TO_FILE_TO_SPLIT SPLIT_SIZE(MB)
# To recreate file  : $ python split_file.py RECREATE PATH_TO_FIRST_SPLIT 

# FILE_SPLIT_HEADER
# ORIGINAL_FILE_NAME
# NUMBER OF SPLITS
def readHeader(path):
    with open(path,"rb") as f:
        l = f.readline()
        if l.strip() != b'FILE_SPLIT_HEADER':
            return None,None
        filename = f.readline().decode('utf-8').strip()
        splits = int(f.readline().decode('utf-8').strip())

        return filename,splits

def writeHeader(path,original_filename,splits):
    with open(path,"w") as f:
        print("FILE_SPLIT_HEADER",file=f)
        print(original_filename,file=f)
        print(splits,file=f)

def split(path,size):
    split_size = int(size * math.pow(2,20))
    directory,file_name = os.path.split(path)
    file_size = int(os.stat(path).st_size)

    if file_size <= split_size:
        print("Error: the size of the split should be less then the size of the original file")
        return False
    
    splits = int(math.ceil(float(file_size)/float(split_size)))
    file_name_no_ext = file_name \
        if not file_name.find('.') else reduce(lambda x,y: x + y,file_name.split('.')[0:-1])

    split0 = os.path.join(directory,file_name_no_ext + ".SPLIT_0")
    writeHeader(split0,file_name,splits)

    with open(path,"rb") as file:
        for s in range(splits):
            split = os.path.join(directory,file_name_no_ext + ".SPLIT_{}".format(s))
            with open(split,"ab") as split:
                data = file.read(split_size)
                split.write(data)

def recreate(path):
    dir,_ = os.path.split(path)
    file_name,splits = readHeader(path)
    if file_name == None:
        print("Error: the specified path is not valid")
        return False

    file_name_no_ext = file_name \
        if not file_name.find('.') else reduce(lambda x,y: x + y,file_name.split('.')[0:-1])

    file_name = "RECONSTRUCTED_"+file_name
    with open(os.path.join(dir,file_name),"wb") as f:
        for s in range(splits):
            split_path = os.path.join(dir,file_name_no_ext+".SPLIT_{}".format(s))
            with open(split_path,"rb") as split:
                # consume header of the first split
                if s==0:
                    for i in range(3):
                        split.readline()
                f.write(split.read())
    


#split("C:\\Users\\giorg\\Desktop\\SplitFiles\\Fantastic.Beasts.The.Crimes.Of.Grindelwald.2018.EXTENDED.1080p.BluRay.x265-RARBG.mp4",100)
recreate("C:\\Users\\giorg\\Desktop\\SplitFiles\\FantasticBeastsTheCrimesOfGrindelwald2018EXTENDED1080pBluRayx265-RARBG.SPLIT_0")

