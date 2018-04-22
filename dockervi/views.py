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

