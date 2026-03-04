import os

def write_file(working_directory, file_path, content):

    #validate directory is within working_directory
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_directory,file_path))
    if os.path.commonpath([abs_working_directory,target_dir]) != abs_working_directory:
        return f'   Error: Cannot write to "{target_dir}" as it is outside the permitted working directory'
    
    #validate directory is a directory
    if os.path.isdir(target_dir):
        return f'   Error: Cannot write to "{target_dir}" as it is a directory'
    
    #validate all parent directories exist
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

    try:
        with open(target_dir, 'w') as f:
            try:
              f.write(content)
              return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            except Exception as e:
                return f'   Error: {e}'
    except OSError as e:
        return f'  Error: {e}'

