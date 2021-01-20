from scapy.all import *
import binascii
import pandas as pd

PCAP_NAME = "PcapFiles/test.pcap"
LUA_NAME = "LuaFiles/descriptor.lua"
FILE_OPEN_ERROR = "This file name does not exists"


class Server:

    def __init__(self):
        self.protocol_fields = {}
        self.protocol_types_fields = {}
        self.opcode_list = []

    def print_dict(self, val):
        for key, value in val.items():
            print(key, ' : ', value)

    def create_msg_types(self):
        """
        This function creates a dictionary of list , which each key stands for a specific opcode and the list
        within it , holds all the parameters that are part of that specific message .
        :return: None.
        """
        self.protocol_types_fields = {self.opcode_list[k]: [] for k in range(len(self.opcode_list))}
        for i in range(len(self.protocol_fields)):
            opcode = self.protocol_fields[i][2]
            self.protocol_types_fields[opcode].append(self.protocol_fields[i][0])
        self.print_dict(self.protocol_types_fields)



    def read_lua(self):
        """
        Creates a dictionary of lists where the number of line is the key and the [<fieldname>,<size>] is the value
        :return: returns True if the file was opened correctly and the dictionary was created , False otherwise.
        """
        ret_val = False
        try:
            lua_f = open(LUA_NAME, "rb")
            c_line = 0
            for line in lua_f:
                line_values = line.split()
                dict_list = [line_values[0].decode()]
                size = line_values[1].decode()
                opcode = int(line_values[2].decode())
                if opcode not in self.opcode_list:
                    self.opcode_list.append(opcode)
                if size == 'uint8':
                    dict_list.append(2)
                elif size == 'uint16':
                    dict_list.append(4)
                elif size == 'uint24':
                    dict_list.append(6)
                elif size == 'uint32':
                    dict_list.append(8)
                else:
                    continue
                dict_list.append(opcode)
                self.protocol_fields[c_line] = dict_list
                c_line += 1
            self.print_dict(self.protocol_fields)
            print("======================================")
            self.create_msg_types()
            lua_f.close()
            ret_val = True
            #print(self.opcode_list)
        except FileNotFoundError:
            print(FILE_OPEN_ERROR)
        return ret_val

    def convert_attributes_list(self):
        """
        Creates a list for the attributes name (the protocol fields)
        :return: the attributes list
        """
        attr_list = []
        for i in self.protocol_fields.values():
            attr_list.append(i[0])
        return attr_list

    def create_csv(self, packet_payload, protocols_list, attr_list):
        protocol_description = self.check_pkt(packet_payload)
        protocols_list.append(list(protocol_description.values()))
        frame = pd.DataFrame(protocols_list, columns=attr_list)
        frame.to_csv("CsvFiles/Attributes.csv", index=False)
        print(frame)

    def parse_pcap(self):
        """
        Parsing the pcap to a csv file.
        :return: return True if the file was parsed into csv , otherwise returns false.
        """
        ret_val = False
        attr_list = self.convert_attributes_list()
        protocols_list = []
        try:
            pkt_list = rdpcap(PCAP_NAME)
            for pkt in pkt_list:
                if Raw in pkt:
                    packet_payload = pkt[Raw].load
                    self.create_csv(packet_payload, protocols_list, attr_list)
            ret_val = True
        except FileNotFoundError:
            print(FILE_OPEN_ERROR)
        return ret_val

    def initialize_proto_dict(self):
        """
        This function creates an intizialize dictionary to use for the csv file where the key will be an attribute of the
        protocol and the initialized value to him will be zero.
        :return: returns a dictionary {<attr_list>..,<0>}
        """
        basic_list = []
        for i in range(len(self.protocol_types_fields)):
            basic_list = basic_list + self.protocol_types_fields[i]

        zeros = ['0' for i in range(len(self.protocol_fields))]
        basic_dict = dict(zip(basic_list, zeros))
        return basic_dict

    def handle_msg_types(self, pkt, id, offset, protocol_list, dict_index, basic_dict):
        if id in self.protocol_types_fields.keys():
            for field_name in self.protocol_types_fields[id]:
                val = pkt[offset:offset + self.protocol_fields[dict_index][1]]
                basic_dict[field_name] = val
                semi_list = [field_name, val]
                protocol_list.append(semi_list)
                offset += self.protocol_fields[dict_index][1]
        return basic_dict

    def check_pkt(self, pkt):
        """
        Checks each packet of the pcap file and creates a list of its data split to fields.
        :param pkt: a packet from the pcap file
        :return: returns a a list with the packet data for the protocol
        """
        basic_dict = self.initialize_proto_dict()
        pkt = binascii.hexlify(pkt)
        pkt = pkt.decode()
        offset = 0
        print("======================================")
        protocol_list = []
        val_type = int(pkt[offset:offset + self.protocol_fields[0][1]])
        for i in range(len(self.protocol_fields)):
            op_code = self.protocol_fields[i][2]
            val = pkt[offset:offset + self.protocol_fields[i][1]]
            if op_code != 0:
                basic_dict = self.handle_msg_types(pkt, val_type, offset, protocol_list, i,basic_dict)
                break
            else:
                p_type = self.protocol_fields[i][0]
                basic_dict[p_type] = val
                semi_list = [self.protocol_fields[i][0], val]
                protocol_list.append(semi_list)
            offset += self.protocol_fields[i][1]
        return basic_dict


def main():
    server = Server()
    ret_val = server.read_lua()
    if ret_val:
        ret_val = server.parse_pcap()


if __name__ == '__main__':
    main()
