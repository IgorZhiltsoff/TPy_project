# TPy_project
Year 1, term 2

Игорь Жильцов, Б05-124

The current programme is a set of testing protocols which check given source code on given test scheme

NOTE: CURRENT VERSION SUPPORTS C++ RUNS ONLY; PYTHON3, HASKELL AND JAVA/SCALA ARE NOT DEBUGGED YET

Sample runs for each protocol is presented in test_cxx.py. 

To conduct a C++ run:
- come up with a problem, solution for which would be tested
- choose one of four testing protocol classes and create a protocol object using __init__, analogous to samples in test.py (inout, in_custom, rand_custom, limited_work_space objects)
- write a correct or incorrect solution to it and create a UserSubmittedData object, initialized with a path to solution and a random integer (used as submission ID), analogous to correct and wrong objects in test_cxx.py
- run 'verdict = protocol_object.check(user_submitted_data=user_submitted_data_object)'. this will create a verdict object, which would have the actual string representation of testing verdict in 'msg' member. Message 'WA' denotes wrong answer, 'AC' - right answer, 'CE' - compilation error 
