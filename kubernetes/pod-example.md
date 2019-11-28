# Pod Example

[TOC]

## pod

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: pod-example
spec:
  containers:
    - name: myapp
      image: ikubernetes/myapp:v1
~~~

## pod-with-env

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: pod-with-env
spec:
  containers:
    - name: filebeat
      image:  ikubernetes/filebeat:5.6.5-alpine
      env:
        - name: REDIS_HOST
          value:  db.ilinux.io:6379
        - name: LOG_LEVEL
          value: info
~~~

## pod-with-port

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: pod-example
spec:
  containers:
    - name: myapp
      image: ikubernetes/myapp:v1
      ports:
        - name: http
          containerPort: 80
          protocol: TCP
~~~

## pod-use-hostnetwork

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: pod-use-hostnetwork
spec:
  containers:
    - name: myapp
      image: ikubernetes/myapp:v1
  hostNetwork: true

~~~

## pod-with-securitycontext

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: pod-with-securitycontext
spec:
  containers:
    - name: busybox
      image: busybox
      command: ["/bin/sh", "-c", "sleep 86400"]
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        allowPrivilegeEscalation: false

~~~

## pod-with-labels

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: pod-with-nodeselector
  labels:
    env: testing
spec:
  containers:
    - name: myapp
      image: ikubernetes/myapp:v1
  nodeSelector:
      disktype:ssd

~~~

## pod-initcontainers

~~~ yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
    - name: myapp-container
      image: ikubernetes/myapp:v1
  
  initContainers:
    - name: init-someting
      image: busybox
      command: ['sh', '-c', 'sleep 10']

~~~

## pod-with-lifecycle

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: lifecycle-demo
spec:
  containers:
    - name: lifecycle-demo-container
      image: ikubernetes/myapp:v1
      lifecycle:
        postStart:
          exec:
            command: ["/bin/sh", "-c", "echo 'lifecycle hooks handler' > /usr/share/nginx/html/test.html"]

~~~

## pod-with-httpget

~~~ yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: liveness
  name: liveness-http
spec:
  containers:
    - name: liveness-http-demo
      image: nginx:1.12-alpine
      ports:
        - name:  http
          containerPort:  80
      lifecycle:
        postStart:
          exec:
            command: ["/bin/sh", "-c", "echo Healthy > /usr/share/nginx/html/healthz"]
      livenessProbe:
        httpGet:
          path: /healthz
          port: http
          scheme: HTTP

~~~

## pod-readiness-exec

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  labels:
    test: readliness-exec
  name: readliness-exec
spec:
  containers:
    - name: readliness-demo
      image: busybox
      args: ["/bin/sh", "-c", "while true; do rm -rf /tmp/ready; sleep 30; touch /tmp/ready; sleep 300; done"]

      readinessProbe:
        exec:
          command: ["test", "-e", "/tmp/ready"]
        initialDelaySeconds: 5
        periodSeconds: 5

~~~

## pod-resouces-demo

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: stress-pod
spec:
  containers:
    - name: stress
      image: ikubernetes/stress-ng
      command: ["/usr/bin/stress-ng", "-m 1", "-c 1", "--metrics-brief"]
      resources:
        requests:
          memory: "128Mi"
          cpu: "200m"

~~~

## pod-with-memleak

~~~ yaml

apiVersion: v1
kind: Pod
metadata:
  name: memleak-pod
  labels:
    app: memleak
spec:
  containers:
    - name:  simmemleak
      image:  saadali/simmemleak
      resources:
        requests:
          memory: "64Mi"
          cpu: "1"
        limits:
          memory: "64Mi"
          cpu: "1"
~~~

## rs-demo

~~~ yaml

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs-example
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rs-demo
  template:
    metadata:
      labels:
        app: rs-demo
    spec:
      containers:
        - name: myapp
          image: ikubernetes/myapp:v1
          ports:
            - name: http
              containerPort: 80

~~~

## deployment

~~~ yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: ikubernetes/myapp:v1
          ports:
            - containerPort: 80
              name: http
~~~

## DaemonSet

~~~ yaml

apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: filebeat-ds
  labels:
    app: filebeat
spec:
  selector:
    matchLabels:
      app: filebeat
  template:
    metadata:
      labels:
        app: filebeat
      name: filebeat
    spec:
      containers:
        - name: filebeat
          image: ikubernetes/filebeat:5.6.5-alpine
          env:
            - name: REDIS_HOST
              value: 192.168.3.16:6379
            - name: LOG_LEVEL
              value: info

~~~

## job

~~~ yaml

apiVersion: batch/v1
kind: Job
metadata:
  name:  job-example
spec:
  template:
    spec:
      containers:
        - name: myjob
          image: alpine
          command: ["/bin/sh", "-c", "sleep 120"]
      restartPolicy: Never

~~~

## job-multi

~~~ yaml

apiVersion: batch/v1
kind: Job
metadata:
  name:  job-multi
spec:
  completions: 5
  parallelism: 2
  template:
    spec:
      containers: 
        - name: myjob
          image: alpine
          command: ["/bin/sh", "-c", "sleep 20"]
      restartPolicy: OnFailure

~~~

## svc

~~~ yaml

kind: Service
apiVersion: v1
metadata:
  name:  myapp-svc
spec:
  selector:
    app:  myapp
  ports:
    - port:  80
      targetPort:  80
~~~

## PV

~~~ yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs-0001
  labels:
    release: stable
spec:
  capacity:
    storage: 25Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: dynamic-data
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: "/data/public"
    server: 192.168.3.16

~~~

## PVC-nfs

~~~ yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-nfs-0001
  lables:
    release: "stable"
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  resources:
    requests:
      storage: 1Gi
  storageClassName: dynamic-data

~~~
