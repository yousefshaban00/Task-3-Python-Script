# Python Task

**Implement a Python or Golang app / script to perform a periodically health-check for the cluster/apps  i.e usage of the pods (cpu,memory), status of pod/node etc. without using kubectl if possible.**


### Step 00: We need to install python and Kubernetes Python client library

install python

python --version

pip install kubernetes

pip install tabulate


### Step 01: We need to import Python client and config from Kubernetes Python client library


**Official Python client library for kubernetes - GitHub**
 - https://github.com/kubernetes-client/python
 
**Documentation**
- All APIs and Models' documentation can be found at the Generated client's README file [link](https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md) 



``` 
from kubernetes import client, config
import json
from tabulate import tabulate

print("Hello")
# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

# Create a client for the CoreV1Api API
v1 = client.CoreV1Api()
# Create a client for the AppsV1Ap API
api_apps= client.AppsV1Api()
# Create a client for the CustomObjectsApi API
api_metric = client.CustomObjectsApi()
# Create a client for the NetworkingV1Api API
api_nw = client.NetworkingV1Api()
# Create a client for the batch/v1 API
api_batch = client.BatchV1Api()
# Create a client for the RbacAuthorizationV1Api API
rbac_client = client.RbacAuthorizationV1Api()
``` 

## Step 02: Functions for Pods

### Step 02.1: We define function to check all pod status and ips.

 
```python
def pod_status():

    ret = v1.list_pod_for_all_namespaces(watch=False)
    #print(ret)
    print("%s\t\t\t%s\t\t\t%s\t\t\t%s" % ("IP", "namespace" , "Pod name", "Status"))
    for i in ret.items:
        print("%s\t\t%s\t\t%s\t\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name, i.status.phase))

pod_status()

```

Output
```python
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
Listing pods with resources:
IP                      namespace                       Pod name                        Status
10.0.2.167              amazon-cloudwatch               cloudwatch-agent-558q8          Running
10.0.1.72               amazon-cloudwatch               cloudwatch-agent-tfh4d          Running
10.0.112.51             amazon-cloudwatch               cloudwatch-agent-x88hj          Running
10.0.112.54             amazon-cloudwatch               fluent-bit-5nxtq                Running
10.0.2.176              amazon-cloudwatch               fluent-bit-q854p                Running
10.0.1.254              amazon-cloudwatch               fluent-bit-qlljx                Running
10.0.2.243              default         app3-nginx-deployment-cd48c8ffb-8mzc7           Running
10.0.1.177              interview               hello-world-de-67ccdb96c7-bfpk7         Running
10.0.2.177              interview               hello-world-es-68b8676bd6-8czl2         Running
10.0.1.190              interview               hello-world-eu-748db46546-f55sm         Running
10.0.112.237            interview               hello-world-fr-56b5cd5569-2blxj         Running
10.0.112.14             istio-ingress           istio-ingress-54464bcb87-ck9g6          Running


```

### Step 02.2: We define function to check usage CPU/MEMROY utilization for Pods.


```python
def pod_cpu_mem_util():
    namespaces = v1.list_namespace()
    for namespace in namespaces.items:
                   # List all pods in the namespace
                    print(namespace.metadata.name)
                    pods = v1.list_namespaced_pod(namespace=namespace.metadata.name)
                    for pod in pods.items:
                        # Get the pod metrics from the metrics-server
                        pod_metrics = api_metric.get_namespaced_custom_object(
                            group="metrics.k8s.io",
                            version="v1beta1",
                            namespace=namespace.metadata.name,
                            plural="pods",
                            name=pod.metadata.name
                        )
                        # Print the CPU and memory usage of the pod
                        cpu_usage = pod_metrics["containers"][0]["usage"]["cpu"]
                        memory_usage = pod_metrics["containers"][0]["usage"]["memory"]
                        print(f"{namespace.metadata.name}/{pod.metadata.name}: CPU usage={cpu_usage}, Memory usage={memory_usage}")

```


```python
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py

mazon-cloudwatch
amazon-cloudwatch/cloudwatch-agent-558q8: CPU usage=4892162n, Memory usage=38284Ki
amazon-cloudwatch/cloudwatch-agent-tfh4d: CPU usage=5484058n, Memory usage=40836Ki
amazon-cloudwatch/cloudwatch-agent-x88hj: CPU usage=5247023n, Memory usage=36348Ki
amazon-cloudwatch/fluent-bit-5nxtq: CPU usage=811030n, Memory usage=30092Ki
amazon-cloudwatch/fluent-bit-q854p: CPU usage=960478n, Memory usage=27376Ki
amazon-cloudwatch/fluent-bit-qlljx: CPU usage=1361353n, Memory usage=34652Ki
default
default/app3-nginx-deployment-cd48c8ffb-8mzc7: CPU usage=126884n, Memory usage=10336Ki
dev
interview
interview/hello-world-de-67ccdb96c7-bfpk7: CPU usage=0, Memory usage=14540Ki
interview/hello-world-es-68b8676bd6-8czl2: CPU usage=0, Memory usage=14536Ki
interview/hello-world-eu-748db46546-f55sm: CPU usage=0, Memory usage=14332Ki
interview/hello-world-fr-56b5cd5569-2blxj: CPU usage=0, Memory usage=14484Ki
interviewx
istio-ingress
istio-ingress/istio-ingress-54464bcb87-ck9g6: CPU usage=2699078n, Memory usage=36604Ki
istio-system
istio-system/istio-egressgateway-688d4797cd-v6sn6: CPU usage=2682460n, Memory usage=35256Ki
istio-system/istio-ingressgateway-6c67bdc48-m57tz: CPU usage=3026131n, Memory usage=34940Ki
istio-system/istiod-68fdb87f7-rsxlq: CPU usage=1703009n, Memory usage=47560Ki
kube-node-lease
kube-public
kube-system
kube-system/aws-node-bsfh5: CPU usage=2292499n, Memory usage=35144Ki
kube-system/aws-node-jjl28: CPU usage=3111146n, Memory usage=35404Ki
kube-system/aws-node-lq97k: CPU usage=2751071n, Memory usage=36432Ki
kube-system/coredns-79989457d9-9q6d8: CPU usage=1102433n, Memory usage=14744Ki
kube-system/coredns-79989457d9-jtmlp: CPU usage=742065n, Memory usage=15084Ki
kube-system/ebs-csi-controller-69774c68f4-p6svn: CPU usage=138866n, Memory usage=12076Ki
kube-system/ebs-csi-controller-69774c68f4-t5dgt: CPU usage=65406n, Memory usage=8048Ki
kube-system/ebs-csi-node-4sxqh: CPU usage=98922n, Memory usage=7036Ki
kube-system/ebs-csi-node-f4cdz: CPU usage=90127n, Memory usage=6820Ki
kube-system/ebs-csi-node-xn7zg: CPU usage=86454n, Memory usage=7084Ki
kube-system/kube-proxy-hs7cm: CPU usage=138934n, Memory usage=12856Ki
kube-system/kube-proxy-plcp7: CPU usage=44922n, Memory usage=12936Ki
kube-system/kube-proxy-r2xrr: CPU usage=229861n, Memory usage=12892Ki
kube-system/radio-dev-ca-aws-cluster-autoscaler-68b99987b8-6vzcc: CPU usage=1992904n, Memory usage=31812Ki
kube-system/radio-dev-metrics-server-54666cdb8c-x4qgq: CPU usage=2921747n, Memory usage=17968Ki

```

