from IPython.display import IFrame

# IFrame = None

# def init_opening(IFrame_from_jupyter):
#     global IFrame
#     IFrame = IFrame_tmp

def open(task):
    """
    Например open(10)
    """
    return IFrame(f'./data/{task}.pdf', width=600, height=300)
