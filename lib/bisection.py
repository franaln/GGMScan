def bisection(fn, vmin, vmax, precision=0.01, max_iteration=100, debug=False):

    """
    Find best value to get fn(best)=0, between vmin and vmax with some precision

    fn must be a function with value as only argument returning an output we want to find the root
    """

    a = vmin
    b = vmax

    v_p = 99
    last_v_p = 0
    iteration = 0

    while abs(v_p) > precision and iteration < max_iteration:

        p = 0.5 * (a + b)

        v_a = fn(a)
        v_b = fn(b)
        v_p = fn(p)

        if debug:
            print('Bisection (%i iteration): a=%.2f -> f(a)=%.2f, b=%.2f -> f(b)=%.2f, p=%.2f -> f(p)=%.2f' % (iteration, a, v_a, b, v_b, p, v_p))

        a = p if v_a*v_p > 0 else a
        b = p if v_b*v_p > 0 else b

        if a == b:
            a = vmax

        iteration += 1

        # last_v_p = v_p
        # if abs(v_a - v_p) <= 1 and abs(v_b - v_p) <= 1:
        #     break


    return p, v_p
