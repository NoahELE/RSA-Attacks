from sympy import continued_fraction_convergents, continued_fraction_iterator


def wiener_attack(e, n):
    iter = continued_fraction_iterator(e / n)
    convergents_iter = continued_fraction_convergents(iter)
    for r in convergents_iter:
        # extract numerator and denominator
        k = r.p
        d = r.q

        if k == 0 or (e * d - 1) % k != 0:
            continue

        phi = (e * d - 1) // k
        b = n - phi + 1

        # check if x^2 - b*x + n = 0 has integer root
        discrim = b**2 - 4 * n
        if discrim >= 0:
            root = int(discrim**0.5)
            if root**2 == discrim and (b + root) % 2 == 0:
                return d
    return None
