# HiveWatch

HiveWatch is a simple Thread Deception Platform that utlizes honeypot technology to collect and monitor for threat and attack data.

## Architecture

The architecure is distributed where some components run on docker locally and some are deployed on Rahti Openshift Platform.

## Configuration

Before running the platform, required configurations need to be made. Set the `MQTT_HOST` value in the `docker-compose.yml`. Specify the route host in the `elasticsearch.yml`, `kibana.yml` and `mosquitto.yml` files. Set the `ABUSEIPDB_API_KEY` value in the `enrichement.yml`. Also log into openshift using `oc login` command.

## How to run

The project includes a bash script that deploys the whole environment. 

```bash
sudo chmod +x start.sh
sudo ./start.sh
```

This will deploy all the services.

## Generating the data

To generate the data you need to ssh into the cowrie honepot and perform some activity like running commands, creating files etc.

Then you can log into kibana interface and create an index template for the new data which is being ingested. After the index template is created, you can create custom dashboards in the `Dashboard` tab and create visualizations as you want. Following is a sample of different data visualizations that can be created:

