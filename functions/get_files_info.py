import os

def get_files_info(working_directory, directory=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory or ""))
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        dir_content = os.listdir(full_path)
        str_result = ""
        for item in dir_content:
            item_path = os.path.join(full_path, item)
            str_result += f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n"
        return str_result.rstrip()
    except Exception as e:
        return f"Error: {e}"
