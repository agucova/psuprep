![PSUPrep](/static/logo.png)

## Introduction - CS50's Final Projectst
**PSUPrep** is a dynamic summary generator for the math university admission test in Chile (*Prueba de Selección Universitaria* or "PSU"). 

The webapp allows students to generate on request a cheat sheet with their selected contents, this way they can easily print a small study aid (conventional cheat sheets for the test usually have around 20 pages).

## Architecture
[Heroku](https://psuprep.herokuapp.com/) hosts a web runner and a Redis database with a full TeXLive installation.

When a request is made, [Gunicorn](https://gunicorn.org/) acts as the HTTPS server and forwards requests, through WSGI, to Flask. When a compile request is made, Flask creates a task in the queue ([huey](https://github.com/coleifer/huey), using Redis) which starts PDFLaTeX compilation through dynamic import of sections. Finally, the resulting PDF is sent to the user. 


![Architecture](/static/arch.png)
