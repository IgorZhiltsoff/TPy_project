def choose_protocol_scheme(verbose):
    if verbose:
        prompt = """
Input protocol scheme, choosing one of 4 options:
    1. InputOutput: requires N input files and N files with correct outputs. 
        The system will run submission on each input and check whether it's equal to corresponding correct output
        
    2. InputCustomChecker: requires N input files and 1 custom checker executable
         The system will run submission on each input and check output with custom checker
         
    3. RandomInputCustomChecker: requires 1 random input generator, 1 custom checker executable and 1 integer X
        The system will generate X random inputs, run submission on all of them and check output with custom checker
    
    4. LimitedWorkSpace: requires 1 "header", 1 "footer" and 1 string denoting file extension (see below)
        The system will take submission source and merge it with header and footer into a compound file:
            <header>
            <submission src>
            <footer>
        Thus, to save this file, we need to know the correct extension for it
        Upon execution, the compound file should print 1 if the submission has passed and 0 otherwise

Input the number of desired protocol: """
    else:
        prompt = """
Input 1 for InputOutput, 
      2 for InputCustomChecker,
      3 for RandomInputCustomChecker,
      4 for LimitedWorkSpace:
"""

    scheme = input(prompt)
