#!/usr/bin/env python
# coding: utf-8

import datetime
import argparse
import glob
import re
import yaml
import copy
import pandas as pd

import numpy as np
import scipy
from scipy.sparse.csgraph import connected_components

import traitlets

import ctapipe

from ctapipe_io_magic import MAGICEventSource

from ctapipe.io import HDF5TableWriter
from ctapipe.core.container import Container, Field
from ctapipe.reco import HillasReconstructor
from ctapipe.image import hillas_parameters
from ctapipe.image.timing import timing_parameters
from ctapipe.instrument import CameraGeometry
from ctapipe.containers import LeakageContainer

from astropy import units as u
from astropy.coordinates import SkyCoord, AltAz

from magicctapipe.utils import MAGIC_Badpixels
# from utils import bad_pixel_treatment
from magicctapipe.utils import MAGIC_Cleaning
from magicctapipe.utils import calc_impact
from magicctapipe.utils.utils import info_message

def get_leakage(camera, event_image, clean_mask):
    """Calculate the leakage with pixels on the border of the image included #IS THIS TRUE?????

    Parameters
    ----------
    camera : CameraGeometry
        Description
    clean_mask : np.array
        Cleaning mask
    event_image : np.array
        Event image

    Returns
    -------
    LeakageContainer
    """

    neighbors = camera.neighbor_matrix_sparse

    # find pixels in the outermost ring
    outermostring = []
    for pix in range(camera.n_pixels):
        if neighbors[pix].getnnz() < 5:
            outermostring.append(pix)

    # find pixels in the second outermost ring
    outerring = []
    for pix in range(camera.n_pixels):
        if pix in outermostring:
            continue
        for neigh in np.where(neighbors[pix][0,:].toarray() == True)[1]:
            if neigh in outermostring:
                outerring.append(pix)

    # needed because outerring has some pixels appearing more than once
    outerring = np.unique(outerring).tolist()
    outermostring_mask = np.zeros(camera.n_pixels, dtype=bool)
    outermostring_mask[outermostring] = True
    outerring_mask = np.zeros(camera.n_pixels, dtype=bool)
    outerring_mask[outerring] = True
    # intersection between 1st outermost ring and cleaning mask
    mask1 = np.array(outermostring_mask) & clean_mask
    # intersection between 2nd outermost ring and cleaning mask
    mask2 = np.array(outerring_mask) & clean_mask

    leakage_pixel1 = np.count_nonzero(mask1)
    leakage_pixel2 = np.count_nonzero(mask2)

    leakage_intensity1 = np.sum(event_image[mask1])
    leakage_intensity2 = np.sum(event_image[mask2])

    size = np.sum(event_image[clean_mask])

    return LeakageContainer(
        pixels_width_1=leakage_pixel1 / camera.n_pixels,
        pixels_width_2=leakage_pixel2 / camera.n_pixels,
        intensity_width_1=leakage_intensity1 / size,
        intensity_width_2=leakage_intensity2 / size,
    )

def get_num_islands(camera, clean_mask, event_image):
    """Get the number of connected islands in a shower image.

    Parameters
    ----------
    camera : CameraGeometry
        Description
    clean_mask : np.array
        Cleaning mask
    event_image : np.array
        Event image

    Returns
    -------
    int
        Number of islands
    """

    neighbors = camera.neighbor_matrix_sparse
    clean_neighbors = neighbors[clean_mask][:, clean_mask]
    num_islands, labels = connected_components(clean_neighbors, directed=False)

    return num_islands

def scale_camera_geometry(camera_geom, factor):
    """Scale given camera geometry of a given (constant) factor
    
    Parameters
    ----------
    camera : CameraGeometry
        Camera geometry
    factor : float
        Scale factor
    
    Returns
    -------
    CameraGeometry
        Scaled camera geometry
    """
    pix_x_scaled = factor*camera_geom.pix_x
    pix_y_scaled = factor*camera_geom.pix_y
    pix_area_scaled = camera_geom.guess_pixel_area(pix_x_scaled, pix_y_scaled, camera_geom.pix_type)

    return CameraGeometry(
        camera_name='MAGICCam',
        pix_id=camera_geom.pix_id,
        pix_x=pix_x_scaled,
        pix_y=pix_y_scaled,
        pix_area=pix_area_scaled,
        pix_type=camera_geom.pix_type,
        pix_rotation=camera_geom.pix_rotation,
        cam_rotation=camera_geom.cam_rotation
    )

