from django.http import HttpResponse
from django.template.loader import get_template
from django.template import context
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
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
    
    value = request.POST.get('submit')
    template = get_template('containerinfo.html')

    if value is None:
        
        client = docker.from_env()
        container = client.containers.get(Id)
        containerdict,volumelist = getContainInfo(container)
        if containerdict['Status'] == 'exited':
            StartIsDisabled = ''
            StopIsDisabled = 'disabled=\'disabled\''
            RestartIsDisabled = 'disabled=\'disabled\''
            PauseIsDisabled = 'disabled=\'disabled\''
            ResumeIsDisabled = 'disabled=\'disabled\''
            KillIsDisabled = 'disabled=\'disabled\''
        else :            
            if containerdict['Paused'] == False:
                StartIsDisabled = 'disabled=\'disabled\''
                StopIsDisabled = ''
                RestartIsDisabled = ''
                PauseIsDisabled = ''
                ResumeIsDisabled = 'disabled=\'disabled\''
                KillIsDisabled = ''
            else:
                StartIsDisabled = 'disabled=\'disabled\''
                StopIsDisabled = 'disabled=\'disabled\''
                RestartIsDisabled = 'disabled=\'disabled\''
                PauseIsDisabled = 'disabled=\'disabled\''
                ResumeIsDisabled = ''
                KillIsDisabled = 'disabled=\'disabled\''


    else:
        client = docker.from_env()
        container = client.containers.get(Id)
        try:
            exec ('container.%s' %value)
        except :
            messages.add_message(request,messages.ERROR, 'Someting Wrong, Please Check') 
            

        client = docker.from_env()
        container = client.containers.get(Id)
        containerdict,volumelist = getContainInfo(container)
        
        if containerdict['Status'] == 'exited':
            StartIsDisabled = ''
            StopIsDisabled = 'disabled=\'disabled\''
            RestartIsDisabled = 'disabled=\'disabled\''
            PauseIsDisabled = 'disabled=\'disabled\''
            ResumeIsDisabled = 'disabled=\'disabled\''
            KillIsDisabled = 'disabled=\'disabled\''
        else :            
            if containerdict['Paused'] == False:
                StartIsDisabled = 'disabled=\'disabled\''
                StopIsDisabled = ''
                RestartIsDisabled = ''
                PauseIsDisabled = ''
                ResumeIsDisabled = 'disabled=\'disabled\''
                KillIsDisabled = ''
            else:
                StartIsDisabled = 'disabled=\'disabled\''
                StopIsDisabled = 'disabled=\'disabled\''
                RestartIsDisabled = 'disabled=\'disabled\''
                PauseIsDisabled = 'disabled=\'disabled\''
                ResumeIsDisabled = ''
                KillIsDisabled = 'disabled=\'disabled\''
        
        

    html = template.render(locals())
    return HttpResponse(html)



@csrf_exempt
def Chart(request, Id):
    client = docker.from_env()
    container = client.containers.get(Id)    
    memoryb = container.stats(decode=True,stream=False)['memory_stats']['usage']                
    memory = round(memoryb/(1024*1024), 2) 
    
    return HttpResponse(json.dumps({'memory':memory}),content_type="application/json")


def Stats(request, Id):
     
    template = get_template('stats.html')
    html = template.render(locals())
    return HttpResponse(html)



def Logs(request, Id):
        pass

def Inspect(request, Id):
        pass



