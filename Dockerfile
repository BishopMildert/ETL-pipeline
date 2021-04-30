FROM python:3.8

WORKDIR /usr/app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 80

ENTRYPOINT [ "python", "-m", "src.app" ]
