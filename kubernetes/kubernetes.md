### Masters && nodes

cat >>/etc/hosts<<EOF
192.168.3.16 k8s-master 
192.168.3.17 k8s-node01
192.168.3.18 k8s-node02
EOF

###### 配置 docker-ce repo
wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

###### 配置kubernetes repo

[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=0

###### 安装 kubernetes key 

rpm --import https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg

###### 安装
yum install docker-ce  kubelet  kubeadm kubectl

###### 启动docker
systemctl start docker
systemctl enable docker

######  配置网络
cat <<EOF>  /etc/sysctl.d/kubernetes.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
vm.swappiness=0
EOF

sysctl -p /etc/sysctl.d/kubernetes.conf

###### kubelet 开机启动

systemctl enable kubelet

###### 忽略swap报错


sed -i 's/\(KUBELET_EXTRA_ARGS=\)/\1"--fail-swap-on=false"/g' /etc/sysconfig/kubelet
vim /etc/sysconfig/kubelet
"--fail-swap-on=false"

###### 获取镜像列表

kubeadm config images list

##### 从代理镜像站更新镜像

docker pull gcr.azk8s.cn/google_containers/kube-apiserver:v1.14.2
docker pull gcr.azk8s.cn/google_containers/kube-controller-manager:v1.14.2
docker pull gcr.azk8s.cn/google_containers/kube-scheduler:v1.14.2
docker pull gcr.azk8s.cn/google_containers/kube-proxy:v1.14.2
docker pull gcr.azk8s.cn/google_containers/pause:3.1
docker pull gcr.azk8s.cn/google_containers/etcd:3.3.10
docker pull gcr.azk8s.cn/google_containers/coredns:1.3.1

docker pull gcr.azk8s.cn/google_containers/kubernetes-dashboard-amd64:v1.10.1

###### 修改镜像标签
docker images |grep gcr.azk8s.cn| awk '{print "docker tag ",$1":"$2,$1":"$2}'|sed -e 's#gcr.azk8s.cn/google_containers#k8s.gcr.io#2' |bash

docker rmi  $(docker image ls  |grep google_containers|awk {'print$1 ":" $2'})

###### 初始化

kubeadm init --pod-network-cidr=10.244.0.0/16 --ignore-preflight-errors=Swap

######  部署flanel

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

kubectl get pods -n kube-system

### nodes

docker pull gcr.azk8s.cn/google_containers/pause:3.1
docker pull gcr.azk8s.cn/google_containers/kube-proxy:v1.14.2

docker images |grep gcr.azk8s.cn| awk '{print "docker tag ",$1":"$2,$1":"$2}'|sed -e 's#gcr.azk8s.cn/google_containers#k8s.gcr.io#2' |bash

docker rmi  $(docker image ls  |grep google_containers|awk {'print$1 ":" $2'})


### fu

kubeadm join 192.168.252.11:6443 --token hzgcls.horwcteyy7eg1yxa --discovery-token-ca-cert-hash sha256:9be1bd4bc657c5fd446702c73e9819227e2b53e40eb76fe75e7f30fe5b5893e8  --ignore-preflight-errors=Swap

kubeadm join 192.168.3.16:6443 --token c53v1z.corlp5auutxy4xkg \
    --discovery-token-ca-cert-hash sha256:975b754267f9fd3172853667e2db6655705e95f7895718c78c556cb44efb0b6f --ignore-preflight-errors=Swap


kubectl get cs
kubectl get ns
kubectl get pods -n kube-system
kubectl get nodes
kubectl describe -n kube-system po kube-flannel
kubectl  describe  pod coredns   -n kube-system
kubectl get pods -n kube-system -o wide
kubectl -n kube-system logs kube-flannel-ds -c install-cni




#####node

[root@node01 ~]# vim /usr/lib/systemd/system/docker.service
[root@node01 ~]# vim /etc/sysconfig/kubelet
[root@node01 ~]# systemctl start docker
