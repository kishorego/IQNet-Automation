
##############################################################
#Loading HLTAPI for Python
##############################################################
from __future__ import print_function
import sth
import time
import json
import os
import sys
import yaml
import re
from pprint import pprint


# file_path =  os.path.pardir()
# print file_path
# file_path =  os.path.dirname(os.path.basename(__file__))
file_path = os.path.dirname(os.path.realpath(__file__))


def Get_Spirent_Config():
	data = yaml.load(open(file_path + '/../libraries/Spirent_Test_Topology.yaml'), Loader=yaml.Loader)

	# with open( file_path + 'Spirent_Test_Topology.yaml') as data_file:
	#     data = yaml.load(data_file,Loader=yaml.FullLoader)
	Spirent_Test_Topology = data['Spirent_Test_Topology']
	return (Spirent_Test_Topology)

def Spirent_VLAN_Transperancy_Traffic_Testing_For_P2P_Service():
	Spirent_Test_Infrastructure = Get_Spirent_Config()

	##############################################################
	# Creation of Spirent Test config with log file
	##############################################################

	test_sta = sth.test_config(
		log='1',
		logfile='SteamConfig-WithPercentageTraffic_logfile',
		vendorlogfile='SteamConfig-WithPercentageTraffic_stcExport',
		vendorlog='1',
		hltlog='1',
		hltlogfile='SteamConfig-WithPercentageTraffic_hltExport',
		hlt2stcmappingfile='SteamConfig-WithPercentageTraffic_hlt2StcMapping',
		hlt2stcmapping='1',
		log_level='7');

	status = test_sta['status']
	if (status == '0'):
		print("run sth.test_config failed")

	##############################################################
	# config the parameters for optimization and parsing
	##############################################################

	test_ctrl_sta = sth.test_control(
		action='enable');

	status = test_ctrl_sta['status']
	if (status == '0'):
		print("run sth.test_control failed")

	##############################################################
	# connect to chassis and reserve port list
	##############################################################
	i = 0
	port_handle = []
	device = Spirent_Test_Infrastructure['Spirent_Chassis_ip']
	port_list = list(Spirent_Test_Infrastructure['Port_Values'].values())
	port_speed = list(Spirent_Test_Infrastructure['Port_Speed'].values())
	port_mode = list(Spirent_Test_Infrastructure['Port_Phy_Mode'].values())
	intStatus = sth.connect(
			device=device,
			port_list=port_list,
			break_locks=1,
			offline=0)
	status = intStatus['status']
	if (status == '1'):
		for port in port_list:
			port_handle.append(intStatus['port_handle'][device][port])
			i += 1
	else:
		print("\nFailed to retrieve port handle!\n")
	#		print(self.port_handle)
	print("Printing Port Handle")
	print(port_handle)
	##############################################################
	# interface config
	##############################################################

	int_ret0 = sth.interface_config(
		mode='config',
		port_handle=port_handle[0],
		create_host='false',
		intf_mode='ethernet',
		phy_mode='copper',
		scheduling_mode='PRIORITY_BASED',
		port_loadunit='PERCENT_LINE_RATE',
		port_load='10',
		enable_ping_response='0',
		control_plane_mtu='1500',
		speed='ether1000',
		duplex='full',
		autonegotiation='1');

	status = int_ret0['status']
	if (status == '0'):
		print("run sth.interface_config failed")
		print(int_ret0)
	else:
		print("***** run sth.interface_config successfully")

	int_ret1 = sth.interface_config(
		mode='config',
		port_handle=port_handle[1],
		create_host='false',
		intf_mode='ethernet',
		phy_mode='copper',
		scheduling_mode='PRIORITY_BASED',
		port_loadunit='PERCENT_LINE_RATE',
		port_load='10',
		enable_ping_response='0',
		control_plane_mtu='1500',
		speed='ether1000',
		duplex='full',
		autonegotiation='1');

	status = int_ret1['status']
	if (status == '0'):
		print("run sth.interface_config failed")
		print(int_ret1)
	else:
		print("***** run sth.interface_config successfully")

	##############################################################
	# create device and config the protocol on it
	##############################################################

	# start to create the device: Device 1
	device_ret0 = sth.emulation_device_config(
		mode='create',
		ip_version='ipv4',
		encapsulation='ethernet_ii',
		port_handle=port_handle[1],
		router_id='192.0.39.8',
		count='1',
		enable_ping_response='0',
		mac_addr='00:10:94:00:00:13',
		mac_addr_step='00:00:00:00:00:01',
		intf_ip_addr='10.0.0.13',
		intf_prefix_len='24',
		resolve_gateway_mac='true',
		gateway_ip_addr='10.0.0.14',
		gateway_ip_addr_step='0.0.0.0',
		gateway_mac='00:10:94:00:00:14',
		intf_ip_addr_step='0.0.0.1');

	status = device_ret0['status']
	if (status == '0'):
		print("run sth.emulation_device_config failed")
		print(device_ret0)
	else:
		print("***** run sth.emulation_device_config successfully")

	# start to create the device: Device 2
	device_ret1 = sth.emulation_device_config(
		mode='create',
		ip_version='ipv4',
		encapsulation='ethernet_ii',
		port_handle=port_handle[0],
		router_id='192.0.39.9',
		count='1',
		enable_ping_response='0',
		mac_addr='00:10:94:00:00:14',
		mac_addr_step='00:00:00:00:00:01',
		intf_ip_addr='10.0.0.14',
		intf_prefix_len='24',
		resolve_gateway_mac='true',
		gateway_ip_addr='10.0.0.13',
		gateway_ip_addr_step='0.0.0.0',
		gateway_mac='00:10:94:00:00:13',
		intf_ip_addr_step='0.0.0.1');

	status = device_ret1['status']
	if (status == '0'):
		print("run sth.emulation_device_config failed")
		print(device_ret1)
	else:
		print("***** run sth.emulation_device_config successfully")

	##############################################################
	# create traffic
	##############################################################
	streamblock_ret2 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:02',
		enable_control_plane='0',
		l3_length='537',
		name='LACP_Stream_/Slow_Protocol',
		fill_type='prbs',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9275');

	status = streamblock_ret2['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret2)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret3 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='888E',
		mac_dst='01:80:C2:00:00:03',
		enable_control_plane='0',
		l3_length='537',
		name='Port_Authentication',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9164');
	streamblock_ret19 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:02',
		enable_control_plane='0',
		l3_length='537',
		name='LACP_Stream_/Slow_Protocol',
		fill_type='prbs',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret19['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret19)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret20 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='888E',
		mac_dst='01:80:C2:00:00:03',
		enable_control_plane='0',
		l3_length='537',
		name='Port_Authentication',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret20['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret20)
	else:
		print("***** run sth.traffic_config successfully")
	# config part is finished
	#############################################################
	# start traffic
	##############################################################
	print("Traffic Started First Time")
	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='run', duration='30');
	time.sleep(60)
	print("After Aging Timer")
	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='clear_stats');
	print("Delay before Second Traffic Started Second Time")
	time.sleep(60)
	print("Traffic Started Second Time")
	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='run',
		duration='10');
	status = traffic_ctrl_ret['status']
	if (status == '0'):
		print("run sth.traffic_control failed")
	# print(traffic_ctrl_ret)
	print("Test Traffic Stopped now adding delay before collecting stats")
	time.sleep(70)
	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='stop')
	print("***** traffic stopped")

	status = traffic_ctrl_ret['status']
	if (status == '0'):
		print("run sth.traffic_control failed")
		print(traffic_ctrl_ret)
	else:
		print("***** run sth.traffic_control successfully")

	print("Traffic collection started")
	##############################################################
	# start to get the traffic results
	##############################################################
	traffic_results_ret = sth.traffic_stats(
		port_handle=[port_handle[0], port_handle[1]],
		mode='all');
	print("Traffic collection stopped")
	status = traffic_results_ret['status']
	if (status == '0'):
		print("run sth.traffic_stats failed")
	pprint(traffic_results_ret)
	cleanup_sta = sth.cleanup_session(
		port_handle=[port_handle[0], port_handle[1]],
		clean_dbfile='1');
	print("Port Cleanedup")
	##############################################################
	# Get required values from Stats
	##############################################################

	traffic_result = str(traffic_results_ret)

	# regex to get rx, tx and streams from traffic_results_ret
	RX = '(streamblock\d+)\S+\s+\S+(rx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
	TX = '(streamblock\d+).*?(tx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'

	StreamBlock = 'streamblock\d+'

	print('Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list)))
	PortStatus = 'Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list))
	StreamBlock = re.findall(StreamBlock, traffic_result)
	print('Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock)))
	StreamStatus = 'Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock))
	rx_stats = re.findall(RX, traffic_result)
	tx_stats = re.findall(TX, traffic_result)

	print('rx_stats= ' + str(rx_stats))
	print('tx_stats= ' + str(tx_stats))

	stats = 'rx_stats= ' + str(rx_stats) + '\ntx_stats= ' + str(tx_stats)

	StreamResult = []

	for i in range(0, len(StreamBlock)):
		if rx_stats[i][2] == tx_stats[i][2]:
			print(str(rx_stats[i][0] + ' = pass'))
			StreamResult.append('pass')

		else:
			print(str(rx_stats[i][0] + ' = fail'))
			StreamResult.append('fail')

	print(str(StreamResult))

	OverallStatus = '\n' + PortStatus + '\n' + StreamStatus + '\n' + stats + '\n' + str(StreamResult)
	# print(OverallStatus)

	return OverallStatus

def Spirent_MAC_Transperancy_Traffic_Testing_For_P2P_Service():
	Spirent_Test_Infrastructure = Get_Spirent_Config()

	##############################################################
	# Creation of Spirent Test config with log file
	##############################################################

	test_sta = sth.test_config(
		log='1',
		logfile='SteamConfig-WithPercentageTraffic_logfile',
		vendorlogfile='SteamConfig-WithPercentageTraffic_stcExport',
		vendorlog='1',
		hltlog='1',
		hltlogfile='SteamConfig-WithPercentageTraffic_hltExport',
		hlt2stcmappingfile='SteamConfig-WithPercentageTraffic_hlt2StcMapping',
		hlt2stcmapping='1',
		log_level='7');

	status = test_sta['status']
	if (status == '0'):
		print("run sth.test_config failed")

	##############################################################
	# config the parameters for optimization and parsing
	##############################################################

	test_ctrl_sta = sth.test_control(
		action='enable');

	status = test_ctrl_sta['status']
	if (status == '0'):
		print("run sth.test_control failed")

	##############################################################
	# connect to chassis and reserve port list
	##############################################################
	i = 0
	port_handle = []
	device = Spirent_Test_Infrastructure['Spirent_Chassis_ip']
	port_list = list(Spirent_Test_Infrastructure['Port_Values'].values())
	port_speed = list(Spirent_Test_Infrastructure['Port_Speed'].values())
	port_mode = list(Spirent_Test_Infrastructure['Port_Phy_Mode'].values())
	intStatus = sth.connect(
		device=device,
		port_list=port_list,
		break_locks=1,
		offline=0)
	status = intStatus['status']
	if (status == '1'):
		for port in port_list:
			port_handle.append(intStatus['port_handle'][device][port])
			i += 1
	else:
		print("\nFailed to retrieve port handle!\n")
	#		print(self.port_handle)
	print("Printing Port Handle")
	print(port_handle)
	##############################################################
	# Spirent Ports configuration
	##############################################################
	for i in range(len(port_list)):
		int_ret0 = sth.interface_config(
			mode='config',
			port_handle=port_handle[i],
			create_host='false',
			intf_mode='ethernet',
			phy_mode='fiber',
			scheduling_mode='RATE_BASED',
			port_loadunit='PERCENT_LINE_RATE',
			port_load='50',
			enable_ping_response='0',
			control_plane_mtu='1500',
			flow_control='false',
			speed='ether1000',
			data_path_mode='normal',
			autonegotiation='0');
		status = int_ret0['status']
		if (status == '0'):
			print("run sth.interface_config failed")
	# print(int_ret0)
	##############################################################
	# create traffic
	##############################################################
	streamblock_ret1 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii_vlan',
		l3_protocol='ipv4',
		ip_id='0',
		ip_src_addr='192.85.1.2',
		ip_dst_addr='192.0.0.1',
		ip_ttl='255',
		ip_hdr_length='5',
		ip_protocol='253',
		ip_fragment_offset='0',
		ip_mbz='0',
		ip_precedence='0',
		ip_tos_field='0',
		vlan_id_repeat='0',
		vlan_id_mode='increment',
		vlan_id_count='4095',
		vlan_id_step='1',
        mac_dst_mode='random',
        mac_dst_repeat_count='0',
        mac_dst_count='1',
        mac_src_count='1',
        mac_src_mode='random',
        mac_src_repeat_count='0',
        mac_src='00:10:94:00:00:02',
        mac_dst='00:00:01:00:00:01',
		vlan_cfi='0',
		vlan_tpid='33024',
		vlan_id='1',
		vlan_user_priority='0',
		enable_control_plane='0',
		l3_length='4978',
		name='StreamBlock_11',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='1500',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		dest_port_list=port_handle[1],
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='6000',
		transmit_mode='multi_burst',
		inter_stream_gap='12',
		rate_mbps='800',
		mac_discovery_gw='192.85.1.1',
		enable_stream='false');

	status = streamblock_ret1['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret1)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret2 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii_vlan',
		l3_protocol='ipv4',
		ip_id='0',
		ip_src_addr='192.85.1.2',
		ip_dst_addr='192.0.0.1',
		ip_ttl='255',
		ip_hdr_length='5',
		ip_protocol='253',
		ip_fragment_offset='0',
		ip_mbz='0',
		ip_precedence='0',
		ip_tos_field='0',
		vlan_id_repeat='0',
		vlan_id_mode='increment',
		vlan_id_count='4095',
		vlan_id_step='1',
        mac_dst_mode='random',
        mac_dst_repeat_count='0',
        mac_dst_count='1',
        mac_src_count='1',
        mac_src_mode='random',
        mac_src_repeat_count='0',
        mac_src='00:10:94:00:00:02',
        mac_dst='00:00:01:00:00:01',
		vlan_cfi='0',
		vlan_tpid='33024',
		vlan_id='1',
		vlan_user_priority='0',
		enable_control_plane='0',
		l3_length='4978',
		name='StreamBlock_12',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='1500',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		dest_port_list=port_handle[0],
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='6000',
		transmit_mode='multi_burst',
		inter_stream_gap='12',
		rate_mbps='800',
		mac_discovery_gw='192.85.1.1',
		enable_stream='false');

	status = streamblock_ret2['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret2)
	else:
		print("***** run sth.traffic_config successfully")

	# config part is finished
	#############################################################
	# start traffic
	##############################################################
	print("Traffic Started First Time")
	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='run', duration='30');
	time.sleep(60)
	print("After Aging Timer")
	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='clear_stats');
	print("Delay before Second Traffic Started Second Time")
	time.sleep(60)
	print("Traffic Started Second Time")
	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='run',
		duration='10');
	status = traffic_ctrl_ret['status']
	if (status == '0'):
		print("run sth.traffic_control failed")
	# print(traffic_ctrl_ret)
	print("Test Traffic Stopped now adding delay before collecting stats")
	time.sleep(70)
	print("Traffic collection started")
	##############################################################
	# start to get the traffic results
	##############################################################
	traffic_results_ret = sth.traffic_stats(
		port_handle=[port_handle[0], port_handle[1]],
		mode='all');
	print("Traffic collection stopped")
	status = traffic_results_ret['status']
	if (status == '0'):
		print("run sth.traffic_stats failed")
	pprint(traffic_results_ret)
	cleanup_sta = sth.cleanup_session(
		port_handle=[port_handle[0], port_handle[1]],
		clean_dbfile='1');
	print("Port Cleanedup")
	##############################################################
	# Get required values from Stats
	##############################################################

	traffic_result = str(traffic_results_ret)

	# regex to get rx, tx and streams from traffic_results_ret
	RX = '(streamblock\d+)\S+\s+\S+(rx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
	TX = '(streamblock\d+).*?(tx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'

	StreamBlock = 'streamblock\d+'

	print('Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list)))
	PortStatus = 'Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list))
	StreamBlock = re.findall(StreamBlock, traffic_result)
	print('Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock)))
	StreamStatus = 'Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock))
	rx_stats = re.findall(RX, traffic_result)
	tx_stats = re.findall(TX, traffic_result)

	print('rx_stats= ' + str(rx_stats))
	print('tx_stats= ' + str(tx_stats))

	stats = 'rx_stats= ' + str(rx_stats) + '\ntx_stats= ' + str(tx_stats)

	StreamResult = []

	for i in range(0, len(StreamBlock)):
		if rx_stats[i][2] == tx_stats[i][2]:
			print(str(rx_stats[i][0] + ' = pass'))
			StreamResult.append('pass')

		else:
			print(str(rx_stats[i][0] + ' = fail'))
			StreamResult.append('fail')

	print(str(StreamResult))

	OverallStatus = '\n' + PortStatus + '\n' + StreamStatus + '\n' + stats + '\n' + str(StreamResult)
	# print(OverallStatus)

	return OverallStatus


def spi2():
	Spirent_Test_Infrastructure = Get_Spirent_Config()

	##############################################################
	# Creation of Spirent Test config with log file
	##############################################################

	test_sta = sth.test_config(
		log='1',
		logfile='SteamConfig-WithPercentageTraffic_logfile',
		vendorlogfile='SteamConfig-WithPercentageTraffic_stcExport',
		vendorlog='1',
		hltlog='1',
		hltlogfile='SteamConfig-WithPercentageTraffic_hltExport',
		hlt2stcmappingfile='SteamConfig-WithPercentageTraffic_hlt2StcMapping',
		hlt2stcmapping='1',
		log_level='7');

	status = test_sta['status']
	if (status == '0'):
		print("run sth.test_config failed")

	##############################################################
	# config the parameters for optimization and parsing
	##############################################################

	test_ctrl_sta = sth.test_control(
		action='enable');

	status = test_ctrl_sta['status']
	if (status == '0'):
		print("run sth.test_control failed")

	##############################################################
	# connect to chassis and reserve port list
	##############################################################
	i = 0
	port_handle = []
	device = Spirent_Test_Infrastructure['Spirent_Chassis_ip']
	port_list = list(Spirent_Test_Infrastructure['Port_Values'].values())
	port_speed = list(Spirent_Test_Infrastructure['Port_Speed'].values())
	port_mode = list(Spirent_Test_Infrastructure['Port_Phy_Mode'].values())
	intStatus = sth.connect(
		device=device,
		port_list=port_list,
		break_locks=1,
		offline=0)
	status = intStatus['status']
	if (status == '1'):
		for port in port_list:
			port_handle.append(intStatus['port_handle'][device][port])
			i += 1
	else:
		print("\nFailed to retrieve port handle!\n")
	#		print(self.port_handle)
	print("Printing Port Handle")
	print(port_handle)
	##############################################################
	# Spirent Ports configuration
	##############################################################
	for i in range(len(port_list)):
		int_ret0 = sth.interface_config(
			mode='config',
			port_handle=port_handle[i],
			create_host='false',
			intf_mode='ethernet',
			phy_mode='fiber',
			scheduling_mode='RATE_BASED',
			port_loadunit='PERCENT_LINE_RATE',
			port_load='50',
			enable_ping_response='0',
			control_plane_mtu='1500',
			flow_control='false',
			speed='ether1000',
			data_path_mode='normal',
			autonegotiation='0');
		status = int_ret0['status']
		if (status == '0'):
			print("run sth.interface_config failed")
	# print(int_ret0)
    ##############################################################
    #interface config
    ##############################################################
	for i in range(len(port_list)):
		int_ret0 = sth.interface_config(
		mode='config',
			port_handle=port_handle[i],
			create_host='false',
			intf_mode='ethernet',
			phy_mode='fiber',
			scheduling_mode='RATE_BASED',
			port_loadunit='PERCENT_LINE_RATE',
			port_load='50',
			enable_ping_response='0',
			control_plane_mtu='1500',
			flow_control='false',
			speed='ether1000',
			data_path_mode='normal',
			autonegotiation='0');
		status = int_ret0['status']
		if (status == '0'):
			print("run sth.interface_config failed")
	# print(int_ret0)
    ##############################################################
    #stream config
    ##############################################################
	streamblock_ret1 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii_vlan',
		l3_protocol='ipv4',
		ip_id='0',
		ip_src_addr='192.85.1.2',
		ip_dst_addr='192.0.0.1',
		ip_ttl='255',
		ip_hdr_length='5',
		ip_protocol='253',
		ip_fragment_offset='0',
		ip_mbz='0',
		ip_precedence='0',
		ip_tos_field='0',
		vlan_id_repeat='0',
		vlan_id_mode='increment',
		vlan_id_count='4095',
		vlan_id_step='1',
		mac_dst_mode='random',
		mac_dst_repeat_count='0',
		mac_dst_count='1',
		mac_src_count='1',
		mac_src_mode='random',
		mac_src_repeat_count='0',
		mac_src='00:10:94:00:00:02',
		mac_dst='00:00:01:00:00:01',
		vlan_cfi='0',
		vlan_tpid='33024',
		vlan_id='1',
		vlan_user_priority='0',
		enable_control_plane='0',
		l3_length='4978',
		name='StreamBlock_11',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='1500',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		dest_port_list=port_handle[1],
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='6000',
		transmit_mode='multi_burst',
		inter_stream_gap='12',
		rate_mbps='800',
		mac_discovery_gw='192.85.1.1',
		enable_stream='false');

	status = streamblock_ret1['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret1)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret2 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii_vlan',
		l3_protocol='ipv4',
		ip_id='0',
		ip_src_addr='192.85.1.2',
		ip_dst_addr='192.0.0.1',
		ip_ttl='255',
		ip_hdr_length='5',
		ip_protocol='253',
		ip_fragment_offset='0',
		ip_mbz='0',
		ip_precedence='0',
		ip_tos_field='0',
		vlan_id_repeat='0',
		vlan_id_mode='increment',
		vlan_id_count='4095',
		vlan_id_step='1',
		mac_dst_mode='random',
		mac_dst_repeat_count='0',
		mac_dst_count='1',
		mac_src_count='1',
		mac_src_mode='random',
		mac_src_repeat_count='0',
		mac_src='00:10:94:00:00:02',
		mac_dst='00:00:01:00:00:01',
		vlan_cfi='0',
		vlan_tpid='33024',
		vlan_id='1',
		vlan_user_priority='0',
		enable_control_plane='0',
		l3_length='4978',
		name='StreamBlock_12',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='1500',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		dest_port_list=port_handle[0],
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='6000',
		transmit_mode='multi_burst',
		inter_stream_gap='12',
		rate_mbps='800',
		mac_discovery_gw='192.85.1.1',
		enable_stream='false');

	status = streamblock_ret2['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret2)
	else:
		print("***** run sth.traffic_config successfully")

	# config part is finished
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
	time.sleep(10)
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
	result = SpirentResult(traffic_results_ret, port_list)
	return result


def L2_Traffic():

    ##############################################################
    #config the parameters for the logging
    ##############################################################

    test_sta = sth.test_config (
            log                                              = '1',
            logfile                                          = 'L2Service_logfile',
            vendorlogfile                                    = 'L2Service_stcExport',
            vendorlog                                        = '1',
            hltlog                                           = '1',
            hltlogfile                                       = 'L2Service_hltExport',
            hlt2stcmappingfile                               = 'L2Service_hlt2StcMapping',
            hlt2stcmapping                                   = '1',
            log_level                                        = '7');

    status = test_sta['status']
    if (status == '0') :
        print("run sth.test_config failed")
        print(test_sta)
    else:
        print("***** run sth.test_config successfully")


    ##############################################################
    #config the parameters for optimization and parsing
    ##############################################################

    test_ctrl_sta = sth.test_control (
            action                                           = 'enable');

    status = test_ctrl_sta['status']
    if (status == '0') :
        print("run sth.test_control failed")
        print(test_ctrl_sta)
    else:
        print("***** run sth.test_control successfully")


    ##############################################################
    #connect to chassis and reserve port list
    ##############################################################

    i = 0
    device = "10.91.113.124"
    port_list = ['11/10','11/6']
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
            print("\n reserved ports",port,":", port_handle[i])
            i += 1
    else :
        print("\nFailed to retrieve port handle!\n")
        print(port_handle)


    ##############################################################
    #interface config
    ##############################################################

    int_ret0 = sth.interface_config (
            mode                                             = 'config',
            port_handle                                      = port_handle[0],
            create_host                                      = 'false',
            intf_mode                                        = 'ethernet',
            phy_mode                                         = 'fiber',
            scheduling_mode                                  = 'RATE_BASED',
            port_loadunit                                    = 'PERCENT_LINE_RATE',
            port_load                                        = '10',
            enable_ping_response                             = '0',
            control_plane_mtu                                = '1500',
            flow_control                                     = 'false',
            speed                                            = 'ether1000',
            data_path_mode                                   = 'normal',
            autonegotiation                                  = '1');

    status = int_ret0['status']
    if (status == '0') :
        print("run sth.interface_config failed")
        print(int_ret0)
    else:
        print("***** run sth.interface_config successfully")

    int_ret1 = sth.interface_config (
            mode                                             = 'config',
            port_handle                                      = port_handle[1],
            create_host                                      = 'false',
            intf_mode                                        = 'ethernet',
            phy_mode                                         = 'fiber',
            scheduling_mode                                  = 'RATE_BASED',
            port_loadunit                                    = 'PERCENT_LINE_RATE',
            port_load                                        = '10',
            enable_ping_response                             = '0',
            control_plane_mtu                                = '1500',
            flow_control                                     = 'false',
            speed                                            = 'ether1000',
            data_path_mode                                   = 'normal',
            autonegotiation                                  = '1');

    status = int_ret1['status']
    if (status == '0') :
        print("run sth.interface_config failed")
        print(int_ret1)
    else:
        print("***** run sth.interface_config successfully")


    ##############################################################
    #create device and config the protocol on it
    ##############################################################

    #start to create the device: Device 1
    device_ret0 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii',
            port_handle                                      = port_handle[1],
            router_id                                        = '192.0.0.1',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:01',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '192.168.71.1',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '192.168.71.2',
            gateway_ip_addr_step                             = '0.0.0.0',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret0['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret0)
    else:
        print("***** run sth.emulation_device_config successfully")

    #start to create the device: Device 2
    device_ret1 = sth.emulation_device_config (
            mode                                             = 'create',
            ip_version                                       = 'ipv4',
            encapsulation                                    = 'ethernet_ii',
            port_handle                                      = port_handle[0],
            router_id                                        = '192.0.0.2',
            count                                            = '1',
            enable_ping_response                             = '1',
            mac_addr                                         = '00:10:94:00:00:02',
            mac_addr_step                                    = '00:00:00:00:00:01',
            intf_ip_addr                                     = '192.168.71.2',
            intf_prefix_len                                  = '24',
            resolve_gateway_mac                              = 'true',
            gateway_ip_addr                                  = '192.168.71.1',
            gateway_ip_addr_step                             = '0.0.0.0',
            intf_ip_addr_step                                = '0.0.0.1');

    status = device_ret1['status']
    if (status == '0') :
        print("run sth.emulation_device_config failed")
        print(device_ret1)
    else:
        print("***** run sth.emulation_device_config successfully")


    ##############################################################
    #create traffic
    ##############################################################

    streamblock_ret1 = sth.traffic_config (
            mode                                             = 'create',
            port_handle                                      = port_handle[0],
            l3_protocol                                      = 'ipv4',
            ip_id                                            = '0',
            ip_ttl                                           = '255',
            ip_hdr_length                                    = '5',
            ip_protocol                                      = '253',
            ip_fragment_offset                               = '0',
            ip_mbz                                           = '0',
            ip_precedence                                    = '6',
            ip_tos_field                                     = '0',
            enable_control_plane                             = '0',
            l3_length                                        = '1500',
            name                                             = 'StreamBlock_1-3',
            fill_type                                        = 'constant',
            fcs_error                                        = '0',
            fill_value                                       = '0',
            frame_size                                       = '1500',
            traffic_state                                    = '1',
            high_speed_result_analysis                       = '1',
            length_mode                                      = 'fixed',
            dest_port_list                                   = ['port1','port2'],
            tx_port_sending_traffic_to_self_en               = 'false',
            disable_signature                                = '0',
            enable_stream_only_gen                           = '1',
            pkts_per_burst                                   = '1',
            inter_stream_gap_unit                            = 'bytes',
            inter_stream_gap                                 = '12',
            rate_mbps                                        = '100',
            mac_discovery_gw                                 = '192.168.71.1');

    status = streamblock_ret1['status']
    if (status == '0') :
        print("run sth.traffic_config failed")
        print(streamblock_ret1)
    else:
        print("***** run sth.traffic_config successfully")

    src_hdl = device_ret0['handle'].split()[0]

    dst_hdl = device_ret1['handle'].split()[0]


    streamblock_ret2 = sth.traffic_config (
            mode                                             = 'create',
            port_handle                                      = port_handle[1],
            emulation_src_handle                             = src_hdl,
            emulation_dst_handle                             = dst_hdl,
            l3_protocol                                      = 'ipv4',
            ip_id                                            = '0',
            ip_ttl                                           = '255',
            ip_hdr_length                                    = '5',
            ip_protocol                                      = '253',
            ip_fragment_offset                               = '0',
            ip_mbz                                           = '0',
            ip_precedence                                    = '6',
            ip_tos_field                                     = '0',
            enable_control_plane                             = '0',
            l3_length                                        = '1500',
            name                                             = 'StreamBlock_1-4',
            fill_type                                        = 'constant',
            fcs_error                                        = '0',
            fill_value                                       = '0',
            frame_size                                       = '1500',
            traffic_state                                    = '1',
            high_speed_result_analysis                       = '1',
            length_mode                                      = 'fixed',
            dest_port_list                                   = ['port1','port2'],
            tx_port_sending_traffic_to_self_en               = 'false',
            disable_signature                                = '0',
            enable_stream_only_gen                           = '1',
            pkts_per_burst                                   = '1',
            inter_stream_gap_unit                            = 'bytes',
            inter_stream_gap                                 = '12',
            rate_mbps                                        = '100',
            mac_discovery_gw                                 = '192.168.71.2');

    status = streamblock_ret2['status']
    if (status == '0') :
        print("run sth.traffic_config failed")
        print(streamblock_ret2)
    else:
        print("***** run sth.traffic_config successfully")

    #config part is finished

    ##############################################################
    #start devices
    ##############################################################



    ##############################################################
    #start traffic
    ##############################################################

    traffic_ctrl_ret = sth.traffic_control (
            port_handle                                      = [port_handle[0],port_handle[1]],
            action                                           = 'run',
            duration                                         = '30');

    status = traffic_ctrl_ret['status']
    if (status == '0') :
        print("run sth.traffic_control failed")
        print(traffic_ctrl_ret)
    else:
        print("***** run sth.traffic_control successfully")


    ##############################################################
    #start to get the device results
    ##############################################################
    time.sleep(30)

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
    else:
        print("***** run sth.traffic_stats successfully, and results is:")
        print(traffic_results_ret)


    ##############################################################
    #clean up the session, release the ports reserved and cleanup the dbfile
    ##############################################################

    cleanup_sta = sth.cleanup_session (
            port_handle                                      = [port_handle[0],port_handle[1]],
            clean_dbfile                                     = '1');

    status = cleanup_sta['status']
    if (status == '0') :
        print("run sth.cleanup_session failed")
        print(cleanup_sta)
    else:
        print("***** run sth.cleanup_session successfully")


    print("**************Finish***************")

    result = SpirentResult(traffic_results_ret, port_list)
    return result

def SpirentResult(traffic_results_ret, port_list):

    ##############################################################
    #Get required values from Stats
    ##############################################################

    traffic_result = str(traffic_results_ret)

    #regex to get rx, tx and streams from traffic_results_ret
    RX = '(streamblock\d+)\S+\s+\S+(rx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
    TX = '(streamblock\d+).*?(tx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
    StreamBlock = 'streamblock\d+'


    print('Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list)))
    PortStatus = 'Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list))

    StreamBlock = re.findall(StreamBlock, traffic_result)
    print('Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock)))
    StreamStatus = 'Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock))

    rx_stats = re.findall(RX, traffic_result)
    tx_stats = re.findall(TX, traffic_result)

    print('rx_stats= ' + str(rx_stats))
    print('tx_stats= ' + str(tx_stats))

    stats = 'rx_stats= ' + str(rx_stats) + '\ntx_stats= ' + str(tx_stats)

    StreamResult = []

    for i in range(0,len(StreamBlock)):
        if rx_stats[i][2] == tx_stats[i][2]:
            print(str(rx_stats[i][0] + ' = pass'))
            StreamResult.append('pass')

        else:
            print(str(rx_stats[i][0] + ' = fail'))
            StreamResult.append('fail')

    print(str(StreamResult))

    OverallStatus = '\n' + PortStatus + '\n' + StreamStatus + '\n' + stats + '\n' + str(StreamResult)
    print(OverallStatus)

    return OverallStatus

def Spirent_L2CP_Transperancy_Traffic_Testing_For_P2P_Service():
	Spirent_Test_Infrastructure = Get_Spirent_Config()

	##############################################################
	# Creation of Spirent Test config with log file
	##############################################################

	test_sta = sth.test_config(
		log='1',
		logfile='SteamConfig-WithPercentageTraffic_logfile',
		vendorlogfile='SteamConfig-WithPercentageTraffic_stcExport',
		vendorlog='1',
		hltlog='1',
		hltlogfile='SteamConfig-WithPercentageTraffic_hltExport',
		hlt2stcmappingfile='SteamConfig-WithPercentageTraffic_hlt2StcMapping',
		hlt2stcmapping='1',
		log_level='7');

	status = test_sta['status']
	if (status == '0'):
		print("run sth.test_config failed")

	##############################################################
	# config the parameters for optimization and parsing
	##############################################################

	test_ctrl_sta = sth.test_control(
		action='enable');

	status = test_ctrl_sta['status']
	if (status == '0'):
		print("run sth.test_control failed")

	##############################################################
	# connect to chassis and reserve port list
	##############################################################
	i = 0
	port_handle = []
	device = Spirent_Test_Infrastructure['Spirent_Chassis_ip']
	port_list = list(Spirent_Test_Infrastructure['Port_Values'].values())
	port_speed = list(Spirent_Test_Infrastructure['Port_Speed'].values())
	port_mode = list(Spirent_Test_Infrastructure['Port_Phy_Mode'].values())
	intStatus = sth.connect(
		device=device,
		port_list=port_list,
		break_locks=1,
		offline=0)
	status = intStatus['status']
	if (status == '1'):
		for port in port_list:
			port_handle.append(intStatus['port_handle'][device][port])
			i += 1
	else:
		print("\nFailed to retrieve port handle!\n")
	#		print(self.port_handle)
	print("Printing Port Handle")
	print(port_handle)
	##############################################################
	# Spirent Ports configuration
	##############################################################
	for i in range(len(port_list)):
		int_ret0 = sth.interface_config(
			mode='config',
			port_handle=port_handle[i],
			create_host='false',
			intf_mode='ethernet',
			phy_mode='fiber',
			scheduling_mode='RATE_BASED',
			port_loadunit='PERCENT_LINE_RATE',
			port_load='50',
			enable_ping_response='0',
			control_plane_mtu='1500',
			flow_control='false',
			speed='ether1000',
			data_path_mode='normal',
			autonegotiation='0');
		status = int_ret0['status']
		if (status == '0'):
			print("run sth.interface_config failed")
	# print(int_ret0)
	##############################################################
	# create device and config the protocol on it
	##############################################################

	# start to create the device: Device 1
	device_ret0 = sth.emulation_device_config(
		mode='create',
		ip_version='ipv4',
		encapsulation='ethernet_ii',
		port_handle=port_handle[1],
		router_id='192.0.39.8',
		count='1',
		enable_ping_response='0',
		mac_addr='00:10:94:00:00:13',
		mac_addr_step='00:00:00:00:00:01',
		intf_ip_addr='10.0.0.13',
		intf_prefix_len='24',
		resolve_gateway_mac='true',
		gateway_ip_addr='10.0.0.14',
		gateway_ip_addr_step='0.0.0.0',
		gateway_mac='00:10:94:00:00:14',
		intf_ip_addr_step='0.0.0.1');

	status = device_ret0['status']
	if (status == '0'):
		print("run sth.emulation_device_config failed")
		print(device_ret0)
	else:
		print("***** run sth.emulation_device_config successfully")

	# start to create the device: Device 2
	device_ret1 = sth.emulation_device_config(
		mode='create',
		ip_version='ipv4',
		encapsulation='ethernet_ii',
		port_handle=port_handle[0],
		router_id='192.0.39.9',
		count='1',
		enable_ping_response='0',
		mac_addr='00:10:94:00:00:14',
		mac_addr_step='00:00:00:00:00:01',
		intf_ip_addr='10.0.0.14',
		intf_prefix_len='24',
		resolve_gateway_mac='true',
		gateway_ip_addr='10.0.0.13',
		gateway_ip_addr_step='0.0.0.0',
		gateway_mac='00:10:94:00:00:13',
		intf_ip_addr_step='0.0.0.1');

	status = device_ret1['status']
	if (status == '0'):
		print("run sth.emulation_device_config failed")
		print(device_ret1)
	else:
		print("***** run sth.emulation_device_config successfully")

	##############################################################
	# create traffic
	##############################################################

	streamblock_ret1 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:02',
		enable_control_plane='0',
		l3_length='537',
		name='LACP_Stream_/Slow_Protocol',
		fill_type='prbs',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9275');

	status = streamblock_ret1['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret1)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret2 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='888E',
		mac_dst='01:80:C2:00:00:03',
		enable_control_plane='0',
		l3_length='537',
		name='Port_Authentication',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9164');

	status = streamblock_ret2['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret2)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret3 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='88EE',
		mac_dst='01:80:C2:00:00:07',
		enable_control_plane='0',
		l3_length='537',
		name='E-LMI',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9148');

	status = streamblock_ret3['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret3)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret4 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:0E',
		enable_control_plane='0',
		l3_length='982',
		name='LLDP',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='1000',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9199');

	status = streamblock_ret4['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret4)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret5 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_dst_mode='increment',
		mac_dst_repeat_count='0',
		mac_dst_count='16',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:20',
		enable_control_plane='0',
		l3_length='537',
		name='GARP/GMRP_StreamBlock',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9147',
		enable_stream='false');

	status = streamblock_ret5['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret5)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret6 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:02',
		enable_control_plane='0',
		l3_length='138',
		name='LACP_MARKER',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='156',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9203');

	status = streamblock_ret6['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret6)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret7 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		enable_control_plane='0',
		l3_length='128',
		name='Link_OAM',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret7['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret7)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret8 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_8023_snap',
		custom_pattern='ABCDEFABCDEF',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:00:0C:CC:CC:CC',
		llc_control='03',
		llc_ssap='AA',
		llc_dsap='AA',
		snap_oui_id='00000C',
		snap_ether_type='2000',
		enable_control_plane='0',
		l3_length='555',
		name='Cisco_CDP_VTP',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9116');

	status = streamblock_ret8['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret8)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret9 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='0802',
		mac_dst='01:00:0C:CC:CC:CC',
		enable_control_plane='0',
		l3_length='110',
		name='Cicso_Shared_STP_',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9223');

	status = streamblock_ret9['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret9)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret10 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		l3_protocol='ipv4',
		l4_protocol='igmp',
		igmp_max_response_time='0',
		igmp_version='2',
		igmp_type='16',
		igmp_msg_type='report',
		igmp_group_addr='225.0.0.1',
		ip_id='0',
		ip_src_addr='192.85.1.2',
		ip_dst_addr='224.0.0.1',
		ip_ttl='255',
		ip_hdr_length='5',
		ip_protocol='2',
		ip_fragment_offset='0',
		ip_mbz='0',
		ip_precedence='0',
		ip_tos_field='0',
		mac_src='00:10:94:00:00:02',
		ether_type='0800',
		mac_dst='01:00:5E:00:00:01',
		enable_control_plane='0',
		l3_length='110',
		name='IPV4_IGMP_multicast',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100',
		mac_discovery_gw='192.85.1.1');

	status = streamblock_ret10['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret10)
	else:
		print("***** run sth.traffic_config successfully")
	streamblock_ret11 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		custom_pattern='ABCDEFABCDEF',
		mac_src='00:10:94:00:00:02',
		ether_type='0000',
		mac_dst='01:00:0C:00:00:01',
		enable_control_plane='0',
		l3_length='110',
		name='Cisco_Inter_Switch_Protocol_(ISL)',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret11['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret11)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret12 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='8902',
		mac_dst='01:80:C2:00:00:35',
		enable_control_plane='0',
		l3_length='537',
		name='SOAM_CCM_Level_5',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9116');

	status = streamblock_ret12['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret12)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret13 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:0E',
		enable_control_plane='0',
		l3_length='110',
		name='PTP_Delay_Request',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret13['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret13)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret14 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_dst_mode='increment',
		mac_dst_repeat_count='0',
		mac_dst_count='16',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:00',
		enable_control_plane='0',
		l3_length='110',
		name='L2CP_MAC_Frame',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100',
		enable_stream='false');

	status = streamblock_ret14['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret14)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret15 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:DD',
		enable_control_plane='0',
		l3_length='110',
		name='Provider_Bridge_MVRP_Address',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret15['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret15)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret16 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:02',
		enable_control_plane='0',
		l3_length='537',
		name='LACP_Stream_/Slow_Protocol',
		fill_type='prbs',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret16['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret16)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret17 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='888E',
		mac_dst='01:80:C2:00:00:03',
		enable_control_plane='0',
		l3_length='537',
		name='Port_Authentication',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret17['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret17)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret18 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='88EE',
		mac_dst='01:80:C2:00:00:07',
		enable_control_plane='0',
		l3_length='537',
		name='E-LMI',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret18['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret18)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret19 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:0E',
		enable_control_plane='0',
		l3_length='982',
		name='LLDP',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='1000',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9109');

	status = streamblock_ret19['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret19)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret20 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_dst_mode='increment',
		mac_dst_repeat_count='0',
		mac_dst_count='16',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:20',
		enable_control_plane='0',
		l3_length='537',
		name='GARP/GMRP_StreamBlock',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100',
		enable_stream='false');

	status = streamblock_ret20['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret20)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret21 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='00:00:01:00:00:01',
		enable_control_plane='0',
		l3_length='138',
		name='LACP_MARKER',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='156',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret21['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret21)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret22 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		enable_control_plane='0',
		l3_length='128',
		name='Link_OAM',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret22['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret22)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret23 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_8023_snap',
		custom_pattern='ABCDEFABCDEF',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:00:0C:CC:CC:CC',
		llc_control='03',
		llc_ssap='AA',
		llc_dsap='AA',
		snap_oui_id='00000C',
		snap_ether_type='2000',
		enable_control_plane='0',
		l3_length='555',
		name='Cisco_CDP_VTP',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret23['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret23)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret24 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='0802',
		mac_dst='01:00:0C:CC:CC:CC',
		enable_control_plane='0',
		l3_length='110',
		name='Cicso_Shared_STP_',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret24['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret24)
	else:
		print("***** run sth.traffic_config successfully")
	streamblock_ret25 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[0],
		l2_encap='ethernet_ii',
		l3_protocol='ipv4',
		l4_protocol='igmp',
		igmp_max_response_time='0',
		igmp_version='2',
		igmp_type='16',
		igmp_msg_type='report',
		igmp_group_addr='225.0.0.1',
		ip_id='0',
		ip_src_addr='192.85.1.2',
		ip_dst_addr='224.0.0.1',
		ip_ttl='255',
		ip_hdr_length='5',
		ip_protocol='2',
		ip_fragment_offset='0',
		ip_mbz='0',
		ip_precedence='0',
		ip_tos_field='0',
		mac_src='00:10:94:00:00:02',
		ether_type='0800',
		mac_dst='01:00:5E:00:00:01',
		enable_control_plane='0',
		l3_length='110',
		name='IPV4_IGMP_multicast',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100',
		mac_discovery_gw='192.85.1.1');

	status = streamblock_ret25['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret25)
	else:
		print("***** run sth.traffic_config successfully")
	streamblock_ret26 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		custom_pattern='ABCDEFABCDEF',
		mac_src='00:10:94:00:00:02',
		ether_type='0000',
		mac_dst='01:00:0C:00:00:01',
		enable_control_plane='0',
		l3_length='110',
		name='Cisco_Inter_Switch_Protocol_(ISL)',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret26['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret26)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret27 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		ether_type='8902',
		mac_dst='01:80:C2:00:00:35',
		enable_control_plane='0',
		l3_length='537',
		name='SOAM_CCM_Level_5',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='555',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret27['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret27)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret28 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:0E',
		enable_control_plane='0',
		l3_length='110',
		name='PTP_Delay_Request',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret28['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret28)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret29 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_dst_mode='increment',
		mac_dst_repeat_count='0',
		mac_dst_count='16',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:00',
		enable_control_plane='0',
		l3_length='110',
		name='L2CP_MAC_Frame',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100',
		enable_stream='false');

	status = streamblock_ret29['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret29)
	else:
		print("***** run sth.traffic_config successfully")

	streamblock_ret30 = sth.traffic_config(
		mode='create',
		port_handle=port_handle[1],
		l2_encap='ethernet_ii',
		mac_src='00:10:94:00:00:02',
		mac_dst='01:80:C2:00:00:DD',
		enable_control_plane='0',
		l3_length='110',
		name='Provider_Bridge_MVRP_Address',
		fill_type='constant',
		fcs_error='0',
		fill_value='0',
		frame_size='128',
		traffic_state='1',
		high_speed_result_analysis='1',
		length_mode='fixed',
		tx_port_sending_traffic_to_self_en='false',
		disable_signature='0',
		enable_stream_only_gen='1',
		pkts_per_burst='1',
		inter_stream_gap_unit='bytes',
		burst_loop_count='30',
		transmit_mode='continuous',
		inter_stream_gap='12',
		rate_pps='9100');

	status = streamblock_ret30['status']
	if (status == '0'):
		print("run sth.traffic_config failed")
		print(streamblock_ret30)
	else:
		print("***** run sth.traffic_config successfully")

	# config part is finished

	##############################################################
	# start devices
	##############################################################

	##############################################################
	# start traffic
	##############################################################

	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='run',
		duration='120');
	time.sleep(130)
	print("***** 130 seconds sleep done")

	traffic_ctrl_ret = sth.traffic_control(
		port_handle=[port_handle[0], port_handle[1]],
		action='stop')
	print("***** traffic stopped")

	status = traffic_ctrl_ret['status']
	if (status == '0'):
		print("run sth.traffic_control failed")
		print(traffic_ctrl_ret)
	else:
		print("***** run sth.traffic_control successfully")

	##############################################################
	# start to get the device results
	##############################################################

	##############################################################
	# start to get the traffic results
	##############################################################

	traffic_results_ret = sth.traffic_stats(
		port_handle=[port_handle[0], port_handle[1]],
		mode='all');

	status = traffic_results_ret['status']
	if (status == '0'):
		print("run sth.traffic_stats failed")
		print(traffic_results_ret)
	else:
		print("***** run sth.traffic_stats successfully, and results is:")
		pprint(traffic_results_ret)


	##############################################################
	# clean up the session, release the ports reserved and cleanup the dbfile
	##############################################################

	cleanup_sta = sth.cleanup_session(
		port_handle=[port_handle[0], port_handle[1]],
		clean_dbfile='1');

	status = cleanup_sta['status']
	if (status == '0'):
		print("run sth.cleanup_session failed")
		print(cleanup_sta)
	else:
		print("***** run sth.cleanup_session successfully")

	print("**************Finish***************")

	##############################################################
	# Get required values from Stats
	##############################################################
	traffic_result = str(traffic_results_ret)
	pprint(traffic_results_ret)
	# regex to get rx, tx and streams from traffic_results_ret
	DROP = '(streamblock\d+).*?\s+\S+(dropped_pkts)\S+\s+\S+(\d+)'
	RX = '(streamblock\d+).*?(rx).*?(total_pkts).*?(\d+)'
	TX = '(streamblock\d+).*?(tx).*?(total_pkts).*?(\d+)'
	pkt_drop = re.findall(DROP, traffic_result)
	rx_stats = re.findall(RX, traffic_result)
	tx_stats = re.findall(TX, traffic_result)
	pprint(rx_stats)
	pprint(tx_stats)
	StreamBlock = 'streamblock\d+'

	print('Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list)))
	PortStatus = 'Spirent Ports= ' + str(port_list) + '\nTotal Ports= ' + str(len(port_list))
	StreamBlock = re.findall(StreamBlock, traffic_result)
	print('Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock)))
	StreamStatus = 'Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock))

	print('rx_stats= ' + str(rx_stats))
	print('tx_stats= ' + str(tx_stats))

	stats = 'rx_stats= ' + str(rx_stats) + '\ntx_stats= ' + str(tx_stats)

	StreamResult = []

	for i in range(0, len(StreamBlock)):
		if rx_stats[i][3] == tx_stats[i][3]:
			print(str(rx_stats[i][0] + ' = pass'))
			StreamResult.append('pass')

		else:
			print(str(rx_stats[i][0] + ' = fail'))
			StreamResult.append('fail')
			print("I m in fail")
		if i==24:
			print("Zero RX")
			print(rx_stats[i][3])
			print(tx_stats[i][3])
	print(str(StreamResult))

	OverallStatus = '\n' + PortStatus + '\n' + StreamStatus + '\n' + stats + '\n' + str(StreamResult)
	print(OverallStatus)

	return OverallStatus
