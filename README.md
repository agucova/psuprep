![PSUPrep](/static/logo.png)

## Introduction - CS50's Final Projectst
**PSUPrep** is a dynamic summary generator for the math university admission test in Chile (*Prueba de Selección Universitaria* or "PSU"). 

The webapp allows students to generate on request a cheat sheet with their selected contents, this way they can easily print a small study aid (conventional cheat sheets for the test usually have around 20 pages).

## Architecture
When a request is made, Gunicorn acts as the HTTPS server and forwards requests, through WSGI, to Flask. When a compile request is made, Flask creates a task in the queue (huey) which starts pdflatex compilation through dynamic import of sections. Finally, the resulting PDF is sent to the user.
![Architecture](/static/arch.png)