def reflected_camera_geometry(camera_geom):
    """Reflect camera geometry (x->-y, y->-x)

    Parameters
    ----------
    camera_geom : CameraGeometry
        Camera geometry

    Returns
    -------
    CameraGeometry
        Reflected camera geometry
    """

    return CameraGeometry(
        camera_name='MAGICCam',
        pix_id=camera_geom.pix_id,
        pix_x=-1.*camera_geom.pix_y,
        pix_y=-1.*camera_geom.pix_x,
        pix_area=camera_geom.guess_pixel_area(camera_geom.pix_x, camera_geom.pix_y, camera_geom.pix_type),
        pix_type=camera_geom.pix_type,
        pix_rotation=camera_geom.pix_rotation,
        cam_rotation=camera_geom.cam_rotation
    )

def process_dataset_mc(input_mask, output_name, cleaning_config):
    """Create event metadata container to hold event / observation / telescope
    IDs and MC true values for the event energy and direction. We will need it
    to add this information to the event Hillas parameters when dumping the
    results to disk.

    Parameters
    ----------
    input_mask : str
        Mask for MC input files. Reading of files is managed
        by the MAGICEventSource class.
    output_name : str
        Name of the HDF5 output file.
    cleaning_config: dict
        Dictionary for cleaning settings

    Returns
    -------
    None
    """

    class InfoContainer(Container):
        obs_id = Field(-1, "Observation ID")
        event_id = Field(-1, "Event ID")
        tel_id = Field(-1, "Telescope ID")
        true_energy = Field(-1, "MC event energy", unit=u.TeV)
        true_alt = Field(-1, "MC event altitude", unit=u.rad)
        true_az = Field(-1, "MC event azimuth", unit=u.rad)
        true_core_x = Field(-1, "MC event x-core position", unit=u.m)
        true_core_y = Field(-1, "MC event y-core position", unit=u.m)
        tel_alt = Field(-1, "MC telescope altitude", unit=u.rad)
        tel_az = Field(-1, "MC telescope azimuth", unit=u.rad)
        n_islands = Field(-1, "Number of image islands")

    class ObsIdContainer(Container):
        obs_id = Field(-1, "Observation ID")

    class ImpactContainer(Container):
        impact = Field(-1, "Impact")

    aberration_factor = 1./1.0713

    cleaning_config["findhotpixels"] = False

    # Now let's loop over the events and perform:
    #  - image cleaning;
    #  - hillas parameter calculation;
    #  - time gradient calculation.
    #  
    # We'll write the result to the HDF5 file that can be used for further processing.

    hillas_reconstructor = HillasReconstructor()

    horizon_frame = AltAz()

    events_not_passing_cleaning       = 0
    events_hillas_calculation_failed  = 0
    events_stereo_calculation_skipped = 0
    events_stereo_calculation_failed  = 0
    events_stereo_calculation_success = 0

    # Opening the output file
    with HDF5TableWriter(filename=output_name, group_name='dl1', overwrite=True) as writer:
        # Event source
        source = MAGICEventSource(input_url=input_mask)

        camera_old = source.subarray.tel[1].camera.geometry
        camera = reflected_camera_geometry(camera_old)
        camera_scaled = scale_camera_geometry(camera, aberration_factor)
        magic_clean = MAGIC_Cleaning.magic_clean(camera_scaled,cleaning_config)

        info_message("Cleaning configuration", prefix='Hillas')
        for item in vars(magic_clean).items():
            print(f"{item[0]}: {item[1]}")
        if magic_clean.findhotpixels:
            for item in vars(magic_clean.pixel_treatment).items():
                print(f"{item[0]}: {item[1]}")

        obs_id_last = -1

        obs_id_last = -1

        # Looping over the events
        for event in source:

            if event.index.obs_id != obs_id_last:
                obs_id_info = ObsIdContainer(obs_id=event.index.obs_id)
                writer.write("mc_header", (obs_id_info, event.mcheader))
                obs_id_last = event.index.obs_id

            tels_with_data = event.r1.tels_with_data

            event_info             = dict()
            leakage_params         = dict()
            timing_params          = dict()
            computed_hillas_params = dict()
            telescope_pointings    = dict()
            array_pointing = SkyCoord(
                alt=event.pointing.array_altitude,
                az=event.pointing.array_azimuth,
                frame=horizon_frame,
            )

            # Looping over the triggered telescopes
            for tel_id in tels_with_data:
                # Obtained image
                event_image = event.dl1.tel[tel_id].image
                # Pixel arrival time map
                event_pulse_time = event.dl1.tel[tel_id].peak_time

                clean_mask, event_image, event_pulse_time = magic_clean.clean_image(event_image, event_pulse_time)

                num_islands = get_num_islands(camera_scaled, clean_mask, event_image)

                event_image_cleaned = event_image.copy()
                event_image_cleaned[~clean_mask] = 0

                event_pulse_time_cleaned = event_pulse_time.copy()
                event_pulse_time_cleaned[~clean_mask] = 0

                if np.any(event_image_cleaned):
                    try:
                        # If event has survived the cleaning, computing the Hillas parameters
                        hillas_params = hillas_parameters(camera_scaled, event_image_cleaned)
                        image_mask = event_image_cleaned > 0
                        timing_params[tel_id] = timing_parameters(
                            camera_scaled,
                            event_image_cleaned,
                            event_pulse_time_cleaned,
                            hillas_params,
                            image_mask
                        )
                        leakage_params[tel_id] = get_leakage(camera_scaled, event_image, clean_mask)

                        computed_hillas_params[tel_id] = hillas_params

                        telescope_pointings[tel_id] = SkyCoord(
                            alt=event.pointing.tel[tel_id].altitude,
                            az=event.pointing.tel[tel_id].azimuth,
                            frame=horizon_frame,
                        )

                        # Preparing metadata
                        event_info[tel_id] = InfoContainer(
                            obs_id=event.index.obs_id,
                            event_id=scipy.int32(event.index.event_id),
                            tel_id=tel_id,
                            true_energy=event.mc.energy,
                            true_alt=event.mc.alt.to(u.rad),
                            true_az=event.mc.az.to(u.rad),
                            true_core_x=event.mc.core_x.to(u.m),
                            true_core_y=event.mc.core_y.to(u.m),
                            tel_alt=event.pointing.tel[tel_id].altitude.to(u.rad),
                            tel_az=event.pointing.tel[tel_id].azimuth.to(u.rad),
                            n_islands=num_islands
                        )

                    except ValueError:
                        print(f"Event ID {event.index.event_id} (obs ID: {event.index.obs_id}; "
                            f"telescope ID: {tel_id}): Hillas calculation failed.")
                        events_hillas_calculation_failed += 1
                        break
                else:
                    print(f"Event ID {event.index.event_id} (obs ID: {event.index.obs_id}; "
                        f"telescope ID: {tel_id}) did not pass cleaning.")
                    events_not_passing_cleaning += 1
                    break

            if len(computed_hillas_params.keys()) > 1:
                if any([computed_hillas_params[tel_id]["width"].value == 0 for tel_id in computed_hillas_params]):
                    print(f"Event ID {event.index.event_id} (obs ID: {event.index.obs_id}) "
                        f"has an ellipse with width=0: stereo parameters calculation skipped.")
                    events_stereo_calculation_skipped += 1
                    continue
                elif any([np.isnan(computed_hillas_params[tel_id]["width"].value) for tel_id in computed_hillas_params]):
                    print(f"Event ID {event.index.event_id} (obs ID: {event.index.obs_id}) "
                        f"has an ellipse with width=NaN: stereo parameters calculation skipped.")
                    events_stereo_calculation_skipped += 1
                    continue
                else:
                    # stereo params
                    stereo_params = hillas_reconstructor.predict(computed_hillas_params, source.subarray, array_pointing)
                    # Storing the result
                    for tel_id in list(event_info.keys()):
                        _impact = calc_impact.calc_impact(
                            stereo_params.core_x.value,
                            stereo_params.core_y.value,
                            stereo_params.az.to("rad").value,
                            stereo_params.alt.to("rad").value,
                            source.subarray.positions[tel_id][0].value,
                            source.subarray.positions[tel_id][1].value,
                            source.subarray.positions[tel_id][2].value
                        )
                        impact = ImpactContainer(impact=_impact)
                        writer.write("hillas_params", (event_info[tel_id], computed_hillas_params[tel_id], leakage_params[tel_id], timing_params[tel_id], impact))
                    event_info[list(event_info.keys())[0]].tel_id = -1
                    # Storing the result
                    writer.write("stereo_params", (event_info[list(event_info.keys())[0]], stereo_params))
                    events_stereo_calculation_success += 1

    print("Event processing statistics ...")
    print(f"\tEvents not passing cleaning: {events_not_passing_cleaning}")
    print(f"\tEvents with hillas calculation failed: {events_hillas_calculation_failed}")
    print(f"\tEvents with stereo calculation skipped: {events_stereo_calculation_skipped}")
    print(f"\tEvents with stereo calculation failed: {events_stereo_calculation_failed}")
    print(f"\tEvents with stereo calculation: {events_stereo_calculation_success}")


