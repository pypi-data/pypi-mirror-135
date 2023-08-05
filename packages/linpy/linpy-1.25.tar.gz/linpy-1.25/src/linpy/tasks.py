from IPython.display import IFrame


def open(q, ex):
    """
    Например open(2, 10) открывает q2.10
    """
    return IFrame(f'q2ex1.pdf', width=600, height=300)
