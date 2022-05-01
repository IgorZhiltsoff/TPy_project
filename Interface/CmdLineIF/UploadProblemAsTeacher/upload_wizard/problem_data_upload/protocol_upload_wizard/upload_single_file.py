from UploadProblemAsTeacher.upload_wizard.helper import copy_file, get_path_suffix


def upload_single_file(semantics, path_to_protocol_dir, key_seq_to_current_dict, custodian):
    short_semantics = semantics[:4]
    file_src = input(f"Input paths to {semantics}: ")
    file_dest = f'{path_to_protocol_dir}/{short_semantics}'
    copy_file(file_src, file_dest)

    suffix = get_path_suffix(file_dest)
    custodian.nested_append(key_seq_to_current_dict + (f'{semantics}files',), suffix)
