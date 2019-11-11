# Pod资源对象

~~~ yaml
apiVersion: v1
kind: Pod
metadata:
    name: nginx-pod
    labels:
      env: qa
      tier: frontend
spec:
    containers:
    - name: nginx
      image: nginx:latest
      imagePullPolicy: Always
      ports:
        - name: http
          containerPort: 80
          protocol: TCP
      command: ["/bin/sh"]
      args: ["-c", "while true; do sleep 30; done"]
      env:
        - name: REDIS_HOST
        - value: 127.0.0.1:6379
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        allowPrivilegeEscalation: false
    hostNetwork: true
    securityContext:
      runAsNonRoot: true
    nodeSelector:
      disktype: ssd
~~~

* metadata: 标准对象的元数据
  * name: 指定pod的名称
  * labels: pod设置标签
    * env: 设置key为env的标签
    * tier: 设置key为frontend的标签
* spec: 指定pod所需的行为
  * containers: 属于Pod的容器列表，创建后无法添加和删除容器,Pod中必须有一个容器，创建后不能被更新。
    * name: 容器名称
    * image: 容器镜像
    * imagePullPolicy: 镜像获取策略
      * Always: 镜像标签为'latest'或镜像不存在时总是从指定的仓库获取镜像
      * IfNotPresent: 仅当本地镜像缺失时才从目标仓库下载镜像
      * Never: 禁止从仓库下载镜像， 即仅使用本地镜像
    * ports: 容器需要公开的端口列表，在此处公开端口可为系统提供关于容器使用的网络连接的其他附加信息，但主要是参考信息, 在这里不指定端口并不会阻止该端口被公开。在容器内默认地址"0.0.0.0"上监听的端口都可以从网络访问。不能被更新
      * name: 当前端口名称
      * containerPort: 需要在Pod对象的IP地址上暴露的容器端口
      * protocol: 端口相关的协议,值仅可为TCP或UDP, 默认TCP
    * command: 简单的说就是容器启动时执行的命令
    * args: command命令的参数
    * env: 配置环境变量列表
      * name: 环境变量的名称
      * value: 环境变量的值
    * securityContext: 容器的安全上下文
      * runAsNonRoot: 设置容器必须以非root用户身份运行
      * runAsUser: 用于运行容器进程入口点的UID
      * allowPrivilegeEscalation: 确定是否可以请求允许特权升级
  * hostNetwork: 为True时,共享节点的网络名称空间
  * securityContext: Pod的安全上下文
  * nodeSelector: 节点标签选择器，根据标签决定pod运行在那些node上
    * disktype: 标签的key为disktype值为ssd的节点上运行当前pod

## 标签

* 版本标签: release:
  * stable
  * canary
  * beta
* 环境标签: environment:
  * dev
  * qa
  * production
* 应用标签: app:
  * ui
  * as
  * pc
  * sc
* 架构层级标签: tier:
  * frontend
  * backend
  * cache
* 分区标签: partition
  * customerA
  * customerB
* 品控级别标签: track:
  * daily
  * weekly
