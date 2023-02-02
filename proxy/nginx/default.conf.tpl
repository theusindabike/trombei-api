upstream trombeiapi {
    server web:8000;
}

server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    location / {
        proxy_pass http://trombeiapi;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }

    location /static_files/static/ {
        alias /vol/static_files/static/;
    }

}