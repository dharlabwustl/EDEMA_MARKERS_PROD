#!/usr/bin/env python
# coding: utf-8

"""
This code will take inputs:
NIFTI:
1. template CT
2. individual session CT: warped to template CT, its infarct mask warped to template CT
3. MRI masks for different regions: warped to the template CT
4. A pre-defined color map of the different MRI mask as CSV.
Method: Taking the warped masks
1. We find the voxels of the infarct mask overlapping with the MRI masks.
2. Display the those overlapping voxels with the corresponding colors of the regions on the grayscale image of the template image.
Outputs from this code will be:
1. A PDF with the Gray scale session image, grayscale template image, grayscale template with the regions mask of the MRI, grayscale template image with the infarct in different MRI regions with the corresponding colors.
2. A CSV file with the distribution of the infarct volume for each region of the MRI for individual session CT


"""
import nibabel as nib
import numpy as np
import pandas as pd
import cv2,argparse
import os,glob,time,inspect
import random,subprocess,inspect
from skimage import exposure 
random.seed(42)
np.random.seed(42)
import nibabel as nib
import numpy as np
from natsort import natsorted


color_map_filename='/software/legend.csv'
import nibabel as nib
import numpy as np
import cv2

# Load the NIfTI image
def get_min_max_intensity(nifti_image_file):
    nifti_image = nib.load(nifti_image_file,) #'brain_image.nii')
    image_data = nifti_image.get_fdata()

    # Isolate the brain area based on intensity values
    # This assumes a general threshold; adjust based on the image's characteristics
    brain_area = image_data[image_data > 0]  # assuming non-zero intensity represents the brain

    # Calculate the intensity range within the brain area
    min_intensity = np.percentile(brain_area, 5)  # lower threshold (5th percentile)
    max_intensity = np.percentile(brain_area, 95) # upper threshold (95th percentile)
    return min_intensity,max_intensity

    # # Clip the image data based on intensity range to enhance contrast
    # clipped_data = np.clip(image_data, min_intensity, max_intensity)
    #
    # # Normalize the clipped data to fit in the range 0-255 (8-bit grayscale)
    # normalized_data = 255 * (clipped_data - min_intensity) / (max_intensity - min_intensity)
    # normalized_data = normalized_data.astype(np.uint8)
    #
    # # Apply CLAHE for further local contrast enhancement
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # enhanced_data = clahe.apply(normalized_data)
    #
    # # Reshape back if needed (if applying on a 3D volume, apply CLAHE slice by slice)
    # # Save or display enhanced image
    # enhanced_nifti = nib.Nifti1Image(enhanced_data, affine=nifti_image.affine)
    # nib.save(enhanced_nifti, enhanced_nifti_image_file) ##'enhanced_brain_image.nii')

def multi_value_mask_as_heatmap(grayscale_img_file,mask_data_file,output_dir=''):
    """
    Generate heatmaps from multi-value masks overlaid on a grayscale image and save each slice as an image file.

    This function takes a grayscale medical image file (e.g., a brain MRI), applies a multi-value mask (e.g., segmented regions)
    to highlight specific regions of interest, and saves each slice of the resulting heatmap as a separate image. The
    function performs intensity stretching on the grayscale image and applies a color map to the mask data.

    Parameters:
    -----------
    grayscale_img_file : str
        Path to the input grayscale NIfTI image file.
        
    mask_data_file : str
        Path to the NIfTI file containing the mask data, where non-zero values represent regions of interest.
        
    output_dir : str, optional
        Directory path to save the output heatmap images. Each slice is saved as a separate PNG file with the prefix `slice_`.

    Returns:
    --------
    int
        Returns 0 upon successful completion.

    Process:
    --------
    1. Loads the grayscale and mask data from the specified NIfTI files.
    2. Creates a background mask to exclude background areas.
    3. Applies intensity stretching to enhance grayscale image visibility.
    4. For each slice, overlays the mask data as a heatmap using a color map (e.g., JET), setting background areas to black.
    5. Saves each generated heatmap image in the output directory.

    Example:
    --------
    multi_value_mask_as_heatmap('brain_image.nii', 'brain_mask.nii', 'output/')

    Notes:
    ------
    - The `grayscale_img_brain_bg` mask is used to set background areas to black in the color-mapped heatmap.
    - The mask data values are normalized and stretched to enhance visualization.
    - Ensure `output_dir` exists before calling this function to avoid errors while saving images.

    Dependencies:
    -------------
    - nibabel (for loading NIfTI files)
    - OpenCV (for applying color maps and saving images)
    - NumPy (for array manipulation)
    """

    grayscale_img=nib.load(grayscale_img_file).get_fdata()
    grayscale_img_brain_bg=grayscale_img==0
    mask_data=nib.load(mask_data_file).get_fdata()
    mask_data=mask_data.astype(np.uint8)
    grayscale_img[mask_data>0]=np.min(grayscale_img)
    grayscale_img = stretch_intensity(grayscale_img, 2300, 2700) * 255
    grayscale_img = grayscale_img.astype(np.uint8)
    grayscale_image_array = np.stack([np.dstack([grayscale_img[:, :, i]] * 3) for i in range(grayscale_img.shape[2])])
    min_non_zero_value = np.min(mask_data[mask_data > 0])
    background_mask_data = mask_data == 0
    #mask_data[mask_data<min_non_zero_value]=min_non_zero_value
    mask_data=normalize_nifti_image(mask_data)*255
    mask_data=mask_data.astype(np.uint8)
    for i in range(mask_data.shape[2]):
        mask=mask_data[:,:,i]
        
        # Create a binary mask where the background (black) is 0
        #background_mask = mask == 0

        #mask[mask<min_non_zero_value]=min_non_zero_value
        #print(f"min mask{np.min(mask)}")

        # Apply a colormap to the grayscale mask (choose one like COLORMAP_JET)
        heatmap = cv2.applyColorMap(mask, cv2.COLORMAP_JET)

        # Set background areas to black in the color map
        heatmap[grayscale_img_brain_bg[:,:,i]] = [0, 0, 0]
        #grayscale_image_array[i]=grayscale_image_array[i]+heatmap
        output_path = os.path.join(output_dir, f'slice_{i:03d}.png')
        cv2.imwrite(output_path, heatmap)   

    return 0
