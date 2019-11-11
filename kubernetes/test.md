kubectl run  nginx-deplpy --image=nginx:1.14-alpine --port=80 --replicas=1 --dry-run=true 
kubectl get deployment

kubectl get pods

kubectl delete nginx-deplpy-5b77b747dc-b4t7j

kubectl expose deployment nginx-deplpy  --name nginx.abc.com --port=80 --target-port=80 --protocol=TCP

kubectl get svc


kubectl  run client  --image=busybox  --replicas=1 -it --restart=Never

kubectl describe  svc nginx 

kubectl  get pods --show-labels

kubectl edit svc  nginx
kubectl delete svc nginx 

kubectl run myapp --image=ikubernetes/myapp:v1 --replicas=2
kubectl expose deployment myapp  --name myapp --port=80 --target-port=80 

kubectl scale --replicas=5 deployment myapp

kubectl set image deployment myapp myapp=ikubernetes/myapp:v2


kubectl rollout  status deployment myapp
kubectl rollout  undo deployment myapp

kubectl edit svc  myapp
NodePort