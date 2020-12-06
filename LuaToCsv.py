from scapy.all import *
import binascii
import pandas as pd

PCAP_NAME = "PcapFiles/fixed.pcap"
LUA_NAME = "LuaFiles/descriptor.lua"
FILE_OPEN_ERROR = "This file name does not exists"


class Server:

    def __init__(self):
        self.protocol_fields = {}

    def print_dict(self):
        for key, value in self.protocol_fields.items():
            print(key, ' : ', value)

    def read_lua(self):
        ret_val = False
        try:
            lua_f = open(LUA_NAME, "rb")
            c_line = 0
            for line in lua_f:
                line_values = line.split()
                dict_list = [line_values[0].decode()]
                size = line_values[1].decode()
                if size == 'uint8':
                    dict_list.append(2)
                elif size == 'uint16':
                    dict_list.append(4)
                elif size == 'uint32':
                    dict_list.append(8)
                else:
                    continue
                self.protocol_fields[c_line] = dict_list
                c_line += 1
            self.print_dict()
            lua_f.close()
            ret_val = True
        except FileNotFoundError:
            print(FILE_OPEN_ERROR)
        return ret_val

    def convert_attributes_list(self):
        attr_list = []
        for i in self.protocol_fields.values():
            attr_list.append(i[0])
        return attr_list

    def parse_pcap(self):
        ret_val = False
        attr_list = self.convert_attributes_list()
        protocols_list = []
        try:
            pkt_list = rdpcap(PCAP_NAME)
            for pkt in pkt_list:
                if Raw in pkt:
                    packet_payload = pkt[Raw].load
                    protocol_description = self.check_pkt(packet_payload)
                    protocols_list.append(protocol_description)
                    packet_payload = binascii.hexlify(packet_payload)
                    packet_payload = packet_payload.decode()
            ret_val = True
        except FileNotFoundError:
            print(FILE_OPEN_ERROR)
        frame = pd.DataFrame(protocols_list,columns=attr_list)
        frame.to_csv("CsvFiles/Attributes.csv", index=False)
        print(frame)
        return ret_val

    def check_pkt(self, pkt):
        pkt = binascii.hexlify(pkt)
        pkt = pkt.decode()
        offset = 0
        protocol_list = []
        """header for all"""
        for i in range(len(self.protocol_fields.values())-2):
            attribute = pkt[offset:offset + self.protocol_fields[i][1]]
            protocol_list.append(attribute)
            offset += self.protocol_fields[i][1]
        p_type = int(protocol_list[0])
        """by message types"""
        if p_type == 1:
            protocol_list.append(pkt[offset:offset + self.protocol_fields[3][1]])
            protocol_list.append('0')
        elif p_type == 2:
            protocol_list.append('0')
            protocol_list.append(pkt[offset:offset + self.protocol_fields[4][1]])
        else:
            pass
        return protocol_list


def main():
    server = Server()
    ret_val = server.read_lua()
    if ret_val:
        ret_val = server.parse_pcap()


if __name__ == '__main__':
    main()
