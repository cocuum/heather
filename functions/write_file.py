from google.genai import types
from os import path,makedirs


def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = path.abspath(working_directory)
        target_dir = path.normpath(path.join(abs_working_directory,file_path))
        
        #validate directory is within working_directory
        if path.commonpath([abs_working_directory,target_dir]) != abs_working_directory:
            return f'   Error: Cannot write to "{target_dir}" as it is outside the permitted working directory'

        #validate directory is a directory
        if path.isdir(target_dir):
            return f'   Error: Cannot write to "{target_dir}" as it is a directory'

        #validate all parent directories exist
        makedirs(path.dirname(target_dir), exist_ok=True)

        with open(target_dir, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'  Error: writing to file: {e}'

# Define the function schema for write_file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file in a specified directory relative to the working directory. If the file already exists, it will be overwritten. The file path must end with a filename and cannot be a directory. All parent directories must already exist or be created by the function. The function returns a success message with the number of characters written or an error message if writing fails.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory (default is the working directory itself). The path must include a filename and cannot be a directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            ),
        },
        required=["file_path","content"],
    )
)