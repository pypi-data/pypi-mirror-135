IFrame = None


def init(iframe):
    global IFrame
    IFrame = iframe



def open(q, ex):
    """
    Сначала нужно вызвать init(IFrame)

    from IPython.display import IFrame

    open(2, 10) открывает q2.10
    """
    return IFrame(f'./11.pdf', width=600, height=300)