def multi_value_mask_as_heatmap_with_nonzero_asmin(grayscale_img_file,mask_data_file,output_dir=''):
    """
    Generate and save heatmaps from multi-value masks, overlaying them on a grayscale image and ensuring minimum
    non-zero values in the mask are visualized with color.

    This function processes a grayscale medical image (e.g., brain MRI) with a mask file that highlights specific regions.
    It normalizes the grayscale and mask images, adjusts the mask so that all values below the minimum non-zero value
    are set to the minimum non-zero value, and overlays the mask as a heatmap. The resulting images are saved slice-by-slice.

    Parameters:
    -----------
    grayscale_img_file : str
        Path to the input grayscale NIfTI image file.

    mask_data_file : str
        Path to the NIfTI file containing the mask data, where non-zero values represent regions of interest.

    output_dir : str, optional
        Directory path to save the output heatmap images. Each slice is saved as a separate PNG file with the prefix `slice_`.

    Returns:
    --------
    int
        Returns 0 upon successful completion.

    Process:
    --------
    1. Loads the grayscale image and mask data from specified NIfTI files.
    2. Sets regions in the grayscale image corresponding to non-zero mask values to the minimum grayscale intensity.
    3. Stretches the grayscale intensity range to enhance contrast and converts to an 8-bit format.
    4. Adjusts mask data to ensure all values below the minimum non-zero value are set to this minimum.
    5. Applies a color map to the mask for each slice and overlays it onto the grayscale image.
    6. Saves each slice with the overlaid heatmap in the specified output directory.

    Example:
    --------
    multi_value_mask_as_heatmap_with_nonzero_asmin('brain_image.nii', 'brain_mask.nii', 'output/')

    Notes:
    ------
    - The `background_mask_data` array is used to identify and mask out background areas in the heatmap.
    - The mask intensity is normalized to span the 0–255 range for better color mapping.
    - Make sure the `output_dir` exists to prevent errors during the save operation.

    Dependencies:
    -------------
    - nibabel (for loading NIfTI files)
    - OpenCV (for applying color maps and saving images)
    - NumPy (for array manipulation)
    """
    
    grayscale_img=nib.load(grayscale_img_file).get_fdata()
    mask_data=nib.load(mask_data_file).get_fdata()
    mask_data=mask_data.astype(np.uint8)
    grayscale_img[mask_data>0]=np.min(grayscale_img)
    grayscale_img = stretch_intensity(grayscale_img, 2300, 2700) * 255
    grayscale_img = grayscale_img.astype(np.uint8)
    grayscale_image_array = np.stack([np.dstack([grayscale_img[:, :, i]] * 3) for i in range(grayscale_img.shape[2])])
    min_non_zero_value = np.min(mask_data[mask_data > 0])
    background_mask_data = mask_data == 0
    mask_data[mask_data<min_non_zero_value]=min_non_zero_value
    mask_data=normalize_nifti_image(mask_data)*255
    mask_data=mask_data.astype(np.uint8)
    for i in range(mask_data.shape[2]):
        mask=mask_data[:,:,i]
        
        # Create a binary mask where the background (black) is 0
        #background_mask = mask == 0

        #mask[mask<min_non_zero_value]=min_non_zero_value
        #print(f"min mask{np.min(mask)}")

        # Apply a colormap to the grayscale mask (choose one like COLORMAP_JET)
        heatmap = cv2.applyColorMap(mask, cv2.COLORMAP_JET)

        # Set background areas to black in the color map
        heatmap[background_mask_data[:,:,i]] = [0, 0, 0]
        grayscale_image_array[i]=grayscale_image_array[i]+heatmap
        output_path = os.path.join(output_dir, f'slice_{i:03d}.png')
        cv2.imwrite(output_path, grayscale_image_array[i])   

    return 0

def normalize_nifti_image(img_data) : #, output_path=None, scale_to_255=False):
    """
    Normalize a 3D NIfTI image array to the range 0–1.

    This function takes a 3D NIfTI image array and scales its values so that the minimum
    value becomes 0 and the maximum value becomes 1. This normalization is useful for
    preparing the image data for visualization or further processing.

    Parameters:
    -----------
    img_data : numpy.ndarray
        A 3D array representing the image data to be normalized.

    Returns:
    --------
    numpy.ndarray
        The normalized image data, with values scaled to the range [0, 1].

    Example:
    --------
    normalized_image = normalize_nifti_image(img_data)

    Notes:
    ------
    - Ensure `img_data` is a 3D array for accurate normalization.
    - If the minimum and maximum values are the same (e.g., in uniform data), this function
      will raise a division by zero error.

    Dependencies:
    -------------
    - NumPy (for array manipulation)
    """

    min_val = np.min(img_data)
    max_val = np.max(img_data)

    # Normalize the image data to range 0–1
    normalized_data = (img_data - min_val) / (max_val - min_val)
    
    return normalized_data

# Usage example
# normalized_image = normalize_nifti_image('path_to_your_image.nii', output_path='normalized_image.nii', scale_to_255=True)

def stretch_intensity(grayscale_img_data,min_intensity,max_intensity):
    """
    Stretch the intensity of a grayscale image to a specified range.

    This function rescales the intensity values of a grayscale image to fit within a specified
    minimum and maximum intensity range, enhancing contrast within the desired limits.

    Parameters:
    -----------
    grayscale_img_data : numpy.ndarray
        A 2D or 3D array representing the grayscale image data.

    min_intensity : int or float
        The minimum intensity value for rescaling. Values in the image below this threshold
        will be mapped to the minimum of the output range.

    max_intensity : int or float
        The maximum intensity value for rescaling. Values in the image above this threshold
        will be mapped to the maximum of the output range.

    Returns:
    --------
    numpy.ndarray
        The intensity-stretched grayscale image with values rescaled to fit the specified range.

    Example:
    --------
    stretched_img = stretch_intensity(grayscale_img_data, 2300, 2700)

    Notes:
    ------
    - This function uses `skimage.exposure.rescale_intensity` for intensity rescaling.
    - Ensure `min_intensity` and `max_intensity` cover the desired intensity range of interest.

    Dependencies:
    -------------
    - scikit-image (for exposure module)
    """

    grayscale_img=exposure.rescale_intensity( grayscale_img_data , in_range=(min_intensity, max_intensity))
    return grayscale_img
## 


# def superimpose_regions_on_ct():
import numpy as np
import cv2

