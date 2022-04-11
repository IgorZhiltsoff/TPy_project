from language_support import *


def get_full_path(mount_point):
    return lambda suffix: f'{mount_point}/{suffix}'


def find_dir(problem_id, path_to_problems_dir):
    return f'{path_to_problems_dir}/{problem_id}'


def get_programming_language_data(protocol_data):
    return eval(protocol_data["programming_language_data"])


def get_conversion_opts(protocol_data):
    return protocol_data["conversion options"]


def get_command_line_opts(protocol_data):
    return protocol_data["command line options"]


def get_scheme(protocol_data):
    return protocol_data["scheme"]


def get_infiles(protocol_data, mount_point):
    return map(get_full_path(mount_point), protocol_data["infiles"])


def get_outfiles(protocol_data, mount_point):
    return map(get_full_path(mount_point), protocol_data["outfiles"])


def get_rand_gen(protocol_data, mount_point):
    return get_full_path(mount_point)(protocol_data["rand"])


def get_custom_checker(protocol_data, mount_point):
    return get_full_path(mount_point)(protocol_data["cust"])


def get_header(protocol_data, mount_point):
    return get_full_path(mount_point)(protocol_data["head"])


def get_footer(protocol_data, mount_point):
    return get_full_path(mount_point)(protocol_data["foot"])


def get_extension(protocol_data):
    return protocol_data["ext"]


def get_test_count(protocol_data):
    return protocol_data["test_count"]
