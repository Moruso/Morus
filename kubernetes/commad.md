# kubectl

kubectl cluster-info
kubectl version --short=true

### kubectl get/describe 资源 选项

* 资源:
    * namespace
    * pods
    * deployments
* 选项:
    * -o # 输出格式
        * yaml 
        * json
        * wide
    * -l # 标签选择

    * -n # 指定命名空间

    * -A # 所有的命名空间


kubectl get namespace -o wide
kubectl get pods -n kube-system -o wide
kubectl describe pods myapp-5c647497bf-zsrtz
kubectl expose deployments/myapp --type="NodePort" --port=80 --name=myapp 
kubectl get svc/myapp
kubectl logs nginx 
kubectl describe services myapp
kubectl scale deployments/myapp --replicas=3
kubectl exec 
kubectl delete
kubectl get pods --show-lables
kubectl get pods -L env, tier
kubectl label pods/pod-example env=production
kubectl label pods/pod-with-labels env=testing --overwrite
kubectl label pods -l "env!=qa" -L env

kubectl run 