### Step 02.3: We define function to check CPU and MEMORY request and limit for each __Container__ of Pods.

 
```python
# cpu and memory request and limit for each container 
def podcpumem():

    pods = v1.list_pod_for_all_namespaces(watch=False)
    try:
        for pod in pods.items:
            for container in pod.spec.containers:
                cpu_request = container.resources.requests.get("cpu", 0)
                cpu_limit = container.resources.limits.get("cpu", 0)
                memory_request = container.resources.requests.get("memory", 0)
                memory_limit = container.resources.limits.get("memory", 0)
                print(f"{pod.metadata.name}/{container.name}: CPU request={cpu_request}, CPU limit={cpu_limit}: memory request={memory_request}, memory limit={memory_limit}")
    except Exception as e:
     print("")

```

Output
```python
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
cloudwatch-agent-558q8/cloudwatch-agent: CPU request=200m, CPU limit=200m: memory request=200Mi, memory limit=200Mi
cloudwatch-agent-tfh4d/cloudwatch-agent: CPU request=200m, CPU limit=200m: memory request=200Mi, memory limit=200Mi
cloudwatch-agent-x88hj/cloudwatch-agent: CPU request=200m, CPU limit=200m: memory request=200Mi, memory limit=200Mi
fluent-bit-5nxtq/fluent-bit: CPU request=500m, CPU limit=0: memory request=100Mi, memory limit=200Mi
fluent-bit-q854p/fluent-bit: CPU request=500m, CPU limit=0: memory request=100Mi, memory limit=200Mi
fluent-bit-qlljx/fluent-bit: CPU request=500m, CPU limit=0: memory request=100Mi, memory limit=200Mi
app3-nginx-deployment-cd48c8ffb-8mzc7/app3-nginx: CPU request=200m, CPU limit=500m: memory request=0, memory limit=0



```




### Step 02.4: We define function to check Images for each __Container__ of Pods.

 
```python
def podimage():

    # Get the pod
    pod = v1.list_pod_for_all_namespaces(watch=False)

    # Get the container images of the pod
    #container_images = [container.image for container in pod.spec.containers]
    for pod in pod.items:
        for container in pod.spec.containers:
            print(f"{pod.metadata.name}:{container.name}: {container.image}")


```

Output
```python
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
cloudwatch-agent-558q8:cloudwatch-agent: amazon/cloudwatch-agent:1.247354.0b251981
cloudwatch-agent-tfh4d:cloudwatch-agent: amazon/cloudwatch-agent:1.247354.0b251981
cloudwatch-agent-x88hj:cloudwatch-agent: amazon/cloudwatch-agent:1.247354.0b251981
fluent-bit-5nxtq:fluent-bit: public.ecr.aws/aws-observability/aws-for-fluent-bit:stable
fluent-bit-q854p:fluent-bit: public.ecr.aws/aws-observability/aws-for-fluent-bit:stable
fluent-bit-qlljx:fluent-bit: public.ecr.aws/aws-observability/aws-for-fluent-bit:stable
app3-nginx-deployment-cd48c8ffb-8mzc7:app3-nginx: k8s.gcr.io/hpa-example
hello-world-de-67ccdb96c7-bfpk7:hello-world-de: adamgolab/hello-world:latest
hello-world-de-67ccdb96c7-bfpk7:istio-proxy: docker.io/istio/proxyv2:1.16.1
hello-world-es-68b8676bd6-8czl2:hello-world-es: adamgolab/hello-world:latest
hello-world-es-68b8676bd6-8czl2:istio-proxy: docker.io/istio/proxyv2:1.16.1
hello-world-eu-748db46546-f55sm:hello-world-de: adamgolab/hello-world:latest
hello-world-eu-748db46546-f55sm:istio-proxy: docker.io/istio/proxyv2:1.16.1
hello-world-fr-56b5cd5569-2blxj:hello-world-fr: adamgolab/hello-world:latest
hello-world-fr-56b5cd5569-2blxj:istio-proxy: docker.io/istio/proxyv2:1.16.1
istio-ingress-54464bcb87-ck9g6:istio-proxy: docker.io/istio/proxyv2:1.16.1
istio-egressgateway-688d4797cd-v6sn6:istio-proxy: docker.io/istio/proxyv2:1.16.1
istio-ingressgateway-6c67bdc48-m57tz:istio-proxy: docker.io/istio/proxyv2:1.16.1
istiod-68fdb87f7-rsxlq:discovery: docker.io/istio/pilot:1.16.1
aws-node-bsfh5:aws-node: 602401143452.dkr.ecr.us-east-1.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1
aws-node-jjl28:aws-node: 602401143452.dkr.ecr.us-east-1.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1
aws-node-lq97k:aws-node: 602401143452.dkr.ecr.us-east-1.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1
coredns-79989457d9-9q6d8:coredns: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/coredns:v1.8.7-eksbuild.3
coredns-79989457d9-jtmlp:coredns: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/coredns:v1.8.7-eksbuild.3
ebs-csi-controller-69774c68f4-p6svn:ebs-plugin: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/aws-ebs-csi-driver:v1.14.0
ebs-csi-controller-69774c68f4-p6svn:csi-provisioner: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-provisioner:v3.3.0-eks-1-23-6
ebs-csi-controller-69774c68f4-p6svn:csi-attacher: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-attacher:v4.0.0-eks-1-23-6   
ebs-csi-controller-69774c68f4-p6svn:csi-snapshotter: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-snapshotter:v6.1.0-eks-1-23-6
ebs-csi-controller-69774c68f4-p6svn:csi-resizer: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-resizer:v1.6.0-eks-1-23-6     
ebs-csi-controller-69774c68f4-p6svn:liveness-probe: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/livenessprobe:v2.8.0-eks-1-24-4ebs-csi-controller-69774c68f4-t5dgt:ebs-plugin: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/aws-ebs-csi-driver:v1.14.0
ebs-csi-controller-69774c68f4-t5dgt:csi-provisioner: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-provisioner:v3.3.0-eks-1-23-6
ebs-csi-controller-69774c68f4-t5dgt:csi-attacher: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-attacher:v4.0.0-eks-1-23-6   
ebs-csi-controller-69774c68f4-t5dgt:csi-snapshotter: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-snapshotter:v6.1.0-eks-1-23-6
ebs-csi-controller-69774c68f4-t5dgt:csi-resizer: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-resizer:v1.6.0-eks-1-23-6     
ebs-csi-controller-69774c68f4-t5dgt:liveness-probe: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/livenessprobe:v2.8.0-eks-1-24-4ebs-csi-node-4sxqh:ebs-plugin: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/aws-ebs-csi-driver:v1.14.0
ebs-csi-node-4sxqh:node-driver-registrar: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-node-driver-registrar:v2.6.1-eks-1-24-4
ebs-csi-node-4sxqh:liveness-probe: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/livenessprobe:v2.8.0-eks-1-24-4
ebs-csi-node-f4cdz:ebs-plugin: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/aws-ebs-csi-driver:v1.14.0
ebs-csi-node-f4cdz:node-driver-registrar: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-node-driver-registrar:v2.6.1-eks-1-24-4
ebs-csi-node-f4cdz:liveness-probe: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/livenessprobe:v2.8.0-eks-1-24-4
ebs-csi-node-xn7zg:ebs-plugin: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/aws-ebs-csi-driver:v1.14.0
ebs-csi-node-xn7zg:node-driver-registrar: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/csi-node-driver-registrar:v2.6.1-eks-1-24-4
ebs-csi-node-xn7zg:liveness-probe: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/livenessprobe:v2.8.0-eks-1-24-4
kube-proxy-hs7cm:kube-proxy: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/kube-proxy:v1.24.7-minimal-eksbuild.2
kube-proxy-plcp7:kube-proxy: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/kube-proxy:v1.24.7-minimal-eksbuild.2
kube-proxy-r2xrr:kube-proxy: 602401143452.dkr.ecr.us-east-1.amazonaws.com/eks/kube-proxy:v1.24.7-minimal-eksbuild.2
radio-dev-ca-aws-cluster-autoscaler-68b99987b8-6vzcc:aws-cluster-autoscaler: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.23.0      
radio-dev-metrics-server-54666cdb8c-x4qgq:metrics-server: k8s.gcr.io/metrics-server/metrics-server:v0.6.2
nginx-ingress-controller-ingress-nginx-controller-8484ddcb7lnnm:controller: registry.k8s.io/ingress-nginx/controller:v1.5.1@sha256:4ba73c697770664c1e00e9f968de14e08f606ff961c76e5d7033a4a9c593c629
nginx-ingress-controller-ingress-nginx-controller-8484ddcb7lnnm:istio-proxy: docker.io/istio/proxyv2:1.16.1


```





