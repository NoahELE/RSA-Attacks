from sympy import continued_fraction_convergents, Rational


def wiener_attack(e, n):
    convergents = continued_fraction_convergents(Rational(e, n))
    for k, d in convergents:
        if k == 0:
            continue
        phi = (e * d - 1) // k
        b = n - phi + 1

        # check if x^2 - s*x + n = 0 has integer root
        discrim = b**2 - 4 * n
        if discrim >= 0:
            root = int(discrim**0.5)
            if root**2 == discrim and (b + root) % 2 == 0:
                return d
    return None
