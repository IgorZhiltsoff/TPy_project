import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.rand_in as rand_in
import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.custom_checker as custom_checker


def upload_specific_protocol(key_seq_to_current_dict, custodian, verbose):
    rand_in.upload_rand(key_seq_to_current_dict, custodian, verbose)
    custom_checker.upload_custom_checker(key_seq_to_current_dict, custodian, verbose)