### Step 02.5: We define function to Print the name of each pod that has a non-zero restartCount

 
```python
def restartpod():
    # List all pods
    pods = v1.list_pod_for_all_namespaces()

    # Print the name of each pod that has a non-zero restartCount
    for pod in pods.items:
        if pod.status.container_statuses[0].restart_count > 0:
            print(f"# Print the name of each pod that has a non-zero restartCount: {pod.metadata.name} namespace: {pod.metadata.namespace}")


```

Output
```python
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
# Print the name of each pod that has a non-zero restartCount: fluent-bit-qlljx namespace: amazon-cloudwatch
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> kubectl get pod fluent-bit-qlljx  -n amazon-cloudwatch
NAME               READY   STATUS    RESTARTS        AGE
fluent-bit-qlljx   1/1     Running   1 (3d10h ago)   3d10h



```


## Step 03: Functions for Nodes
### Step 03.1: We define function to check usage CPU/MEMROY utilization for Nodes.


```python
def nodemetric():
# List all nodes
#metrics_client = client.MetricsV1beta1Api()
    #nodes = v1.list_node_metrics()  
    node = v1.list_node()
    for node in node.items:
        print(node.metadata.name)
        node_metrics = api_metric.get_cluster_custom_object(
                                group="metrics.k8s.io",
                                version="v1beta1",
                            # namespace=namespace.metadata.name,
                                plural="nodes",
                                name=node.metadata.name
                            )
       # print(node_metrics)
             # Print the CPU and memory usage of the pod
        cpu_memroy_usage  = node_metrics["usage"]
        print(cpu_memroy_usage)

```


Output
```python
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
ip-10-0-1-254.ec2.internal
{'cpu': '73105537n', 'memory': '1121608Ki'}
ip-10-0-112-54.ec2.internal
{'cpu': '59928424n', 'memory': '1168696Ki'}
ip-10-0-2-176.ec2.internal
{'cpu': '55849814n', 'memory': '1002372Ki'}

```


### Step 03.2: We define function to check  status for Nodes.


```python
def nodestatus():
    print("Listing node with status:")
    nodes = v1.list_node(watch=False)
    #nodes =v1.read_node()
    #print(nodes)
    print("%s\t\t%s\t\t%s\t\t%s\t\t\t%s" % ("Node Name", "Node Instance Type","internal IP", "External IP" ,"status"))
    for i in nodes.items:
        label = i.metadata.labels
        instance_type = label.get('beta.kubernetes.io/instance-type')
        ip_address_internal = i.status.addresses[0].address
        ip_address_ex = i.status.addresses[1].address

```


Output
```python
PS C:\terraform-on-aws-eks-main\New folder\Get_Course> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
Listing node with status:
Node Name               Node Instance Type              internal IP             External IP                     status
ip-10-0-1-254.ec2.internal      t3.large                10.0.1.254              ip-10-0-1-254.ec2.internal              Ready
ip-10-0-112-54.ec2.internal     t3.medium               10.0.112.54             54.198.200.79           Ready
ip-10-0-2-176.ec2.internal      t3.large                10.0.2.176              ip-10-0-2-176.ec2.internal              Ready

```




## Step 04: Functions for deployments
### Step 04.1: We define function to Print Desired replicas","Current replicas","Ready replicas" for Deplotments


```python
def deploytab():
    # Data to be included in the table
    data = []   
    deployment = api_apps.list_deployment_for_all_namespaces()
   # print("%s\t%s\t%s\t%s" % ("deployment name", "Desired replicas", "Current replicas","Ready replicas"))
    for i in deployment.items:
        #x = i.spec.replicas
        #print(x)
       # print("%s\t%s\t%s\t%s" % (i.metadata.name, i.spec.replicas, i.status.replicas,i.status.ready_replicas))
        data.append([i.metadata.name, i.spec.replicas, i.status.replicas,i.status.ready_replicas])

    table = tabulate(data, headers=["deployment name", "Desired replicas","Current replicas","Ready replicas"], tablefmt="grid")
    print(table)

```


To output the results of a for loop as a formatted table in Python, you can use the **tabulate library**. tabulate is a Python library that allows you to easily create formatted tables in Python.


Output
```python
PS C:\terraform-on-aws-eks-main\New folder\Get_Course> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
+---------------------------------------------------+--------------------+--------------------+------------------+
| deployment name                                   |   Desired replicas |   Current replicas |   Ready replicas |
+===================================================+====================+====================+==================+
| app3-nginx-deployment                             |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| hello-world-de                                    |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| hello-world-es                                    |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| hello-world-eu                                    |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| hello-world-fr                                    |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| istio-ingress                                     |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| istio-egressgateway                               |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| istio-ingressgateway                              |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| istiod                                            |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| coredns                                           |                  2 |                  2 |                2 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| ebs-csi-controller                                |                  2 |                  2 |                2 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| radio-dev-ca-aws-cluster-autoscaler               |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| radio-dev-metrics-server                          |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+
| nginx-ingress-controller-ingress-nginx-controller |                  1 |                  1 |                1 |
+---------------------------------------------------+--------------------+--------------------+------------------+

```



## Step:05 Function for Ingress
### Step 05.1: We define function to Print details of Ingress


```python
def ingress():
    # List all ingresses
    ingresses = api_nw.list_ingress_for_all_namespaces()

    # Print the name, namespace, and rules of each ingress
    for ingress in ingresses.items:
        print(f"Ingress: {ingress.metadata.name}")
        print(f"Namespace: {ingress.metadata.namespace}")
        print(f"Rules:")
        for rule in ingress.spec.rules:
            print(f"  Host: {rule.host}")
            print(f"  Path: {rule.http.paths[0].path}")
            print(f"  Backend: {rule.http.paths[0].backend.service.name}:{rule.http.paths[0].backend.service.port}")
        print()

```


Output
```python
PS C:\terraform-on-aws-eks-main\New folder\Get_Course> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
Ingress: xyz-x
Namespace: interview
Rules:
  Host: None
  Path: /de
  Backend: hello-world-de:{'name': None, 'number': 80}
  Host: None
  Path: /fr
  Backend: hello-world-fr:{'name': None, 'number': 80}
  Host: None
  Path: /es
  Backend: hello-world-es:{'name': None, 'number': 80}

```


## Step:06 Function for Namespaces
### Step 06.1: We define function to Print namespace without any workload 


```python
def ns_no_workload():
    namespaces = v1.list_namespace()
    #exception if empty pod ? pod status running 
    for namespace in namespaces.items:
       
        pods = v1.list_namespaced_pod(namespace=namespace.metadata.name)
        lenx =len(pods.items)
        #print(lenx)
        if lenx == 0:
                print(namespace.metadata.name)


```


Output
```python
PS C:\terraform-on-aws-eks-main\New folder\Get_Course> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
dev
interviewx
kube-node-lease
kube-public

```


## Step:07 Function for Persistent Voumes and Persistent Voumes Claims 
### Step 07.1: We define function to Print status of Persistent Voumes and Persistent Voumes Claims 


