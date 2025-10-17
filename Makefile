build:
	docker build -t worker:latest .
	minikube image rm worker:latest
	minikube image load worker:latest

deploy:
	kubectl apply -f infra/kubernetes/deployment.yaml

delete:
	kubectl delete -f infra/kubernetes/deployment.yaml
	
redeploy:
	kubectl delete -f infra/kubernetes/deployment.yaml
	kubectl apply -f infra/kubernetes/deployment.yaml

install-deps:
	pip install -r requirements.txt

list-incidents:
	python3 list_incidents.py 