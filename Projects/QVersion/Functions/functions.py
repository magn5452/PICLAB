def poly21(vars, *params):
    I, T = vars
    p00, p10, p01, p11, p20 = params
    y = p00 + p10 * I + p01 * T + p11 * I * T + p20 * I ** 2
    return y

def poly22(vars, *params):
    I, T = vars
    p00, p10, p01, p11, p20, p02 = params
    y = p00 + p10 * I + p01 * T + p11 * I * T + p20 * I ** 2 + p02 * T ** 2
    return y

def poly222(vars, *params):
    I, T = vars
    p00, p10, p01, p11, p20, p02, p21, p12 = params
    y = p00 + p10 * I + p01 * T + p11 * I * T + p20 * I ** 2 + p02 * T ** 2 + p12 * I * T ** 2 + + p21 * I ** 2 * T
    return y