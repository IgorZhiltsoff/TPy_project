from data_custodian import JsonDataCustodian
from UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard import upload_protocol


def upload_problem_data(path_to_dir, verbose):
    # CREATE CUSTODIAN
    custodian = JsonDataCustodian(path_to_dir, 'problem_data')
    upload_protocol(path_to_dir, 0, custodian, verbose)

    protocol_number = 1
    while input("Add another protocol? [Y/n]") == 'Y':
        upload_protocol(path_to_dir, protocol_number, custodian, verbose)
        protocol_number += 1

    # FINISH
    custodian.dump_data()
