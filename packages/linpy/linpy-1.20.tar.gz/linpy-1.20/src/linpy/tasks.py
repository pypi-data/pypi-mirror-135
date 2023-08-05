IFrame = None


def init_opening(iframe_from_jupyter):
    """
    from IPython.display import IFrame
    init_opening(IFrame)
    """
    global IFrame
    IFrame = iframe_from_jupyter


def open(task):
    """
    Например open(10)
    """
    return IFrame(f'{task}.pdf', width=600, height=300)
