from UploadProblemAsTeacher.upload_wizard.helper import copy_file, get_path_suffix


def upload_numerous_files(semantics, path_to_protocol_dir, key_seq_to_current_dict, custodian):
    print(f"Input paths to {semantics}put files, one-by-one (\033[91minput path to directory with files: coming soon\033[0m)")  # todo
    test_count = custodian.nested_get_item(key_seq_to_current_dict + ('test_count',))
    for test in range(test_count):
        file_src = input(f"Input path to {semantics}put file #{test}: ")
        file_dest = f'{path_to_protocol_dir}/{test}.{semantics}'
        copy_file(file_src, file_dest)

        suffix = get_path_suffix(file_dest)
        custodian.nested_append(key_seq_to_current_dict + (f'{semantics}files',), suffix)
