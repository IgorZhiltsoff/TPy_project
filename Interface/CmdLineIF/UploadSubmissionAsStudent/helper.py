from language_support import *


def get_full_path(mount_point):
    return lambda suffix: f'{mount_point}/{suffix}'


def find_dir(problem_id, path_to_problems_dir):
    return f'{path_to_problems_dir}/{problem_id}'


def get_execution_and_conversion_data_set(protocol_data):
    execution_and_conversion_data_set = set()
    raw_execution_and_conversion_data_set = protocol_data['execution_and_conversion_data_set']
    for key in raw_execution_and_conversion_data_set:
        execution_and_conversion_data = raw_execution_and_conversion_data_set[key]
        programming_language_data = get_programming_language_data(execution_and_conversion_data)

        time_limit = get_time_limit(execution_and_conversion_data)
        memory_limit_megabytes = get_memory_limit_megabytes(execution_and_conversion_data)

        conversion_opts = get_conversion_opts(execution_and_conversion_data)
        command_line_opts = get_command_line_opts(execution_and_conversion_data)

        execution_and_conversion_data_set.add(
            ExecutionAndConversionData(
                language_data=programming_language_data,

                time_limit_seconds=time_limit,
                memory_limit_megabytes=memory_limit_megabytes,

                conversion_opts=conversion_opts,
                command_line_opts=command_line_opts
            )
        )
    return execution_and_conversion_data_set


def get_programming_language_data(execution_and_conversion_data):
    return eval(execution_and_conversion_data["programming_language_data"])


def get_time_limit(execution_and_conversion_data):
    return execution_and_conversion_data["time limit"]


def get_memory_limit_megabytes(execution_and_conversion_data):
    return execution_and_conversion_data["memory limit"]


def get_conversion_opts(execution_and_conversion_data):
    return execution_and_conversion_data["conversion options"]


def get_command_line_opts(execution_and_conversion_data):
    return execution_and_conversion_data["command line options"]


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
