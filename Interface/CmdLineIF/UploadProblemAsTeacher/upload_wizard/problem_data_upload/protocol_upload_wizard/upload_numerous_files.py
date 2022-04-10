from UploadProblemAsTeacher.upload_wizard.aux import copy_file


def upload_numerous_files(semantics, path_to_protocol_dir, key_seq_to_current_dict, custodian):
    print(f"Input paths to {semantics}put files, one-by-one (\033[91minput path to directory with files: coming soon\033[0m)")  # todo
    test_count = custodian.nested_get_item(key_seq_to_current_dict + ('test_count',))
    for test in range(test_count):
        file_src = input(f"Input path to {semantics}put file #{test_count}: ")
        file_dest = f'{path_to_protocol_dir}/{test_count}.{semantics}'
        copy_file(file_src, file_dest)

        suffix = file_dest[file_dest.find('TPy_project'):]
        custodian.nested_append(key_seq_to_current_dict + (f'{semantics}files',), suffix)