```python
def p_volume():
    pvs = v1.list_persistent_volume()

    # Print the status of each PV
    print("Persistent Volume (PV)")
    for pv in pvs.items:
        print(f"{pv.metadata.name}: {pv.status.phase}")

        # List all PVCs in the namespace
        pvcs = v1.list_persistent_volume_claim_for_all_namespaces()

        # Print the status of each PVC
    print("Persistent Volume Claim (PVC)")
    for pvc in pvcs.items:
        print(f"{pvc.metadata.name}: {pvc.status.phase}")

```


Output
```python
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
Persistent Volume (PV)
pv-volume-2: Bound
Persistent Volume Claim (PVC)
pvc-claim-2: Bound

```

## Step:08 Function for Jobs
### Step 08.1: We define function to Print status of Jobs


```python
def jobs():
    # Get the namespace to list jobs in
    #namespace = "default"

    # List all jobs in the namespace
    #jobs = api_batch.list_namespaced_job(namespace=namespace)
    namespaces = v1.list_namespace()
    # Print the status of each job
    for namespace in namespaces.items:
                   # List all pods in the namespace
        jobs = api_batch.list_namespaced_job(namespace=namespace.metadata.name)
        print(namespace.metadata.name)
        for job in jobs.items:
            print(f"Job {job.metadata.name}: status={job.status.conditions[0].type}")
```


## Step:09 Function for Service Accpimt & Role,ClusterRole, Rolebinding,ClusterRoleBinding

### Step 09.1: We define function to Print Service Accounts with Annotations 



```python
def sa_annotation():
    # Get the namespace to list service accounts in
    #namespace = "default"
    data = [] 
    namespaces = v1.list_namespace()
    for namespace in namespaces.items:
        # List all service accounts in the namespace
        service_accounts = v1.list_namespaced_service_account(namespace=namespace.metadata.name)

        # Print the status of each service account
        for service_account in service_accounts.items:
             data.append([service_account.metadata.name,service_account.metadata.namespace,service_account.metadata.annotations])
           # print(f"Service account {service_account.metadata.name} : namespace={service_account.metadata.namespace}: Annotations={service_account.metadata.annotations}")
    table = tabulate(data, headers=["service_account_name", "service account namespace","service account annotations"], tablefmt="simple")
    print(table)


```


Output
```python
service_account_name                    service account namespace    service account annotations
--------------------------------------  ---------------------------  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
cloudwatch-agent                        amazon-cloudwatch            {'kubectl.kubernetes.io/last-applied-configuration': '{"apiVersion":"v1","kind":"ServiceAccount","metadata":{"annotations":{},"name":"cloudwatch-agent","namespace":"amazon-cloudwatch"}}\n'}
default                                 amazon-cloudwatch
fluent-bit                              amazon-cloudwatch            {'kubectl.kubernetes.io/last-applied-configuration': '{"apiVersion":"v1","kind":"ServiceAccount","metadata":{"annotations":{},"name":"fluent-bit","namespace":"amazon-cloudwatch"}}\n'}
default                                 default


```
### Step 09.2: We define function to Print service account name with role


```python
def role_sa():


    # List all role bindings in the cluster
    role_bindings = rbac_client.list_role_binding_for_all_namespaces().items
    data = [] 
    # Print the subject name and role name of each role binding
    for role_binding in role_bindings:
        subject_name = role_binding.subjects[0].name
        subject_namespace = role_binding.subjects[0].namespace
        role_name = role_binding.role_ref.name
        data.append([subject_name,subject_namespace,role_name])
        #print(f"Role binding {role_binding.metadata.name}: subject_name={subject_name},: subject_namespace={subject_namespace}, role={role_name}")
    table = tabulate(data, headers=[ "Subject name","Subject namespace","role_name"], tablefmt="grid")
    print(table)

```

Output
```python
--------------------------+
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
+----------------------------------------+--------------------------+------------------------------------------------+
| Subject name                           | Subject namespace        | role_name                                      |
+========================================+==========================+================================================+
| eks-developer-group                    | default                  | radio-dev-eksdeveloper-role                    |
+----------------------------------------+--------------------------+------------------------------------------------+
| istio-ingress                          |                          | istio-ingress                                  |
+----------------------------------------+--------------------------+------------------------------------------------+
| istio-egressgateway-service-account    |                          | istio-egressgateway-sds                        |
+----------------------------------------+--------------------------+------------------------------------------------+
| istio-ingressgateway-service-account   |                          | istio-ingressgateway-sds                       |
+----------------------------------------+--------------------------+------------------------------------------------+
| istiod                                 | istio-system             | istiod                                         |
+----------------------------------------+--------------------------+------------------------------------------------+
| istiod-service-account                 | istio-system             | istiod-istio-system                            |
+----------------------------------------+--------------------------+------------------------------------------------+
| bootstrap-signer                       | kube-system              | system:controller:bootstrap-signer             |
+----------------------------------------+--------------------------+------------------------------------------------+
| eks:vpc-resource-controller            |                          | eks-vpc-resource-controller-role               |
+----------------------------------------+--------------------------+------------------------------------------------+
| eks:addon-manager                      |                          | eks:addon-manager                              |
+----------------------------------------+--------------------------+------------------------------------------------+
| eks:authenticator                      |                          | eks:authenticator                              |
+----------------------------------------+--------------------------+------------------------------------------------+
| eks:certificate-controller             |                          | eks:certificate-controller                     |
+----------------------------------------+--------------------------+------------------------------------------------+
| eks:cloud-controller-manager           |                          | extension-apiserver-authentication-reader      |
+----------------------------------------+--------------------------+------------------------------------------------+
| eks:fargate-manager                    |                          | eks:fargate-manager                            |
+----------------------------------------+--------------------------+------------------------------------------------+
| eks:k8s-metrics                        |                          | eks:k8s-metrics                                |
+----------------------------------------+--------------------------+------------------------------------------------+
| eks:node-manager                       |                          | eks:node-manager                               |
+----------------------------------------+--------------------------+------------------------------------------------+
| cluster-autoscaler                     | kube-system              | radio-dev-ca-aws-cluster-autoscaler            |
+----------------------------------------+--------------------------+------------------------------------------------+
| radio-dev-metrics-server               | kube-system              | extension-apiserver-authentication-reader      |
+----------------------------------------+--------------------------+------------------------------------------------+
| system:kube-controller-manager         |                          | extension-apiserver-authentication-reader      |
+----------------------------------------+--------------------------+------------------------------------------------+
| system:kube-controller-manager         |                          | system::leader-locking-kube-controller-manager |
+----------------------------------------+--------------------------+------------------------------------------------+
| system:kube-scheduler                  |                          | system::leader-locking-kube-scheduler          |
+----------------------------------------+--------------------------+------------------------------------------------+
| bootstrap-signer                       | kube-system              | system:controller:bootstrap-signer             |
+----------------------------------------+--------------------------+------------------------------------------------+
| cloud-provider                         | kube-system              | system:controller:cloud-provider               |
+----------------------------------------+--------------------------+------------------------------------------------+
| token-cleaner                          | kube-system              | system:controller:token-cleaner                |
+----------------------------------------+--------------------------+------------------------------------------------+
| nginx-ingress-controller-ingress-nginx | nginx-ingress-controller | nginx-ingress-controller-ingress-nginx         |
+----------------------------------------+--------------------------+------------------------------------------------+

```

### Step 09.3: We define function to Print roles for service accounts 


```python
def roles():
    # Set the namespace and name of the role to get
    #namespace = "default"
    #name = "radio-dev-eksdeveloper-role "

    # Get the role
    #role = rbac_client.read_namespaced_role(name=name, namespace=namespace)
    roles = rbac_client.list_role_for_all_namespaces().items
    for role in roles:
        print(f"Role {role.metadata.name} in namespace {role.metadata.namespace} ")
    #print(roles)
    # Print the rules of the role
        for i in role.rules:
            print(f"Rule: api_groups={i.api_groups}, resources={i.resources}, verbs={i.verbs}")
        print("\n")

```

