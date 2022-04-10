import UploadProblemAsTeacher.upload_wizard as upload_wizard
import sys

if __name__ == '__main__':
    upload_wizard.upload_problem(sys.argv[1], sys.argv[2] == '1')
