from google.genai import types
from os import path

from config import MAXCHARS


def get_file_content(working_directory,file_path):
    
    try:
        #validate directory is within working_directory
        abs_working_directory = path.abspath(working_directory)
        target_file = path.normpath(path.join(abs_working_directory, file_path))

        if path.commonpath([abs_working_directory,target_file]) != abs_working_directory:
            return f'   Error: Cannot list "{target_file}" as it is outside the permitted working directory'

        #validate file is a file
        if not path.isfile(target_file):
            return f'   Error: File not found or is not a regular file: "{target_file}"'
        
        try:
            with open(target_file,'r') as f:
                message = f.read(MAXCHARS)
                if f.read(1) != '':
                    message += f'[...File "{target_file}" truncated at {MAXCHARS} characters]'
                return message
        except Exception as e:
            return f'    Error: {e}'
            
    except OSError as e:
        return f'   Error: {e}'

# Define the function declaration for get_file_content
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file in a specified directory relative to the working directory, providing the content of the file up to MAXCHARS characters and content has been truncated if file has more than MAXCHARS characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory (default is the working directory itself). The path must include a filename and cannot be a directory.",
            ),
        },
        required=["file_path"],
    ),
)