# Koora

College project
Group Name : Dali's


For Dokcer Users : 
    RUN 
        docker-compose run kooraApp

For Non Docker Users : 
    RUN
        virtualenv .
        source bin/activate
        pip install -r requirements.txt
        export $(cat .env)"
        cd src/
        python manage.py runserver 0.0.0.0:$APP_PORT
