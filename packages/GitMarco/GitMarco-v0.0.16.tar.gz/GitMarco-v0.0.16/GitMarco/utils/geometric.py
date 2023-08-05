import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator


def stl2mesh3d(stl_mesh):
    # stl_mesh is read by nympy-stl from a stl file; it is  an array of faces/triangles (i.e. three 3d points)
    # this function extracts the unique vertices and the lists I, J, K to define a Plotly mesh3d

    p, q, r = stl_mesh.vectors.shape  # (p, 3, 3)

    # the array stl_mesh.vectors.reshape(p*q, r) can contain multiple copies of the same vertex;
    # extract unique vertices from all mesh triangles

    vertices, ixr = np.unique(stl_mesh.vectors.reshape(p * q, r), return_inverse=True, axis=0)
    i = np.take(ixr, [3 * k for k in range(p)])
    j = np.take(ixr, [3 * k + 1 for k in range(p)])
    k = np.take(ixr, [3 * k + 2 for k in range(p)])

    return vertices, i, j, k


def grid2grid_interp(grid, new_grid, feature, fill_value=None,
                     correction: bool = False, n: int = 25):
    """
    :param grid: original grid
    :param new_grid: new_grid to interpolate on
    :param feature: values on the original grid
    :param fill_value: filling value for intepolation failures
    :param correction: apply or not a correction on nan values based on n neighbors
    :param n: number of neighbors
    :return:

    Intepolates features from grid to new_grid, filling wrong values with fill_value or nan and
    applying a correction to nan averaging with n closest neighbors
    """

    if fill_value is None:
        interp = LinearNDInterpolator(list(zip(grid[:, 0], grid[:, 1], grid[:, 2])),
                                      feature,
                                      rescale=False,
                                      )
    else:
        interp = LinearNDInterpolator(list(zip(grid[:, 0], grid[:, 1], grid[:, 2])),
                                      feature,
                                      rescale=False,
                                      fill_value=fill_value
                                      )
    y = interp(new_grid[:, 0], new_grid[:, 1], new_grid[:, 2])

    if correction and fill_value is None:
        for i, item in enumerate(y):
            if np.isnan(item):
                y[i] = node_neighbors_average(new_grid[i:i + 1], new_grid, y, n=n)

    return y


def node_neighbors_average(
        node,
        nodes,
        values,
        n: int = 50):
    """
    :param node: objective node
    :param nodes: grid nodes
    :param values: values calculated in nodes
    :param n: number of neighbors
    :return value: averaged value

    Find the the average value for a node based on n closest neighbors
    """

    nodes = np.asarray(nodes)

    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)

    df = pd.DataFrame()
    df['dist_2'] = dist_2
    df['values'] = values
    df.sort_values('dist_2', inplace=True)
    df = df.iloc[:n, :]

    new_values = df['values'][np.array(df.index, dtype=int)]
    new_values = new_values[~np.isnan(new_values)]

    value = np.mean(new_values)

    return value

