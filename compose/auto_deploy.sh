#! /bin/bash

# This shell script quickly deploys your project to your
# DigitalOcean Droplet

if [ -z "$BRILLIANT_CLOUD_IP_ADDRESS" ]
then
    echo "BRILLIANT_CLOUD_IP_ADDRESS not defined"
    exit 0
fi

git archive --format tar --output ./project.tar master

echo 'Uploading project...'

rsync ./project.tar ubuntu@$BRILLIANT_CLOUD_IP_ADDRESS:/tmp/project.tar

echo 'Uploading project...'

echo 'Building image...'
ssh -o StrictHostKeyChecking=no ubuntu@$BRILLIANT_CLOUD_IP_ADDRESS << 'ENDSSH'
    sudo mkdir -p /app
    sudo rm -rf /app/* && sudo tar -xf /tmp/project.tar -C /app
    docker-compose -f /app/docker-compose.prod.yml build
    sudo supervisorctl restart flask-celery-app
ENDSSH
echo 'Build complete.'
