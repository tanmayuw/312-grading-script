# 312-grading-script

grading script for CSE 312: grader.py grades the submissions csv files downloaded from gradescope. 

The internal structure uses [gradelib library](https://eldridgejm.github.io/gradelib/#gradelib.Gradebook).
 Allows for organization of assignments into various groups including Psets (written and coding) Concept Checks, 
Extra credit assignments and more. Score can be assigned using the score() method in the gradelib and GPA/letter grades can be assigned 
by using the other appropriate methods listed in the library documentation. Assuming the similar structure of assignments, this script 
can be used across multiple offerings with minor modifications. Note that gradelib does not provide custom lateness deductions and by default 
assumes all late submissions to be scored 0, unless you forgive the late deductions. I have implemented the custom deduction for Concept checks 
as a sample and you can use a similar structure to have custom deductions for lateness. 
