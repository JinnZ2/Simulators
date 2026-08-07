"""Geometry domain helpers: packing and TSP-style distance matrices."""

from __future__ import annotations

import math

import numpy as np


def packing_density(sphere_r: float, box_dims: list[float] | tuple[float, ...]) -> float:
    """Volume packing density of identical spheres in a box.

    Computes how many spheres of radius ``sphere_r`` fit along each box
    dimension (grid packing) and returns the fraction of the box volume
    occupied by the spheres.

    Args:
        sphere_r: Sphere radius.
        box_dims: Box side lengths (2D or 3D).

    Returns:
        Packing density in ``[0, 1]`` (may be 0 if no sphere fits).
    """
    dims = [float(d) for d in box_dims]
    d = 2.0 * sphere_r
    counts = [int(dim // d) for dim in dims]
    n = math.prod(counts)
    k = len(dims)
    if k == 3:
        sphere_vol = (4.0 / 3.0) * math.pi * sphere_r ** 3
    elif k == 2:
        sphere_vol = math.pi * sphere_r ** 2
    else:
        raise ValueError("box_dims must have 2 or 3 dimensions")
    box_vol = math.prod(dims)
    return float(n * sphere_vol / box_vol)


def tsp_distance_matrix(points: np.ndarray | list[list[float]]) -> np.ndarray:
    """Euclidean distance matrix for a set of points.

    Args:
        points: Array-like of shape ``(n, dim)``.

    Returns:
        Symmetric ``(n, n)`` numpy array of pairwise Euclidean distances.
    """
    pts = np.asarray(points, dtype=float)
    diff = pts[:, None, :] - pts[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))
