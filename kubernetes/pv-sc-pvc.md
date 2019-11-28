# pv-sc-pvc

[TOC]

## SC

存储类（storage class) 是kubernetes资源类型的一种，它是由管理员为管理PV之便而按需创建的类别（逻辑组）。存储类的好处之一便是支持PV的动态创建

**sc关键字段:**

* provisioner(供给方): 即提供了存储资源的存储系统，存储类要依赖Provisioner来判定要使用的存储插件以便适配到目标存储系统。kubernetes内建有多种供方(Provisioner), 还支持用户一句Kubernetes规则自定义
* parameters(参数): 存储类使用参数描述要关联到的存储券，不过，不同的provisioner可用的参数各不相同。
* reclaimPolicy: 为当前存储类动态创建的PV指定回收策略， 可用值为Delete(默认)和Retain; 不过，那些由管理员手工创建的PV的回收策略则取决于它们自身的定义
* volumeBindingMode: 定义如何为PVC完成供给和绑定， 默认值为"VolumeBindingImmediate"; 此选项仅在启用了存储卷调度功能时才能生效。
* mountOptions: 由当前类动态创建的PV的挂载选项列表

### Gluster 存储系统的SC

~~~ yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1beta1
metadata:
    name: glusterfs
provisioner: kubernetes.io/glusterfs
parameters:
    resturl: "http://heketi.ilinux.io:8080"
    restauthenabled: "false"
    restuser: "ik8s"
    restuserkey: "ik8s.io"

~~~

## PV

~~~ shell
kubect get pv -A
~~~

***PV资源生命周期的各个阶段***

* Available: 可用状态的自有资源，尚未被PVC绑定
* Bound: 已经绑定至某PVC
* Released: 绑定的PVC已经被删除，但资源尚未被集群收回
* Failed: 因自动回收资源失败而处于的故障状态

**PV关键字段:**

* Capacity: 当前PV的容量
* volumeMode: 卷模型，用于指定此卷可被用作文件系统还是裸格式的块设备，默认是Filesystem
* accessModes: 访问模式
  * ReadWriteOnce: 仅可被单个节点读写挂载；命令行中简写为RWO
  * ReadOnlyMany: 可被多个节点同时读写挂载； 命令行中简写为ROX
  * ReadWriteMany: 可被多个节点同时读写挂载；命令行中简写为RWX
* persistentVolumeReclaimPolicy: PV空间被释放时的处理机制；可用类型仅为一下几种:
  * Retain: 默认， 保持不动，由管理员随后手动回收
  * Recycle: 空间回收，即删除存储卷目录下的所有文件(包括子目录和隐藏文件)，目前仅NFS和hostPath支持此操作
  * Delete: 删除存储卷，仅部分云端存储系统支持，如AWS EBS, GCE PD, Azure Disk 和Cinder
* storageClassName: 当前PV所属的StorageClass的名车，默认为空，即不属于任何StorageClass. PV和SC通过此字段关联。
* mountOptions: 挂载选项组成的列表，如ro, soft和hard等。

### NFS存储后端的PV

~~~ yaml

kind: PersistentVolume
metadata:
    name: pv-nfs-0001
    labels:
        release: stable
spec:
    capacity:
        storage: 5Gi
    volumeMode: Filesystem
    accessModes:
        - ReadWriteMany
    persistentVolumeReclaimPolicy: Recycle
    storeageClassName: nfs
    mountOptions:
        - hard
        - nfsvers=4.1
    nfs:
        path: "/data/nfs_data"
        service: 192.168.3.16

~~~

### RDB存储后端的PV

~~~ yaml
apiVersion: v1
kind: PersistentVolume
metadata:
    name: pv-rbd-0001
spec:
    capacity:
        storage: 2Gi
    accessModes:
        - ReadWriteOnce
    rbd:
        monitors:
            - ceph-mon01.ilinux.io:6789
            - ceph-mon02.ilinux.io:6789
            - ceph-mon03.ilinux.io:6789
        pool: kube
        image: pv-rbd-001
        user: admin
        secretRef:
            name: ceph-secret
        fsType: ext4
        readOnly: false
    persistentVolumeReclaimPolicy: Recycle

~~~

## PVC

创建pvc时对pv发起使用申请，即为"绑定"。PV和PVC是一一对应的关系，响应PVC申请的PV必须要能够容纳PVC的请求条件。

1. 存储供给
    1. 静态供给: 静态供给是指由集群管理员手动创建一定数量PV的资源供应方式。
    2. 动态供给: 不存在某静态的PV匹配到用户的PVC申请时，Kubernetes集群会尝试为PVC动态创建符合需求的PV，此为动态供给。这种方式依赖于存储类的辅助，PVC必须向一个事先存在的存储类发起动态的分配PV的请求，没有指定存储类的PVC请求会禁止使用动态创建PV的方式

2. 存储绑定:
    用户基于一系列存储需求和访问模式定义好pvc后，Kubernetes系统的控制器即会为查找匹配的PV，并于找到之后在此二者之间建立关联关系，而后它们二者之间的状态即转为"绑定(Binding)"。PV是为PVC而动态创建的，则该PV专用于其PVC，若是无法为PVC找到可匹配的PV，则PVC将一直处于未绑定(unbound)状态，直到有符合条件的PV出现并完成绑定方才可用

    1. 存储使用(Using): Pod资源基于persistenVolumeClaim卷类型的定义，将选定的PVC关联为存储卷，而后即可为内部的容器所使用。
    2. PVC保护(Protection): 为了避免使用中的存储卷被移除而导致数据丢失，启用了PVC保护机制，万一有用户删除了仍处于某Pod资源使用中的PVC时，Kubernetes不会立即予以移除，而是推迟到不再被任何 Pod资源使用后方才执行删除操作。处于此种阶段的PVC资源的status 字段为“Termination” ，并且其Finalizers字段中包含“ kubernetes.io/pvc-protection ” 。

3. 存储回收(Reclaiming)策略:
    1. 留存(Retain)
        留存策略意味着在删除PVC之后, Kubernetes系统不会自动删除 PY，而仅仅是将它置于“释放”(released)状态,不过,此种状态的PV尚且不能被其他PVC申请所绑定,因为此前的申请生成的数据仍然存在，需要由管理员于动决定其后续处理方案.这就意味着,如果想要再次使用此类的PV资源,则需要由管理员按下面的步骤手动执行删除操作.
        1. 删除pv之后，此PV的数据依然留存于外部的存储之上
        2. 手工清理存储系统上依然留存的数据
        3. 手工删除存储系统级的存储卷以释放空间，以便再次创建，或者直接将其重新创建为PV。
    2. 回收(Recycle)
        如果可被底层存储插件支持，资源回收策略会在存储卷上执行数据删除操作并让PV资源再次变为可被Claim.
    3. 删除(Delete)
        对于支持Deleted回收策略的存储插件来说，在pvc被删除后会直接移除PV对象，同时移除的还有PV相关的外部存储系统上的存储资产(asset)。
4. 扩展PVC

### 使用SC创建PVC

~~~ yaml
apiVersion: v1
kind: persistentVolumeClaim
metadata:
    name: pvc-gluster-dynamic-0001
    namespace: Test
    annotations:
        volume.beta.kubernetes.io/storage-class: glusterfs
spec:
    storageClassName: "glusterfs"
    accessModes:
        - ReadWriteOnce
    volumeMode: Filesystem
    resources:
        requests:
            storage: 5Gi
~~~
