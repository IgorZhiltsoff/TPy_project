import json
from testing_protocols import *
from UploadSubmissionAsStudent.helper import *


def retrieve_problem_data(problem_id, path_to_problems_dir, mount_point):
    return parse_problem_data(problem_id, extract_problem_data(problem_id, path_to_problems_dir), mount_point)


def extract_problem_data(problem_id, path_to_problems_dir):
    problem_dir = find_dir(problem_id, path_to_problems_dir)
    path_to_data = f'{problem_dir}/problem_data.json'
    with open(path_to_data) as data:
        extracted = json.load(data)
    return extracted


def parse_problem_data(problem_id, extracted, mount_point):
    protocol_datas = extracted['protocols']

    testing_protocols_set = set()
    for key in protocol_datas:
        testing_protocols_set.add(parse_protocol_data(protocol_datas[key], mount_point))

    return ProblemData(
        problem_id=problem_id,
        testing_protocols_set=testing_protocols_set
    )


def parse_protocol_data(protocol_data, mount_point):
    scheme = get_scheme(protocol_data)
    execution_and_conversion_data_set = get_execution_and_conversion_data_set(protocol_data)

    return eval(f'parse_{scheme}')(protocol_data, execution_and_conversion_data_set, mount_point)


def parse_inout(protocol_data, execution_and_conversion_data_set, mount_point):
    paths_to_infiles = get_infiles(protocol_data, mount_point)
    paths_to_outfiles = get_outfiles(protocol_data, mount_point)
    input_output_paths_dict = dict(zip(paths_to_infiles, paths_to_outfiles))  # json arrays order is guaranteed

    x = InputOutput(
        input_output_paths_dict=input_output_paths_dict,
        execution_and_conversion_data_set=execution_and_conversion_data_set
    )
    return x


def parse_in_custom(protocol_data, execution_and_conversion_data_set, mount_point):
    input_paths_set = set(get_infiles(protocol_data, mount_point))
    path_to_checker_exec = get_custom_checker(protocol_data, mount_point)

    return InputCustomChecker(
        input_paths_set=input_paths_set,
        path_to_checker_exec=path_to_checker_exec,
        execution_and_conversion_data_set=execution_and_conversion_data_set
    )


def parse_rand_custom(protocol_data, execution_and_conversion_data_set, mount_point):
    path_to_input_generation_exec = get_rand_gen(protocol_data, mount_point)
    path_to_checker_exec = get_custom_checker(protocol_data, mount_point)
    test_count = get_test_count(protocol_data)

    return RandomInputCustomChecker(
        path_to_input_generation_exec=path_to_input_generation_exec,
        path_to_checker_exec=path_to_checker_exec,
        test_count=test_count,
        execution_and_conversion_data_set=execution_and_conversion_data_set
    )


def parse_limited_work_space(protocol_data, execution_and_conversion_data_set, mount_point):
    path_to_header = get_header(protocol_data, mount_point)
    path_to_footer = get_footer(protocol_data, mount_point)
    extension = get_extension(protocol_data)

    return LimitedWorkSpace(
        path_to_header=path_to_header,
        path_to_footer=path_to_footer,
        extension=extension,
        execution_and_conversion_data_set=execution_and_conversion_data_set
    )
