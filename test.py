from kubernetes import client, config
import json
from tabulate import tabulate


print("Hello")
# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
api_apps= client.AppsV1Api()
api_metric = client.CustomObjectsApi()
api_nw = client.NetworkingV1Api()
rbac_client = client.RbacAuthorizationV1Api()
# Create a client for the batch/v1 API
api_batch = client.BatchV1Api()

# Create a MetricsV1beta1Api client
#metrics_client = client.MetricsV1beta1Api()

# Create a NetworkingV1beta1Api client


#podips()

def pod_status ():
  
    ret = v1.list_pod_for_all_namespaces(watch=False)
    #print(ret)
    print("%s\t\t\t%s\t\t\t%s\t\t\t%s" % ("IP", "namespace" , "Pod name", "Status"))
    for i in ret.items:
        print("%s\t\t%s\t\t%s\t\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name, i.status.phase))

#pod_status()



def nodeips ():
    print("Listing nodes with their IPs:")
    ret = v1.list_node(watch=False)
    
    for i in ret.items:
        print(i.metadata.name)

#nodeips()

#podips()
"""
v1.list_node()  
v1.list_namespace()
v1.list_pod_for_all_namespaces()
v1.list_persistent_volume_claim_for_all_namespaces()
v1.list_namespaced_pod(namespace=’default’)
v1.list_namespaced_service(namespace=’default’)
list_service_for_all_namespaces
"""

"""
lnode=v1.list_node()
for i in lnode.items:
        print(f"{i.metadata.name}:{i.status.phase}")
"""

def podcpu():
    pods = v1.list_pod_for_all_namespaces().items

    # Iterate through the list of pods
    for pod in pods:
    # Get the namespace and pod name
        namespace = pod.metadata.namespace
        pod_name = pod.metadata.name

        # Call the 'read_namespaced_pod_metrics' method to get the metrics for the pod
        metrics = v1.read_namespaced_pod_status(name=pod_name, namespace=namespace)
        print(metrics)
        # The 'cpu_usage' field in the 'metrics' object contains the CPU usage data for the pod
        cpu_usage = metrics.containers[0].usage.cpu

        # Print the CPU usage data for the pod
        print(f"CPU usage for pod {pod_name} in namespace {namespace}: {cpu_usage}")

#podcpu()



#podstatus() - Done

#"--------------------------------------------------------------------"
#pod and Containers



#status pod
def podstatus():
    print("Listing pods with status:")
    pods = v1.list_pod_for_all_namespaces(watch=False)
    
    for i in pods.items:
        print(f"{i.metadata.name}:{i.status.phase}")

#podstatus()



def podips ():
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    #print(ret)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


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




# Pod CPU and Memory Utilization Test
def podres():
    namespace = "default"
    pod_name = "app3-nginx-deployment-cd48c8ffb-8mzc7"

    # Get the pod metrics
    pod_metrics = api_metric.read_namespaced_pod_metrics(name=pod_name, namespace=namespace)

    # Get the CPU and memory usage of the pod
    cpu_usage = pod_metrics.containers[0].usage.cpu
    memory_usage = pod_metrics.containers[0].usage.memory

    # Print the CPU and memory usage
    print(f"CPU usage: {cpu_usage}")
    print(f"Memory usage: {memory_usage}")


#podres()

#pod or Container images
def podimage():

    # Get the pod
    pod = v1.list_pod_for_all_namespaces(watch=False)

    # Get the container images of the pod
    #container_images = [container.image for container in pod.spec.containers]
    for pod in pod.items:
        for container in pod.spec.containers:
            print(f"{pod.metadata.name}:{container.name}: {container.image}")

#podimage()




# for specifc namespace and pod
#mertic server on kubernetes using python
def util():
        # Set the namespace and pod name
    namespace = "default"
    pod_name = "app3-nginx-deployment-cd48c8ffb-8mzc7"

    # Get the pod metrics from the metrics-server
    pod_metrics = api_metric.get_namespaced_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        namespace=namespace,
        plural="pods",
        name=pod_name
    )

    # Print the CPU and memory usage of the pod
    cpu_usage = pod_metrics["containers"][0]["usage"]["cpu"]
    memory_usage = pod_metrics["containers"][0]["usage"]["memory"]
    print(f"CPU usage: {cpu_usage}")
    print(f"Memory usage: {memory_usage}")
   # print(f"{pod.metadata.name}: CPU request={cpu_request}, CPU limit={cpu_limit}: memory request={memory_request}, memory limit={memory_limit}")

#util()


#ingress-nginx-controller-85df9f7466-cpjmp   0/1     CrashLoopBackOff   365 (3m25s ago)   22h
#restart Count CrashBack OFF
def restartpod():
    # List all pods
    pods = v1.list_pod_for_all_namespaces()

    # Print the name of each pod that has a non-zero restartCount
    for pod in pods.items:
        if pod.status.container_statuses[0].restart_count > 0:
            print(f"# Print the name of each pod that has a non-zero restartCount: {pod.metadata.name} namespace: {pod.metadata.namespace}")

#restartpod()



