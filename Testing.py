# test file
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


def add_counter_label(frame):
    """
    Adds the ID column to the panda frame
    :param frame: a panda frame
    :return: a fixed panda frame with an additional id column
    """
    frame_len = len(frame)
    frame = frame.assign(ID=np.arange(0, frame_len))
    return frame


class ResultsDPI:

    def __init__(self):
        self.df_smalltrain = pd.read_csv("CsvFiles/AlgoTest.csv")
        self.df_stest = pd.read_csv("CsvFiles/AlgoSmallTest.csv")
        self.df_results = pd.read_csv("CsvFiles/Results.csv")
        self.min_max = []

    def stage2(self):
        """ STAGE 2 - MIN <-> MAX [[min,max],[min,max]....,[min,max]] """
        grouped = self.df_smalltrain.groupby('num_class')
        normal = grouped.get_group(1)  # normal
        normal_max_list = list(normal.max())
        normal_min_list = list(normal[normal > 0].min())
        normal_min_list = list(map(int, normal_min_list))
        self.min_max = map(list, zip(normal_min_list, normal_max_list))
        print("=======================================")
        print("STAGE 2")
        self.min_max = list(self.min_max)
        print(self.min_max)

    def stage3(self):
        """ STAGE 3 - adding ID column to the test and result panda frames """
        self.df_stest = add_counter_label(self.df_stest)
        self.df_results = add_counter_label(self.df_results)
        print("=======================================")
        print("STAGE 3")
        print(self.df_stest)
        print(self.df_results)

    def stage4(self):
        """
        Stage 4 - DPI , compare between the two lists ID and check if each field is between
        the min and max of each attribute
        (taking anomaly from results (anomaly = 0))
        """
        print("=======================================")
        print("STAGE 4")
        self.df_stest = self.df_stest[self.df_stest.num_class != 1]
        # merges the prediction with their values
        check_pd = pd.merge(self.df_stest, self.df_results, on='ID')
        check_pd_fix = check_pd.drop(["num_class_x", "num_class_y", "p_type_y", "ID"], axis=1)
        check_pd_fix.to_csv("CsvFiles/Check.csv")
        print(self.min_max)
        columns = check_pd_fix.columns.tolist()
        for index, row in check_pd_fix.iterrows():
            lst = row.tolist()
            print(lst)
            for i in range(len(self.min_max) - 1):  # -1 so it won't run on the class
                if lst[i] != 0:
                    if lst[i] < self.min_max[i][0]:
                        print(f"Lower than {self.min_max[i][0]} in {columns[i]}")
                    elif lst[i] > self.min_max[i][1]:
                        print(f"Higher than {self.min_max[i][1]} in {columns[i]}")

    def initialize(self):
        self.stage2()
        self.stage3()
        self.stage4()


def main():
    dpi = ResultsDPI()
    dpi.initialize()


if __name__ == "__main__":
    main()






