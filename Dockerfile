FROM python:3.6.8-alpine3.9

RUN apk --no-cache add tzdata && \
        cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
        echo "Asia/Seoul" > /etc/timezone

COPY . /dorian

WORKDIR /dorian

RUN python setup.py install

ENTRYPOINT ["python", "main.py"]