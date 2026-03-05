import os
import subprocess
from google import genai

schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file in a specified directory relative to the working directory and return the output. The file must be a .py file and execution is subject to a timeout of 30 seconds. Output includes both STDOUT and STDERR. If the process exits with a non-zero code, that is also included in the output.", 
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="File path to read content from, relative to the working directory (default is the working directory itself). The path must include a filename and cannot be a directory."
            ),
            "args": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                items=genai.types.Schema(
                    type=genai.types.Type.STRING
                ),
                description="Optional list of string arguments to pass to the Python file when executing"
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):

    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_directory,file_path))
    
    #validate directory is within working_directory
    if os.path.commonpath([abs_working_directory, target_file]) != abs_working_directory:
        return f'    Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    #is file a file?
    if not os.path.isfile(target_file):
        return f'   Error: "{file_path}" does not exist or is not a regular file'
    
    #is file .py?
    if not target_file.endswith(".py"):
        return f'   Error: "{file_path}" is not a Python file'
    
    #subprocess to run a file
    command = ["python", target_file]

    if args != None:
        command.extend(args)
    
    try:
        sbp = subprocess.run(command,capture_output=True,text=True,timeout=30)
    except Exception as e:
        return f'   Error: executing Python file: {e}'
    
    output = ""
    try:
        if sbp.returncode != 0:
            output = output + f'Process exited with code {sbp.returncode}'
        elif len(sbp.stdout) == 0 and len(sbp.stderr) == 0:
            output = output + f'No output produced'
        else:
            output = output + f'STDOUT: {sbp.stdout}' + f'STDERR: {sbp.stderr}'
    except Exception as e:
        return f'   Error: executing Python file: {e}'

    return output