def write_numbers_with_no_overlap(image, centroids, numbers, color=(255, 255, 255)):
    """
    Write numbers at the centroids, adjusting the position to avoid overlap.

    Parameters:
    - image: The image on which to write the numbers (in RGB format).
    - centroids: List of centroid coordinates [(y1, x1), (y2, x2), ...] (as (y, x) for NumPy convention).
    - numbers: List of numbers corresponding to the centroids.
    - color: Color of the text (default is white).
    """
    # Validate inputs
    if len(centroids) != len(numbers):
        raise ValueError("Centroids and numbers must have the same length.")

    # Create a copy of the image to avoid mutating the original
    output_image = image.copy()

    # Track text positions to avoid overlap
    text_positions = []

    for i, (centroid, number) in enumerate(zip(centroids, numbers)):
        # Convert (y, x) to (x, y) for OpenCV
        text_position = (centroid[1], centroid[0])

        # Adjust position to avoid overlap
        for previous_position in text_positions:
            if np.linalg.norm(np.array(text_position) - np.array(previous_position)) < 30:  # Adjust threshold as needed
                text_position = (text_position[0], text_position[1] + 30)

        # Add the current text position to the list
        text_positions.append(text_position)

        # Write the number on the image
        output_image = cv2.putText(
            output_image,
            str(number),
            text_position,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1,
            cv2.LINE_AA
        )

    return output_image

# def write_numbers_with_no_overlap(image, centroids, numbers, color=(255, 255, 255)):
   
#     """
#     Write numbers at the centroids, adjusting the position to avoid overlap.

#     Parameters:
#     - image: The image on which to write the numbers (in RGB format).
#     - centroids: List of centroid coordinates [(y1, x1), (y2, x2), ...] (as (y, x) for NumPy convention).
#     - numbers: List of numbers corresponding to the centroids.
#     - color: Color of the text (default is white).
#     """
#     text_positions = []  # To keep track of text positions and avoid overlap

#     for i, (centroid, number) in enumerate(zip(centroids, numbers)):
#         text_position = (centroid[1], centroid[0])  # OpenCV expects (x, y), so reverse (y, x) from centroid

#         # Check for overlapping with previous text positions
#         for previous_position in text_positions:
#             # If too close, adjust the current text position
#             if np.linalg.norm(np.array(text_position) - np.array(previous_position)) < 30:  # Threshold to detect proximity
#                 text_position = (text_position[0], text_position[1] + 30)  # Shift text downward by 30 pixels

#         # Add the current text position to the list to track it
#         text_positions.append(text_position)
#         # print(image.shape)
#         # Write the number at the adjusted position
#         # print(image)
#         return
#         image=cv2.putText(image.astype(np.uint8), str(number), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

#     return image.get()   
#     return 0
def call_superimpose_regions_overlapping_infarct_on_ct(args):
    grayscale_img_path=args.stuff[1]
    min_intensity=args.stuff[2]
    max_intensity=args.stuff[3] 
    infarct_mask_filename=args.stuff[4]
    output_dir=args.stuff[5]
    predefined_legend=args.stuff[6]
    mask_img_paths=args.stuff[7:]
    try:
        superimpose_regions_overlapping_infarct_on_ct(grayscale_img_path, min_intensity,max_intensity,mask_img_paths,infarct_mask_filename,output_dir,predefined_legend)
    except:
        print('I FAILED at :{}'.format(inspect.stack()[0][3]))

import os
import pandas as pd
import nibabel as nib
import numpy as np
import cv2
def superimpose_regions_overlapping_infarct_on_ct_for_average_infarct(grayscale_img_path, mask_img_paths, infarct_mask_filename, output_dir, predefined_legend,image_prefix,splitter='_fixed',thresh=[500,700]):
    # Load predefined legend as a dictionary for faster lookups
    predefined_legend_df = pd.read_csv(predefined_legend).set_index('masknumber')['color'].apply(eval).to_dict()

    # Load grayscale image and normalize intensity
    grayscale_img = nib.load(grayscale_img_path).get_fdata()
    # grayscale_img =(stretch_intensity (grayscale_img,thresh[0],thresh[1])*255).astype(np.uint8) #
    # grayscale_img =((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)
    min_int,max_int=extract_central_slice_intensity_range(grayscale_img, output_size=100)
    # grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)
    grayscale_img=stretch_intensity(grayscale_img,min_int,max_int)*255

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize a 3D RGB image array for each slice
    grayscale_image_array = np.stack([np.dstack([grayscale_img[:, :, i]] * 3) for i in range(grayscale_img.shape[2])])

    # Load infarct mask and binarize it
    infarct_mask_data = nib.load(infarct_mask_filename).get_fdata()
    # infarct_mask_data = (infarct_mask_data > 0.5).astype(np.uint8)

    mask_number_list = []
    color_list = []
    centroid_mask_number = []

    # Process each mask
    for mask_img_path in sorted(mask_img_paths, key=lambda x: int(os.path.basename(x).split(splitter)[0].split('_')[-1])):
        mask_number = int(os.path.basename(mask_img_path).split(splitter)[0].split('_')[-1])

        if mask_number not in predefined_legend_df:
            continue

        mask_color = tuple(predefined_legend_df[mask_number])
        mask_number_list.append(mask_number)
        color_list.append(mask_color)

        # Load the mask image
        mask_img = nib.load(mask_img_path).get_fdata()

        for i in range(grayscale_img.shape[2]):
            mask_slice = mask_img[:, :, i]

            # Mask only overlapping regions with the infarct mask
            mask_slice[infarct_mask_data[:, :, i] < 1] = 0
            grayscale_image_array[i][mask_slice > 0] = mask_color

            # Calculate centroid for each non-zero mask region
            if np.any(mask_slice > 0):
                coords = np.column_stack(np.where(mask_slice > 0))
                centroid = np.mean(coords, axis=0).astype(int)
                centroid_mask_number.append((i, centroid, mask_number, mask_color))

    # Save modified slices as PNG
    for i in range(grayscale_img.shape[2]):
        for _, centroid, mask_num, color in filter(lambda x: x[0] == i, centroid_mask_number):
            grayscale_image_array[i] = write_numbers_with_no_overlap(
                grayscale_image_array[i], [centroid], [mask_num], grayscale_img.shape[1]
            )

        output_path = os.path.join(output_dir, f'{image_prefix}_{i:03d}.png')
        cv2.imwrite(output_path, grayscale_image_array[i])

    print(f"Images saved in {output_dir} directory")
    return mask_number_list, color_list

