FROM nginx:alpine

COPY ./nginx/* /etc/nginx/
COPY ./run.sh /run.sh

RUN apk add --no-cache openssl bash
RUN chmod +x /run.sh

VOLUME [ "/vol/static", "/vol/www" ]

CMD ["/run.sh"]