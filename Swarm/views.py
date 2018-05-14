from django.http import HttpResponse
from django.template.loader import get_template
from django.template import context
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import docker

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
               print (containerdict['State'])
               if containerdict['State'] == 'running':
                  containerdict['IsRunning'] = 1

               containerdict['Created'] = j['CreatedAt']

               containerlist.append(containerdict.copy())

    template = get_template('serviceinfo.html')
    html = template.render(locals())
    return HttpResponse(html)
