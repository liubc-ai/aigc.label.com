#!/bin/bash
PROJECT_DIR=$(pwd)
IMAGE_NAME=aigc.label.com
DATA_DIR="/mnt/d/AIGC/data"
PORT=7865

function build_image(){
    docker ps -a | grep ${IMAGE_NAME}:latest | awk {'print $1'} | xargs docker rm -f 
    docker build -t ${IMAGE_NAME}:latest .
    # remove medium images
    docker images | grep none | awk {'print $3'} | xargs docker rmi -f 
}

function clean_container(){
    docker ps -a | grep ${IMAGE_NAME}:latest | awk {'print $1'} | xargs docker rm -f
}

function start_container(){
    docker run \
        --rm \
        -p ${PORT}:${PORT} \
        -v ${DATA_DIR}:/data \
        -d ${IMAGE_NAME}:latest
}

function view_docker_logs(){
    tail -f "/web/tomcat/logs/aigc.label.com/stdout.log"
}

function view_container_id() {
    docker ps -a | grep "${IMAGE_NAME}" | awk {'print $1'}
}

function exec_container(){
    container_id=$(view_container_id)
    docker exec -it ${container_id} /bin/bash
}

function ssh_tunnel(){
    ssh -fNR 0.0.0.0:7865:localhost:7865 42135@$(hostname).local
}

function push_image(){
    docker login --username liubochong --password liubochong
    docker push liubochong/aigc.label.com:latest
}

function pull_image(){
    docker login --username liubochong --password liubochong
    docker pull liubochong/aigc.label.com:latest
}

cat << "EOF"
1. build_image
2. start_container
3. clean_container
4. view_docker_logs
5. view_container_id
6. exec_container
7. ssh_tunnel
8. push_image
9. pull_image

EOF

read num
case $num in
1)
    build_image
    ;;
2)
    start_container
    ;;
3)
    clean_container
    ;;
4)
    view_docker_logs
    ;;
5)
    view_container_id
    ;;
6)
    exec_container
    ;;
7)
    ssh_tunnel
    ;;
8)
    push_image
    ;;
9)
    pull_image
    ;;
esac