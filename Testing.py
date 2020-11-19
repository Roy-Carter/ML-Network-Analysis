#Test file
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def encode(df):
    """
    A function to encode every column I need so it will be a computer readable value (numbers).
    :param df:the current data frame we are looking at
    :return: an array of the category listed in its continuous values
    """
    encoder = LabelEncoder()
    target = encoder.fit_transform(df)
    return np.array(target)


def edit_frame(frame):
    """
    edits the panda frame so it'll only have continuous values and no string values (readable computer values)
    :param frame: a panda frame
    :return: a fixed panda frame with no continuous values
    """
    num_class = encode(frame['class'])
    frame['num_class'] = num_class

    num_proto = encode(frame['protocol_type'])
    frame['num_proto'] = num_proto

    service_num = encode(frame['service'])
    frame['service_num'] = service_num

    flag_num = encode(frame['flag'])
    frame['flag_num'] = flag_num

    frame = frame.drop(['class', 'protocol_type', 'service', 'flag'], axis=1)
    return frame


def add_counter_label(frame):
    """
    Adds the ID column to the panda frame
    :param frame: a panda frame
    :return: a fixed panda frame with an additional id column
    """
    frame_len = len(frame)
    frame = frame.assign(ID=np.arange(0, frame_len))
    return frame

""" STAGE 2 - MIN <-> MAX [[min,max],[min,max]....,[min,max]] """

df_smalltrain = pd.read_csv("CsvFiles/SmallTrain.csv")
df_smalltrain = edit_frame(df_smalltrain)
grouped = df_smalltrain.groupby('num_class')
normal = grouped.get_group(1)

normal_max_list = list(normal.max())
normal_min_list = list(normal.min())
min_max = map(list, zip(normal_min_list, normal_max_list))
print("=======================================")
print("STAGE 2")
print(list(min_max))

""" STAGE 3 - adding ID column to the test and result panda frames """
df_stest = pd.read_csv("CsvFiles/SmallTest.csv")
df_stest = edit_frame(df_stest)
df_stest = add_counter_label(df_stest)

df_results = pd.read_csv("CsvFiles/Results.csv")
df_results = add_counter_label(df_results)
print("=======================================")
print("STAGE 3")
print(df_stest)
print(df_results)

"""
Stage 4 - DPI , compare between the two lists ID and check if each field is between
the min and max of each attribute
(taking anomaly from results (anomaly = 0))
"""
df_results =df_results.groupby('Class')
results_anomaly = df_results.get_group(0)

print("=======================================")
print("STAGE 4")
print(results_anomaly)



