from kubernetes import client, config

class KubeCheck(object):
    def __init__(self, stack_name):
        self._kubeconf = "/root/.kube/config"
        config.load_kube_config(self._kubeconf)
        self._stack_name = self._get_ns(stack_name)

    def _get_ns(self, stack_name):
        v1 = client.CoreV1Api()
        ns = None
        for i in v1.list_namespace().items:
            if i.metadata.name == stack_name:
                ns=i.metadata.name
                return ns
            else:
                continue
                
        if ns == None:
            error = "Application "+stack_name+" not found"
            raise Exception(error)

    def get_pod_status(self):
        v1 = client.CoreV1Api()
        pod_list = []
        try:
            for i in v1.list_namespaced_pod(self._stack_name).items:
                pod_list.append(i.metadata.name)
                #print i.metadata.name
        except Exception as e:
            raise Exception(e)
 
        pod_status = {}
        for i in pod_list:
            pod_status['name'] = i
            pod_status = v1.read_namespaced_pod_status(i,self._stack_name).status.phase
            if pod_status == "Running" or "Succeeded"
                pod_status['status'] = "Normal"
                pod_status['msg'] = v1.read_namespaced_pod_status(i,self._stack_name).status.phase
            else:
                pod_status['status'] = "Abnormal"
                pod_status['msg'] = i + ": " + v1.read_namespaced_pod_status(i,self._stack_name).status.phase

        return pod_status


    def get_pod_svc(self):
        pass


    def get_ingress(self):
        v1 = client.ExtensionsV1beta1Api()
        ingress = {}
        for i in v1.list_namespaced_ingress(self._stack_name).items:
            for j in i.spec.rules:
                if j.host:
                    ingress['ingress'] = j.host
                else:
                    ingress['ingress'] = "None"
            if i.spec.tls:
                ingress['tls'] = i.spec.tls
            else:
                ingress['tls'] = "None" 
        return ingress

    

























        