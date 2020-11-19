# PAGE FOR SELF EXPLANATIONS
"""
num_proto 	num_class
			
ICMP = 0		Anomaly = 0		
TCP = 1          Normal = 1
UDP = 2


#EXPLANATION :
https://blog.exsilio.com/all/accuracy-precision-recall-f1-score-interpretation-of-performance-measures/#:~:text=F1%20score%20%2D%20F1%20Score%20is,and%20false%20negatives%20into%20account.
-----------------------------------------------------------------------------------------------------------------------
True Positives (TP) - These are the correctly predicted positive values which means that the value of actual class is
yes and the value of predicted class is also yes
-----------------------------------------------------------------------------------------------------------------------
True Negatives (TN) - These are the correctly predicted negative values which means that the value of actual class is
no and value of predicted class is also no
-----------------------------------------------------------------------------------------------------------------------
False Positives (FP) – When actual class is no and predicted class is yes
-----------------------------------------------------------------------------------------------------------------------
False Negatives (FN) – When actual class is yes but predicted class in no
-----------------------------------------------------------------------------------------------------------------------
Accuracy is the most intuitive performance measure and it is
simply a ratio of correctly predicted observation to the total observations
Accuracy = TP+TN/TP+FP+FN+TN
-----------------------------------------------------------------------------------------------------------------------
Precision is the ratio of correctly predicted positive observations to the total predicted positive observations
Precision = TP/TP+FP
-----------------------------------------------------------------------------------------------------------------------
Recall is the ratio of correctly predicted positive observations to the all observations in actual class - yes
Recall = TP/TP+FN
-----------------------------------------------------------------------------------------------------------------------
F1 score - F1 Score is the weighted average of Precision and Recall.
Therefore, this score takes both false positives and false negatives into account
F1 Score = 2*(Recall * Precision) / (Recall + Precision)
-----------------------------------------------------------------------------------------------------------------------

print("accuracy " + str(accuracy_score(y_test, y_pred)))
print("Precision score " + str(precision_score(y_test, y_pred)))
print("Recall score " + str(recall_score(y_test, y_pred)))
print("F1 score " + str(f1_score(y_test, y_pred)))


returns the most optimiszed decision tree
The parameters of the estimator(My decision tree) used to apply these methods are optimized by
cross-validated grid-search over a parameter grid.

dtc - estimator the algorithm

cv = KFold Algorithm , cross validation , checks with every set of the data for the best results so i won't have
to decide by myself what is counted as a good test/train split , it checks all the possible combinations
and chooses to use the one with the best percentages for success.
in practice its common to devide to 10 fold cross validation

verbose = Controls the verbosity: the higher, the more messages about the build process

n_jobs=-1 - allows all process to run at the same time

scoring - the way it scores each outcome , can be by accuracy , by weight , by average 
param_grid - Dictionary with parameters names (str) as keys and lists of parameter settings to try as values,
or a list of such dictionaries, in which case the grids spanned by each dictionary in the list are explored.
This enables searching over any sequence of parameter settings.
Fitting the cv *size = 10* folds for each of the *list(2,25)* candidates
---------------------------------------------------------------------------
# Create a parameter grid: map the parameter names to the values that should be searched
# Simply a python dictionary
# Key: parameter name
# Value: list of values that should be searched for that parameter
# Single key-value pair for param_grid
param_grid: 
the grid search model will be able to tell us with criteria is better to use in the decision tree gini or entropy.
max_depth - we want to limit the amount of trees you'd wanna keep it low so plot(the output pic will be in a normal size)
min_samples_leaf - specifies the minimum number of samples required to be at a leaf node ,



MultiOutPutClassifier - allows to output multiple checks , instead of just assigning one label to my data
i'm going by protocol and class label so i want to check if its from a specific protocol and output 0/1 for it 
and also want to check if its a normal / anomaly (like the faces analysis [1 , 0 , 1]

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

"""