Output
```python
PS C:\terraform-on-aws-eks-main\Task\Istio-Task\Task-3-python> & C:/Users/hp/AppData/Local/Programs/Python/Python311/python.exe c:/terraform-on-aws-eks-main/Task/Istio-Task/Task-3-python/test.py
Hello
Role radio-dev-eksdeveloper-role in namespace dev 
Rule: api_groups=['', 'apps', 'extensions'], resources=['*'], verbs=['*']
Rule: api_groups=['batch'], resources=['jobs', 'cronjobs'], verbs=['*']


Role istio-ingress in namespace istio-ingress
Rule: api_groups=[''], resources=['secrets'], verbs=['get', 'watch', 'list']


Role istio-egressgateway-sds in namespace istio-system
Rule: api_groups=[''], resources=['secrets'], verbs=['get', 'watch', 'list']


Role istio-ingressgateway-sds in namespace istio-system
Rule: api_groups=[''], resources=['secrets'], verbs=['get', 'watch', 'list']


Role istiod in namespace istio-system
Rule: api_groups=['networking.istio.io'], resources=['gateways'], verbs=['create']
Rule: api_groups=[''], resources=['secrets'], verbs=['create', 'get', 'watch', 'list', 'update', 'delete']
Rule: api_groups=[''], resources=['configmaps'], verbs=['delete']


Role istiod-istio-system in namespace istio-system
Rule: api_groups=['networking.istio.io'], resources=['gateways'], verbs=['create']
Rule: api_groups=[''], resources=['secrets'], verbs=['create', 'get', 'watch', 'list', 'update', 'delete']


Role system:controller:bootstrap-signer in namespace kube-public
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'list', 'watch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['update']
Rule: api_groups=['', 'events.k8s.io'], resources=['events'], verbs=['create', 'patch', 'update']


Role eks-vpc-resource-controller-role in namespace kube-system
Rule: api_groups=['apps'], resources=['deployments'], verbs=['get', 'list', 'watch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'list', 'watch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['create', 'list', 'watch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'update', 'patch']
Rule: api_groups=[''], resources=['events'], verbs=['create']
Rule: api_groups=['coordination.k8s.io'], resources=['leases'], verbs=['create']
Rule: api_groups=['coordination.k8s.io'], resources=['leases'], verbs=['get', 'update']


Role eks:addon-manager in namespace kube-system
Rule: api_groups=['policy'], resources=['poddisruptionbudgets'], verbs=['create', 'delete', 'get', 'list', 'patch', 'update', 'watch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['create', 'delete', 'get', 'list', 'patch', 'update', 'watch']
Rule: api_groups=['apps'], resources=['daemonsets'], verbs=['create', 'delete', 'get', 'list', 'patch', 'update', 'watch']
Rule: api_groups=['apps'], resources=['deployments'], verbs=['create', 'delete', 'get', 'list', 'patch', 'update', 'watch']
Rule: api_groups=[''], resources=['services'], verbs=['create', 'delete', 'get', 'list', 'patch', 'update', 'watch']
Rule: api_groups=[''], resources=['serviceaccounts'], verbs=['create', 'delete', 'get', 'list', 'patch', 'update', 'watch']


Role eks:authenticator in namespace kube-system
Rule: api_groups=[''], resources=['events'], verbs=['create', 'update', 'patch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'list', 'watch']


Role eks:certificate-controller in namespace kube-system
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'update', 'create']
Rule: api_groups=['coordination.k8s.io'], resources=['leases'], verbs=['create']
Rule: api_groups=['coordination.k8s.io'], resources=['leases'], verbs=['get', 'update']


Role eks:fargate-manager in namespace kube-system
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'update', 'patch', 'delete']
Rule: api_groups=[''], resources=['configmaps'], verbs=['create']
Rule: api_groups=[''], resources=['events'], verbs=['get', 'list']


Role eks:k8s-metrics in namespace kube-system
Rule: api_groups=['apps'], resources=['daemonsets'], verbs=['get']
Rule: api_groups=['apps'], resources=['deployments'], verbs=['get']


Role eks:node-manager in namespace kube-system
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'update', 'patch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['create']
Rule: api_groups=[''], resources=['events'], verbs=['get', 'list']


Role extension-apiserver-authentication-reader in namespace kube-system
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'list', 'watch']


Role radio-dev-ca-aws-cluster-autoscaler in namespace kube-system
Rule: api_groups=[''], resources=['configmaps'], verbs=['create']
Rule: api_groups=[''], resources=['configmaps'], verbs=['delete', 'get', 'update']


Role system::leader-locking-kube-controller-manager in namespace kube-system
Rule: api_groups=[''], resources=['configmaps'], verbs=['watch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'update']


Role system::leader-locking-kube-scheduler in namespace kube-system
Rule: api_groups=[''], resources=['configmaps'], verbs=['watch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'update']


Role system:controller:bootstrap-signer in namespace kube-system
Rule: api_groups=[''], resources=['secrets'], verbs=['get', 'list', 'watch']


Role system:controller:cloud-provider in namespace kube-system
Rule: api_groups=[''], resources=['configmaps'], verbs=['create', 'get', 'list', 'watch']


Role system:controller:token-cleaner in namespace kube-system
Rule: api_groups=[''], resources=['secrets'], verbs=['delete', 'get', 'list', 'watch']
Rule: api_groups=['', 'events.k8s.io'], resources=['events'], verbs=['create', 'patch', 'update']


Role nginx-ingress-controller-ingress-nginx in namespace nginx-ingress-controller
Rule: api_groups=[''], resources=['namespaces'], verbs=['get']
Rule: api_groups=[''], resources=['configmaps', 'pods', 'secrets', 'endpoints'], verbs=['get', 'list', 'watch']
Rule: api_groups=[''], resources=['services'], verbs=['get', 'list', 'watch']
Rule: api_groups=['networking.k8s.io'], resources=['ingresses'], verbs=['get', 'list', 'watch']
Rule: api_groups=['networking.k8s.io'], resources=['ingresses/status'], verbs=['update']
Rule: api_groups=['networking.k8s.io'], resources=['ingressclasses'], verbs=['get', 'list', 'watch']
Rule: api_groups=[''], resources=['configmaps'], verbs=['get', 'update']
Rule: api_groups=[''], resources=['configmaps'], verbs=['create']
Rule: api_groups=['coordination.k8s.io'], resources=['leases'], verbs=['get', 'update']
Rule: api_groups=['coordination.k8s.io'], resources=['leases'], verbs=['create']
Rule: api_groups=[''], resources=['events'], verbs=['create', 'patch']
Rule: api_groups=['discovery.k8s.io'], resources=['endpointslices'], verbs=['list', 'watch', 'get']

```

## Final : Build Dockerfile for python kubernetes Script to test Health status for cluster

A Dockerfile is a text file that contains instructions for building a Docker image. It specifies the base image to use, the dependencies to install, and any additional configuration or commands to run.

**requirements.txt**
kubernetes
tabulate

**Dockerfile**


```Bash
COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update
RUN curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.7/2022-10-31/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
RUN mv kubectl /usr/local/bin/
RUN kubectl version --short --client
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install -i /usr/local/aws-cli -b /usr/local/bin
RUN region=$(aws ec2 describe-availability-zones --output text --query 'AvailabilityZones[0].[RegionName]')
RUN echo $region
RUN cluster_name = $(aws eks list-clusters --query 'clusters[0]' --output text)
RUN echo $cluster_name
RUN aws eks update-kubeconfig --name $cluster_name --region $region

#RUN aws eks update-kubeconfig --name radio-dev-ekstask1 --profile default --region us-east-1
#aws eks update-kubeconfig --name <cluster-name> --profile <profile-name> --region <region-name>
# ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
# Run app.py when the container launches
CMD ["python", "test.py"]
```
 
 docker build -t pythonimage .
