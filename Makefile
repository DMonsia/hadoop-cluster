.ONESHELL:

# Build docker image
build:
	docker build -t monsia/hadoop2 .

create-network:
	docker network create --driver=bridge hadoop

# Run container
create-master:
	docker run -itd \
    	--net=hadoop \
    	-p 50070:50070 \
    	-p 8088:8088 \
    	--name master \
    	--hostname master \
    	monsia/hadoop2

create-slave:
	docker run -itd \
		-p ${port}:8042 \
		--net=hadoop \
		--name ${hostname} \
		--hostname ${hostname} \
		monsia/hadoop2