def process_dataset_data(input_mask, output_name, cleaning_config, bad_pixels_config):
    """Create event metadata container to hold event / observation / telescope
    IDs and MC true values for the event energy and direction. We will need it
    to add this information to the event Hillas parameters when dumping the
    results to disk.

    Parameters
    ----------
    input_mask : str
        Mask for real data input files. Reading of files is managed
        by the MAGICEventSource class.
    output_name : str
        Name of the HDF5 output file.
    cleaning_config: dict
        Dictionary for cleaning settings
    bad_pixels_config: dict
        Dictionary for bad pixels settings

    Returns
    -------
    None
    """

    class InfoContainer(Container):
        obs_id = Field(-1, "Observation ID")
        event_id = Field(-1, "Event ID")
        tel_id = Field(-1, "Telescope ID")
        mjd = Field(-1, "Event MJD")
        tel_alt = Field(-1, "MC telescope altitude", unit=u.rad)
        tel_az = Field(-1, "MC telescope azimuth", unit=u.rad)
        n_islands = Field(-1, "Number of image islands")

    class ImpactContainer(Container):
        impact = Field(-1, "Impact")

    aberration_factor = 1./1.0713

    # Now let's loop over the events and perform:
    #  - image cleaning;
    #  - hillas parameter calculation;
    #  - time gradient calculation.
    #  
    # We'll write the result to the HDF5 file that can be used for further processing.

    hillas_reconstructor = HillasReconstructor()

    horizon_frame = AltAz()

    previous_event_id = 0

    events_not_passing_cleaning       = 0
    events_hillas_calculation_failed  = 0
    events_stereo_calculation_skipped = 0
    events_stereo_calculation_failed  = 0
    events_stereo_calculation_success = 0

    # Opening the output file
    with HDF5TableWriter(filename=output_name, group_name='dl1', overwrite=True) as writer:
        # Creating an input source
        source = MAGICEventSource(input_url=input_mask) #max_events=1000

        camera_old = source.subarray.tel[1].camera.geometry
        camera = reflected_camera_geometry(camera_old)
        camera_scaled = scale_camera_geometry(camera, aberration_factor)
        magic_clean = MAGIC_Cleaning.magic_clean(camera_scaled,cleaning_config)
        badpixel_calculator = MAGIC_Badpixels.MAGICBadPixelsCalc(config=bad_pixels_config)

        info_message("Cleaning configuration", prefix='Hillas')
        for item in vars(magic_clean).items():
            print(f"{item[0]}: {item[1]}")
        if magic_clean.findhotpixels:
            for item in vars(magic_clean.pixel_treatment).items():
                print(f"{item[0]}: {item[1]}")

        info_message("Bad pixel configuration", prefix='Hillas')
        for item in vars(badpixel_calculator).items():
            print(f"{item[0]}: {item[1]}")

        # Looping over the events
        for event in source:
            #Exclude pedestal runs??
            #print(event.index.obs_id, event.index.event_id, event.meta['number_subrun'])
            if previous_event_id == event.index.event_id:
                continue
            previous_event_id = copy.copy(event.index.event_id)

            tels_with_data = event.r1.tels_with_data

            event_info             = dict()
            leakage_params         = dict()
            timing_params          = dict()
            computed_hillas_params = dict()
            telescope_pointings    = dict()
            array_pointing = SkyCoord(
                alt=event.pointing.array_altitude,
                az=event.pointing.array_azimuth,
                frame=horizon_frame,
            )

            # Looping over the triggered telescopes
            for tel_id in tels_with_data:
                # Obtained image
                event_image = event.dl1.tel[tel_id].image
                # Pixel arrival time map
                event_pulse_time = event.dl1.tel[tel_id].peak_time

                badrmspixel_mask = badpixel_calculator.get_badrmspixel_mask(event)
                deadpixel_mask = badpixel_calculator.get_deadpixel_mask(event)
                unsuitable_mask = np.logical_or(badrmspixel_mask[tel_id-1], deadpixel_mask[tel_id-1])

                clean_mask, event_image, event_pulse_time = magic_clean.clean_image(event_image, event_pulse_time,unsuitable_mask=unsuitable_mask)

                num_islands = get_num_islands(camera_scaled, clean_mask, event_image)

                event_image_cleaned = event_image.copy()
                event_image_cleaned[~clean_mask] = 0

                event_pulse_time_cleaned = event_pulse_time.copy()
                event_pulse_time_cleaned[~clean_mask] = 0

                if np.any(event_image_cleaned):
                    try:
                        # If event has survived the cleaning, computing the Hillas parameters
                        hillas_params = hillas_parameters(camera_scaled, event_image_cleaned)
                        image_mask = event_image_cleaned > 0
                        timing_params[tel_id] = timing_parameters(
                            camera_scaled,
                            event_image_cleaned,
                            event_pulse_time_cleaned,
                            hillas_params,
                            image_mask
                        )
                        leakage_params[tel_id] = get_leakage(camera_scaled, event_image, clean_mask)

                        computed_hillas_params[tel_id] = hillas_params

                        telescope_pointings[tel_id] = SkyCoord(
                            alt=event.pointing.tel[tel_id].altitude,
                            az=event.pointing.tel[tel_id].azimuth,
                            frame=horizon_frame,
                        )

                        # Preparing metadata
                        event_info[tel_id] = InfoContainer(
                            obs_id=event.index.obs_id,
                            event_id=scipy.int32(event.index.event_id),
                            tel_id=tel_id,
                            mjd=event.trigger.time.mjd,
                            tel_alt=event.pointing.tel[tel_id].altitude.to(u.rad),
                            tel_az=event.pointing.tel[tel_id].azimuth.to(u.rad),
                            n_islands=num_islands
                        )

                    except ValueError:
                        print(f"Event ID {event.index.event_id} (obs ID: {event.index.obs_id}; "
                            f"telescope ID: {tel_id}): Hillas calculation failed.")
                        events_hillas_calculation_failed += 1
                        break
                else:
                    print(f"Event ID {event.index.event_id} (obs ID: {event.index.obs_id}; "
                        f"telescope ID: {tel_id}) did not pass cleaning.")
                    events_not_passing_cleaning += 1
                    break

            if len(computed_hillas_params.keys()) > 1:
                if any([computed_hillas_params[tel_id]["width"].value == 0 for tel_id in computed_hillas_params]):
                    print(f"Event ID {event.index.event_id} (obs ID: {event.index.obs_id}) "
                        f"has an ellipse with width=0: stereo parameters calculation skipped.")
                    events_stereo_calculation_skipped += 1
                    continue
                elif any([np.isnan(computed_hillas_params[tel_id]["width"].value) for tel_id in computed_hillas_params]):
                    print(f"Event ID {event.index.event_id} (obs ID: {event.index.obs_id}) "
                        f"has an ellipse with width=NaN: stereo parameters calculation skipped.")
                    events_stereo_calculation_skipped += 1
                    continue
                else:
                    # stereo params
                    stereo_params = hillas_reconstructor.predict(computed_hillas_params, source.subarray, array_pointing)
                    # Storing the result
                    for tel_id in list(event_info.keys()):
                        _impact = calc_impact.calc_impact(
                            stereo_params.core_x.value,
                            stereo_params.core_y.value,
                            stereo_params.az.to("rad").value,
                            stereo_params.alt.to("rad").value,
                            source.subarray.positions[tel_id][0].value,
                            source.subarray.positions[tel_id][1].value,
                            source.subarray.positions[tel_id][2].value
                        )
                        impact = ImpactContainer(impact=_impact)
                        writer.write("hillas_params", (event_info[tel_id], computed_hillas_params[tel_id], leakage_params[tel_id], timing_params[tel_id], impact))
                    event_info[list(event_info.keys())[0]].tel_id = -1
                    # Storing the result
                    writer.write("stereo_params", (event_info[list(event_info.keys())[0]], stereo_params))
                    events_stereo_calculation_success += 1

    print("Event processing statistics ...")
    print(f"\tEvents not passing cleaning: {events_not_passing_cleaning}")
    print(f"\tEvents with hillas calculation failed: {events_hillas_calculation_failed}")
    print(f"\tEvents with stereo calculation skipped: {events_stereo_calculation_skipped}")
    print(f"\tEvents with stereo calculation failed: {events_stereo_calculation_failed}")
    print(f"\tEvents with stereo calculation: {events_stereo_calculation_success}")


