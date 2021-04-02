import numpy as np


def rotate(origin: np.ndarray, points: np.ndarray, angle: float) -> np.ndarray:
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.

    origin:  1D-Array [x,   y]
    points:  2D-Array [xs, ys]
    returns: 2D-Array [xs, ys]
    """
    ox, oy = origin
    px, py = points

    qx = ox + np.math.cos(angle) * (px - ox) - np.math.sin(angle) * (py - oy)
    qy = oy + np.math.sin(angle) * (px - ox) + np.math.cos(angle) * (py - oy)

    return np.array([qx, qy])


def _main():
    min_x = -1
    min_y = -3
    max_x = 2
    max_y = 5

    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2
    origin = [cx, cy]

    degrees = 45
    angle = np.deg2rad(360 - degrees)

    points = [[min_x, min_x, max_x, max_x], [min_y, max_y, min_y, max_y]]

    points = np.array(points)

    print(origin)
    print(points)
    r = rotate(origin, points, angle)

    print(r)

    import matplotlib.pyplot as plt

    plt.scatter(cx, cy)
    plt.scatter(points[0], points[1])
    plt.scatter(r[0], r[1])
    plt.show()


if __name__ == "__main__":
    _main()
