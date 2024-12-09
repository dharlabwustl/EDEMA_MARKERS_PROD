import csv,sys,os
import nibabel as nib
import numpy as np
from scipy.spatial.distance import directed_hausdorff
import SimpleITK as sitk

import nibabel as nib
import numpy as np
from sklearn.metrics import mutual_info_score
def load_nifti_mask(file_path):
    """
    Load a NIfTI mask file and return the binary mask array.
    """
    nifti_data = nib.load(file_path)
    mask = nifti_data.get_fdata()
    return (mask > 0).astype(np.int8)  # Convert to binary mask

def dice_coefficient(mask1, mask2):
    """
    Calculate the Dice Similarity Coefficient (DSC) between two binary masks.
    """
    intersection = np.sum(mask1 * mask2)
    sum_masks = np.sum(mask1) + np.sum(mask2)
    if sum_masks == 0:
        return 1.0  # Perfect score if both masks are empty
    return 2.0 * intersection / sum_masks

def jaccard_index(mask1, mask2):
    """
    Calculate the Jaccard Index between two binary masks.
    """
    intersection = np.sum(mask1 * mask2)
    union = np.sum(mask1 + mask2) - intersection
    if union == 0:
        return 1.0  # Perfect score if both masks are empty
    return intersection / union

def hausdorff_distance(mask1, mask2):
    """
    Calculate the Hausdorff Distance between two binary masks.
    """
    points1 = np.column_stack(np.where(mask1 > 0))
    points2 = np.column_stack(np.where(mask2 > 0))
    if points1.size == 0 or points2.size == 0:
        return np.inf  # Undefined if either mask is empty
    h1 = directed_hausdorff(points1, points2)[0]
    h2 = directed_hausdorff(points2, points1)[0]
    return max(h1, h2)



save_metrics_to_csv(csv_output, mask1_path, mask2_path, dice, jaccard, hausdorff)

print(f"Metrics saved to {csv_output}")


def load_nifti_image(file_path):
    """
    Load a NIfTI file and return its image data as a numpy array.
    """
    nifti_data = nib.load(file_path)
    image_data = nifti_data.get_fdata()
    return image_data

def calculate_mutual_information(image1, image2, bins=256):
    """
    Calculate the Mutual Information (MI) between two images.

    Parameters:
    - image1: First image array.
    - image2: Second image array.
    - bins: Number of bins for histogram calculation (default is 256).

    Returns:
    - Mutual Information value.
    """
    # Flatten the images to 1D arrays
    image1_flat = image1.flatten()
    image2_flat = image2.flatten()

    # Calculate the joint histogram
    joint_hist, _, _ = np.histogram2d(image1_flat, image2_flat, bins=bins)

    # Normalize the joint histogram to get joint probabilities
    joint_prob = joint_hist / joint_hist.sum()

    # Compute marginal probabilities
    prob_image1 = np.sum(joint_prob, axis=1)
    prob_image2 = np.sum(joint_prob, axis=0)

    # Compute MI using the formula
    non_zero_indices = joint_prob > 0  # Avoid log(0) issues
    mi = np.sum(joint_prob[non_zero_indices] *
                np.log(joint_prob[non_zero_indices] /
                       (prob_image1[:, None] * prob_image2)[non_zero_indices]))
    return mi

# # Example usage
# image1_path = "path_to_image1.nii"
# image2_path = "path_to_image2.nii"
#
# # Load images
# image1 = load_nifti_image(image1_path)
# image2 = load_nifti_image(image2_path)
#
# # Calculate Mutual Information
# mi = calculate_mutual_information(image1, image2)
#
# # Print the result
# print(f"Mutual Information: {mi:.4f}")
def calculate_mutual_information(image1_path, image2_path):
    """
    Calculate the Mutual Information (MI) between two NIfTI images using SimpleITK.

    Parameters:
    - image1_path: Path to the first NIfTI image.
    - image2_path: Path to the second NIfTI image.

    Returns:
    - Mutual Information value.
    """
    # Read the images
    image1 = sitk.ReadImage(image1_path, sitk.sitkFloat32)
    image2 = sitk.ReadImage(image2_path, sitk.sitkFloat32)

    # Create a histogram-based mutual information metric
    mutual_information_metric = sitk.MutualInformationHistogramImageToImageMetricv4()

    # Set the images for the metric
    mutual_information_metric.SetFixedImage(image1)
    mutual_information_metric.SetMovingImage(image2)

    # Compute the metric value
    mi = mutual_information_metric.GetValue()
    return mi
