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
