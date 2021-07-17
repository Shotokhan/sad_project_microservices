# sad_project_microservices
<br>
This is a project related to Software Architecture Design (SAD) exam. It is the implementation part of the first iteration of a Scrum process, and it involves 3 microservices: a controller for users, a controller for vaccine bookings and a gateway for the previous services. See the documentation for more infos (it is in Italian because the course was held in Italian). <br>
<br> The Makefile is very useful to automate build & test of the services. In particular, each Dockerfile calls a wrapper script, which runs all tests and then runs the app if and only if all tests pass.
<br>

# Build & Test
You can build this project using the provided Makefile, or you can build each service with its docker-compose.yml file.
<br>
In the first case:
```
make build
make up
make logs
make stop
... and so on
```
To ensure the correct communication among microservices, you have to configure the gateway. See Configuration. <br>
If you want to build and make up a single service, for example gestione_utenti, from sources root:
```
cd gestione_utenti
docker-compose up --build -d
docker-compose logs
```
Each Dockerfile executes a wrapper script, which executes all unit tests for the related microservice, and if all tests pass, then the app is executed.
<br> <br>
To execute integration tests, make sure that the 3 services are up and correctly configured, i.e. the gateway correctly proxies requests to the other services (if you fail to do so, the first integration tests will fail, because they "ping" the system).
<br>
Then, again open a terminal in the sources root and issue the following commands:
```
cd integration_test
python run_all_tests.py
```
If no error is thrown, then all tests are OK, and you will be given the number of tests executed and the time elapsed.

# Configuration
There are 3 configuration files:

- gateway/volume/config.json
- gestione_prenotazioni/volume/config.json
- gestione_utenti/volume/config.json

<br>
Let's start from the bottom: gestione_utenti.
<br> <br>

```
{
	"port": 5000,
	"debug": true,
	"db": "sqlite:////usr/src/app/volume/users.db",
	"secret": "dont_use_this_in_production",
	"session_validity_days": 7
} 
```
The "port" parameter is the port on which the Flask application will listen: if you change it, you have to change the port in the related docker-compose.yml (the one on the right side), otherwise you will not be able to reach the app.
<br>
The "debug" parameter tells Flask if it has to run in debug mode or not.
<br>
The "db" parameter is the URL of the database: you are not forced to use a SQLite DB because SQLAlchemy is used for ORM, but some back-end code assumes to have a serverless DB.
<br>
The "secret" parameter is used to sign session cookies.
<br>
The "session_validity_keys" impacts on cookies' expiration date.
<br> <br>
Let's go ahead to gestione_prenotazioni.
<br> <br>

```
{
	"port": 5000,
	"debug": true,
	"db": "sqlite:////usr/src/app/volume/bookings.db",
	"secret": "dont_use_this_in_production",
	"session_validity_days": 7,
	"deltaDays": 3,
	"maxBookingsPerDay": 5
} 
```
"secret" parameter must be the same between gestione_utenti and gestione_prenotazioni, i.e. there is a shared secret.
<br>
"deltaDays" and "maxBookingsPerDay" parameters are related to application logic.
<br>
The "deltaDays" parameter impacts the scheduling of dataVaccino: if D_0 is the day in which a Paziente issues a Prenotazione and D_V is scheduled dataVaccino, then:

```
D_V >= D_0 + deltaDays
``` 
The "maxBookingsPerDay" parameter is the maximum number of bookings that can be scheduled in each day.
<br> <br>
Finally, let's the configuration of the gateway.
<br> <br>

```
{
	"port": 5000,
	"debug": true,
	"gestione_utenti_url": "http://172.21.0.1:5001",
	"gestione_prenotazioni_url": "http://172.21.0.1:5002",
	"requests_timeout": 2
} 
```
Since the gateway proxies requests to the other microservices, it needs to know where they are located on the network.
<br>
It works both in local networks and over Internet: you just need to specify their URLs. <br>
If you build all the microservices using the provided Makefile, then you may want to know which local IP addresses you should use. <br>

```
make build
make up
make logs
ifconfig
```
In the logs, you can see something like:

```
...
gateway_1  |  * Running on http://172.21.0.2:5000/ (Press CTRL+C to quit)
...
```

And, after issuing "ifconfig" command, you will see something like:

```
...
br-ef26eaab39a7: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.21.0.1  netmask 255.255.0.0  broadcast 172.21.255.255
        inet6 fe80::42:17ff:fe2b:23c8  prefixlen 64  scopeid 0x20<link>
        ether 02:42:17:2b:23:c8  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
...
```
It means that the gateway can access the host network by using the IP address 172.21.0.1; the other two services will be accessible on the host network on the ports specified by the docker-compose.yml file (the left side, on each file).
<br>
So, when you write the URL of the proxied microservices deployed using the Makefile, you use the IP of the host network as viewed by the gateway as IP address, and you use the ports specified in gestione_utenti/docker-compose.yml and gestione_prenotazioni/docker-compose.yml on the left sides as ports.
<br>
Now you're ready to setup "gestione_utenti_url" and "gestione_prenotazioni_url" parameters.
<br>
The "requests_timeout" parameter is the timeout, expressed in seconds, for the request that the gateway issues against a proxied microservice.
<br>

# License
This project is licensed under the [GPL-3.0 license](LICENSE).