# =================
# === Main code ===
# =================

# --------------------------
# Adding the argument parser
arg_parser = argparse.ArgumentParser(description="""
This tools computes the Hillas parameters for the specified data sets.
""")

arg_parser.add_argument("--config", default="config.yaml",
                        help='Configuration file to steer the code execution.')
arg_parser.add_argument("--usereal",
                        help='Process only real data files.',
                        action='store_true')
arg_parser.add_argument("--usemc",
                        help='Process only simulated data files.',
                        action='store_true')
arg_parser.add_argument("--usetest",
                        help='Process only test files.',
                        action='store_true')
arg_parser.add_argument("--usetrain",
                        help='Process only train files.',
                        action='store_true')

parsed_args = arg_parser.parse_args()
# --------------------------

# ------------------------------
# Reading the configuration file

file_not_found_message = """
Error: can not load the configuration file {:s}.
Please check that the file exists and is of YAML or JSON format.
Exiting.
"""

try:
    config = yaml.safe_load(open(parsed_args.config, "r"))
except IOError:
    print(file_not_found_message.format(parsed_args.config))
    exit()

if 'data_files' not in config:
    print('Error: the configuration file is missing the "data_files" section. Exiting.')
    exit()

if 'image_cleaning' not in config:
    print('Error: the configuration file is missing the "image_cleaning" section. Exiting.')
    exit()
