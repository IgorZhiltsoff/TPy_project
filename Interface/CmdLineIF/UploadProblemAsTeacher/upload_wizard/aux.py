import subprocess


def copy_file(path_to_src, path_to_dest):
    print(path_to_dest)
    subprocess.run(['cp', path_to_src, path_to_dest])


def create_dir(path_to_dir):
    subprocess.run(['mkdir', path_to_dir])
    return path_to_dir


def get_path_suffix(path):
    return path[path.find('TPy_project'):]
