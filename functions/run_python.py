import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and return its output, error and optionally its return code, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that we will execute, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if os.path.commonpath([full_path, working_directory_abs]) != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        result = subprocess.run(args=["python", file_path], timeout=30, capture_output=True, text=True, cwd=working_directory)
        if not result.stdout and not result.stderr:
            return "No output produced."
        if result.returncode != 0:
            return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}\nProcess exited with code {result.returncode}"
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
