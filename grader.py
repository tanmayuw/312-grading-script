# write a script which takes in the grades csv from Gradescope and computes their grades 
# according to the syllabus. The late deductions on the psets are already factored in to 
# their grade

# Return a csv of name, UW id, pset percent, quiz percent, cc percent, and overall percent 
# according to the weighting in syllabus



import csv
import re
import numpy as np
import gradelib as glib # NOTE: install first with pip install git+https://github.com/eldridgejm/gradelib
import pandas as pd


########## read in the records ##########

records = pd.read_csv('~/312_grades.csv')
dict = records.to_dict()

# all the fields we need in the final result
results = {'name' : list() , 
            'uwid' : list(), 
            'pset_per' : list(), 
            'quiz_per' : list(),
            'cc_per' : np.zeros(len(records)).tolist(),
            'overall_per': list() 
            }


for i in range(len(records)):
    results['name'].append( records['First Name'][i] + " " + records['Last Name'][i] )
    results['uwid'].append( records['Email'][i].split('@')[0])

##################



####### external library  #######

#read and create gradebook. We don't allow any lateness fudge on submissions
gradebook = glib.Gradebook.from_gradescope('~/312_grades.csv', lateness_fudge=0)



########## Define the different types of assignments ##########

#Handle Extra Credit (EC)
ecs = gradebook.assignments.containing('extra credit')
gradebook_ec = gradebook.keep_assignments(ecs)

#gradebook without EC problems
gradebook_abs = gradebook.remove_assignments(ecs)


####### Applying late policy to assignmets which don't have 
####### late penalty counted (Concept checks / CCs for our case) #######
ccs = gradebook_abs.assignments.containing('concept check')
gradebook_ccs = gradebook_abs.keep_assignments(ccs)

cc_dict  = gradebook_ccs.points.fillna(0).to_dict()
cc_max = gradebook_ccs.maximums.to_dict()
max = sum(cc_max.values())

late_dict = gradebook_ccs.late.to_dict()

for assignment in late_dict:
    for i,sid in enumerate(late_dict[assignment].keys()):
        if (late_dict[assignment][sid]):
            results['cc_per'][i] += (cc_dict[assignment][sid]) * 0.5
        else:
            results['cc_per'][i] += (cc_dict[assignment][sid])
        


#Handle EC CCs or more EC assignments
ec_dict  = gradebook_ec.points.fillna(0).to_dict()

for assignment in ec_dict:
    for i,sid in enumerate(ec_dict[assignment]):
        results['cc_per'][i] += (ec_dict[assignment][sid])

#get fraction (between 0 and 1) score
for i in range(len(results['cc_per'])):
    results['cc_per'][i] = results['cc_per'][i] / max

##################



########## Assignments for which Late penalty is already accounted for or is 0 ###########

# forgiving all lates in other assignments
gradebook_abs = (
    gradebook_abs
    .forgive_lates(99999999)
)

# Other scores:
psets = gradebook_abs.assignments.containing('pset')
gradebook_psets = gradebook_abs.keep_assignments(psets)
pset_score = gradebook_psets.score(psets).fillna(0).to_list() 


quizzes = gradebook_abs.assignments.containing('quiz')
gradebook_quizzes = gradebook_abs.keep_assignments(quizzes)
quiz_score = gradebook_quizzes.score(quizzes).fillna(0).to_list() 

for i in range(len(pset_score)):
    results['pset_per'].append(pset_score[i])
    results['quiz_per'].append(quiz_score[i])

##################

####### Overall percentage/ fraction score #######

for i in range(len(records)):
    results['overall_per'].append( results['pset_per'][i] * 0.5 + results['quiz_per'][i] * 0.4 + 
        results['cc_per'][i] * 0.1 )

##################


####### Save as csv #######
result_csv = pd.DataFrame.from_dict(results)
result_csv.to_csv('~/312_results.csv', index=False)
##################

##########################################





