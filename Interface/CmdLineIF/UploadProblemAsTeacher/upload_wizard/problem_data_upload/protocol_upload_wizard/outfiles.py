from UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.upload_numerous_files import upload_numerous_files


def upload_outfiles(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    upload_numerous_files('out', path_to_protocol_dir, key_seq_to_current_dict, custodian)
