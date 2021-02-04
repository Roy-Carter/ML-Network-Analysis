import pandas as pd

"""1000 packets
correct : 
type - 1/2
flag - 2-4
seq - 3-6
if request : req 101-103
if response : res 203,206 , check_it 2/3
"""
from random import randint

p_type_lst = []
flag_lst = []
seq_lst = []
req_lst = []
res_lst = []
check_it_lst = []
for i in range(1000):
    proto_type = randint(1, 2)
    flag = randint(2, 4)
    seq = randint(3, 6)
    p_type_lst.append(proto_type)
    flag_lst.append(flag)
    seq_lst.append(seq)

    if proto_type == 1:
        req = randint(101, 103)
        req_lst.append(req)
        res_lst.append(0)
        check_it_lst.append(0)

    elif proto_type == 2:
        res = randint(203, 206)
        res_lst.append(res)
        check_it = randint(2, 3)
        check_it_lst.append(check_it)
        req_lst.append(0)
    else:
        pass

details = {"p_type": p_type_lst, "flag": flag_lst, "seq": seq_lst, "my_data_req": req_lst,
           "my_data_res": res_lst, "check_it": check_it_lst, "num_class": [1 for i in range(1000)]}
frame = pd.DataFrame(details)

#INCORRECT DATA ADDITION
p_type_lst = []
flag_lst = []
seq_lst = []
req_lst = []
res_lst = []
check_it_lst = []
for i in range(1000):
    proto_type = randint(1, 2)
    flag = randint(2, 8)
    seq = randint(3, 11)
    p_type_lst.append(proto_type)
    flag_lst.append(flag)
    seq_lst.append(seq)

    if proto_type == 1:
        req = randint(101, 201)
        req_lst.append(req)
        res_lst.append(0)
        check_it_lst.append(0)

    elif proto_type == 2:
        res = randint(203, 233)
        res_lst.append(res)
        check_it = randint(2, 13)
        check_it_lst.append(check_it)
        req_lst.append(0)
    else:
        req_lst.append(0)
        res_lst.append(0)
        check_it_lst.append(0)


details1 = {"p_type": p_type_lst, "flag": flag_lst, "seq": seq_lst, "my_data_req": req_lst,
           "my_data_res": res_lst, "check_it": check_it_lst, "num_class": [0 for i in range(1000)]}
frame1 = pd.DataFrame(details1)


df_row = pd.concat([frame, frame1])
# shuffle the DataFrame rows
df_row = df_row.sample(frac=1)
print(df_row)
df_row.to_csv("CsvFiles/AlgoSmallTest.csv", index=False)