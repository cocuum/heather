from google.genai import types
from os import path,listdir

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    
    #validate directory is within working_directory
    abs_working_directory = path.abspath(working_directory)

    target_dir = path.normpath(
        path.join(abs_working_directory, 
                     directory,)
    )

    if path.commonpath([abs_working_directory,target_dir]) != abs_working_directory:
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #validate directory is a directory
    if not path.isdir(target_dir):
        return f'   Error: "{target_dir}" is not a directory'
    
    #record directory content in list
    list_directory = []
    for target in listdir(target_dir):
        
        try:
            file_size = path.getsize(
                path.join(target_dir,target)
            )
        except Exception as e:
            return f'   Error: {e}'
        
        try:
            is_dir = path.isdir(
                path.join(target_dir,target)
            )
        except Exception as e:
            return f'   Error: {e}'
        
        s = f' - {target}: file_size={file_size}, is_dir={is_dir}'
        list_directory.append(s)

    message = "\n".join(list_directory)

    return message
