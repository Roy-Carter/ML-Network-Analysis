from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import pandas as pd
import numpy as np

from doctest import testmod # for testing purposes


def test_classifier(model, test):
    """
    This functions purpose is to classify the input csv file by the module and create
    an output csv file containing the algorithm results :
    duration , protocol type and a list of [num_proto ,num_class] for better clarification when reading.
    :param model: the trained module .
    :param test: the csv file we would like to check on the module
    :return: No returns , output withhin the function.
    """

    num_class = encode(test['class'])
    test['num_class'] = num_class

    num_proto = encode(test['protocol_type'])
    test['num_proto'] = num_proto

    service_num = encode(test['service'])
    test['service_num'] = service_num

    flag_num = encode(test['flag'])
    test['flag_num'] = flag_num

    df_test = test[['duration', 'dst_bytes', 'wrong_fragment', 'su_attempted', 'num_root',
                    'num_file_creations', 'num_shells', 'num_access_files', 'is_guest_login', 'srv_count',
                    'same_srv_rate',
                    'srv_diff_host_rate', 'dst_host_same_srv_rate', 'num_proto', 'flag_num', 'num_class']]

    test = df_test.drop(['num_class', 'num_proto'], axis=1)

    t_pred = model.predict(test)
    class_p, protocol_p = edit_output(t_pred)
    check_results = pd.DataFrame({'Class': class_p, 'Protocol': protocol_p})
    print("===============================")
    check_results.to_csv("CsvFiles/Results.csv", index=False)


def edit_output(t_pred):
    """
    receives the prediction output and transforms the prediction output to class and protocol lists
    :param t_pred: the prediction outputs
    :return: returns two lists of class prediction and protocol prediction
    """
    t_pred = list(t_pred)
    class_p = []
    protocol_p = []
    for arr_val in t_pred:
        class_p.append(arr_val[0])
        protocol_p.append((arr_val[1]))
    return class_p, protocol_p


def grid_summary(final_data_test, x_test, x_train, y_test, y_train):
    """
    Summarizes the grid classification process .
    :param final_data_test: Best grid estimator tree , holds the best decision tree settings for most
    optimized results.
    :param x_test: holds the split data set for the testing part for the grid
    :param x_train: holds the split data set for the training part for the grid
    :param y_test: holds the label column to test for the grid
    :param y_train: holds the label column to train for the grid
    :return: No return .
    """
    print("===============================")
    print("Accuracy for the grid module :")
    print(f'Test:{final_data_test.score(x_test, y_test):.3f}')
    print(f'Train:{final_data_test.score(x_train, y_train):.3f}')

    best_feat = pd.DataFrame({'features': x_train.columns, 'importance': final_data_test.feature_importances_})
    print("===============================")
    print(best_feat.sort_values('importance', ascending=False))


def encode(df):
    """
    A function to encode every column I need so it will be a computer readable value (numbers).
    :param df:the current data frame we are looking at
    :return: an array of the category listed in its continuous values
    """
    encoder = LabelEncoder()
    target = encoder.fit_transform(df)
    return np.array(target)


def main():
    """testmod(name='testing', verbose=True)"""
    train = pd.read_csv("CsvFiles/SmallTrain.csv")

    num_class = encode(train['class'])
    train['num_class'] = num_class

    num_proto = encode(train['protocol_type'])
    train['num_proto'] = num_proto

    service_num = encode(train['service'])
    train['service_num'] = service_num

    flag_num = encode(train['flag'])
    train['flag_num'] = flag_num

    df_working = train[['duration', 'dst_bytes', 'wrong_fragment', 'su_attempted', 'num_root',
                     'num_file_creations', 'num_shells', 'num_access_files', 'is_guest_login',
                     'srv_count', 'same_srv_rate', 'srv_diff_host_rate', 'dst_host_same_srv_rate',
                     'num_proto', 'flag_num', 'num_class']]


    # y1 is my main target , multi label classification
    y1 = df_working[['num_class', 'num_proto']]
    # this is a single target for plotting purpose
    y = df_working[['num_class']]
    """
    dropping my two targets
    #axis = 0 for rows , axis = 1 for columns
    """
    X = df_working.drop(['num_class', 'num_proto'], axis=1)
    print("model description")
    print(X.describe())

    # for the grid , finding the best tree option
    x_train1, x_test1, y_train1, y_test1 = train_test_split(X, y1, test_size=.2)
    # for the multioutclsput classification
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.2)

    # min samples_leaf indicator - don't consider a split that leaves less than min_samples_leaf
    split_range = list(range(2, 25))
    param_grid = {'criterion': ('gini', 'entropy'), 'max_depth': (np.arange(1, 10)), 'min_samples_leaf': split_range}

    dtc = tree.DecisionTreeClassifier()
    dt_grid = GridSearchCV(dtc, param_grid, cv=10, n_jobs=-1, verbose=2, scoring='accuracy')
    # fit the grid with data
    dt_grid.fit(x_train, y_train)
    # best estimator (the best decision tree settings basically)
    dt_final = dt_grid.best_estimator_
    dt_final.fit(x_train, y_train)

    #y_pred can be used for classification_report (in the print explanations.py)
    y_pred = dt_final.predict(x_test)

    grid_summary(dt_final, x_test, x_train, y_test, y_train)

    model = MultiOutputClassifier(dt_final)
    model.fit(x_train1, y_train1)  # training the model this could take a little time
    accuracy = model.score(x_test1, y_test1)  # comparing result with the test part set from

    data = {'Accuracy': [accuracy], 'Algorithm': ['DecisionTreeClassifier']}
    algorithm_output = pd.DataFrame(data)

    print("===============================")
    print("Training Accuracy Using Multi label:")
    print(algorithm_output)

    test = pd.read_csv("CsvFiles/SmallTest.csv")
    test_classifier(model, test)


if __name__ == "__main__":
    main()