# TPy_project
Year 1, term 2

Игорь Жильцов, Б05-124

The current programme is a set of testing protocols which check given source code on given test scheme

NOTE: CURRENT VERSION SUPPORTS C++ AND PYTHON3 RUNS ONLY; HASKELL IS  NOT DEBUGGED YET; JAVA/SCALA IS NOT IMPLEMENTED

The current role model supplies 2 roles: TEACHER and STUDENT
A Teacher can upload problems and a Student can solve them

To upload a problem as Teacher, run "make" in Interface/CmdLineIF/UploadProblemAsTeacher and then "sudo make run" ("sudo" is required to enable submission execution as "nobody" for safety). The verbose mode is on by default, elaborate instructions will be provided in run-time. Additionaly, an Activity and UseCase diagrams are provided in the same directory
To upload a problem, you need to provide the following FILES:
- (optional) statement.{txt, pdf, md}
- test files (see according test protocol for details)
Thus, it is better to create the required files before running


To upload a solution as Student, run "make" in Interface/CmdLineIF/UploadSubmissionAsStudent and then "make run"
