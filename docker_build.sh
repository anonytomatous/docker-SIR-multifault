containername=$1

docker ps -aq --filter "name=$containername" | grep -q . && docker stop $containername && docker rm $containername
docker build --tag sir-dataset:latest ./docker/
docker run -dt --name $containername -v $(pwd)/docker/workspace:/root/workspace -v $(pwd)/coverage_files:/root/coverage_files -v $(pwd)/failing_tests:/root/failing_tests -v $(pwd)/faulty_lines:/root/faulty_lines sir-dataset:latest
docker exec -it $containername /bin/bash
