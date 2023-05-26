# TPy_project
Year 1, term 2

Игорь Жильцов, Б05-124

The current programme is a set of testing protocols which check given source code on given test scheme

NOTE: CURRENT VERSION SUPPORTS C++ AND PYTHON3 RUNS ONLY; HASKELL IS  NOT DEBUGGED YET; JAVA/SCALA IS NOT IMPLEMENTED

Sample runs for each protocol are presented in test_cxx.py and test_python3.py. 

To conduct a C++ run:
- come up with a problem, solution for which would be tested
- choose one of four testing protocol classes and create a protocol object using __init__, analogous to samples in test_cxx.py (inout, in_custom, rand_custom, limited_work_space objects)
- write a correct or incorrect solution to it and create a UserSubmittedData object, initialized with a path to solution and a random integer (used as submission ID), analogous to correct and wrong objects in test_cxx.py
- run 'verdict = protocol_object.check(user_submitted_data=user_submitted_data_object)'. this will create a verdict object, which would have the actual string representation of testing verdict in 'msg' member. Message 'WA' denotes wrong answer, 'AC' - right answer, 'CE' - compilation error, 'RE' - runtime error


To conduct a Python3 run:
- come up with a problem, solution for which would be tested
- choose one of four testing protocol classes and create a protocol object using __init__, analogous to samples in test_python3.py (inout, in_custom, rand_custom, limited_work_space objects)
- write a correct or incorrect solution to it and create a UserSubmittedData object, initialized with a path to solution and a random integer (used as submission ID), analogous to correct and wrong objects in test_python3.py
- run 'verdict = protocol_object.check(user_submitted_data=user_submitted_data_object)'. this will create a verdict object, which would have the actual string representation of testing verdict in 'msg' member. Message 'WA' denotes wrong answer, 'AC' - right answer, 'RE' - runtime error 

The current role model supplies 2 roles: TEACHER and STUDENT
A Teacher can upload problems and a Student can solve them

To upload a problem as Teacher, run "make" in Interface/CmdLineIF/UploadProblemAsTeacher and then "sudo make run" ("sudo" is required to enable submission execution as "nobody" for safety). The verbose mode is on by default, elaborate instructions will be provided in run-time. Additionaly, an Activity and UseCase diagrams are provided in the same directory
To upload a problem, you need to provide the following FILES:
- (optional) statement.{txt, pdf, md}
- test files (see according test protocol for details)
Thus, it is better to create the required files before running


To upload a solution as Student, run "make" in Interface/CmdLineIF/UploadSubmissionAsStudent and then "make run"
