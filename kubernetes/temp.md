kubectl get node 获取所有节点
kubectl describe node node_name  节点的详细信息

kubectl get deployment
kubectl run  创建并运行一个镜像


kubectl run 

kubectl expose 暴露端口。

kubectl expose deployment nginx-deploy  --name=nginx  --port=80 --target-port=80 --protocol=TCP

kubectl get pods --show-labels

kubectl get svc

kubectl get pods -n kube-system -o wide

kubectl get svc -n kube-system

kubectl scale --replicas=3 deployment myapp 动态修改

kubectl set image  deployment myapp myapp=ikubernetes/myapp:v2

kubectl rollout undo deployment myapp 回滚



kubernetes 常用资源
    workload: Pod, ReplicaSet, Deployment, StatefulSet, DaemonSet, Job, Cronjob,
    服务发现及均衡： Service, Ingress
    配置及存储： Volume, CSI
                ConfigMap ,Secret
                DOwnwaredAPI
    集群级资源:
        Namespace, Node, Role, ClusterRole, RoleBinding, ClusterRoleBinding
    
    元数据型资源：
        HPA， PodTemplate, LimitRange


kubectl get pod myapp-5bc569c47d-2drh2 -o yaml

apiVersion group/version 省略表示是core
kind: Pod 资源类别
metadata: 元数据
spec: 规格, 目标的期望状态 
status: 当前状态。


创建资源的放法:
    apiserver 仅接收json格式的资源定义;
    ymal格式提供配置清单，apiserver 可自动将其转为json格式，然后再提交

大部分资源配置清单：
    
    apiVersion beta版，稳定版
        kubectl api-versions

    kind 资源类别
    
    metadata: 元数据
        name: 名字必须是唯一的。
        namespace: 名称空间
        labels 标签
            annotations

        每个的资源的引用PATH
            /api/{Group}/{version}/namespaces/NAMESPACE/TYPE/NAME

    spec: 期望的状态， disired state
    status: 当前状态  current state, 本字段由 kubernetes 自动更新，无法更新

    kubectl explain pods
    kubectl explain pods.metadata


~~~
apiVersion: v1
kind: Pod
metadata:
    name: pod-demo
    namespace: default
    labels:
        app: myapp
        tier: frontend
spec:
    containers:
    - name: myapp
      image: ikubernetes/myapp:v1
    - name: busybox
      image: buybox: latest
      command:
      - "/bin/sh"
      - "-c"
      - "echo $(date) >> /usr/share/nginx/html/index.html; sleep 5"

~~~

kubectl create -f pod-demo.yaml
kubectl logs pod-dome myapp/busybox

kubectl exec -it pod-demo -c myapp -- /bin/sh/


资源的清单格式:
    一级字段: apiVersion(groups/version), kind, metadata(name, namespace, labels, annotations, ...), spec

    Pod资源:
        spec.containers 
        - name 
          image
          imagePullPolicy
            Always, Never, IfNotPresent
    修改镜像默认应用
    

pod 生命周期



apiVersion: v1
kind: Pod
metadata:
    name: liveness-exec-pod
    namespace: default
spec:
    containers:
    - name: liveness-exec-container
      image: busybox: latest
      imagePullPolicy: IfNotPresent
      command: ["/bin/sh", "-c", "touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 3600" ]
      livenessProbe:
        exec:
          command: ["test", "-e", "/tmp/healthy"]
        initialDelaySeconds: 1
        periodSeconds: 3



kubectl create -f liveness-exec.yaml
kubectl get pods -w



apiVersion: v1
kind: Pod
metadata:
    name: poststart-pod
    namespace: default

spec:
    containers:
    - name: busybox-httpd
      image: busybox:latest
      imagePullPolicy: IfNotPresent

      lifecycle:
          postStart:
              exec:
                  command: ["/bin/sh", "-c", "mkdir -p /data/web/html; echo 'Home Page' >> /data/web/html/index.html"]

      command: ["/bin/httpd"]
      args: ["-f", "-h /data/web/html"]

kubectl patch deployments myapp-deploy \
-p '{"spec": {"strategy": {"rollingUpdate": {"maxSurge": 1, "maxUnavailable": 0}}}}'




#### rs-demo.yaml

apiVersion: apps/v1
kind: ReplicaSet
metadata:
    name: myapp
    namespace: default

spec: # 控制器的spec
    replicas: 2
    selector:
        matchLabels:
            app: myapp
            release: canary

    template:
        metadata:
            name: myapp-pod
            labels: 
                app: myapp
                release: canary
                environment: qa
        spec:
            containers:
            - name: myapp-container
              image: ikubernetes/myapp:v1
              ports:
                - name: http
                  containerPort: 80

####








