FROM node:11.14-slim
LABEL maintainer="apiotrowski312 <apiotrowski312@gmail.com>"

RUN apt-get update && \
    apt-get -y install python3 python3-pip python3-dev python3-pil && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN pip3 install -e .[everything]

RUN python3 -m shuup_workbench migrate
RUN python3 -m shuup_workbench shuup_init

RUN python3 setup.py build_resources
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'admin')" | python3 -m shuup_workbench shell

RUN python3 -m shuup_workbench collectstatic
RUN pip3 install uwsgi

#EXPOSE 8000
CMD uwsgi --http :8000 --module shuup_workbench.wsgi --check-static ./shuup_workbench/var/
