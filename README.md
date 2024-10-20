# RSA Attacks

This repo contains implementations of some attacks on RSA encryption algorithm.

## Attacks

### Chosen Ciphertext Attack

Build the image

```sh
cd chosen_ciphertext
docker build -t chosen-ciphertext .
```

Run the image

```sh
docker run --rm -it chosen-ciphertext
```

### Fermat Factorization Attack

Build the image

```sh
cd fermat
docker build -t fermat .
```

Run the image

```sh
docker run --rm -it fermat
```

### Pollard Factorization Attack

Build the image

```sh
cd pollard
docker build -t pollard .
```

Run the image

```sh
docker run --rm -it pollard
```

### Broadcast Attack

### Wiener's Attack

Build the image

```sh
cd wieners
docker build -t wieners .
```
or load the image

```sh
docker load -i wieners.tar
```

Run the image with optional environmental variables
```sh
docker run --rm -it \
  -e NUM_BITS=<num_bits> \
  -e WIENER=<wiener_vulnerable> \
  -e TIMEOUT=1 \
  wieners
```
 - NUM_BITS: number of bits of p and q, e.g., 10, 256, 512, etc. Currently,
the server takes quite some time to generate keys of size 1024 and
above. It’s recommended to use smaller number to run the container.
 - WIENER: if ”y” or ”Y” specified, the scheme is Wiener’s vulnerable
and it is expected to obtain the private key d. Default to ”y”.
 - TIMEOUT: timeout in second for the attacker to attack the server

### Heninger Attack

Build the image

```sh
cd Heninger_attack
docker build -t heninger .
```

Run the image

```sh
docker run --rm -it heninger
```

> NOTE: This attack might fail due to the randomness of the algorithm. You should use a bit size between 512 and 2048.
