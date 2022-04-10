import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.infiles as infiles
import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.outfiles as outfiles


def upload_specific_protocol(path_to_protocol_dir, key_seq_to_current_dict, custodian):
    infiles.upload_infiles(path_to_protocol_dir, key_seq_to_current_dict, custodian)
    outfiles.upload_outfiles(path_to_protocol_dir, key_seq_to_current_dict, custodian)
