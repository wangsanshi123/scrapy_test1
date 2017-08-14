#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import socket
import traceback
import warnings

warnings.filterwarnings('ignore')
__author__ = 'yangsheng'

def request_socket(server_ip, server_port, matter):
    try:
        address = (server_ip, server_port)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
        client.send(matter.encode('utf-8'))
        resultstr = client.recv(20480).decode('utf-8')
    except Exception as e:
        print(traceback.format_exc())
    client.close()
    dict_result = json.loads(resultstr)
    # print(dict_result)
    return dict_result
