from UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.upload_single_file \
    import upload_single_file


def upload_specific_protocol(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    upload_header(path_to_protocol_dir, key_seq_to_current_dict, custodian)
    upload_footer(path_to_protocol_dir, key_seq_to_current_dict, custodian)
    upload_extension(key_seq_to_current_dict, custodian)


def upload_header(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    upload_single_file('head', path_to_protocol_dir, key_seq_to_current_dict, custodian)


def upload_footer(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    upload_single_file('foot', path_to_protocol_dir, key_seq_to_current_dict, custodian)


def upload_extension(key_seq_to_current_dict, custodian):
    extension = input('Input extension: ')
    custodian.nested_fill_in(key_seq_to_current_dict + ('ext',), extension)
