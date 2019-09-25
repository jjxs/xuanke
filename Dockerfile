FROM ubuntu:latest
LABEL maintainer 957990586@qq.com
WORKDIR /opt
RUN apt-get update -y
RUN apt-get install -y mysql-server libmysqlclient-dev redis-server python3 python3-pip python3-dev git supervisor nginx
RUN sed -i 's/bind 127.0.0.1 ::1/bind 127.0.0.1/g' /etc/redis/redis.conf

#clone workflowdemo code
RUN mkdir -p /var/log/web
WORKDIR /opt
RUN git clone https://github.com/jjxs/xuanke.git
WORKDIR /opt/xuanke
RUN pip3 install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

#create database user and import data
RUN service mysql restart
RUN mysql -uroot -e "CREATE DATABASE if not exists xuanke DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
RUN mysql -uroot -e "CREATE USER root@127.0.0.1 IDENTIFIED BY '123456'"
RUN mysql -uroot -e "GRANT ALL PRIVILEGES ON xuanke.* TO 'root'@'127.0.0.1';"
Run mysql -uroot -e "flush privileges"
#RUN mysql --one-database loonflownew < /opt/workflowdemo/loonflow.sql

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic
RUN python3 createsuperuser.py

#clone loonflow code
#WORKDIR /opt
#RUN git clone https://github.com/blackholll/loonflow.git
#WORKDIR /opt/loonflow
#RUN git checkout develop
#WORKDIR /opt/loonflow/requirements
#RUN pip3 install -r dev.txt



ADD nginx.conf /etc/nginx/nginx.conf
ADD supervisord.conf /etc/supervisor/supervisord.conf
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
#RUN cp -rf /opt/loonflow/static/* /opt/workflowdemo/static/
EXPOSE 80
EXPOSE 8000
#CMD ["/docker-entrypoint.sh", "start"]