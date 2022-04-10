import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.infiles as infiles
import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.custom_checker as custom_checker


def upload_specific_protocol(key_seq_to_current_dict, custodian, verbose):
    infiles.upload_infiles(key_seq_to_current_dict, custodian, verbose)
    custom_checker.upload_custom_checker(key_seq_to_current_dict, custodian, verbose)
