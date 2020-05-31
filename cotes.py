import sys
import os
import shutil

codes = sys.argv[1:]

if len(codes)==0:
    print("usage: codes code0 code1 code2 ..., codes -l")
    exit(0)
    
script_path = os.path.split(os.path.realpath(__file__))[0]
cwd = os.getcwd()

if sys.argv[1]=="-l":
    [print(i) for i in os.listdir(os.path.join(script_path, "codes"))]
    exit(0)

for code in codes:
    to_copy = os.path.join(script_path, "codes", code)
    for item in os.listdir(to_copy):
        item = os.path.join(to_copy, item)
        if (os.path.isfile(item)):
            shutil.copy2(item, cwd)
        else:
            shutil.copytree(item, cwd)
    
