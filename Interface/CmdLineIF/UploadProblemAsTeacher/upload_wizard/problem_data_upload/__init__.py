from UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard import upload_protocol


def upload_problem_data(custodian, path_to_dir, verbose):
    # HAND OVER CONTROL
    print("Now we are ready to upload testing protocols. You will be given a chance to specify them one-by-one")
    upload_protocol(path_to_dir, 0, custodian, verbose)
    protocol_number = 1
    while input("Add another protocol? [Y/n]") == 'Y':
        upload_protocol(path_to_dir, protocol_number, custodian, verbose)
        protocol_number += 1

    # FINISH
    custodian.dump_data()
