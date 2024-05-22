FROM python:3.9
WORKDIR /var/
COPY . .
# #Install Package Dependencies
RUN apt-get update -y
RUN apt install nano -y
RUN pip install --requirement /var/house_price/requirements.txt
RUN apt-get update && apt-get install -y python3
RUN apt-get install libevent-dev -y
# # #Instal & Configuration Supervisor
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY docker-config/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker-config/service.conf /etc/supervisor/conf.d/service.conf

# #Folder Directory
WORKDIR /var/house_price/

# #START USING SUPERVISORD
CMD ["/usr/bin/supervisord"]
# CMD ["/usr/local/bin/python", "app.py"]