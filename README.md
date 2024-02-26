# pjecz-portal-notarias

Es un sistema web hecho en Flask para que las Notarias entreguen Edictos y revisen Escrituras.

## Configurar

Crear un archivo con las variables de entorno `.env`

```bash
# Flask, para SECRET_KEY use openssl rand -hex 24
FLASK_APP=portal_notarias.app
FLASK_DEBUG=1
SECRET_KEY=xxxxxxxx

# Database
DB_HOST=127.0.0.1
DB_PORT=8432
DB_NAME=pjecz_plataforma_web
DB_USER=xxxxxxxx
DB_PASS=xxxxxxxx
SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://xxxxxxxx:xxxxxxxx@127.0.0.1:8432/pjecz_plataforma_web"

# Google Cloud Storage
CLOUD_STORAGE_DEPOSITO=xxxxxxxx

# Host
HOST=http://127.0.0.1:5000

# Redis
REDIS_URL=redis://127.0.0.1:8379
TASK_QUEUE=pjecz_portal_notarias

# Salt sirve para cifrar el ID con HashID, debe ser igual en la API
SALT=xxxxxxxx

# Si esta en PRODUCTION se evita reiniciar la base de datos
DEPLOYMENT_ENVIRONMENT=develop
```

Crear un bash script para cargar las variables y el entorno virtual

```bash
if [ -f ~/.bashrc ]
then
    . ~/.bashrc
fi

if command -v figlet &> /dev/null
then
    figlet Portal Notarias
else
    echo "== Portal Notarias"
fi
echo

if [ -f .env ]
then
    echo "-- Variables de entorno"
    source .env && export $(sed '/^#/d' .env | cut -d= -f1)
    export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp-api-keys/justicia-digital-gob-mx-perseo-diana.json"
    echo "   CLOUD_STORAGE_DEPOSITO: ${CLOUD_STORAGE_DEPOSITO}"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_PORT: ${DB_PORT}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   DEPLOYMENT_ENVIRONMENT: ${DEPLOYMENT_ENVIRONMENT}"
    echo "   FLASK_APP: ${FLASK_APP}"
    echo "   GOOGLE_APPLICATION_CREDENTIALS: ${GOOGLE_APPLICATION_CREDENTIALS}"
    echo "   HOST: ${HOST}"
    echo "   REDIS_URL: ${REDIS_URL}"
    echo "   SALT: ${SALT}"
    echo "   SECRET_KEY: ${SECRET_KEY}"
    echo "   SQLALCHEMY_DATABASE_URI: ${SQLALCHEMY_DATABASE_URI}"
    echo "   TASK_QUEUE: ${TASK_QUEUE}"
    echo
    export PGHOST=$DB_HOST
    export PGPORT=$DB_PORT
    export PGDATABASE=$DB_NAME
    export PGUSER=$DB_USER
    export PGPASSWORD=$DB_PASS
fi

if [ -d .venv ]
then
    echo "-- Python Virtual Environment"
    source .venv/bin/activate
    echo "   $(python3 --version)"
    export PYTHONPATH=$(pwd)
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo
    echo "-- Arrancar Flask o RQ Worker"
    alias arrancar="flask run --port=5000"
    alias fondear="rq worker ${TASK_QUEUE}"
    echo "   arrancar = flask run --port=5000"
    echo "   fondear = rq worker ${TASK_QUEUE}"
    echo
fi
```
