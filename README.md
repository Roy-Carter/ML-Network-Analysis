# ML - Algorithm (Decision Tree Classifier)


## :shipit: ML - Algorithm for the Analyzer Project :shipit:

### Supervised Algorithm for network analysis

#### Code Flow :
* [**Step 1**] - trains the algorithm (organizing data , creating grid and taking best module to use the classification process on)

* [**Step 2**] - organizes the test set (different csv file) 	

* [**Step 3**] - running the module on the test file

* [**Step 4**] - creating CSV file called Results.csv that describes the results

#### CSV Files usage explanation :
 
| CSV Files | Meaning |
| ------ | ------ |
| SmallTrain | training the data on a 3MB file |
| BigTrain | training the data on a 14MB file |
| SmallTest | testing the data on a 2MB file |
| Results | The outcome of the algorithm with the [Class , Protocol] |

#### Field Values for Protocol 
| Field | ID |
| ------ | ------ |
| ICMP | 0 |
| TCP | 1 |
| UDP | 2 |

#### Field Values for Class
| Field | ID |
| ------ | ------ |
| Anomaly | 0 |
| Normal | 1 |

### Todos
 -  Check about the SelectKbest to select best feature usage --> [SelectKBest On Decision Tree](https://www.youtube.com/watch?v=siwo7A0fcRk) .
 -  Check about how to present the decision tree with matplotlib / graphviz .
 -  Output which of the features are the one casuing it to be labeled as **Anomaly**.
 