def superimpose_regions_overlapping_infarct_on_ct(grayscale_img_path, mask_img_paths, infarct_mask_filename, output_dir, predefined_legend,image_prefix,splitter='_fixed',thresh=[500,700]):
    # Load predefined legend as a dictionary for faster lookups
    predefined_legend_df = pd.read_csv(predefined_legend).set_index('masknumber')['color'].apply(eval).to_dict()

    # Load grayscale image and normalize intensity
    grayscale_img = nib.load(grayscale_img_path).get_fdata()
    # grayscale_img =(stretch_intensity (grayscale_img,thresh[0],thresh[1])*255).astype(np.uint8) #
    # grayscale_img =((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)
    min_int,max_int=extract_central_slice_intensity_range(grayscale_img, output_size=100)
    # grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)
    grayscale_img=stretch_intensity(grayscale_img,min_int,max_int)*255

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize a 3D RGB image array for each slice
    grayscale_image_array = np.stack([np.dstack([grayscale_img[:, :, i]] * 3) for i in range(grayscale_img.shape[2])])

    # Load infarct mask and binarize it
    infarct_mask_data = nib.load(infarct_mask_filename).get_fdata()
    infarct_mask_data = (infarct_mask_data > 0.5).astype(np.uint8)

    mask_number_list = []
    color_list = []
    centroid_mask_number = []

    # Process each mask
    for mask_img_path in sorted(mask_img_paths, key=lambda x: int(os.path.basename(x).split(splitter)[0].split('_')[-1])):
        mask_number = int(os.path.basename(mask_img_path).split(splitter)[0].split('_')[-1])

        if mask_number not in predefined_legend_df:
            continue

        mask_color = tuple(predefined_legend_df[mask_number])
        mask_number_list.append(mask_number)
        color_list.append(mask_color)

        # Load the mask image
        mask_img = nib.load(mask_img_path).get_fdata()

        for i in range(grayscale_img.shape[2]):
            mask_slice = mask_img[:, :, i]

            # Mask only overlapping regions with the infarct mask
            mask_slice[infarct_mask_data[:, :, i] < 1] = 0
            grayscale_image_array[i][mask_slice > 0] = mask_color

            # Calculate centroid for each non-zero mask region
            if np.any(mask_slice > 0):
                coords = np.column_stack(np.where(mask_slice > 0))
                centroid = np.mean(coords, axis=0).astype(int)
                centroid_mask_number.append((i, centroid, mask_number, mask_color))

    # Save modified slices as PNG
    for i in range(grayscale_img.shape[2]):
        for _, centroid, mask_num, color in filter(lambda x: x[0] == i, centroid_mask_number):
            grayscale_image_array[i] = write_numbers_with_no_overlap(
                grayscale_image_array[i], [centroid], [mask_num], grayscale_img.shape[1]
            )

        output_path = os.path.join(output_dir, f'{image_prefix}_{i:03d}.png')
        cv2.imwrite(output_path, grayscale_image_array[i])

    print(f"Images saved in {output_dir} directory")
    return mask_number_list, color_list

def superimpose_singlemask_on_gray_ct_threshgiven(grayscale_img_path, infarct_mask_filename, output_dir, color_tuple, image_prefix,thresh=[20,60]):
    # Load and normalize grayscale image
    grayscale_img = nib.load(grayscale_img_path).get_fdata()
    min_int,max_int=extract_central_slice_intensity_range(grayscale_img, output_size=100)
    # grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)
    grayscale_img=stretch_intensity(grayscale_img,min_int,max_int)*255
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load infarct mask and binarize it
    infarct_mask_data = nib.load(infarct_mask_filename).get_fdata()
    infarct_mask_data = (infarct_mask_data > 0.5).astype(np.uint8)

    # Initialize a 3D RGB image array for each slice
    grayscale_image_array = np.stack([np.dstack([grayscale_img[:, :, i]] * 3) for i in range(grayscale_img.shape[2])])

    # Superimpose mask color on each slice
    for i in range(grayscale_img.shape[2]):
        mask_slice = infarct_mask_data[:, :, i]

        # Apply color only on mask regions
        grayscale_image_array[i][mask_slice > 0] = color_tuple

        # Save the result as a PNG image
        output_path = os.path.join(output_dir, f'{image_prefix}_{i:03d}.png')
        cv2.imwrite(output_path, grayscale_image_array[i])

    print(f"Images saved in {output_dir} directory")

    # print(f"Images saved in {output_dir} directory")
    # return mask_number_list, color_list
def superimpose_singlemask_on_gray_ct_original(grayscale_img_path, infarct_mask_filename, output_dir, color_tuple, image_prefix,thresh=[20,60]):
    # Load and normalize grayscale image
    grayscale_img = nib.load(grayscale_img_path).get_fdata()
    min_int=thresh[0]
    max_int=thresh[1] ##extract_central_slice_intensity_range(grayscale_img, output_size=100)
    # grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)
    grayscale_img=stretch_intensity(grayscale_img,min_int,max_int)*255
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load infarct mask and binarize it
    infarct_mask_data = nib.load(infarct_mask_filename).get_fdata()
    infarct_mask_data = (infarct_mask_data > 0.5).astype(np.uint8)

    # Initialize a 3D RGB image array for each slice
    grayscale_image_array = np.stack([np.dstack([grayscale_img[:, :, i]] * 3) for i in range(grayscale_img.shape[2])])

    # Superimpose mask color on each slice
    for i in range(grayscale_img.shape[2]):
        mask_slice = infarct_mask_data[:, :, i]

        # Apply color only on mask regions
        grayscale_image_array[i][mask_slice > 0] = color_tuple

        # Save the result as a PNG image
        output_path = os.path.join(output_dir, f'{image_prefix}_{i:03d}.png')
        cv2.imwrite(output_path, grayscale_image_array[i])

    print(f"Images saved in {output_dir} directory")

    # print(f"Images saved in {output_dir} directory")
    # return mask_number_list, color_list
