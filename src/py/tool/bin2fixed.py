def bin2fixed(signed, N, Nf, num):
    shift = 1
    result = 0
    q = -Nf
    
    if signed == 'S':
        sig = num & (1 << N-1)
        if sig:
            num = ~num + 1
    elif signed == 'U':
        sig = 0
    else:
        raise ValueError("S for signed, U for unsigned")

    while (N - Nf) > q:
        if num & shift:
            result += 2**q
            
        q += 1
        shift = shift << 1
        
    
    return -result if sig else result