def save_metrics_to_csv(csv_file, listofmetrics ): #dice, jaccard, hausdorff):
    """
    Save the calculated metrics to a CSV file.
    """

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(listofmetrics) ##[mask1_name, mask2_name, dice, jaccard, hausdorff])

def calculate_entropy(probabilities):
    """
    Calculate entropy from a probability distribution.
    """
    probabilities = probabilities[probabilities > 0]  # Avoid log(0)
    return -np.sum(probabilities * np.log(probabilities))

def calculate_normalized_mutual_information(image1_path, image2_path, bins=256):
    """
    Calculate Normalized Mutual Information (NMI) between two images using SimpleITK.

    Parameters:
    - image1_path: Path to the first image (NIfTI).
    - image2_path: Path to the second image (NIfTI).
    - bins: Number of bins for histogram calculation.

    Returns:
    - Normalized Mutual Information (NMI).
    """
    # Load the images
    image1 = sitk.GetArrayFromImage(sitk.ReadImage(image1_path))
    image2 = sitk.GetArrayFromImage(sitk.ReadImage(image2_path))

    # Flatten the images to 1D arrays
    image1_flat = image1.flatten()
    image2_flat = image2.flatten()

    # Compute joint histogram
    joint_histogram, _, _ = np.histogram2d(image1_flat, image2_flat, bins=bins)
    joint_prob = joint_histogram / joint_histogram.sum()  # Normalize to probabilities

    # Marginal probabilities
    prob_image1 = np.sum(joint_prob, axis=1)  # Sum along columns
    prob_image2 = np.sum(joint_prob, axis=0)  # Sum along rows

    # Compute entropies
    H_A = calculate_entropy(prob_image1)
    H_B = calculate_entropy(prob_image2)
    H_AB = calculate_entropy(joint_prob.flatten())

    # Compute NMI
    nmi = (H_A + H_B) / H_AB
    return nmi

# # Example Usage
# image1_path = "path_to_image1.nii"
# image2_path = "path_to_image2.nii"


# print(f"Normalized Mutual Information: {nmi:.4f}")



#################### APPLICATION ###############################
# Example usage
image1_path = sys.argv[1] #"path_to_image1.nii"
image2_path = sys.argv[2] #"path_to_image2.nii"
# Calculate Mutual Information
mi_value = calculate_mutual_information(image1_path, image2_path)
nmi = calculate_normalized_mutual_information(image1_path, image2_path)
# Print the result
print(f"Mutual Information: {mi_value:.4f}")
# Example Usage
mask1_path = sys.argv[3] #"path_to_mask1.nii"
mask2_path = sys.argv[4] #"path_to_mask2.nii"
# Load masks
mask1 = load_nifti_mask(mask1_path)
mask2 = load_nifti_mask(mask2_path)
# Compute metrics
dice = dice_coefficient(mask1, mask2)
jaccard = jaccard_index(mask1, mask2)
hausdorff = hausdorff_distance(mask1, mask2)

# Save metrics
csv_output = image2_path.split('.nii')[0]+"_metrics_results.csv"
header = ["Mask1", "Mask2", "Dice Similarity Coefficient", "Jaccard Index", "Hausdorff Distance","Mutual Information","Normalized Mutual Information"]
listofmetrics=[os.path.basename(image1_path), os.path.basename(image2_path),dice, jaccard, hausdorff,mi_value,nmi]
try:
    # Add header only if file doesn't exist
    with open(csv_output, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
except FileExistsError:
    pass  # File exists, do nothing
save_metrics_to_csv(csv_output, listofmetrics )