docker tag pythonimage yousefshaban/kubpython:firsttry
docker push yousefshaban/kubpython:firsttry
 
 
## Run Docker Image to check Health status for Cluster
```python
PS C:\Allinaz_Task\Task-1-EKS-Terraform> kubectl run yousef --image=yousefshaban/kubpython:2.0.0

PS C:\Allinaz_Task\Task-1-EKS-Terraform> kubectl describe pod yousef 
Name:         yousef
Namespace:    default
Priority:     0
Node:         ip-10-0-1-254.ec2.internal/10.0.1.254
Start Time:   Wed, 28 Dec 2022 17:34:18 +0100
Labels:       run=yousef
Annotations:  kubernetes.io/psp: eks.privileged
Status:       Pending
IP:
IPs:          <none>
Containers:
  yousef:
    Container ID:
    Image:          yousefshaban/kubpython:2.0.0
    Image ID:
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       ContainerCreating
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-59sbz (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             False
  ContainersReady   False
Volumes:
  kube-api-access-59sbz:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  22s   default-scheduler  Successfully assigned default/yousef to ip-10-0-1-254.ec2.internal
  Normal  Pulling    22s   kubelet            Pulling image "yousefshaban/kubpython:2.0.0"
PS C:\Allinaz_Task\Task-1-EKS-Terraform> kubectl logs  yousef        
Hello
IP                      namespace                       Pod name                        Status
10.0.2.167              amazon-cloudwatch               cloudwatch-agent-558q8          Running
10.0.1.72               amazon-cloudwatch               cloudwatch-agent-tfh4d          Running
10.0.112.51             amazon-cloudwatch               cloudwatch-agent-x88hj          Running
10.0.112.54             amazon-cloudwatch               fluent-bit-5nxtq                Running
10.0.2.176              amazon-cloudwatch               fluent-bit-q854p                Running
10.0.1.254              amazon-cloudwatch               fluent-bit-qlljx                Running
10.0.2.243              default         app3-nginx-deployment-cd48c8ffb-8mzc7           Running
10.0.1.219              default         yousef          Running
10.0.1.177              interview               hello-world-de-67ccdb96c7-bfpk7         Running
10.0.2.177              interview               hello-world-es-68b8676bd6-8czl2         Running
10.0.1.190              interview               hello-world-eu-748db46546-f55sm         Running
10.0.112.237            interview               hello-world-fr-56b5cd5569-2blxj         Running
10.0.1.88               istio-ingress           istio-ingress-54464bcb87-4mt2f          Running
10.0.112.106            istio-system            istiod-7f8c8bb8c8-sb2rr         Running
10.0.1.254              kube-system             aws-node-bsfh5          Running
10.0.2.176              kube-system             aws-node-jjl28          Running
10.0.112.54             kube-system             aws-node-lq97k          Running
10.0.112.114            kube-system             coredns-79989457d9-9q6d8                Running
10.0.112.175            kube-system             coredns-79989457d9-jtmlp                Running
10.0.1.156              kube-system             ebs-csi-controller-69774c68f4-p6svn             Running
10.0.2.188              kube-system             ebs-csi-controller-69774c68f4-t5dgt             Running
10.0.2.73               kube-system             ebs-csi-node-4sxqh              Running
10.0.1.17               kube-system             ebs-csi-node-f4cdz              Running
10.0.112.166            kube-system             ebs-csi-node-xn7zg              Running
10.0.112.54             kube-system             kube-proxy-hs7cm                Running
10.0.1.254              kube-system             kube-proxy-plcp7                Running
10.0.2.176              kube-system             kube-proxy-r2xrr                Running
10.0.1.240              kube-system             radio-dev-ca-aws-cluster-autoscaler-68b99987b8-6vzcc            Running
10.0.2.147              kube-system             radio-dev-metrics-server-54666cdb8c-x4qgq               Running
10.0.2.138              kube-system             tiller-deploy-6679847b75-4nrkw          Pending
10.0.1.122              nginx-ingress-controller                nginx-ingress-controller-ingress-nginx-controller-f6fd8fbb82lz9         Running  
```

## AWS CodePipeline+CodeBuild using Terraform to make automation process for Python Task

**we use AWS CodePipeline to make automatically test,build and deploy python app (Cluster health check) as the follwoing steps:**


#### Step 00: We define Terraform Settings and provider `c1-version.tf`

```
terraform {
  required_version = ">= 1.0.0"
   required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.48.0"
     }
   }

  # Adding Backend as S3 for Remote State Storage
  backend "s3" {
    bucket = "aws-eks-terraform"
    key    = "dev/py-pipelinee/terraform.tfstate"
    region = "us-east-1" 

    # For State Locking
    dynamodb_table = "py-pipeline"    
  }    



}

provider "aws" {
  region = var.aws_region
}

```

#### Step 01: We define Github Source as Connection for Pipeline `c2-source.tf`


```

resource "aws_codestarconnections_connection" "github" {
  name = "github-connection"
  provider_type = "GitHub"
  #provider_version = "2"
  #host_arn = "arn:aws:codestar-connections:us-east-1:962490649366:connection/efs-1"
 # host_arn = aws_codestar_connections_host.github.arn
  #access_token_arn = "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:GITHUB_SECRET_NAME"
 # access_token_arn = "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:GITHUB_SECRET_NAME"

}



```


#### Step 02: We define IAM roles and Polices for AWS CodePipeline and CodeBuild `c3-iam-role-policy.tf`


```
resource "aws_iam_role" "containerAppBuildProjectRole" {
  name = "containerAppBuildProjectRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# add managed Polcy
# IAM full access

resource "aws_iam_policy_attachment" "IAMFullAccess" {
  name       = "IAMFullAccess"
  policy_arn = "arn:aws:iam::aws:policy/IAMFullAccess"
  roles      = [aws_iam_role.containerAppBuildProjectRole.name]
}

# S3 Full access
resource "aws_iam_policy_attachment" "AmazonS3FullAccess" {
  name       = "AmazonS3FullAccess"
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  roles      = [aws_iam_role.containerAppBuildProjectRole.name]
}

# DynamoDB full access
resource "aws_iam_policy_attachment" "AmazonDynamoDBFullAccess" {
  name       = "AmazonDynamoDBFullAccess"
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  roles      = [aws_iam_role.containerAppBuildProjectRole.name]
}


resource "aws_iam_role" "apps_codepipeline_role" {
  name = "apps-code-pipeline-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codepipeline.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

```

*  **buildspec  = "${file("buildspec_python.yml")}"**

