1. Build the images

```
$ docker-compose -f ./attack-docker-compose.yaml build
```

2. Run interactive client

```
$ docker-compose -f ./attack-docker-compose.yaml run client /bin/bash
```

> this will automatically starts the server

3. Run the interactive attacker in another terminal (it is not interactive at the moment. will be implemented)

```
$ docker-compose -f ./attack-docker-compose.yaml run attacker /bin/bash
```

> this will automatically starts the server
