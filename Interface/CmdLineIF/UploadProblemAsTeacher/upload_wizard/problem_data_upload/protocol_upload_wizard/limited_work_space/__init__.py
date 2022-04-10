from UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.upload_single_file \
    import upload_single_file


def upload_header(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    upload_single_file('header', path_to_protocol_dir, key_seq_to_current_dict, custodian)


def upload_footer(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    upload_single_file('footer', path_to_protocol_dir, key_seq_to_current_dict, custodian)