# ------------------------------

if parsed_args.usereal and parsed_args.usemc:
    data_type_to_process = config['data_files']
elif parsed_args.usereal:
    data_type_to_process = ['data']
elif parsed_args.usemc:
    data_type_to_process = ['mc']
else:
    data_type_to_process = config['data_files']

if parsed_args.usetrain and parsed_args.usetest:
    data_sample_to_process = ['train_sample', 'test_sample']
elif parsed_args.usetrain:
    data_sample_to_process = ['train_sample']
elif parsed_args.usetest:
    data_sample_to_process = ['test_sample']
else:
    data_sample_to_process = ['train_sample', 'test_sample']

telescopes_to_process = list(config['image_cleaning'].keys())

for data_type in data_type_to_process:
    for sample in data_sample_to_process:
        for telescope_type in telescopes_to_process:
            if telescope_type not in config['data_files'][data_type][sample]:
                raise ValueError(f'Telescope type "{telescope_type}" is not in the configuration file')

            if telescope_type not in config['image_cleaning']:
                raise ValueError(f'Telescope type "{telescope_type}" does not have image cleaning settings')

            info_message(f'Data "{data_type}", sample "{sample}", telescope "{telescope_type}"',
                prefix='Hillas')

            is_mc = data_type.lower() == "mc"

            cleaning_config = config['image_cleaning'][telescope_type]
            bad_pixels_config = config['bad_pixels'][telescope_type]

            if is_mc:
                process_dataset_mc(input_mask=config['data_files'][data_type][sample][telescope_type]['input_mask'],
                    output_name=config['data_files'][data_type][sample][telescope_type]['hillas_output'], cleaning_config=cleaning_config)
            else:
                process_dataset_data(input_mask=config['data_files'][data_type][sample][telescope_type]['input_mask'],
                    output_name=config['data_files'][data_type][sample][telescope_type]['hillas_output'], cleaning_config=cleaning_config, bad_pixels_config=bad_pixels_config)
