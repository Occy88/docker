docker stop $(docker ps -aq)
docker rm -f $(docker ps -aq)
docker volume rm $(docker volume ls -q)
docker network prune -f
docker rmi -f $(docker images -q)