```
version: 0.2

#env:
  #variables:
     # key: "There are no variables"
  #parameter-store:
     # key: "There are no variables"

phases:
  install:
    #If you use the Ubuntu standard image 2.0 or later, you must specify runtime-versions.
    #If you specify runtime-versions and use an image other than Ubuntu standard image 2.0, the build fails.
    runtime-versions:
       python: 3.10

  pre_build:
    commands:
     - apt-get update
     - pip install -r python_app_Pipeline/Dockerfile_py_Pipeline/requirements.txt
     - curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
     - unzip awscliv2.zip
     - sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update
   #  - REGION=us-east-1
     - REGION=$(aws ec2 describe-availability-zones --output text --query 'AvailabilityZones[0].[RegionName]')

     - AWS_ACCOUNTID=962490649366
     #- COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1???7)
    # - IMAGE_TAG=${COMMIT_HASH:=latest}
   #  - EKS_NAME= $(aws eks list-clusters --query 'clusters[0]' --output text)
     - EKS_NAME=radio-dev-ekstask1
     -  curl -o aws-iam-authenticator https://amazon-eks.s3.us-east-1.amazonaws.com/1.21.2/2021-07-05/bin/linux/amd64/aws-iam-authenticator
     - chmod +x ./aws-iam-authenticator
     - mkdir -p ~/bin && cp ./aws-iam-authenticator ~/bin/aws-iam-authenticator && export PATH=~/bin:$PATH
     - curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.7/2022-10-31/bin/linux/amd64/kubectl
     - chmod +x kubectl
     - mv ./kubectl /usr/local/bin/kubectl
     - echo Update kubeconfig???
     - aws eks update-kubeconfig --name ${EKS_NAME} --region ${REGION}
     - kubectl version --short --client
   #  - cat ~/.aws/config
  #  - cat ~/.aws/credentials
  #   - cat ~/.kube/config
     - aws sts get-caller-identity
   #  - mkdir -p ~/.aws/
   #  - echo "[profile codebuild]" >> ~/.aws/config
  #   - echo "role_arn = arn:aws:iam::$AWS_ACCOUNT_ID:role/containerAppBuildProjectRole" >> ~/.aws/config
   #  - echo "region = us-east-1"
   #  - echo "output = json"
   #  - cat ~/.aws/config
  #  -  aws eks update-kubeconfig --name ${EKS_NAME} --region ${REGION} --role-arn arn:aws:iam::962490649366:role/containerAppBuildProjectRole
    # -  aws eks update-kubeconfig --name ${EKS_NAME} --region ${REGION} 
     - kubectl get pod
     - kubectl get svc
     - echo $IMAGE_REPO_NAME
     - echo $IMAGE_TAG
     #- echo $PASS
     # define PASS as AWS SSM Parameter Store 
     - password=$(aws ssm get-parameters --region us-east-1 --names PASS --with-decryption --query Parameters[0].Value)
     - password=`echo $password | sed -e 's/^"//' -e 's/"$//'`
     - python python_app_Pipeline/test.py

     #- $IMAGE_REPO_NAME=yousefshaban/my-python-app
    # - $IMAGE_TAG=latest

  build:
    commands:
      - docker login --username yousefshaban --password ${password}
      - echo Build started on `date`
      - echo Building the Docker image...          
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG python_app_Pipeline/Dockerfile_py_Pipeline
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $IMAGE_REPO_NAME:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $IMAGE_REPO_NAME:$IMAGE_TAG


```





#### Step 03: We define AWS CodeBuild Projects for Pipeline `c4-build.tf`


```
# aws codebuild - First - python and auth with K8s  ************************************

resource "aws_codebuild_project" "containerAppBuild" {
  badge_enabled  = false
  build_timeout  = 60
  name           = "python_app"



  queued_timeout = 480
  service_role   = aws_iam_role.containerAppBuildProjectRole.arn
  tags = {
    Environment = var.env
  }

  artifacts {
    encryption_disabled = false
    # name                   = "container-app-code-${var.env}"
    # override_artifact_name = false
    packaging = "NONE"
    type      = "CODEPIPELINE"
  }



  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:6.0"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true
    type                        = "LINUX_CONTAINER"
    environment_variable {
              name  = "IMAGE_REPO_NAME"
              type  = "PLAINTEXT"
              value = "yousefshaban/my-python-app"
    }

    environment_variable {
              name  = "IMAGE_TAG"
              type  = "PLAINTEXT"
              value = "latest"
    }



  }


  logs_config {
    cloudwatch_logs {
      status = "ENABLED"
    }

    s3_logs {
      encryption_disabled = false
      status              = "DISABLED"
    }
  }

# how we can dd more source for aws_codebuild_project

  source {

    buildspec  = "${file("buildspec_python.yml")}"
    git_clone_depth     = 0
    insecure_ssl        = false
    report_build_status = false
  #  type                = "CODEPIPELINE"
    type                = "CODEPIPELINE"
  }
}



```



#### Step 04: We define AWS CodePipeline for all Stages of Source and Builds `c5-pipeline.tf`


```
resource "aws_s3_bucket" "cicd_bucket" {
  bucket = "my-artifact-store-i"
#  acl    = "private"
}

resource "aws_codepipeline" "node_app_pipeline" {
  name     = "python-app-pipeline"
  role_arn = aws_iam_role.apps_codepipeline_role.arn
  tags = {
    Environment = var.env
  }
  artifact_store {
    location = aws_s3_bucket.cicd_bucket.bucket
    type     = "S3"
  }


  stage {
    name = "Source"

    action {
      category = "Source"
      input_artifacts = []
      name            = "Source"
      output_artifacts = [
        "SourceArtifact",
      ]
      #owner     = "ThirdParty"
      owner     = "AWS"
      provider  = "CodeStarSourceConnection"     
      #provider  = "GitHub"
      run_order = 1
      version   = "1"   # ??? 1 or 2 
      configuration = {
        ConnectionArn    = aws_codestarconnections_connection.github.arn
        FullRepositoryId = var.python_project_repository_name
        BranchName       = var.python_project_repository_branch
      }



    }
  }





  stage {
  
    name = "Build-python"

    action {
       name = "Build-python"
      category = "Build"
         run_order = 2
      # region ??
      configuration = {
        "EnvironmentVariables" = jsonencode(
          [
            {
              name  = "environment"
              type  = "PLAINTEXT"
              value = var.env
            },
            {
              name  = "AWS_DEFAULT_REGION"
              type  = "PLAINTEXT"
              value = var.aws_region
            },
            #   {
            #   name  = "PASS" >>> you can add on parameter store and use it on Buildspec.yml
            #   - password=$(aws ssm get-parameters --region us-east-1 --names PASS --with-decryption --query Parameters[0].Value)
            # - password=`echo $password | sed -e 's/^"//' -e 's/"$//'`
            #   type  = "PARAMETER_STORE"
            #   value = "ACCOUNT_ID"
  
 
          ]
        )
        "ProjectName" = aws_codebuild_project.containerAppBuild.name
      }
      input_artifacts = [
        "SourceArtifact",
      ]
     
      output_artifacts = [
        "BuildArtifact",
      ]
      owner     = "AWS"
      provider  = "CodeBuild"
   #   run_order = 1
      version   = "1"
    }
  }



```



#### Step 05: We define Outputs `c6-outputs.tf`


```
output "code_build_project" {
  value = aws_codebuild_project.containerAppBuild.arn
}
output "python_codepipeline_project" {
  value = aws_codepipeline.python_pipeline.arn
}



```



#### Step 06: We define Variables `c7-variables.tf`


```

variable "aws_region" {
  description = "AWS region to launch servers."
  default     = "us-east-1"
}
variable "env" {
  description = "Targeted Depolyment environment"
  default     = "dev"
}
variable "python_project_repository_name" {
  description = "Nodejs Project Repository name to connect to"
  default     = "yousefshaban00/pipeline01"
}
variable "python_project_repository_branch" {
  description = "Nodejs Project Repository branch to connect to"
  default     = "main"
}


variable "artifacts_bucket_name" {
  description = "S3 Bucket for storing artifacts"
  default     = "python-app"
}


```



#### Outputs and Verify 