def saveslicesofnifti_withgiventhresh_inmri(filename,min_intensity,max_intensity,savetodir=""):
    filename_nib=nib.load(filename)
    filename_gray_data_np=filename_nib.get_fdata()
    min_int,max_int=extract_central_slice_intensity_range(filename_gray_data_np, output_size=100)
    # grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)
    # grayscale_img=stretch_intensity(grayscale_img,min_int,max_int)*255
    min_img_gray=np.min(filename_gray_data_np)
    img_gray_data=0
    if not os.path.exists(savetodir):
        savetodir=os.path.dirname(filename)
    # if min_img_gray>=0:
    img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(min_int, max_int))
    # img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(1000, 1200))
    # else:
    #     img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(20, 60))
    #     # img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(0, 200))
    for x in range(img_gray_data.shape[2]):
        slice_number="{0:0=3d}".format(x)
        cv2.imwrite(os.path.join(savetodir,os.path.basename(filename).split(".nii")[0]+"_"+slice_number+".jpg" ),img_gray_data[:,:,x]*255 )



def extract_central_slice_intensity_range(img_data, output_size=100):
    # Load the NIfTI file
    # nifti_img = nib.load(nifti_path)
    # img_data = nifti_img.get_fdata()  # Get the image data as a NumPy array

    # Get the dimensions of the image
    dims = img_data.shape
    print(f"Image dimensions: {dims}")

    # Assuming the central slice is in the middle along the third axis
    center_z = dims[2] // 2
    central_slice = img_data[:, :, center_z]

    # Calculate the center of the slice
    center_x, center_y = dims[0] // 2, dims[1] // 2

    # Extract a 100x100 region around the center
    half_size = output_size // 2
    x_start = max(center_x - half_size, 0)
    x_end = min(center_x + half_size, dims[0])
    y_start = max(center_y - half_size, 0)
    y_end = min(center_y + half_size, dims[1])

    # Extract the central region
    extracted_slice = central_slice[x_start:x_end, y_start:y_end]
    return np.min(extracted_slice),np.max(extracted_slice)
def superimpose_singlemask_on_gray_ct(grayscale_img_path, infarct_mask_filename, output_dir, color_tuple, image_prefix):
    # Load and normalize grayscale image
    grayscale_img = nib.load(grayscale_img_path).get_fdata()
    grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load infarct mask and binarize it
    infarct_mask_data = nib.load(infarct_mask_filename).get_fdata()
    infarct_mask_data = (infarct_mask_data > 0.5).astype(np.uint8)

    # Initialize a 3D RGB image array for each slice
    grayscale_image_array = np.stack([np.dstack([grayscale_img[:, :, i]] * 3) for i in range(grayscale_img.shape[2])])

    # Superimpose mask color on each slice
    for i in range(grayscale_img.shape[2]):
        mask_slice = infarct_mask_data[:, :, i]

        # Apply color only on mask regions
        grayscale_image_array[i][mask_slice > 0] = color_tuple

        # Save the result as a PNG image
        output_path = os.path.join(output_dir, f'{image_prefix}_{i:03d}.png')
        cv2.imwrite(output_path, grayscale_image_array[i])

    print(f"Images saved in {output_dir} directory")

    # print(f"Images saved in {output_dir} directory")
    # return mask_number_list, color_list
#

