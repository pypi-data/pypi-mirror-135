# This file is derived from cta-lstchain v0.8.4 (lstchain/image/modifier.py)

import logging

import numpy as np
from ctapipe.calib.camera import CameraCalibrator
from ctapipe.io import EventSource, read_table
from numba import njit
from scipy.interpolate import interp1d
from traitlets.config import Config


__all__ = [
    'add_noise_in_pixels',
    'set_numba_seed',
    'random_psf_smearer'
]

log = logging.getLogger(__name__)


# number of neighbors of completely surrounded pixels of hexagonal cameras:
N_PIXEL_NEIGHBORS = 6
SMEAR_PROBABILITIES = np.full(N_PIXEL_NEIGHBORS, 1 / N_PIXEL_NEIGHBORS)


def add_noise_in_pixels(rng, image, extra_noise_in_dim_pixels,
                        extra_bias_in_dim_pixels, transition_charge,
                        extra_noise_in_bright_pixels):
    """
    Addition of Poissonian noise to the pixels

    Parameters
    ----------
    rng : `numpy.random.default_rng`
        Random number generator
    image: `np.ndarray`
        Charges (p.e.) in the camera
    extra_noise_in_dim_pixels: `float`
        Mean additional number of p.e. to be added (Poisson noise) to
        pixels with charge below transition_charge. To be tuned by
        comparing the starting MC and data
    extra_bias_in_dim_pixels: `float`
        Mean bias (w.r.t. original charge) of the new charge in pixels.
        Should be 0 for non-peak-search pulse integrators. To be tuned by
        comparing the starting MC and data
    transition_charge: `float`
        Border between "dim" and "bright" pixels. To be tuned by
        comparing the starting MC and data
    extra_noise_in_bright_pixels: `float`
        Mean additional number of p.e. to be added (Poisson noise) to
        pixels with charge above transition_charge. This is unbiased,
        i.e. Poisson noise is introduced, and its average subtracted,
        so that the mean charge in bright pixels remains unaltered.
        This is because we assume that above transition_charge the
        integration window is determined by the Cherenkov light, and
        would not be modified by the additional NSB noise (presumably
        small compared to the C-light). To be tuned by
        comparing the starting MC and data

    Returns
    -------
    image: `np.ndarray`
        Modified (noisier) image

    """

    bright_pixels = image > transition_charge
    noise = np.where(bright_pixels, extra_noise_in_bright_pixels,
                     extra_noise_in_dim_pixels)
    bias = np.where(bright_pixels, -extra_noise_in_bright_pixels,
                    extra_bias_in_dim_pixels - extra_noise_in_dim_pixels)

    image = image + rng.poisson(noise) + bias

    return image


@njit(cache=True)
def set_numba_seed(seed):
    np.random.seed(seed)


@njit(cache=True)
def random_psf_smearer(image, fraction, indices, indptr):
    """
    Random PSF smearer

    Parameters
    ----------
    image: `np.ndarray`
        Charges (p.e.) in the camera
    indices : `camera_geometry.neighbor_matrix_sparse.indices`
        Pixel indices.
    indptr : camera_geometry.neighbor_matrix_sparse.indptr
    fraction: `float`
        Fraction of the light in a pixel that will be distributed among its
        immediate surroundings, i.e. immediate neighboring pixels, according
        to Poisson statistics. Some light is lost for pixels  which are at
        the camera edge and hence don't have all possible neighbors

    Returns
    -------
    new_image: `np.ndarray`
        Modified (smeared) image

    """

    new_image = image.copy()
    for pixel in range(len(image)):

        if image[pixel] <= 0:
            continue

        to_smear = np.random.poisson(image[pixel] * fraction)

        if to_smear == 0:
            continue

        # remove light from current pixel
        new_image[pixel] -= to_smear

        # add light to neighbor pixels
        neighbors = indices[indptr[pixel]: indptr[pixel + 1]]
        n_neighbors = len(neighbors)

        # all neighbors are equally likely to receive the charge
        # we always distribute the charge into 6 neighbors, so that charge
        # on the edges of the camera is lost
        neighbor_charges = np.random.multinomial(to_smear, SMEAR_PROBABILITIES)

        for n in range(n_neighbors):
            neighbor = neighbors[n]
            new_image[neighbor] += neighbor_charges[n]

    return new_image
