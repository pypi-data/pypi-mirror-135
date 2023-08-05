
from scapy.all import *
import pandas as pd
from IPython.core.display import update_display, display

import random


# Collect field names from IP/TCP/UDP (These will be columns in DF)
ip_fields = [field.name for field in IP().fields_desc]
tcp_fields = [field.name for field in TCP().fields_desc]
udp_fields = [field.name for field in UDP().fields_desc]
icmp_fields = [field.name for field in ICMP().fields_desc]

# TODO remove this method
def add_one(number):
    return number + 1


class CapCake():

    # todo implement limited display
    def __init__(self, columns):
        if not isinstance(columns, list):
            print("Columns should be a list") # todo use logger 
            raise TypeError("Columns should be list")
            
        self.columns = columns
        self.packets = pd.DataFrame(columns=columns)
        self.display_id = display(self.packets,display_id=True).display_id
        
    def _add_to_packets(self,pkt):
        column_values = dict()
        
        for column in self.columns:
            column_values[ column ] = None
           
        if 'time' in self.columns:
            column_values['time'] = packet.time
        
        # todo make a function for parsing ip part it
        for field in ip_fields:
            if field not in self.columns:
                continue
                
            field_value = pkt[IP].fields[field]
                
            if field == 'options':
                # Retrieving number of options defined in IP Header
                column_values[field] = len(field_value)
            elif field == 'proto':
                
                if(field_value== 17):
                    column_values['proto'] = 'udp'
                elif(field_value== 6):
                    column_values['proto'] = 'tcp'
                elif(field_value==1):
                    column_values['proto'] ='icmp'
                else :
                    column_values['proto'] = field_value
            else:
                column_values[field] = field_value 
        
        
        
        # todo make a function for parsing TCP part it
        layer_type = type(pkt[IP].payload)
        
        if layer_type == type(TCP()):            
            for field in tcp_fields:
                if field not in self.columns:
                    continue

                field_value = pkt[layer_type].fields[field]

                try:
                    if field == 'options':
    #                    column_values.append(len(packet[layer_type].fields[field]))
                        column_values['options'] = field_value[0]
                    elif field == 'seq':
                        # todo make seq number percision optional
                        column_values['seq'] = str(int(field_value)%10000)
                    elif field == 'ack':
                        column_values['ack'] = str(int(field_value)%10000)
                    else:
                        column_values[field] = field_value
                except Exception as e:
                    print ("exp message: "+ str(e))
                    column_values[field] = None
    
        if layer_type == type(ICMP()):
            for field in icmp_fields:
                if field not in self.columns:
                    continue

                field_value = pkt[layer_type].fields[field]

                try:
                    if field == 'options':
                        column_values['options'] = field_value[0]
                    elif field == 'code':
                        if field_value == 3 :
                            column_values['code'] = 'port-unreachable'
                        else :
                            column_values['code'] = field_value
                    elif field == 'type':
                        if field_value == 3 :
                            column_values['type'] = 'dest-unreach'
                        else :
                            column_values['type'] = field_value
                    else:
                        column_values[field] = field_value
                except Exception as e:
                    print ("exp message: "+ str(e))
                    column_values[field] = None
        
        print(column_values)
        
        self.packets = self.packets.append(column_values,ignore_index=True)
        
        
#         self.packets.loc[len(self.packets)] = [random.randint(0,1024),random.randint(0,1024), 'tcp']
        update_display(self.packets, display_id =self.display_id)
        
    # todo make it non-blocking
    def capture(self, iface, filter, count):

        pcap = sniff(iface=iface, filter=filter,count=count, prn=self._add_to_packets)
        
        return pcap
        

        
#         for field in icmp_fields:
#             try:
#                 if field == 'options':
#                     field_values.append(packet[layer_type].fields[field][0])
#                 elif field == 'code':
#                     if packet[layer_type].fields[field] == 3 :
#                         field_values.append('port-unreachable')
#                     else :
#                         field_values.append(packet[layer_type].fields[field])
#                 elif field == 'type':
#                     if packet[layer_type].fields[field] == 3 :
#                         field_values.append('dest-unreach')
#                     else :
#                         field_values.append(packet[layer_type].fields[field])
#                 else:
#                     field_values.append(packet[layer_type].fields[field])
#             except:
#                 field_values.append(None)
    
#         # Append payload
#         field_values.append(len(packet[layer_type].payload))
#         field_values.append(packet[layer_type].payload.original)
#         field_values.append(binascii.hexlify(packet[layer_type].payload.original))
#         # Add row to DF
#         df_append = pd.DataFrame([field_values], columns=dataframe_fields)
#         df = pd.concat([df, df_append], axis=0)
#     # Reset Index
#     df = df.reset_index()
#     # Drop old index column
#     df = df.drop(columns="index")
#     return df
