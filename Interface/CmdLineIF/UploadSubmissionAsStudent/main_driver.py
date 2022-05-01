import submission_wizard
import sys

if __name__ == '__main__':
    submission_wizard.submission_wizard(sys.argv[1], sys.argv[2] == '1', sys.argv[3])
