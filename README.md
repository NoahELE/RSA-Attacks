# RSA Attacks

This repo contains implementations of some attacks on RSA encryption algorithm.

## Attacks

### Chosen Ciphertext Attack

1. Build the image

```sh
cd chosen_ciphertext
docker build -t chosen-ciphertext .
```
or directly pull the image

```sh
docker pull noahele/chosen-ciphertext:latest
```

2. Run the image

```sh
docker run --rm -it chosen-ciphertext
```
or (if pulled from Docker hub)
```sh
docker run --rm -it noahele/chosen-ciphertext
```


### Fermat Factorization Attack

1. Build the image

```sh
cd fermat
docker build -t fermat .
```
or directly pull the image

```sh
docker pull noahele/fermat:latest
```

2. Run the image

```sh
docker run --rm -it fermat
```
or (if pulled from Docker hub)
```sh
docker run --rm -it noahele/fermat
```

### Pollard Factorization Attack

1. Build the image

```sh
cd pollard
docker build -t pollard .
```
or directly pull the image

```sh
docker pull noahele/pollard:latest
```

2. Run the image

```sh
docker run --rm -it pollard
```
or (if pulled from Docker hub)
```sh
docker run --rm -it noahele/pollard
```

### Broadcast Attack

1. Build the image

```sh
cd broadcast
docker build -t broadcast .
```
or directly pull the image

```sh
docker pull noahele/broadcast:latest
```

2. Run the image with optional environmental variables
```sh
docker run --rm -it \
  -e PUB_EXP=<e> \
  -e NUM_RECEIVER=<num_receiver> \
  -e TEXT=<text> \
  -e PAD=<random_pad> \
  -e TIMEOUT=1 \
  broadcast
```
or (if pulled from Docker hub)
```sh
docker run --rm -it
  -e PUB_EXP=<e> \
  -e NUM_RECEIVER=<num_receiver> \
  -e TEXT=<text> \
  -e PAD=<random_pad> \
  -e TIMEOUT=1 \
  noahele/broadcast
```

 - PUB_EXP: the public exponent used for encryption. Default to 3.
 - NUM_RECEIVER: number of receiver in the boardcast. Default to 3.
 - TEXT: the broadcast message. Default to "welcome to broadcast attack simulation".
 - PAD: random padding for the plaintext before encryption. Default to `False`.
 - TIMEOUT: timeout in second for the attacker to attack the server

### Wiener's Attack

1. Build the image

```sh
cd wieners
docker build -t wieners .
```
or directly pull the image

```sh
docker pull noahele/wieners:latest
```

2. Run the image with optional environmental variables
```sh
docker run --rm -it \
  -e NUM_BITS=<num_bits> \
  -e WIENER=<wiener_vulnerable> \
  -e TIMEOUT=1 \
  wieners
```
or (if pulled from Docker hub)
```sh
docker run --rm -it
  -e NUM_BITS=<num_bits> \
  -e WIENER=<wiener_vulnerable> \
  -e TIMEOUT=1 \
  noahele/wieners
```
 - NUM_BITS: number of bits of p and q, e.g., 10, 256, 512, etc. Currently,
the server takes quite some time to generate keys of size 1024 and
above. It’s recommended to use smaller number to run the container.
 - WIENER: if ”y” or ”Y” specified, the scheme is Wiener’s vulnerable
and it is expected to obtain the private key d. Default to ”y”.
 - TIMEOUT: timeout in second for the attacker to attack the server

### Common Modulus Attack

1. Build the image

```sh
cd common-modulus
docker build -t common-modulus .
```
or directly pull the image

```sh
docker pull noahele/common-modulus:latest
```

2. Run the image

```sh
docker run --rm -it common-modulus
```
or (if pulled from Docker hub)
```sh
docker run --rm -it noahele/common-modulus
```

### Heninger Attack

1. Build the image

```sh
cd Heninger_attack
docker build -t heninger .
```
or directly pull the image

```sh
docker pull noahele/heninger:latest
```

2. Run the image

```sh
docker run --rm -it heninger
```
or (if pulled from Docker hub)
```sh
docker run --rm -it noahele/heninger
```

> NOTE: This attack might fail due to the randomness of the algorithm. You should use a bit size between 512 and 2048.
