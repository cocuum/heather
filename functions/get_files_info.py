import os

def get_files_info(working_directory, directory="."):
    
    #validate directory is within working_directory
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))
    if os.path.commonpath([abs_working_directory,target_dir]) != abs_working_directory:
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #validate directory is a directory
    if not os.path.isdir(target_dir):
        return f'   Error: "{target_dir}" is not a directory'
    
    #record directory content in dictionary
    list_directory = []
    for target in os.listdir(target_dir):
        
        try:
            file_size = os.path.getsize(os.path.join(target_dir,target))
        except Exception as e:
            return f'   Error: {e}'
        
        try:
            is_dir = os.path.isdir(os.path.join(target_dir,target))
        except Exception as e:
            return f'   Error: {e}'
        
        s = f' - {target}: file_size={file_size}, is_dir={is_dir}'
        list_directory.append(s)

    message = "\n".join(list_directory)

    return message