#
# def superimpose_regions_overlapping_infarct_on_ct(grayscale_img_path, min_intensity,max_intensity,mask_img_paths,infarct_mask_filename,output_dir,predefined_legend):
#     """
#     Superimpose multi-regional masks on a CT grayscale image, highlighting regions overlapping with an infarct mask.
#
#     This function overlays multiple mask images on a CT grayscale image, applying specific colors to each mask region
#     based on a predefined legend. It highlights regions that overlap with an infarct mask, and saves each slice of
#     the result as a PNG image. Additionally, it marks centroids of regions with mask numbers to differentiate them visually.
#
#     Parameters:
#     -----------
#     grayscale_img_path : str
#         Path to the input CT grayscale NIfTI image file.
#
#     min_intensity : int or float
#         The minimum intensity value for rescaling the grayscale image.
#
#     max_intensity : int or float
#         The maximum intensity value for rescaling the grayscale image.
#
#     mask_img_paths : list of str
#         List of paths to NIfTI files containing the mask data for each region to be overlaid.
#
#     infarct_mask_filename : str
#         Path to the NIfTI file containing the infarct mask data.
#
#     output_dir : str
#         Directory path to save the output images, with each slice saved as a separate PNG file.
#
#     predefined_legend : str
#         Path to a CSV file defining mask colors for each mask number. The CSV file should have columns
#         'masknumber' (integer) and 'color' (RGB tuple in string format).
#
#     Returns:
#     --------
#     tuple
#         A tuple of two lists:
#         - mask_number_list: List of mask numbers applied to the CT image.
#         - color_list: List of colors corresponding to each mask number.
#
#     Process:
#     --------
#     1. Loads the grayscale and infarct mask images from the specified NIfTI files.
#     2. Rescales grayscale intensity to enhance visibility within the specified range.
#     3. Applies each mask as a color overlay, based on predefined colors, only in regions overlapping with the infarct.
#     4. Marks the centroid of each mask region with its mask number.
#     5. Saves each modified slice as a PNG file in the output directory.
#
#     Example:
#     --------
#     mask_numbers, colors = superimpose_regions_overlapping_infarct_on_ct(
#         'ct_image.nii', 1, 5, mask_img_paths, 'infarct_mask.nii', 'output/', 'legend.csv'
#     )
#
#     Notes:
#     ------
#     - Ensure `output_dir` exists or is created before running to prevent errors while saving images.
#     - The function uses the `stretch_intensity` function to adjust grayscale image contrast.
#     - The `write_numbers_with_no_overlap` function is called to place mask numbers at region centroids.
#
#     Dependencies:
#     -------------
#     - nibabel (for loading NIfTI files)
#     - OpenCV (for applying colors and saving images)
#     - NumPy (for array manipulation)
#     - pandas (for loading the predefined legend CSV)
#     """
#
#     print("grayscale_img_path::{}\n, min_intensity::{}\n,max_intensity::{}\n,mask_img_paths::{}\n,infarct_mask_filename::{}\n,output_dir::{}\n,predefined_legend::{}\n".format(grayscale_img_path, min_intensity,max_intensity,mask_img_paths,infarct_mask_filename,output_dir,predefined_legend))
#     predefined_legend_df=pd.read_csv(predefined_legend)
#     print(predefined_legend_df)
#     grayscale_img = nib.load(grayscale_img_path).get_fdata()
#
#     os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
#     #grayscale_img=normalize_nifti_image(grayscale_img)*255
# #     grayscale_img = stretch_intensity(grayscale_img, 1, 5) * 255
#
#     ####################################
#     data_min = np.min(grayscale_img)
#     data_max = np.max(grayscale_img)
#
#     # Perform Min-Max normalization to scale data to [0, 1]
#     grayscale_img = (grayscale_img - data_min) / (data_max - data_min)
#     grayscale_img=grayscale_img*255
#     ######################
#     grayscale_img = grayscale_img.astype(np.uint8)
#     grayscale_image_array = np.stack([np.dstack([grayscale_img[:, :, i]] * 3) for i in range(grayscale_img.shape[2])])
#
#     infarct_mask_data=nib.load(infarct_mask_filename).get_fdata()
#     infarct_mask_data[infarct_mask_data>0.5]=1
#     infarct_mask_data[infarct_mask_data<1]=0
#     # Iterate through each mask and apply it to the grayscale images
#     centroid_mask_number=[]
#     mask_number_list=[]
#     color_list=[]
#     mask_number_list_filename=[]
#     for mask_img_path in mask_img_paths:
#         print(f"mask_img_path::{mask_img_path}")
# #         mask_number=os.path.basename(mask_img_path).split('_fixed_scct_strippedResampled1_lin1.nii.gz')[0].split('_')[-1]
# #         mask_number=os.path.basename(mask_img_path).split('_region_')[1].split('_')[0]
#         mask_number=os.path.basename(mask_img_path).split('resampled')[0].split('_')[-1]
#         if mask_number.isdigit():
#     #     warped_1_mov_ArterialAtlas_label_5resampled_mov_fixed_scct_strippedResampled1_normalized_fix_lin1_BET.nii.gz
#             print(mask_number)
#     #         mask_number_list.append(int(mask_number))
#             mask_number_list_filename.append([mask_img_path,int(mask_number)])
#     #         print(mask_number)
#     #     print(mask_number_list_filename)
#         mask_number_list_filename = sorted(mask_number_list_filename, key=lambda x: x[1])
#         mask_number_list=[]
#         for each_element in mask_number_list_filename:
#             print(each_element)
#             mask_color = eval(predefined_legend_df[predefined_legend_df['masknumber']==int(each_element[1])].reset_index().at[0,'color']) #np.array([random.randint(0, 255) for _ in range(3)])  # Random mask color
#             print(predefined_legend_df[predefined_legend_df['masknumber']==int(int(each_element[1]))])
#             color_list.append((int(mask_color[0]),int(mask_color[1]),int(mask_color[2])))
#     #         # Load the mask image
#             mask_img = nib.load(each_element[0]).get_fdata()
#             mask_number_list.append(int(each_element[1]))
#             for i in range(grayscale_img.shape[2]):
#                 mask_slice = mask_img[:, :, i]
#                 mask_slice[infarct_mask_data[:,:,i]<1]=np.min(mask_img)
#                 grayscale_image_array[i][mask_slice > 0] = mask_color  # Apply the mask color
#                 #########
#                 if np.sum(mask_slice)>0:
#                     coords = np.column_stack(np.where(mask_slice > 0))  # Get coordinates of non-zero mask pixels
#                     centroid = np.mean(coords, axis=0).astype(int)
#         #         # Apply mask to each slice in a vectorized manner
#                     centroid_mask_number.append([i,centroid,int(each_element[1]),mask_color])
#
#         # Save all the modified slices as PNG
#         for i in range(grayscale_img.shape[2]):
#             for x in range(len(centroid_mask_number)):
#     #             image_width = grayscale_img.shape[1]
#                 if centroid_mask_number[x][0]==i:
#                     grayscale_image_array[i]=write_numbers_with_no_overlap( grayscale_image_array[i], [centroid_mask_number[x][1]], [centroid_mask_number[x][2]], grayscale_img.shape[1])
#             output_path = os.path.join(output_dir, f'slice_{i:03d}.png')
#             cv2.imwrite(output_path, grayscale_image_array[i])
#         print(f"Images saved in {output_dir} directory")
#     return mask_number_list,color_list
def call_regional_vol_and_images(args):
    grayscale_img_path=args.stuff[1]
    min_intensity=args.stuff[2]
    max_intensity=args.stuff[3]
    infarct_mask_filename=args.stuff[4]
    template_nifti_file=args.stuff[5]
    output_dir=args.stuff[6]
    predefined_legend=args.stuff[7]
    session_id=args.stuff[8]
    scan_id=args.stuff[9]
    region_mask_type=args.stuff[10]
    mask_img_paths=args.stuff[11:]
    print(mask_img_paths)
    
    superimpose_regions_overlapping_infarct_on_ct(grayscale_img_path, min_intensity,max_intensity,mask_img_paths,infarct_mask_filename,output_dir,predefined_legend)
    df=volumes_regions_overlapping_infarct_on_ct( mask_img_paths,infarct_mask_filename,template_nifti_file,region_mask_type)
    session_name=get_session_label(session_id,outputfile="NONE.csv") #args.stuff[9]
    df["session_id"]=""
    df["session_id"]=session_id
    df["scan_id"]=""
    df["scan_id"]=scan_id
    df["session_scan_name"]=""
    session_scan_ct=os.path.basename(infarct_mask_filename).split('mov_')[1].split('_resaved_infarct_auto_removesmall')[0]
    df["session_scan_name"]=session_scan_ct
#     mov_COLI_HLP45_02152022_1123_6_resaved_infarct_auto_removesmallresampled_mov_fixed_scct_strippedResampled1_normalized_fix_lin1.nii.gz#session_scan_ct_name
    df["region_mask_source"]=""
    df["region_mask_source"]=os.path.basename(template_nifti_file)
    df["session_name"]=""
    df["session_name"]=session_name
    date_time = time.strftime("_%m_%d_%Y",now)
    outputfilename=os.path.join(os.path.dirname(infarct_mask_filename),session_scan_ct+'_with_mask'+os.path.basename(template_nifti_file).split('.nii')[0]+'_regional_volumes'+date_time+'.csv')
    df.to_csv("outputfilename.csv",index=False)
    
