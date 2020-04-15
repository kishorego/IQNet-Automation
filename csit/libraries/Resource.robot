*** Settings ***
Documentation     Resource file containing all the PYTHON API implementations.
Library           String
Library           Collections
Library           ${CURDIR}//Connect_devices.py
Library           ${CURDIR}//Commands.py
Resource          ${CURDIR}//Resource.robot    #Resource    Resource.robot

*** Variables ***

*** Keywords ***
Setup Actions
    Log To Console    Setup Actions done here
    #    log to console    ${CURDIR}
    ${Topo_data}    Get Data
    #log to console    ${Topo_data}
    ${DEV_DICT}    get from dictionary    ${Topo_data}    Device_Details    #get all device details
    ${LINK_DICT}    get from dictionary    ${Topo_data}    Link_Details     #get all link details

    #NCS R1 & R2 details
    ${Link_R1_R2}    get from dictionary    ${LINK_DICT}    Link_R1_R2  #get NCS_R1/R2 link dictionary
    ${PORT_R1_10}    get from dictionary    ${Link_R1_R2}    R1      #get NCS_R1 link
    ${PORT_R2_10}    get from dictionary    ${Link_R1_R2}    R2      #get NCS_R2 link
    Builtin.Set_Suite_Variable    ${PORT_R1_10}                        #global variable
    Builtin.Set_Suite_Variable    ${PORT_R2_10}                        #global variable
    ${R1_DICT}    get from dictionary    ${DEV_DICT}    NCS_R1              #NCS_R1 dictionary
    ${R1_net_connect}    Make Connection    ${R1_DICT}                      #ssh to NCS_R1
    Builtin.Set_Suite_Variable    ${R1_net_connect}
    Log To Console    Connection Establihed to NCS_R1
    ${R2_DICT}    get from dictionary    ${DEV_DICT}    NCS_R2              #NCS_R2 dictionary
    ${R2_net_connect}    Make Connection    ${R2_DICT}                      #ssh to NCS_R2
    Builtin.Set_Suite_Variable    ${R2_net_connect}
    Log To Console    Connection Establihed to NCS_R2

    #LTS R3 & R4 details
#    ${Link_R3}    get from dictionary    ${LINK_DICT}    Link_R3             #get R3 link dictionary
#    ${PORT_R3_1}    get from dictionary    ${Link_R3}    R3_1
#    ${PORT_R3_5}    get from dictionary    ${Link_R3}    R3_5
#    Builtin.Set_Suite_Variable    ${PORT_R3_1}                        #global variable
#    Builtin.Set_Suite_Variable    ${PORT_R3_5}                        #global variable
#    ${R3_DICT}    get from dictionary    ${DEV_DICT}    LTS_R3              #LTS_R3 dictionary
#    ${R3_net_connect}    Make Connection Accedian    ${R3_DICT}                      #ssh to LTS_R3
#    Builtin.Set_Suite_Variable    ${R3_net_connect}
#    Log To Console    Connection Establihed to LTS_R3

Teardown Actions
    Log To Console    Teardown Actions done here
    Close Connection    ${R1_net_connect}
    Close Connection    ${R2_net_connect}
#    Close Connection    ${R3_net_connect}

CONFIGURE POLICY-MAP-EGR
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}   template_data=${template_data}
    should not contain    ${commit_result}    fail

## NCS config ##
CONFIGURE SERVICE-POLICY-MAP
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE SERVICE-POLICY-MAP-INTF
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    policy_intf=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE INTERFACE
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    interface=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE SUB-INTERFACE
    [Arguments]    ${connect_id}    ${sub_intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    sub_interface=${sub_intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE L2VPN
    [Arguments]    ${connect_id}    ${sub_intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    attch_ckt_intf=${sub_intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE EVPN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE CFM
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE CFM-INTF
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    cfm_ckt_intf=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE LLF
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    llf_intf=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

SHOW COMMAND
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${show_cmd_result}    Show Commands    ${connect_id}    template_name=${${template_name}}    template_data=${template_data}    textfsm_template=${template_name}
    [Return]    ${show_cmd_result}


UNCONFIGURE CFM
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE EVPN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE L2VPN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE SUB-INTF
    [Arguments]    ${connect_id}    ${sub_intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    sub_interface=${sub_intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE INTF
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    interface=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE SERVICE-POLICY-MAP
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail


## Accedian Config ## LTS ##

ENABLE ACCEDIAN-PORT
    [Arguments]    ${connect_id}    ${port_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    port_name=${port_name}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE ACCEDAIN-REGULATOR
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE ACCEDAIN-REGULATOR
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE ACCEDAIN-FILTER
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE ACCEDAIN-FILTER
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE VID-SET
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE VID-SET
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE TRAFFIC-POLICY
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE TRAFFIC-POLICY
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE CFM-MEG-ACCEDIAN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE CFM-MEG-ACCEDIAN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE CFM-MEP-ACCEDIAN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE CFM-MEP-ACCEDIAN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error
