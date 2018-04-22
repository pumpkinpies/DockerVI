import docker
client = docker.from_env()
Info = client.networks.list()
print (Info)
