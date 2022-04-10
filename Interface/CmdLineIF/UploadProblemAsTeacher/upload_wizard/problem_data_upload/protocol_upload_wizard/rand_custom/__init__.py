import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.rand_in as rand_in
import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.custom_checker as custom_checker


def upload_specific_protocol(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    rand_in.upload_rand(path_to_protocol_dir, key_seq_to_current_dict, custodian)
    custom_checker.upload_custom_checker(path_to_protocol_dir, key_seq_to_current_dict, custodian)
