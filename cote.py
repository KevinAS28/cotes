"""
Code Template by Kevin Agusto

version: 0.1
"""

import sys
import argparse
from conf import Conf
import os
from decor import *
import traceback
import time
import pwd
import datetime
import platform 
import json

desc = """
Code Template - KevinAS28
"""

def join_address(lst):
    toreturn = ""
    for c in lst:
        toreturn = os.path.join(toreturn, c)
    return toreturn

template_dir = "templates"
special_handler = {"":""} #the language that need special handling function. format = language_name:function_name
working_dir = os.getcwd()
program_path = os.path.realpath(__file__)
program_dir = join_address(os.path.split(program_path)[:-1])
parser = argparse.ArgumentParser(description=desc) #argument parser
conf = Conf(os.path.join(program_dir, "cote.conf")) #configuration parser
default_language = conf.getVal("default_language")
language_configuration_file_name = "language.conf"

#later will be initiated
user_code = []
output_code = []
avail_languages = dict({}) #language: conf object

def scan_languages(dir=template_dir):
    languages = os.listdir(os.path.join(program_dir, template_dir))
    toreturn = dict({})
    for lang in languages:
        try:
            toreturn[lang] = (Conf(os.path.join(program_dir, dir , lang, language_configuration_file_name)))
        except Exception as err:
            Error("Possibility the language {} is doesn't have language.conf".format(lang))
            traceback.print_exc()
            
    return toreturn
    
def generate_info(language, langver):
    user = pwd.getpwuid(os.getuid())[0]
    time = datetime.datetime.now().isoformat()
    osname = platform.system()
    osver = platform.release()
    info0 = """Author: {}
File Created at: {}
{} {}
OS: {} {}""".format(user, time, language, langver, osname, osver)
    info = ""
    startcomment = avail_languages[language].getVal("start_comment")
    stopcomment = avail_languages[language].getVal("stop_comment")
    for line in info0.split("\n"):
        info += startcomment+line+stopcomment+"\n"
    info+="\n\n\n"
    return info

def process_code(the_code, specific=None, to_import=[], output=None, write_info=False):    
    global output_code
    global user_code

    user_code = the_code.split(" ")
    if (output==None):
        output_code = []
    else:
        output_code = output.split(" ")    
    index = 0

    for code in user_code:
        code0 = os.path.split(code)
        language = ""
        
        #if the language is not specified, then use default language
        if ((len(code0)==2 )and (code0[0]=="")):
            code = os.path.join(default_language, code)
            code0 = os.path.split(code)
        
        language = code0[0]
        
        #check if special handler needed, then run the function
        if (language in special_handler.keys()):
            special_handler[code0[0]](code)
            continue

        langconf = avail_languages[language]
        code = os.path.join(program_dir, template_dir, code) + langconf.getVal("extension")
        if (not(os.access(code, os.R_OK))):
            Error("The code {} ({}) is not availble. please add that first".format(code0[-1], code))

        output = ""
        try:
            output += os.path.join(working_dir, output_code[index]) + langconf.getVal("extension")
        except:
            output += os.path.split(code)[-1]
            
        if (os.access(output, os.R_OK)):
            if (not(conf.getVal("overwrite_if_exist")=="0")):
                Warn("{} is already exist and configuration say i must skip it".format(output))
                continue

        with open(output, "w+") as write:
            with open(code, "r") as read:
                towrite = ""
                if (write_info):
                    towrite += generate_info(langconf.getVal("language"), "")
                towrite += read.read()
                write.write(towrite)

        index+=1
        print(f"{output} [Done]")

def generate_code(the_codes_specifics, outputs, write_info):
    if (len(list(the_codes_specifics.keys()))!=len(outputs) or len(outputs)==0):
        raise ValueError(f"lenght of the_codes_specifics: {the_codes_specifics} is not the same as the lenght of outputs: {outputs}")
    index = 0
    for code in the_codes_specifics:
        specifics = the_codes_specifics[code]
        output = outputs[index]

        index+=1


def list_to_dict(the_list):
    toreturn = dict()
    if ((len(the_list)%2) != 0) or (len(the_list)==0):
        raise ValueError(f"\"{the_list}\" : the length is not even or empty. must be: \"code0 specific0 code1 specific1\" format")
    for index in range(0, int(len(the_list)), 2):
        toreturn[the_list[index]] = the_list[index+1]
    return toreturn

def main():
    parser.add_argument("c", nargs="*", default=None)
    parser.add_argument("-c", "--code", help='Need an argument, see the language list (-lsl)', default=None, nargs="*")
    parser.add_argument("-o", "--output", help="output filename", nargs="*", default=None)
    parser.add_argument("-wi", "--write-info", help="write some information to your code", action="store_const", const=True)
    parser.add_argument("-lsl", "--list-languages", help="show the list of availble languages in our templates", action="store_const", const=True)
    #parser.add_argument("-df", "--default languages", help="show your current default language")
    #parser.add_argument("-addl", "--add language", help="add a language")
    #parser.add_argument("-addls", "--add languages", help="add languages")
    all_args = (parser.parse_args(sys.argv[1:])).__dict__
    print(all_args)
    return 0

    global avail_languages
    if (all_args["code"]!=None):
        avail_languages = scan_languages()
        # process_code(
        #     the_code = json.loads(all_args["code"][0] if all_args["c"]==None else all_args["code"][0]), 
        #     specific = all_args["specific"],
        #     to_import = all_args["to_import"],
        #     output = all_args["output"],
        #     write_info = True if all_args["write_info"] else False
        #     )
        generate_code(
            the_codes_speciifc=list_to_dict(all_args["code"]if all_args["c"]==[] else all_args["c"]),
            outputs=all_args["output"],
            write_info=all_args["write_info"]
            )

        

    elif (all_args["list_languages"]!=None):
        avail_languages = scan_languages()
        print("Availble Languages ({}): ".format(str(len(avail_languages.keys()))))
        for lang in avail_languages.keys():
            print("{} --- {} {}".format(lang, avail_languages[lang].getVal("real_language_name"), avail_languages[lang].getVal("extension")))

    else:
        parser.print_usage()

    return 0    


if __name__=="__main__":
    sys.exit(main())




