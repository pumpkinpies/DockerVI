from django.http import HttpResponse
from django.template.loader import get_template
from django.template import context
from datetime import datetime
import docker


def Dashboard(request):
    template = get_template('index.html')
    client = docker.from_env()
    info = client.info()
    HostName = info['Name']
    DockerVersion = info['ServerVersion']
    CpuNum = info['NCPU']
    Memoryb = info['MemTotal']
    Memory = str(round(Memoryb/(1024*1024*1024), 2))+' GB'
    Containers = info['Containers']
    ContainersRunning = info['ContainersRunning']
    Images = len(client.images.list())
    Volumes = len(client.volumes.list())
    Networks = len(client.networks.list())

    html = template.render(locals())

    return HttpResponse(html)

def Containers(request):
    template = get_template('container.html')
    client = docker.from_env()
    templist = client.containers.list(all=True)
    containerdict = {}
    containerlist = []
    for item in templist:
        containerdict['Name'] = item.attrs['Name'][1:]
        containerdict['Image'] = item.attrs['Config']['Image']
        containerdict['IPAddress'] = item.attrs['NetworkSettings']['IPAddress']
        containerdict['Status'] = item.attrs['State']['Status']
        containerdict['IsRunning'] = ""
        if containerdict['Status'] == 'running':
           containerdict['IsRunning'] = 1
        PortBindings = item.attrs['HostConfig']['PortBindings']
        for i in PortBindings:
            for j in PortBindings[i]:
                containerdict['Ports'] = j['HostPort']+' '
        containerlist.append(containerdict.copy())

    html = template.render(locals())
    return HttpResponse(html)


def Images(request):
    template = get_template('image.html')
    client = docker.from_env()
    templist = client.images.list()
    imagedict = {}
    imagelist = []
    for item in templist:
        imagedict['Id'] = item.attrs['Id']
        imagedict['Created'] = item.attrs['Created'][:19]
        imagedict['Tag'] = item.attrs['RepoTags'] 
        imagelist.append(imagedict.copy())
    html = template.render(locals())
    return HttpResponse(html)
    
def Volumes(request):
    template = get_template('volume.html')
    client = docker.from_env()
    templist = client.volumes.list()
    volumedict = {}
    volumelist = []
    for item in templist:
        volumedict['Name'] = item.attrs['Name']
        volumedict['Mountpoint'] = item.attrs['Mountpoint']
        volumedict['Mountpoint'] = volumedict['Mountpoint'][:27]+'...'+volumedict['Mountpoint'][-9:]
        volumedict['Driver'] = item.attrs['Driver']
        volumedict['Labels'] = item.attrs['Labels']
        volumelist.append(volumedict.copy())
    html = template.render(locals())
    return HttpResponse(html)

def Networks(request):
    template = get_template('network.html')
    client = docker.from_env()
    templist = client.networks.list()
    networklist = []
    networkdict = {}
    for item in templist:
        networkdict['Name'] = item.attrs['Name']
        networkdict['Scope'] = item.attrs['Scope']
        networkdict['Driver'] = item.attrs['Driver']
        if item.attrs['IPAM']['Config'] != []:
            networkdict['Gateway'] = item.attrs['IPAM']['Config'][0]['Gateway']
            networkdict['Subnet'] = item.attrs['IPAM']['Config'][0]['Subnet']
        else:
            networkdict['Gateway'] = ""
            networkdict['Subnet'] = ""
        networklist.append(networkdict.copy())
    html = template.render(locals())
    return HttpResponse(html)
