# Description
This python script can split a big file into smaller files and then can recreate the original file from the splits. It's useful to overcome size limitations existing in some content sharing or cloud storage applications.
# How to Run
## Split a file
To split the file <b>example.dat</b> with size 1000MB into splits of 10MB run the command:
```shell
$ python split_file.py SPLIT ABS_PATH_TO/example.dat 10
```
The program will produce in the same directory a folder <b>SPLITS</b> containing the 100 splits, each split is named like the original file but the extension is replaced with "SPLIT_N" where N is the number of the split.
## Recreate a file
To recreate example.dat run the command:
```shell
$ python split_file.py RECREATE ABS_PATH_TO/example.SPLIT_0
```
Where the second argument is the absolute path of the first split (The one with extension SPLIT_0)