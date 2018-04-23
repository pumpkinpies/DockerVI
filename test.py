import docker
client = docker.from_env()
Info = client.networks.list(names='host',greedy=True)
print (Info)
