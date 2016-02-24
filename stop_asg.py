from asg import nova_client,ASG_NAME
import os
import signal
from openstackclient.common import utils

f = open(ASG_NAME, 'r')
content = f.readlines()
if content:
    pid = content[0]
    os.kill(int(pid), signal.SIGTERM)
    for i in range(1:len(content)):
        server = nova_client.servers.find(id=content[i])
        notify_LB_remove(server)
        nova_client.servers.delete(content[i])
        utils.wait_for_delete(nova_client.servers, content[i])
        
print 'ok'
            
