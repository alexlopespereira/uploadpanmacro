FROM tiangolo/uwsgi-nginx-flask:flask

COPY ./app /app

# copy over our requirements.txt file
COPY ./app/requirements.txt /tmp/
# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

RUN export LC_ALL="en_US.UTF-8" && export LC_CTYPE="en_US.UTF-8"
#RUN dpkg-reconfigure locales