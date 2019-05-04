import numpy as np


def find_toppings_and_pizza():
    """
    :return: dummy result for toppings and pizza
    """
    return {"red circles": [[-1., 0, -0.7], [-.5, 0, -0.7], [.3, .3, -0.7]],
            "black rings": [np.random.rand(3) for _ in range(4)],
            "yellow triangles": [],
            "pink squares": [],
            "blue fish": [],
            "pizza_outer": [[0, 0, -.7]],
            "pizza_inner": [[.1, .1, -.7], [-.1, .1, -.7]]}


