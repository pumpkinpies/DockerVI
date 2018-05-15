from django.http import HttpResponse
from django.template.loader import get_template
from django.template import context
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import docker

iplist = ['192.168.56.102']

def Nodes(request):
    client = docker.from_env()
    templist = client.nodes.list()
    nodelist = []
    nodedict = {}
    if templist != None:
       for item in templist:
           nodedict['Id'] = item.attrs['ID']
           nodedict['Status'] = item.attrs['Status']['State']
           nodedict['Hostname'] = item.attrs['Description']['Hostname']
           nodedict['Availability'] = item.attrs['Spec']['Availability']
           nodedict['Role'] = item.attrs['Spec']['Role']
           nodedict['IP'] = item.attrs['Status']['Addr']
           nodedict['IsRunning'] = ''
           if nodedict['Status'] == 'ready':
              nodedict['IsRunning'] = 1
           nodelist.append(nodedict.copy())

    client2 = docker.from_env()
    templist = client2.services.list()
    servicelist = []
    servicedict = {}

    if templist != None:
        for item in templist:
            servicedict['Id'] = item.attrs['ID']
            servicedict['Name'] = item.attrs['Spec']['Name']
            servicedict['Image'] = item.attrs['Spec']['TaskTemplate']['ContainerSpec']['Image']
            servicedict['Mode'] = ''

            for key in item.attrs['Spec']['Mode'].keys():
                servicedict['Mode'] += key + '' 
                if key == 'Replicated':
                    servicedict['Replicas'] = item.attrs['Spec']['Mode'][key]['Replicas']
            servicelist.append(servicedict.copy())


    template = get_template('swarm.html')
    html = template.render(locals())
    return HttpResponse(html)

def Services(request, Id):
    client = docker.from_env()
    templist = client.services.list(filters=({ 'id':Id }))

    containerlist = []
    containerdict = {}
    if templist != None:
        for i in templist:
            templist2 = i.tasks()
            for j in templist2:
               containerdict['Id'] = j['Status']['ContainerStatus']['ContainerID']
               containerdict['Image'] = j['Spec']['ContainerSpec']['Image']
               NodeId = j['NodeID']
               containerdict['Node'] =  client.nodes.get(NodeId).attrs['Description']['Hostname']
               containerdict['State'] = j['Status']['State']
               containerdict['IsRunning'] = '' 
             #  print (containerdict['State'])
               if containerdict['State'] == 'running':
                  containerdict['IsRunning'] = 1

               containerdict['Created'] = j['CreatedAt']

               containerlist.append(containerdict.copy())

    template = get_template('serviceinfo.html')
    html = template.render(locals())
    return HttpResponse(html)


def computmcn(container):
    container_stats = container.stats(decode=True,stream=False)

    memoryb = container_stats['memory_stats']['usage']                
    memory = round(memoryb/(1024*1024), 2)

    system_delta = container_stats['cpu_stats']['system_cpu_usage']-container_stats['precpu_stats']['system_cpu_usage']
    cpu_delta = container_stats['cpu_stats']['cpu_usage']['total_usage']-container_stats['precpu_stats']['cpu_usage']['total_usage']
    cpu_count=len(container_stats['cpu_stats']['cpu_usage']['percpu_usage'])
    cpu = round((float(cpu_delta)/float(system_delta))*cpu_count*100.0,2)
    
    tx = round(container_stats['networks']['eth0']['tx_bytes']/1024, 2)
    rx = round(container_stats['networks']['eth0']['rx_bytes']/1024, 2)

    return memory, cpu,  tx ,rx



@csrf_exempt
def ServicesChart(request, Id):

    client = docker.from_env()
    templist = client.services.list(filters=({ 'id':Id }))
    
    IDdict = {}
    IDlist = []

    containerlist = [] 
    
    if templist != None:
        for i in templist:
            templist2 = i.tasks()
            for j in templist2:
              IDdict['Id'] = j['Status']['ContainerStatus']['ContainerID']
              IDlist.append(IDdict.copy())

    for i in IDlist:
      try:
        clientL = docker.from_env()
        container = clientL.containers.get(i['Id'])
      except:
        clientR = docker.DockerClient(base_url = 'tcp://'+iplist[0]+':5678')
        container = clientR.containers.get(i['Id'])
      finally:
        containerlist.append(container)

    memory, cpu, tx, rx = 0, 0, 0 ,0 

    for container in containerlist:
        a ,b ,c, d = computmcn(container)
        memory += a
        cpu += b
        tx += c
        rx += d
    
    memory = round(memory, 2)
    cpu = round(cpu, 2)
    tx = round(tx, 2)
    rx = round(rx, 2)

    return HttpResponse(json.dumps({'memory':memory,'cpu':cpu,'tx':tx,'rx':rx}),content_type="application/json")
