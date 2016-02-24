import sys
import time
import os
from os import environ as env
from novaclient import client as nclient
from openstackclient.common import utils
import keystoneclient.v2_0.client as ksclient
import ceilometerclient.client as cclient
import pprint
import numpy
import requests
import traceback
sys.stdout = open('asg.log', 'w')
print(env['OS_USERNAME'])
print(env['OS_PASSWORD'])

keystone = ksclient.Client(auth_url=env['OS_AUTH_URL'],
                           username=env['OS_USERNAME'],
                           password=env['OS_PASSWORD'],
                           tenant_name=env['OS_TENANT_NAME'],
                           region_name=env['OS_REGION_NAME'])

ceiclient = cclient.get_client(2,auth_url=env['OS_AUTH_URL'],
                           username=env['OS_USERNAME'],
                           password=env['OS_PASSWORD'],
                           tenant_name=env['OS_TENANT_NAME'],
                           region_name=env['OS_REGION_NAME'])

nova_client = nclient.Client(2, env['OS_USERNAME'],env['OS_PASSWORD'],env['OS_TENANT_NAME'],env['OS_AUTH_URL'], env['OS_REGION_NAME'])

current_instances = []
COOLDOWN = float(env['COOLDOWN'])
LB_IPADDR = env['LB_IPADDR']
CPU_UPPER_TRES = float(env['CPU_UPPER_TRES'])
CPU_LOWER_TRES = float(env['CPU_LOWER_TRES'])
MIN_INSTANCE = int(env['MIN_INSTANCE'])
MAX_INSTANCE = int(env['MAX_INSTANCE'])
EVAL_PERIOD = float(env['EVAL_PERIOD'])
EVAL_COUNT = int(env['EVAL_COUNT'])
DELTA = int(env['DELTA'])
ASG_IMAGE = env['ASG_IMAGE']
ASG_FLAVOR = env['ASG_FLAVOR']
ASG_NAME = env['ASG_NAME']
print 'DELTA', DELTA
index = 0
def main():
    prev_action_time = time.time()
    count = 0
    global current_instances
    current_instances = launch_instance(MIN_INSTANCE)
    notify_LB_add(current_instances)
    time.sleep(COOLDOWN)
    print current_instances
    while True:
        cpu_utils = []
        qurey = []
        current_time = time.time()
        ### query ceilometer for cpu utilization data    
        for ins in current_instances:
            print ins.to_dict()['id']
            query = [{"field": "resource_id", "op": "eq", "value": ins.to_dict()['id']}]
            sample = ceiclient.samples.list(meter_name='cpu_util', limit=1, q=query)
            if sample:
                cpu_utils.append(sample[0].to_dict()['counter_volume'])
        print current_time, cpu_utils
        mean_val =  numpy.mean(cpu_utils)
        if mean_val > CPU_UPPER_TRES:
            print 'greater'
            if count >=0:
                count = count + 1
            else:
                count = 1
        elif mean_val < CPU_LOWER_TRES:
            print 'less'
            if count < 0:
                count = count -1
            else:
                count = -1
    
        if(current_time - prev_action_time > COOLDOWN):
            if(count >= EVAL_COUNT) and (len(current_instances) + DELTA <= MAX_INSTANCE):
                prev_action_time = time.time()
                new_servers = launch_instance(DELTA)
                current_instances = current_instances + new_servers
                notify_LB_add(new_servers)
                print "added", DELTA, "instances"
                count = 0
            elif (count <= (0 - EVAL_COUNT)) and (len(current_instances) - DELTA >=MIN_INSTANCE):
                prev_action_time = time.time()
                print "remove"
                removed = remove_instance(DELTA)
                notify_LB_remove(removed)
                count = 0
        update_to_localfile()
        time.sleep(EVAL_PERIOD)                   
    #print novaclient.networks.list()


def launch_instance(num):
    num = int(num)
    global index
    asg_flavor = nova_client.flavors.find(name=ASG_FLAVOR)
    asg_image = nova_client.images.find(name=ASG_IMAGE)
    net = nova_client.networks.find(label='private')
    ret= []
    for i in range(0,num):
        ret.append(nova_client.servers.create(ASG_NAME+str(index), flavor=asg_flavor.id, image=asg_image.id, nics=[{'net-id':net.id}]))
        index = index + 1
    for i in range(0, num):    
        if not utils.wait_for_status(nova_client.servers.get, ret[i].id):
            print "failed to start new instance "+ str(i)
        else:
            ret[i] = nova_client.servers.find(id=ret[i].id)
    return ret

def remove_instance(num):
    global current_instances
    num = int(num)
    for i in range(0, num):
        nova_client.servers.delete(current_instances[i].id)
        utils.wait_for_delete(nova_client.servers, current_instances[i].id)
    removed = current_instances[0:num]
    current_instances = current_instances[num:]
    return removed

def notify_LB_remove(server):
    for s in server:
        addr = get_server_addr(s)
        print LB_IPADDR, addr
        payload = {'ip': addr}
        r = requests.get("http://"+LB_IPADDR+":8080/remove", params=payload)
        print r.text

def notify_LB_add(server):
    for s in server:
        addr = get_server_addr(s)
        print LB_IPADDR, addr
        payload = {'ip': addr}
        r = requests.get("http://"+LB_IPADDR+":8080/add", params=payload)
        print r.url 

def get_server_addr(server):
    try:
       #print server.__dict__
       return server.addresses['private'][0]['addr']
    except IndexError, KeyError:
       traceback.print_exc()
       return None

def update_to_localfile():
    f = open(ASG_NAME,'w')
    f.write(str(os.getpid())+'\n')
    for s in current_instances:
        f.write(s.id+'\n')
    f.close()



if __name__ == "__main__": main()
