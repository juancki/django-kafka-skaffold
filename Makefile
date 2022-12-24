template-dev:
	helm template k8s/helm/django-kafka-skaffold -f k8s/helm/django-kafka-skaffold/values.yaml -f k8s/helm/django-kafka-skaffold/values-environment-dev.yaml

template:
	helm template k8s/helm/django-kafka-skaffold -f k8s/helm/django-kafka-skaffold/values.yaml