import json
import os
import sys
import yaml
import sth
import time
from pprint import pprint
# file_path =  os.path.pardir()
# print file_path
# file_path =  os.path.dirname(os.path.basename(__file__))
file_path = os.path.dirname(os.path.realpath(__file__))
def spi2():
    data = yaml.load(open('Spirent_Test_Topology.yaml'), Loader=yaml.Loader)
    
##    with open( file_path + '\..\Topology\Spirent_Test_Topology.yaml') as data_file:
##        data = yaml.load(data_file,Loader=yaml.FullLoader)
    interface_config = data['sth_interface_config']
    Booked_ports = data['Spirent_Port_Booking']
    Stream_config = data['Spirent_stream_config']
    Spirent_Test_Infra = data['Spirent_Test_Infrastructure']
    return (Booked_ports, interface_config, Stream_config, Spirent_Test_Infra)

Booked_ports, Interface_config, Stream_config, Spirent_Test_Infra = spi2()

test_sta = sth.test_config (
		log                                              = '1',
		logfile                                          = 'SteamConfig-WithPercentageTraffic_logfile',
		vendorlogfile                                    = 'SteamConfig-WithPercentageTraffic_stcExport',
		vendorlog                                        = '1',
		hltlog                                           = '1',
		hltlogfile                                       = 'SteamConfig-WithPercentageTraffic_hltExport',
		hlt2stcmappingfile                               = 'SteamConfig-WithPercentageTraffic_hlt2StcMapping',
		hlt2stcmapping                                   = '1',
		log_level                                        = '7');
Number_of_ports = Spirent_Test_Infra['Number_of_ports']
status = test_sta['status']
if (status == '0') :
	print("run sth.test_config failed")
	print(test_sta)
##############################################################
#config the parameters for optimization and parsing
##############################################################

test_ctrl_sta = sth.test_control (
		action                                           = 'enable');

status = test_ctrl_sta['status']
if (status == '0') :
	print("run sth.test_control failed")
	print(test_ctrl_sta)
##############################################################
#connect to chassis and reserve port list
##############################################################
i = 0
device = "10.91.113.124"
port_list = list(Booked_ports.values())
port_handle = []
intStatus = sth.connect (
		device                                           = device,
		port_list                                        = port_list,
		break_locks                                      = 1,
		offline                                          = 0 )

status = intStatus['status']

if (status == '1') :
	for port in port_list :
		port_handle.append(intStatus['port_handle'][device][port])
		i += 1
else :
	print("\nFailed to retrieve port handle!\n")
	print(port_handle)

##############################################################
#interface config
##############################################################

Interface_config['port_handle'] = port_handle[0]
int_ret0 = sth.interface_config (**Interface_config)
status = int_ret0['status']
if (status == '0') :
	print("run sth.interface_config failed")
	print(int_ret0)
Interface_config['port_handle'] = port_handle[1]
int_ret1 = sth.interface_config (**Interface_config)
status = int_ret1['status']
if (status == '0') :
	print("run sth.interface_config failed")
	print(int_ret0)
##############################################################
#stream config
##############################################################
Stream_config['port_handle'] = port_handle[0]
Stream_config['dest_port_list'] = port_handle[1]
Stream_config['name'] =  'Stream From 9-3 to 9-4'
streamblock_ret1 = sth.traffic_config(**Stream_config)
status = streamblock_ret1['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret1)
Stream_config['port_handle'] = port_handle[1]
Stream_config['dest_port_list'] = port_handle[0]
Stream_config['name'] =  'Stream From 9-4 to 9-3'
streamblock_ret1 = sth.traffic_config(**Stream_config)
status = streamblock_ret1['status']
if (status == '0') :
	print("run sth.traffic_config failed")
	print(streamblock_ret1)
#############################################################
#start traffic
##############################################################
print("Traffic Started")
traffic_ctrl_ret = sth.traffic_control (
		port_handle                                      = [port_handle[0],port_handle[1]],
		action                                           = 'run',
        duration                                         = '30');

status = traffic_ctrl_ret['status']
if (status == '0') :
	print("run sth.traffic_control failed")
	print(traffic_ctrl_ret)
print("Test Traffic Stopped now adding delay before collecting stats")
#time.sleep(1)
print("Traffic collection started")
##############################################################
#start to get the traffic results
##############################################################
traffic_results_ret = sth.traffic_stats (
		port_handle                                      = [port_handle[0],port_handle[1]],
		mode                                             = 'all');

status = traffic_results_ret['status']
if (status == '0') :
	print("run sth.traffic_stats failed")
	print(traffic_results_ret)
##############################################################
#Get required values from Stats
##############################################################
Streams_rx_stat = []
Streams_tx_stat = []
for i in range(1,Number_of_ports+1):
	Port_Index = 'port'+ str(i)
	Stream_Index = 'streamblock' + str(i)
	Streams_rx_stats = traffic_results_ret[Port_Index]['stream'][Stream_Index]['rx']
	Streams_tx_stats = traffic_results_ret[Port_Index]['stream'][Stream_Index]['tx']
	Streams_rx_stat.append(int(Streams_rx_stats['total_pkt_bytes']))
	Streams_tx_stat.append(int(Streams_tx_stats['total_pkt_bytes']))

if((Streams_tx_stat[0] == Streams_rx_stat[1]) and (Streams_tx_stat[1] == Streams_rx_stat[0])):
	print("Great Test Case is passed")
	print("streamblock1 TX = ", Streams_tx_stat[0], "streamblock1 RX = ", Streams_rx_stat[0], "streamblock2 TX = ",
		  Streams_tx_stat[1], "streamblock2 RX = ", Streams_rx_stat[1])
else:
	print("Oops Tst Case Failed")
	print("streamblock1 TX = ", Streams_tx_stat[0], "streamblock1 RX = ", Streams_rx_stat[0], "streamblock2 TX = ",
		  Streams_tx_stat[1], "streamblock2 RX = ", Streams_rx_stat[1])
	Stream1_packet_loss_in_msec = ((Streams_tx_stat[0] - Streams_rx_stat[1]) / 1000)
	Stream2_packet_loss_in_msec = ((Streams_tx_stat[1] - Streams_rx_stat[0]) / 1000)


