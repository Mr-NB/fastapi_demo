FROM python:3.8.2-alpine
LABEL AUTHOR="Nancy-Niu"
USER root

RUN apk add --no-cache --update gcc musl-dev libxslt-dev libffi-dev libressl-dev zlib-dev freetype-dev lcms2-dev tiff-dev tk-dev tcl-dev libxml2-dev  libgcc openssl-dev curl
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -i https://pypi.douban.com/simple -r requirements.txt --upgrade --ignore-installed six
COPY . .

EXPOSE 8084

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
