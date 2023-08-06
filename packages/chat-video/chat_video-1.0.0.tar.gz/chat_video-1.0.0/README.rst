DjangoVideoChat

Description 
A Group video calling application using the Agora Web SDK with a Django backend.

How to use this source code

Step 1
Install requirements

Step 2
Update Agora credentals
In order to use this project you will need to replace the agora credentials in (views.py) and (streams.js).

Create an account at agora.io and create an (app). 
Once you create your app, you will want to copy the (appid) & (appCertificate) to update (views.py) and (streams.js).


Step 3
Start server

python manage.py runserver


