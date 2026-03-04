import os
from config import MAXCHARS

def get_file_content(working_directory,file_path):
    
    #validate directory is within working_directory
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
    if os.path.commonpath([abs_working_directory,target_file]) != abs_working_directory:
        return f'   Error: Cannot list "{target_file}" as it is outside the permitted working directory'
    
    #validate file is a file
    if not os.path.isfile(target_file):
        return f'   Error: File not found or is not a regular file: "{target_file}"'
    
    try:
        with open(target_file,'r') as f:
            try:
                fr = f.read(MAXCHARS)
                if f.read(1) != '':
                    fr += f'[...File "{target_file}" truncated at {MAXCHARS} characters]'
            except Exception as e:
                return f'    Error: {e}'
    except OSError as e:
        return f'   Error: {e}'
    
    return fr