![Alt text](python_app_Pipeline/Capture1.PNG)
![Alt text](python_app_Pipeline/Capture2.PNG)
```

[Container] 2023/01/02 17:24:53 Running command echo $IMAGE_REPO_NAME
yousefshaban/my-python-app

[Container] 2023/01/02 17:24:53 Running command echo $IMAGE_TAG
latest

[Container] 2023/01/02 17:24:53 Running command password=$(aws ssm get-parameters --region us-east-1 --names PASS --with-decryption --query Parameters[0].Value)

[Container] 2023/01/02 17:24:53 Running command password=`echo $password | sed -e 's/^"//' -e 's/"$//'`

[Container] 2023/01/02 17:24:53 Running command python python_app_Pipeline/test.py
Hello
IP          namespace           Pod name            Status
10.0.2.167      amazon-cloudwatch       cloudwatch-agent-558q8      Running
10.0.1.72       amazon-cloudwatch       cloudwatch-agent-tfh4d      Running
10.0.111.230        amazon-cloudwatch       cloudwatch-agent-wr2lc      Running
10.0.112.51     amazon-cloudwatch       cloudwatch-agent-x88hj      Running
10.0.112.54     amazon-cloudwatch       fluent-bit-5nxtq        Running
10.0.111.178        amazon-cloudwatch       fluent-bit-psk2n        Running
10.0.2.176      amazon-cloudwatch       fluent-bit-q854p        Running
10.0.1.254      amazon-cloudwatch       fluent-bit-qlljx        Running
10.0.112.244        bookinfo        details-v1-7d4d9d5fcb-2dd7d     Running
10.0.2.159      bookinfo        productpage-v1-66756cddfd-sqnc7     Running
10.0.1.251      bookinfo        ratings-v1-85cc46b6d4-cl9cs     Running
10.0.2.70       bookinfo        reviews-v1-777df99c6d-wdzt9     Running
10.0.112.184        bookinfo        reviews-v2-cdd8fb88b-q4dl7      Running
10.0.1.235      bookinfo        reviews-v3-58b6479b-xx9fx       Running
10.0.112.59     default     adservice-798c5794b9-hvs9k      Running
10.0.2.120      default     app3-nginx-deployment-6794896487-2rnxq      Running
10.0.1.133      default     cartservice-7685cbbd4b-wxbb9        Running
10.0.112.225        default     checkoutservice-9b7dc8f59-rrpqn     Running
10.0.1.41       default     currencyservice-56bf544587-kdmnr        Running
10.0.111.182        default     efs-write-app       Running
10.0.2.141      default     emailservice-6c8d4c548f-zfn5b       Running
10.0.112.115        default     frontend-69d869947d-82jrq       Running
10.0.111.120        default     loadgenerator-77c94f6f99-gvnk9      Running
10.0.2.177      default     myapp1-9b7f4874f-g6gtb      Running
10.0.1.19       default     myapp1-9b7f4874f-q7m95      Running
10.0.2.90       default     paymentservice-6677674b85-s9xpz     Running
10.0.2.226      default     productcatalogservice-57c8f7778c-ddv2h      Running
10.0.111.237        default     recommendationservice-6569854945-xc7mc      Running
10.0.112.67     default     redis-cart-8f764486f-qx8hk      Running
10.0.111.146        default     shippingservice-76f6b7897c-ssfhr        Running
10.0.1.177      interview       hello-world-de-7f7dd84f4-5vlc5      Running
10.0.1.237      interview       hello-world-dee-787bf79bfb-snbvg        Running
10.0.111.168        interview       hello-world-es-578f4f859c-dqp4w     Running
10.0.1.190      interview       hello-world-eu-748db46546-f55sm     Running
10.0.2.243      interview       hello-world-fr-7fbccc49f4-vg9sj     Running
10.0.112.36     istio-system        grafana-749f67cb6f-4jclt        Running
10.0.2.19       istio-system        istio-cni-node-7gmjg        Running
10.0.111.32     istio-system        istio-cni-node-7l92z        Running
10.0.112.106        istio-system        istio-cni-node-bczpg        Running
10.0.1.88       istio-system        istio-cni-node-bhwjk        Running
10.0.111.206        istio-system        istio-egressgateway-688d4797cd-csj48        Running
10.0.111.166        istio-system        istio-ingressgateway-6bd9cfd8-vj9dc     Running
10.0.111.165        istio-system        istiod-68fdb87f7-wcl7t      Running
10.0.111.85     istio-system        kiali-5dd4b8584f-k64km      Running
10.0.1.47       istio-system        prometheus-5f9557c5dc-bcwmr     Running
10.0.2.131      istio-system        zipkin-5d8dc88bdc-l4l8d     Running
10.0.1.254      kube-system     aws-node-bsfh5      Running
10.0.2.176      kube-system     aws-node-jjl28      Running
10.0.112.54     kube-system     aws-node-lq97k      Running
10.0.111.178        kube-system     aws-node-vtddl      Running
10.0.112.114        kube-system     coredns-79989457d9-9q6d8        Running
10.0.112.175        kube-system     coredns-79989457d9-jtmlp        Running
10.0.1.156      kube-system     ebs-csi-controller-69774c68f4-p6svn     Running
10.0.2.188      kube-system     ebs-csi-controller-69774c68f4-t5dgt     Running
10.0.2.73       kube-system     ebs-csi-node-4sxqh      Running
10.0.1.17       kube-system     ebs-csi-node-f4cdz      Running
10.0.111.130        kube-system     ebs-csi-node-krs4d      Running
10.0.112.166        kube-system     ebs-csi-node-xn7zg      Running
10.0.1.174      kube-system     efs-csi-controller-6d7b578777-kn9ml     Running
10.0.2.86       kube-system     efs-csi-controller-6d7b578777-lp9g9     Running
10.0.112.54     kube-system     efs-csi-node-gpp6t      Running
10.0.1.254      kube-system     efs-csi-node-j5bbh      Running
10.0.111.178        kube-system     efs-csi-node-jhrpr      Running
10.0.2.176      kube-system     efs-csi-node-wgn9c      Running
10.0.112.54     kube-system     kube-proxy-hs7cm        Running
10.0.1.254      kube-system     kube-proxy-plcp7        Running
10.0.2.176      kube-system     kube-proxy-r2xrr        Running
10.0.111.178        kube-system     kube-proxy-r64wh        Running
10.0.1.240      kube-system     radio-dev-ca-aws-cluster-autoscaler-68b99987b8-6vzcc        Running
10.0.2.147      kube-system     radio-dev-metrics-server-54666cdb8c-x4qgq       Running
10.0.2.138      kube-system     tiller-deploy-6679847b75-4nrkw      Pending
10.0.1.122      nginx-ingress-controller        nginx-ingress-controller-ingress-nginx-controller-f6fd8fbb82lz9     Running

[Container] 2023/01/02 17:24:56 Phase complete: PRE_BUILD State: SUCCEEDED
[Container] 2023/01/02 17:24:56 Phase context status code:  Message: 
[Container] 2023/01/02 17:24:56 Entering phase BUILD
[Container] 2023/01/02 17:24:56 Running command docker login --username yousefshaban --password ${password}
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

[Container] 2023/01/02 17:24:56 Running command echo Build started on `date`
Build started on Mon Jan 2 17:24:56 UTC 2023

[Container] 2023/01/02 17:24:56 Running command echo Building the Docker image...
Building the Docker image...

[Container] 2023/01/02 17:24:56 Running command docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG python_app_Pipeline/Dockerfile_py_Pipeline
Sending build context to Docker daemon  22.02kB

Step 1/5 : FROM python:3.8
3.8: Pulling from library/python
32de3c850997: Pulling fs layer
fa1d4c8d85a4: Pulling fs layer

Step 5/5 : CMD ["python", "test.py"]
 ---> Running in 914c8952648c
Removing intermediate container 914c8952648c
 ---> 476026435f89
Successfully built 476026435f89
Successfully tagged yousefshaban/my-python-app:latest

[Container] 2023/01/02 17:25:21 Running command docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $IMAGE_REPO_NAME:$IMAGE_TAG

[Container] 2023/01/02 17:25:21 Phase complete: BUILD State: SUCCEEDED
[Container] 2023/01/02 17:25:21 Phase context status code:  Message: 
[Container] 2023/01/02 17:25:21 Entering phase POST_BUILD
[Container] 2023/01/02 17:25:21 Running command echo Build completed on `date`
Build completed on Mon Jan 2 17:25:21 UTC 2023

[Container] 2023/01/02 17:25:21 Running command echo Pushing the Docker image...
Pushing the Docker image...

[Container] 2023/01/02 17:25:21 Running command docker push $IMAGE_REPO_NAME:$IMAGE_TAG
The push refers to repository [docker.io/yousefshaban/my-python-app]

```