# CPU and Memory utilization for all pod on namespace
def pod_cpu_mem_util():


    # List all namespaces
    namespaces = v1.list_namespace()
    # Print the number of pods in each namespace
    #exception if empty pod ? pod status running 
    # Print the CPU and memory usage of all pods in each namespace
    # for namespace in namespaces.items:
       
    #     pods = v1.list_namespaced_pod(namespace=namespace.metadata.name)
    #     lenx =len(pods.items)
    #     for pod in pods.items:
    #         # Check if all containers in the pod are running
    #         running = True
    #         print(namespace.metadata.name)
    #         for container_status in pod.status.containerStatuses:
    #             print(container_status)
    #             if container_status.state.running is None:
    #                 running = False
    #                 continue
        # print(f"{namespace.metadata.name}: {len(pods.items)} pods")
      #  print(lenx)
        #if lenx > 0:

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

#pod_cpu_mem_util()


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
      #  cpu_usage = node_metrics["containers"][0]["usage"]["cpu"]
        #memory_usage = node_metrics["containers"][0]["usage"]["memory"]
        #print(f"{namespace.metadata.name}/{pod.metadata.name}: CPU usage={cpu_usage}, Memory usage={memory_usage}")

        #nodes = v1.list_node_metrics()
        # Print the metric data for each node
        # for node in nodes.items:
        #     print(f"Node: {node.metadata.name}")
        #     print(f"CPU usage: {node.usage.cpu}")
        #     print(f"Memory usage: {node.usage.memory}")
        #     print()

#nodemetric()














#"--------------------------------------------------------------------"
#Node

def nodename():
    # Set the node name
    node_name = "ip-10-0-1-254.ec2.internal"

    # Get the node
    node = v1.read_node(name=node_name)

    # # Print the node's memory and CPU usage
    # for condition in node.status.conditions:
    #     if condition.type == "MemoryPressure":
    #         print(f"Memory pressure: {condition.status}")
    #     elif condition.type == "CPUPressure":
    #         print(f"CPU pressure: {condition.status}")


# Get the allocatable CPU for the node
#allocatable_cpu = nodex.status.allocatable['cpu']
#print(f"Allocatable CPU: {allocatable_cpu}")

#print(nodex)
#for condition in nodex.status.conditions:
  #  print(f"{condition.type}: {condition.status}")

#print((nodex.status.conditions[3]).get('type'))
#x=nodex.status.conditions[3].type

#z=type(x)
#print(x)

#xx =x.get['type']
#print(xx)
#status node
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
        #print(ip_address)
        #print(f"{i.metadata.name}:{instance_type}:{i.status.conditions[3].type}")
       
        print("%s\t%s\t\t%s\t\t%s\t\t%s" % (i.metadata.name, instance_type, ip_address_internal,ip_address_ex,i.status.conditions[3].type))

#nodestatus()

#"--------------------------------------------------------------------"
# Deployment

def deploy():
   # namespace = "default"
#deployment_name = "app3-nginx-deployment "

    # Get the deployment
    #deployment = api_apps.read_namespaced_deployment()
    deployment = api_apps.list_deployment_for_all_namespaces()
    print("%s\t%s\t%s\t%s" % ("deployment name", "Desired replicas", "Current replicas","Ready replicas"))
    for i in deployment.items:
        #x = i.spec.replicas
        #print(x)
        print("%s\t%s\t%s\t%s" % (i.metadata.name, i.spec.replicas, i.status.replicas,i.status.ready_replicas))
    #print(deployment)
    # Print the deployment status
   # print(f"Desired replicas: {deployment.spec.replicas}")
   # print(f"Current replicas: {deployment.status.replicas}")
    #print(f"Ready replicas: {deployment.status.ready_replicas}")

#deploy()

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
#workload running with single replica
#deploytab()


#"--------------------------------------------------------------------"
# Services 
#status svc







#"--------------------------------------------------------------------"
# Ingress

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

#ingress()

# second funtion
## return annotations




#"--------------------------------------------------------------------"
# stsus ns 
#namespace without any workload 

def ns_no_workload():
    print("namespace without any workload") 
    namespaces = v1.list_namespace()
    # Print the number of pods in each namespace
    #exception if empty pod ? pod status running 
    # Print the CPU and memory usage of all pods in each namespace
    for namespace in namespaces.items:
       
        pods = v1.list_namespaced_pod(namespace=namespace.metadata.name)
        lenx =len(pods.items)
        #print(lenx)
        if lenx == 0:
                print(namespace.metadata.name)

#ns_no_workload()
#"--------------------------------------------------------------------"
#status PV and #status PVC and SC


# List all PVs
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

#p_volume()



#"--------------------------------------------------------------------"
#Job
#CronJob
def jobs():
    # Get the namespace to list jobs in
    #namespace = "default"

    # List all jobs in the namespace
    #jobs = api_batch.list_namespaced_job(namespace=namespace)
    namespaces = v1.list_namespace()
    for namespace in namespaces.items:
                
        jobs = api_batch.list_namespaced_job(namespace=namespace.metadata.name)
        print(namespace.metadata.name)
        for job in jobs.items:
            print(f"Job {job.metadata.name}: status={job.status.conditions[0].type}")

#jobs()


#"--------------------------------------------------------------------"
#Configmap


# return all SA with annotations
# def sa():
#     # Get the namespace to list service accounts in
#     #namespace = "default"
#     namespaces = v1.list_namespace()
#     for namespace in namespaces.items:
#         # List all service accounts in the namespace
#         service_accounts = v1.list_namespaced_service_account(namespace=namespace.metadata.name)

#         # Print the status of each service account
#         for service_account in service_accounts.items:
#             print(f"Service account {service_account.metadata.name} : namespace={service_account.metadata.namespace}: Annotations={service_account.metadata.annotations}")


# Table
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

# name SA role name + roles 
# Create a client for the rbac/v1 API


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