def volumes_regions_overlapping_infarct_on_ct( mask_img_paths,infarct_mask_filename,template_nifti_file,region_mask_type,infarct_volume_after_reg,infarct_volume_before_reg=1,splitter='_fixed'):


    template_nifti_nib = nib.load(template_nifti_file)

    infarct_mask_nib=nib.load(infarct_mask_filename)
    infarct_mask_data=infarct_mask_nib.get_fdata()
    infarct_mask_data[infarct_mask_data>0.5]=1
    infarct_mask_data[infarct_mask_data<1]=0
    # Iterate through each mask and apply it to the grayscale images


    # Declare an empty DataFrame
    df = pd.DataFrame()



    # Display the DataFrame
    # print(df)
    df = pd.DataFrame(index=range(1))
    print("MAIN YAHAN HOON")
    for mask_img_path in mask_img_paths:
        command="echo I am  at :: {} >> software/error.txt".format(inspect.stack()[0][3])
        subprocess.call(command,shell=True)

        
#         mask_number=os.path.basename(mask_img_path).split('_fixed_scct_strippedResampled1_lin1.nii.gz')[0].split('_')[-1]
#         mask_number=os.path.basename(mask_img_path).split('_region_')[1].split('_')[0]
        mask_number=os.path.basename(mask_img_path).split(splitter)[0].split('_')[-1]
        df[f"{region_mask_type}_region{mask_number}"]=""
        print(mask_number)
        mask_img = nib.load(mask_img_path).get_fdata()
        mask_img[mask_img>0.5]=1
        mask_img[mask_img<1]=0
        volume_territory=(np.sum(mask_img)*np.product(template_nifti_nib.header["pixdim"][1:4]))/1000         
        mask_img[(infarct_mask_data < 1)] =0 # | (mask_img < 1)] = 0
        volume=(np.sum(mask_img)*np.product(template_nifti_nib.header["pixdim"][1:4]))/1000 
###(((np.sum(mask_img)*np.product(template_nifti_nib.header["pixdim"][1:4]))/1000  )/infarct_volume_after_reg) *infarct_volume_before_reg
        df[f"{region_mask_type}_region{mask_number}"]=volume
        df[f"{region_mask_type}_region{mask_number}_territory"]=volume_territory
    return df[natsorted(df.columns)]




def count_frequency_of_a_voxel(infarctmasks):

    """
    Calculate and save the frequency of voxel occurrence across multiple infarct masks.

    This function processes a list of infarct mask NIfTI files, binarizing each mask and summing
    the presence of each voxel across all masks. The frequency of each voxel across the masks is 
    then saved as a NIfTI file with values normalized between 0 and 1. Additionally, the normalized 
    data is saved in the 0–255 range.

    Parameters:
    -----------
    infarctmasks : list of str
        List of paths to NIfTI files representing individual infarct masks. Non-zero values indicate
        infarct regions in each mask.

    Returns:
    --------
    numpy.ndarray
        A 3D array representing the cumulative frequency of each voxel across all infarct masks.

    Process:
    --------
    1. Iterates through each infarct mask file in `infarctmasks`.
    2. Binarizes each mask, setting values greater than 0.5 to 1 and others to 0.
    3. Adds each binarized mask to a cumulative mask (`infarc_mask_data_all`) to count voxel frequencies.
    4. Saves the frequency map as a NIfTI file (`infarc_mask_data_all_frequency.nii.gz`), normalized to the 0–1 range.
    5. Also saves a version of the frequency map scaled to the 0–255 range (`infarc_mask_data_all_0_255.nii.gz`).

    Example:
    --------
    frequency_data = count_frequency_of_a_voxel(['mask1.nii.gz', 'mask2.nii.gz', 'mask3.nii.gz'])

    Notes:
    ------
    - Ensure `infarctmasks` contains paths to valid NIfTI files.
    - The function uses the `normalize_nifti_image` function to scale data between 0 and 1 for visualization.

    Dependencies:
    -------------
    - nibabel (for loading and saving NIfTI files)
    - NumPy (for array manipulation)
    """

    infarc_mask_data_all=0
    for infarc_mask_id in range(len(infarctmasks)):
        if infarc_mask_id==0:
            infarc_mask_nib=nib.load(infarctmasks[infarc_mask_id])
            infarc_mask_nib_data=infarc_mask_nib.get_fdata()
            infarc_mask_nib_data[infarc_mask_nib_data>0.5]=1
            infarc_mask_nib_data[infarc_mask_nib_data<1]=0
            infarc_mask_data_all=infarc_mask_nib_data
        if infarc_mask_id>0:
            infarc_mask_nib=nib.load(infarctmasks[infarc_mask_id])
            infarc_mask_nib_data=infarc_mask_nib.get_fdata()
            infarc_mask_nib_data[infarc_mask_nib_data>0.5]=1
            infarc_mask_nib_data[infarc_mask_nib_data<1]=0
            infarc_mask_data_all=infarc_mask_data_all+infarc_mask_nib_data #nib.load(infarctmasks[infarc_mask_id]).get_fdata()
    img_nib=nib.Nifti1Image(infarc_mask_data_all/len(infarctmasks),affine=infarc_mask_nib.affine,header=infarc_mask_nib.header)
    nib.save(img_nib,'infarc_mask_data_all_frequency.nii.gz')
    img_nib=nib.Nifti1Image(normalize_nifti_image(infarc_mask_data_all/len(infarctmasks) )*255,affine=infarc_mask_nib.affine,header=infarc_mask_nib.header)
    nib.save(img_nib,'infarc_mask_data_all_0_255.nii.gz')
    return infarc_mask_data_all
####################################################################
# !cp /media/atul/WDJan20222/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/download_with_session_ID.py ./
# !cp /media/atul/WDJan20222/WASHU_WORKS/PROJECTS/DOCKERIZE/NWU/PYCHARM/EDEMA_MARKERS_PROD/utilities_simple_trimmed.py ./
# !export XNAT_USER='atulkumar'
# !export XNAT_PASS='Mrityor1!'
# !export XNAT_HOST='https://snipr.wustl.edu'
import SimpleITK as sitk
import numpy as np
import matplotlib as plt
import SimpleITK as sitk
import numpy as np

