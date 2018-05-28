"""dockervi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import Dashboard,Containers, Images,Volumes,Networks
from Containers.views import ContainerInfo,Stats,Chart
from Swarm.views import Nodes,Services,ServicesChart,NodesInfo


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Dashboard),
    url(r'^Containers$',Containers),
    url(r'^Containers/(\w+)$',ContainerInfo),
    url(r'^Containers/(\w+)/Stats$', Stats),
    url(r'^Containers/(\w+)/Stats/chart$', Chart),
    url(r'^Images$', Images),
    url(r'^Volumes$', Volumes),
    url(r'^Networks$', Networks),
    url(r'^Swarm$', Nodes),
    url(r'^Swarm/(\w+)/Service$', Services),
    url(r'^Swarm/(\w+)/Service/chart$', ServicesChart),
    url(r'^Swarm/(\d+.\d+.\d+.\d+)/Node$', NodesInfo),
]

