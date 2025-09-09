def Fermat_factor(N, e, ct):

    max_diff=10**6
    a = isqrt(N)
    if a * a < N:
        a += 1


    limit = max_diff // 2
    
    for _ in range(limit):
        diff = a*a - N
        if is_square(diff):  # b^2 なら即 return
            b = isqrt(diff)
            p = a + b
            q = a - b
        
            try:
                phi = (p-1) * (q-1)
                d = pow(e, -1, phi)
                plain_hex = pow(ct, d, p*q)
                plain_text = long_to_bytes(plain_hex)
                return plain_text.decode()
            except Exception:
                return N_prime(N, e, ct)

        a += 1
    return N_prime(N, e, ct)
    