def post_process_smooothing_closing(file_path,binary_threshold=0.5,smooth_sigma=2.0):
    # Load the NIfTI file
    # file_path = '/media/atul/WDJan20222/WASHU_WORKS/PROJECTS/SNIPR/TESTDEEPREGBASEDREGISTRATION/input/warped_1_mov_COLI_HLP45_02152022_1123_6_resaved_infarct_auto_removesmall_fixed_COLIHM620406202215542_lin1_BET.nii.gz'
    deformed_mask = sitk.ReadImage(file_path, sitk.sitkFloat32)
    deformed_mask = sitk.Cast(deformed_mask, sitk.sitkUInt8)

    # 1. Smooth the mask using a Gaussian filter
    smoothed_mask = sitk.SmoothingRecursiveGaussian(deformed_mask, sigma=smooth_sigma)
    smoothed_mask_array=sitk.GetArrayFromImage(smoothed_mask)
    smoothed_mask_array[smoothed_mask_array>binary_threshold]=1
    smoothed_mask_array_image=sitk.GetImageFromArray(smoothed_mask_array)
    smoothed_mask_array_image=sitk.Cast(smoothed_mask_array_image,sitk.sitkUInt8)
    smoothed_mask_array_image.CopyInformation(deformed_mask)
    # smoothed_mask = sitk.Cast(smoothed_mask, sitk.sitkUInt8)
    # 2. Threshold the smoothed mask to create a binary mask
    # threshold_lower = 0.001
    # threshold_upper = 1.0
    # binary_mask = sitk.BinaryThreshold(smoothed_mask, lowerThreshold=threshold_lower, upperThreshold=threshold_upper, insideValue=1, outsideValue=0)

    # 3. Apply morphological closing to fill small holes
    kernel_radius = [2, 2, 2]  # Radius for closing in 3D
    closed_mask = sitk.BinaryMorphologicalClosing(smoothed_mask_array_image, kernelRadius=kernel_radius)

    # # 4. Remove small connected components (noise)
    # connected_components = sitk.ConnectedComponent(deformed_mask)
    # label_shape_filter = sitk.LabelShapeStatisticsImageFilter()
    # label_shape_filter.Execute(connected_components)

    # # Retain only components larger than a minimum size
    # min_size = 200
    # cleaned_mask = sitk.Image(connected_components.GetSize(), sitk.sitkUInt8)
    # cleaned_mask.CopyInformation(connected_components)

    # for label in label_shape_filter.GetLabels():
    #     if label_shape_filter.GetPhysicalSize(label) >= min_size:
    #         cleaned_mask = cleaned_mask | (connected_components == label)
    # 4. Remove small connected components (noise) based on physical volume
    connected_components = sitk.ConnectedComponent(closed_mask)
    label_shape_filter = sitk.LabelShapeStatisticsImageFilter()
    label_shape_filter.Execute(connected_components)

    # Set the minimum volume threshold in physical units (e.g., mm³)
    min_volume = 1000  # Adjust this based on your requirements

    # Create an empty binary mask to store components meeting the volume threshold
    cleaned_mask = sitk.Image(connected_components.GetSize(), sitk.sitkUInt8)
    cleaned_mask.CopyInformation(connected_components)

    # Iterate through the connected components and filter by physical volume
    for label in label_shape_filter.GetLabels():
        physical_volume = label_shape_filter.GetPhysicalSize(label)  # Volume in physical units
        if physical_volume >= min_volume:
            # Add the component to the cleaned mask
            cleaned_mask = cleaned_mask | (connected_components == label)

    # Save the post-processed mask
    # Save the post-processed mask
    output_path =file_path # "post_processed_mask.nii.gz"
    sitk.WriteImage(cleaned_mask, output_path)

    print(f"Post-processed mask saved to {output_path}")
    show_all_slices(sitk.GetArrayFromImage(deformed_mask), axis=2, cmap="gray")
    cleaned_mask_array = sitk.GetArrayFromImage(cleaned_mask)
    show_all_slices(cleaned_mask_array, axis=2, cmap="gray")
    infarct_mask=output_path #'/media/atul/WDJan20222/WASHU_WORKS/PROJECTS/SNIPR/TESTDEEPREGBASEDREGISTRATION/workinginput/mov_COLI_HLP45_02152022_1123_6_resaved_infarct_auto_removesmall_fixed_COLIHM620406202215542_lin1_BET.nii.gz'
    infarct_mask_sitk=sitk.ReadImage(infarct_mask)
    volume_array = sitk.GetArrayFromImage(infarct_mask_sitk)
    show_all_slices(volume_array, axis=2, cmap="gray")

# Convert the SimpleITK image to a NumPy array for visualization

import matplotlib.pyplot as plt
import numpy as np

def show_all_slices(volume, axis=2, cmap="gray"):
    """
    Visualizes all slices in a 3D volume as a montage.
    Args:
        volume: 3D NumPy array.
        axis: Axis along which to slice (default: 2 for transverse slices).
        cmap: Colormap for the images (default: "gray").
    """
    # # Check the axis and reshape the volume
    # if axis == 0:
    #     slices = np.moveaxis(volume, 0, -1)  # Make axis 0 the last axis
    # elif axis == 1:
    #     slices = np.moveaxis(volume, 1, -1)  # Make axis 1 the last axis
    # elif axis == 2:
    #     slices = volume  # Axis 2 (default) is already the last axis
    # else:
    #     raise ValueError("Invalid axis. Choose 0, 1, or 2.")

    num_slices = volume.shape[0]  # Total slices along the selected axis
    cols = 10  # Number of columns in the montage
    rows = int(np.ceil(num_slices / cols))  # Number of rows in the montage

    # Create a montage grid
    fig, axes = plt.subplots(rows, cols, figsize=(20, rows * 2))
    axes = axes.flatten()

    for i in range(rows * cols):
        if i < num_slices:
            axes[i].imshow(volume[i, :, : ], cmap=cmap)
            axes[i].axis("off")
            axes[i].set_title(f"Slice {i}")
        else:
            axes[i].axis("off")  # Turn off unused subplots

    plt.tight_layout()
    plt.show()

# Example usage:
# Assume `volume` is a 3D NumPy array
# Transverse slices are along the z-axis (axis=2):
# volume_array = sitk.GetArrayFromImage(cleaned_mask_array)  # Convert to NumPy array
# deformed_mask

def main():
    print("WO ZAI ::{}".format("main"))
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    name_of_the_function=args.stuff[0]
    return_value=0
    if name_of_the_function == "call_superimpose_regions_overlapping_infarct_on_ct":
        return_value=call_superimpose_regions_overlapping_infarct_on_ct(args)  #call_regional_vol_and_images
    if name_of_the_function == "call_regional_vol_and_images":
        return_value=call_regional_vol_and_images(args)        
    return return_value
if __name__ == '__main__':
    main()



