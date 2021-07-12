# sad_project_microservices
<br>
This is a project related to Software Architecture Design (SAD) exam. It is the implementation part of the first iteration of a Scrum process, and it involves 3 microservices: a controller for users, a controller for vaccine bookings and a gateway for the previous services. See the documentation for more infos (it is in Italian because the course was held in Italian). <br>
<br> The Makefile is very useful to automate build & test of the services. In particular, each Dockerfile calls a wrapper script, which runs all tests and then runs the app if and only if all tests pass.
