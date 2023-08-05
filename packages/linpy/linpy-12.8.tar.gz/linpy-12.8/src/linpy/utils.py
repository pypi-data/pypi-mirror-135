from sympy import *


from IPython.display import IFrame
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

extract_to = './data'


def open_pdf(q, ex):
    return IFrame(f'{extract_to}/{q}-{ex}.pdf', 600, 300)


def download_and_unzip(url, extract_to='.'):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


def load():
    url = 'https://drive.google.com/u/0/uc?id=19xIQPABFRfV8veUC3anXIBxBbUEeA37D&export=download'
    download_and_unzip(url, extract_to='.')



def get_inversions(d: dict):
    """
    Принимает словарь, в котором ключ это i
    а значение это p(i)


    Пример входных данных:
    {1:2, 2:6, 3:9, 4:4, 5:7, 6:5, 7:8, 8:1, 9:3}
    Пример выходных данных:
    [1, 4, 6, 2, 3, 2, 2, 0, 0],
    [0, 0, 0, 2, 1, 3, 1, 7, 6],
    [7, 0, 6, 2, 3, 0, 1, 1, 0]


    Возвращает вектор инверсий, левый вектор
    инверсий, правый вектор инверсий
    """
    right = dict()
    left = dict()
    vec = dict()
    for i, val1 in d.items():
        r, l, v = 0, 0, 0

        inv_p = {value: key for key, value in d.items()}

        for k, val2 in d.items():
            if i > k and val1 < val2:
                r += 1

            if i < k and val1 > val2:
                l += 1

        for k, val2 in inv_p.items():
            if k > i and inv_p[k] < inv_p[i]:
                v += 1

        left[i], right[i], vec[i] = l, r, v

    left = list(dict(sorted(left.items())).values())
    right = list(dict(sorted(right.items())).values())
    vec = list(dict(sorted(vec.items())).values())
    return left, right, vec


def smart_decomposition(A):
    """
    Раскладывает квадратную матрицу A на произведение
    элементарных матриц

    Возвращает history где первый элемент - это первая примененная
    операция, второй - вторая, и так далее

    Чтобы восстановить матрицу A используя элементарные матрицы
    s = 1
    for i in history:
        s *= i.inv()

    """
    I = eye(A.shape[0])

    def P_op(n, m):
        return I.elementary_row_op('n<->m', n, m)

    def M_op(n, k):
        return I.elementary_row_op('n->kn', n, k)

    def A_op(n, m, k):
        return I.elementary_row_op('n->n+km', row1=n, row2=m, k=k)

    history = []

    # Будем приводитеть матрицу к единичной, чтобы
    # потом получить Ek * ... * E2 * E1 * A = I
    # и выразить A = E1 * E2 * ... * Ek
    new_A = A

    for col in range(new_A.shape[1]):
        # Выбираем главный элемент
        element_to_one = new_A[col, col]
        # Создаем операцию чтобы сделать единичку из него
        op = M_op(col, 1 / element_to_one)
        history.append(op)
        # Применяем операцию
        new_A = op * new_A
        for row in range(new_A.shape[0]):
            # Зануляем все строчки над и под гланым элементов
            if row != col:
                # Выбираем элемент который будет занулять
                element_to_zero = new_A[row, col]
                # Создаем операцию для зануления
                op = A_op(row, col, -element_to_zero)
                history.append(op)
                # Применяем операцию
                new_A = op * new_A

    return history
