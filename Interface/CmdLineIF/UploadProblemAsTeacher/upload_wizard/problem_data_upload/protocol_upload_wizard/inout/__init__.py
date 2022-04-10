import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.infiles as infiles
import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.outfiles as outfiles


def upload_specific_protocol(key_seq_to_current_dict, custodian, verbose):
    infiles.upload_inputs(key_seq_to_current_dict, custodian, verbose)
    outfiles.upload_inputs(key_seq_to_current_dict, custodian, verbose)
