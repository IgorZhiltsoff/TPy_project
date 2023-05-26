from UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.upload_single_file import upload_single_file


def upload_custom_checker(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    upload_single_file('custom checker executable', path_to_protocol_dir, key_seq_to_current_dict, custodian)
