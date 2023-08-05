def task1():
    """
    Дайте определние комплексного числа в алгебраической форме...


    Запись комплексного числа z в виде z = x + iy где x, y - действительные число
    и i - мнимая единица - комплексное число в алгебраической форме

    z = |z| * (cos(alpha) + i * sin(alpha)) - тригонометрическая форма
    z = |z| * e^{i * alpha}


       |     z_2                 z1 (a1 b1)
       |      /---------         z2 (a2 b2)
    l2 |    /         /          z3 (0, 0)
       |  /          /                | a1  a2 |
       |/alpha      /             S = | b1  b2 | = l1 * l2 * sin(alpha)
       |------>-------
       z3  l1  z1
    """
    pass


IFrame = None


def init_opening(IFrame_tmp):
    global IFrame
    IFrame = IFrame_tmp


def task2():
    return IFrame("./2.pdf", width=600, height=300)