def get_inversions(d: dict):
    """
    Принимает словарь, в котором ключ это i
    а значение это p(i).

    Пример входных данных:
    {1:2, 2:6, 3:9, 4:4, 5:7, 6:5, 7:8, 8:1, 9:3}

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
