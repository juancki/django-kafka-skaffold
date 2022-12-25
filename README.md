# django-kafka-skaffold

Demo project to test the skaffold/helm/kubernetes configuration for a Django rest_framework with Kafka integration.

Details:
- Uses default `sqlite3` DB.
- Uses `logpipe` for kafka integration.
- Ovrrides default save / update methods in [app/models.py](app/models.py)


### Run
You can run the examplec:
- `skaffold run -p dev` to launch the deployment and start the kafka cluster.
```
Waiting for deployments to stabilize...
 - deployment/django-deployment is ready. [2/3 deployment(s) still pending]
 - statefulset/backend-kafka is ready.
 - statefulset/backend-zookeeper is ready. [1/3 deployment(s) still pending]
Deployments stabilized in 1.291 second
You can also run [skaffold run --tail] to get the logs
```
- Port forward `kubectl port-forward svc/django-svc 8000:8000`


### Check the integration
1. Open an terminal and run kafkacat `kcat` against localhost:9094.
```
kcat -b localhost:9094 -C -t people  -J
```
2. Open a second terminal and POST message with cURL:
```bash
curl -X POST --data-binary '{"first_name":"first","last_name":"second"}' -H 'Content-Type: application/json' localhost:8000/app/ -v
```

The results should look like this:
```json
{"topic":"people","partition":0,"offset":18,"tstype":"create","ts":1672006861223,"broker":0,"key":"19aa868c-c9ad-46be-adb7-2291bfc61bbc","payload":"json:{\"type\":\"person\",\"version\":1,\"message\":{\"uuid\":\"19aa868c-c9ad-46be-adb7-2291bfc61bbc\",\"first_name\":\"first\",\"last_name\":\"second\"}}"}
```

