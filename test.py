import sqlite3
import docker
import time


def create_ctable():
    conn = sqlite3.connect('docker.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS container 
        (Id CHAR(64) NOT NULL, 
        logtime TIMESTAMP default (strftime('%s','now')), 
        mem DECIMAL(20,2),
        cpu DECIMAL(20,2),
        rx DECIMAL(20,2),
        tx DECIMAL(20,2)
        ); ''')
    except:
        print ('Create Table Falied')
        return False

    conn.commit()  
    conn.close()


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


def insert_container(Id, mem, cpu, rx, tx):
    conn = sqlite3.connect('docker.db')
    cursor = conn.cursor()
    cursor.execute('insert into container (Id, mem, cpu, rx, tx) values (\'%s\',%s,%s,%s,%s)' %(Id, mem, cpu, rx, tx))
    conn.commit()  
    conn.close()

def get_container_data():

    client = docker.from_env()
    node_list = client.nodes.list()
    node_ip_list = []

    #ip find
    if node_list != None:
        for node in node_list:
            node_ip_list.append(node.attrs['Status']['Addr'])     

    container_list = []
    for ip in node_ip_list:
        client = docker.DockerClient(base_url = 'tcp://'+ip+':5678')
        container_list.extend(client.containers.list())
    

    if container_list != None:
        for container in container_list:
            memory, cpu,  tx ,rx = computmcn(container)
            Id = container.attrs['Id'] 

            mem = round(memory, 2)
            cpu = round(cpu, 2)
            tx = round(tx, 2)
            rx = round(rx, 2)

            insert_container(Id, mem, cpu, rx, tx)





if __name__ == '__main__':
    
    Flag = True
    #i = 1
    create_ctable()

    while Flag:
        start = time.time()

        get_container_data()
        #i += 1

        end = time.time()
        print ('total time: '+str(end-start))

        #if i == 3:
        #    Flag = False
        time.sleep(20)
