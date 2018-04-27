from django.http import HttpResponse
from django.template.loader import get_template
from django.template import context
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import docker


def getContainInfo(container):
    containerdict = {}
    containerdict['Id'] = container.attrs['Id']
    containerdict['Name'] = container.attrs['Name'][1:]
    containerdict['IPAddress'] = container.attrs['NetworkSettings']['IPAddress']
    containerdict['Status'] = container.attrs['State']['Status']
    containerdict['Image'] = container.attrs['Config']['Image']
    containerdict['Paused'] = container.attrs['State']['Paused']
    
    if container.attrs['Config']['Cmd'] != None:
        containerdict['CMD'] = ' '.join([str(i) for i in container.attrs['Config']['Cmd']])
    #for multiports
    PortBindings = container.attrs['HostConfig']['PortBindings']
    if PortBindings != None:
        for i in PortBindings:
            for j in PortBindings[i]:
                containerdict['Ports'] = j['HostPort']+' '


    volumedict = {}
    volumelist = []
    templist = container.attrs['Mounts']
    if templist != None:
        for item in templist:
            volumedict['Host'] = item['Source']
            volumedict['Container'] = item['Destination']
            volumelist.append(volumedict.copy())

    return containerdict,volumelist


@csrf_exempt
def ContainerInfo(request, Id):
    template = get_template('containerinfo.html')
    client = docker.from_env()
    container = client.containers.get(Id)
    value = request.POST.get('submit')

    if value is None:
        containerdict,volumelist = getContainInfo(container)
        if containerdict['Status'] == 'exited':
            StartIsDisabled = ''
            StopIsDisabled = 'disabled=\'disabled\''
            RestartIsDisabled = 'disabled=\'disabled\''
            PauseIsDisabled = ''
            ResumeIsDisabled = 'disabled=\'disabled\''
            KillIsDisabled = ''
        else :
            StartIsDisabled = 'disabled=\'disabled\''
            StopIsDisabled = ''
            RestartIsDisabled = ''
            KillIsDisabled = ''
            if containerdict['Paused'] == False:
                PauseIsDisabled = ''
                ResumeIsDisabled = ''
            else:
                PauseIsDisabled = 'disabled=\'disabled\''
                ResumeIsDisabled = ''
    else:
        exec ('container.%s' %value)
        containerdict,volumelist = getContainInfo(container)
        if containerdict['Status'] == 'exited':
            StartIsDisabled = ''
            StopIsDisabled = 'disabled=\'disabled\''
            RestartIsDisabled = 'disabled=\'disabled\''
            PauseIsDisabled = ''
            ResumeIsDisabled = 'disabled=\'disabled\''
            KillIsDisabled = ''
        else :
            StartIsDisabled = 'disabled=\'disabled\''
            StopIsDisabled = ''
            RestartIsDisabled = ''
            KillIsDisabled = ''
            if containerdict['Paused'] == False:
                PauseIsDisabled = ''
                ResumeIsDisabled = ''
            else:
                PauseIsDisabled = 'disabled=\'disabled\''
                ResumeIsDisabled = ''
        

    html = template.render(locals())
    return HttpResponse(html)


def Stats(request, Id):
        pass

def Logs(request, Id):
        pass

def Inspect(request, Id):
        pass


