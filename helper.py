import os
from pathlib import Path

def split_path(s: str) -> tuple[str, str]:
    """
    Splits Filepath into file and path

    *Arguments:*
        s: String

    *Example:*
        file, path = splitPath(s) 
    """
    import os
    f = os.path.basename(s)
    p = s[:-(len(f))-1]
    return str(f), str(p)

def mkdir_if_not_exist(directory: str) -> str:
    """
    Makes directory if not exists and returns the string

    *Arguments*:
        dir: String

    *Example*:
        dir = mkdir_if_not_exist(dir) 
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def get_path_file_extension(input_file: str) -> tuple[str, str, str]:
    """ 
    Returns path, the filename and the filename without extension.

    *Arguments:*
        input_file: String

    *Example:*
        path, file, file_wo_extension = get_path_file_extension(input_file)
    """
    file, path = split_path(input_file)
    file_wo_extension = Path(Path(input_file).stem).stem
    return path, file, file_wo_extension
