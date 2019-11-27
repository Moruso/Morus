# pv-sc-pvc

## pv

~~~ shell
kubect get pv -A
~~~

### PV资源生命周期的各个阶段

* Available: 可用状态的自有资源，尚未被PVC绑定
* Bound: 已经绑定至某PVC
* Released: 绑定的PVC已经被删除，但资源尚未被集群收回
* Failed: 因自动回收资源失败而处于的故障状态

### 通用字段

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
