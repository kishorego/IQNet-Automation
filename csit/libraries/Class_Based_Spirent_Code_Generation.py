
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
	Spirent_Test_Topology = data['Spirent_Test_Topology']
	return (Spirent_Test_Topology)


class Spirent_L2_Traffic_Gen:
	def __init__(self, **kwargs):
		self.port_handle = []
		self.port_list = []

	def Port_Init(self):
		Spirent_Test_Infrastructure = Get_Spirent_Config()
		Number_of_ports = Spirent_Test_Infrastructure['Number_of_ports']
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
		device = Spirent_Test_Infrastructure['Spirent_Chassis_ip']
		port_list = list(Spirent_Test_Infrastructure['Port_Values'].values())
		self.port_list = port_list
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
				self.port_handle.append(intStatus['port_handle'][device][port])
				i += 1
		else:
			print("\nFailed to retrieve port handle!\n")
		#		print(self.port_handle)
		print(self.port_handle)
		##############################################################
		# Spirent Ports configuration
		##############################################################
		for i in range(len(port_list)):
			int_ret0 = sth.interface_config(
			mode='config',
			port_handle=self.port_handle[i],
			create_host='false',
			intf_mode = 'ethernet',
			phy_mode = port_mode[i],
			scheduling_mode='RATE_BASED',
			port_loadunit='PERCENT_LINE_RATE',
			port_load='50',
			enable_ping_response='0',
			control_plane_mtu='1500',
			flow_control='false',
			speed=port_speed[i],
			data_path_mode='normal',
			autonegotiation='1');
			status = int_ret0['status']
			if (status == '0'):
				print("run sth.interface_config failed")
			# print(int_ret0)

	def Stream_Config_Creation_Without_VLAN_Mbps(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			self.Frame_Size = 1500
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		print("Inside Init, Remove this print after testing")
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
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
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='6000',
			transmit_mode='multi_burst',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		return(streamblock_ret)
	# config part is finished

	def Stream_Config_Creation_Without_VLAN_PPS(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			self.Frame_Size = 1500
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_PPS' in kwargs.keys():
			self.rate_pps = kwargs['Rate_PPS']
		else:
			self.rate_pps = '1000'
		print("Inside Init, Remove this print after testing")
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
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
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='6000',
			transmit_mode='multi_burst',
			inter_stream_gap='12',
			rate_pps=self.rate_pps,
			mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		return(streamblock_ret)
	# config part is finished
	def Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			self.Frame_Size = 1500
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'Outer_VLAN_EtherType' in kwargs.keys():
			self.vlan_outer_tpid = str(int(kwargs['Outer_VLAN_EtherType'], 10))
		else:
			self.vlan_outer_tpid = '34984'
		if 'Outer_VLAN_Priority' in kwargs.keys():
			self.vlan_outer_user_priority = str(int(kwargs['Outer_VLAN_Priority'], 10))
		else:
			self.vlan_outer_user_priority = 3
		if 'Outer_VLAN_ID' in kwargs.keys():
			self.vlan_id_outer = str(int(kwargs['Outer_VLAN_ID'], 10))
		else:
			self.vlan_id_outer = '1000'
		self.l2_encap = 'ethernet_ii_vlan'
		if 'Inner_VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['Inner_VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'Inner_VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['Inner_VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'Inner_VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		print("Inside Init, Remove this print after testing")
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap=self.l2_encap,
			vlan_outer_tpid=self.vlan_outer_tpid,
			vlan_id_outer=self.vlan_id_outer,
			vlan_outer_user_priority = self.vlan_outer_user_priority,
			vlan_tpid = self.vlan_tpid,
			vlan_id = self.vlan_id,
			vlan_user_priority = self.vlan_user_priority,
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
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='6000',
			transmit_mode='multi_burst',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		return(streamblock_ret)
	# config part is finished
	def Stream_Config_Creation_Dual_Tagged_VLAN_dot1q_Mbps(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			self.Frame_Size = 1500
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'Outer_VLAN_EtherType' in kwargs.keys():
			self.vlan_outer_tpid = str(int(kwargs['Outer_VLAN_EtherType'], 10))
		else:
			self.vlan_outer_tpid = '33024'
		if 'Outer_VLAN_Priority' in kwargs.keys():
			self.vlan_outer_user_priority = str(int(kwargs['Outer_VLAN_Priority'], 10))
		else:
			self.vlan_outer_user_priority = 3
		if 'Outer_VLAN_ID' in kwargs.keys():
			self.vlan_id_outer = str(int(kwargs['Outer_VLAN_ID'], 10))
		else:
			self.vlan_id_outer = '1000'
		self.l2_encap = 'ethernet_ii_vlan'
		if 'Inner_VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['Inner_VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'Inner_VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['Inner_VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'Inner_VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		print("Inside Init, Remove this print after testing")
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap=self.l2_encap,
			vlan_outer_tpid=self.vlan_outer_tpid,
			vlan_id_outer=self.vlan_id_outer,
			vlan_outer_user_priority = self.vlan_outer_user_priority,
			vlan_tpid = self.vlan_tpid,
			vlan_id = self.vlan_id,
			vlan_user_priority = self.vlan_user_priority,
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
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='6000',
			transmit_mode='multi_burst',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		return(streamblock_ret)
	# config part is finished
	def Stream_Config_Creation_Single_Tagged_VLAN_Mbps(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			self.Frame_Size = 1500
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		self.l2_encap = 'ethernet_ii'
		print("Inside Init, Remove this print after testing")
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap=self.l2_encap,
			vlan_tpid = self.vlan_tpid,
			vlan_id = self.vlan_id,
			vlan_user_priority = self.vlan_user_priority,
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
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='6000',
			transmit_mode='multi_burst',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		return(streamblock_ret)
	# config part is finished
	def Generate_Stream_Traffic(self, StreamBlock):
		#############################################################
		# start traffic
		##############################################################
		pprint(StreamBlock)
		print("Printed StreamBlock")
		time.sleep(60)
		stream_handle = StreamBlock['stream_id']
		print("Traffic Started First Time")
		traffic_ctrl_ret = sth.traffic_control(
			stream_handle=[stream_handle],
			action='run', duration='30');
		time.sleep(60)
		print("After Aging Timer")
		traffic_ctrl_ret = sth.traffic_control(
			stream_handle=[stream_handle],
			action='clear_stats');
		print("Delay before Second Traffic Started Second Time")
		time.sleep(60)
		print("Traffic Started Second Time")
		traffic_ctrl_ret = sth.traffic_control(
			stream_handle=[stream_handle],
			action='run',
			duration='10');
		status = traffic_ctrl_ret['status']
		if (status == '0'):
			print("run sth.traffic_control failed")
		# print(traffic_ctrl_ret)
		print("Test Traffic Stopped now adding delay before collecting stats")
		time.sleep(70)
		print("Traffic collection started")

	def Generate_Traffic(self):
		#############################################################
		# start traffic
		##############################################################
		print("Traffic Started First Time")
		traffic_ctrl_ret = sth.traffic_control(
			port_handle= self.port_handle,
			action='run', duration='30');
		time.sleep(60)
		print("After Aging Timer")
		traffic_ctrl_ret = sth.traffic_control(
			port_handle=self.port_handle,
			action='clear_stats');
		print("Delay before Second Traffic Started Second Time")
		time.sleep(60)
		print("Traffic Started Second Time")
		traffic_ctrl_ret = sth.traffic_control(
			port_handle=self.port_handle,
			action='run',
			duration='10');
		status = traffic_ctrl_ret['status']
		if (status == '0'):
			print("run sth.traffic_control failed")
		# print(traffic_ctrl_ret)
		print("Test Traffic Stopped now adding delay before collecting stats")
		time.sleep(70)
		print("Traffic collection started")

	def Traffic_Collection(self):
		##############################################################
		# start to get the traffic results
		##############################################################
		traffic_results_ret = sth.traffic_stats(
			port_handle=self.port_handle,
			mode='all');
		print("Traffic collection stopped")
		status = traffic_results_ret['status']
		if (status == '0'):
			print("run sth.traffic_stats failed")
		pprint(traffic_results_ret)
		cleanup_sta = sth.cleanup_session(
			port_handle=self.port_handle,
			clean_dbfile='1');
		print("Port Cleanedup")
		##############################################################
		# Get required values from Stats
		##############################################################

		self.traffic_result = str(traffic_results_ret)

	def Validate_Traffic_Result(self):

		# regex to get rx, tx and streams from traffic_results_ret
		RX = '(streamblock\d+)\S+\s+\S+(rx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
		TX = '(streamblock\d+).*?(tx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'

		StreamBlock = 'streamblock\d+'

		print('Spirent Ports= ' + str(self.port_list) + '\nTotal Ports= ' + str(len(self.port_list)))
		PortStatus = 'Spirent Ports= ' + str(self.port_list) + '\nTotal Ports= ' + str(len(self.port_list))
		StreamBlock = re.findall(StreamBlock, self.traffic_result)
		print('Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock)))
		StreamStatus = 'Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock))
		rx_stats = re.findall(RX, self.traffic_result)
		tx_stats = re.findall(TX, self.traffic_result)

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

def Create_Class_Based_Spirent_L2_Gen(**kwargs):
	Spirent_L2_Gen = Spirent_L2_Traffic_Gen (**kwargs)
	return (Spirent_L2_Gen)

