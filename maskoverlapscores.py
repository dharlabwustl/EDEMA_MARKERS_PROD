import trimesh
from skimage import measure
from scipy.spatial import ConvexHull
import cv2
import csv,sys,os
import nibabel as nib
import numpy as np
from scipy.spatial.distance import directed_hausdorff
import SimpleITK as sitk
from scipy.spatial import Delaunay
import nibabel as nib
import numpy as np
from sklearn.metrics import mutual_info_score
import numpy as np
from scipy.spatial.distance import cdist
def load_nii_mask(input_nii_path):
    """
    Load a binary mask from a NIfTI file.

    Parameters:
        input_nii_path (str): Path to the NIfTI mask file.

    Returns:
        binary_mask (numpy.ndarray): Binary mask data (1 for mask, 0 for background).
        affine (numpy.ndarray): Affine transformation matrix of the NIfTI file.
        header (nibabel.Nifti1Header): Header information of the NIfTI file.
    """
    # Load the NIfTI file
    nii_img = nib.load(input_nii_path)

    # Extract data, affine, and header
    mask_data = nii_img.get_fdata()
    affine = nii_img.affine
    header = nii_img.header

    # Convert the mask to binary (ensure only 1s and 0s)
    binary_mask = np.where(mask_data > 0, 1, 0).astype(np.uint8)

    return binary_mask, affine, header
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




def load_nifti_image(file_path):
    """
    Load a NIfTI file and return its image data as a numpy array.
    """
    nifti_data = nib.load(file_path)
    image_data = nifti_data.get_fdata()
    return image_data


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
def overlap_ratio(mask1, mask2):
    """
    Calculate the overlap ratio of Mask 1 relative to its volume.

    Parameters:
    - mask1: Binary numpy array of Mask 1 (values are 0 or 1).
    - mask2: Binary numpy array of Mask 2 (values are 0 or 1).

    Returns:
    - Overlap ratio (relative to Mask 1).
    """
    # Compute the intersection of the two masks
    intersection = np.logical_and(mask1, mask2).sum()

    # Compute the total volume of Mask 1
    mask1_volume = mask1.sum()

    # Handle edge case where Mask 1 is empty
    if mask1_volume == 0:
        return 0.0

    # Calculate overlap ratio
    overlap = intersection / mask1_volume
    return overlap
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

def calculate_mutual_information(image1_path, image2_path, bins=256):
    image1 = load_nifti_image(image1_path)
    image2 = load_nifti_image(image2_path)
    """
    Calculate the Mutual Information (MI) between two images.

    Parameters:
    - image1: First image as a 2D or 3D numpy array.
    - image2: Second image as a 2D or 3D numpy array.
    - bins: Number of bins for histogram calculation (default=256).

    Returns:
    - Mutual Information (MI).
    """
    # Flatten the images into 1D arrays
    image1 = image1.flatten()
    image2 = image2.flatten()

    # Compute joint histogram
    joint_hist, _, _ = np.histogram2d(image1, image2, bins=bins)

    # Normalize to get joint probability distribution
    joint_prob = joint_hist / joint_hist.sum()

    # Compute marginal probabilities
    prob_image1 = np.sum(joint_prob, axis=1)  # Sum along rows
    prob_image2 = np.sum(joint_prob, axis=0)  # Sum along columns

    # Compute joint entropy
    joint_entropy = calculate_entropy(joint_prob.flatten())

    # Compute marginal entropies
    entropy_image1 = calculate_entropy(prob_image1)
    entropy_image2 = calculate_entropy(prob_image2)

    # Calculate Mutual Information
    mutual_information = entropy_image1 + entropy_image2 - joint_entropy
    return mutual_information

def calculate_normalized_mutual_information(image1_path, image2_path, bins=256):
    image1 = load_nifti_image(image1_path)
    image2 = load_nifti_image(image2_path)
    """
    Calculate the Normalized Mutual Information (NMI) between two images.

    Parameters:
    - image1: First image as a 2D or 3D numpy array.
    - image2: Second image as a 2D or 3D numpy array.
    - bins: Number of bins for histogram calculation (default=256).

    Returns:
    - Normalized Mutual Information (NMI).
    """
    # Flatten the images into 1D arrays
    image1 = image1.flatten()
    image2 = image2.flatten()

    # Compute joint histogram
    joint_hist, _, _ = np.histogram2d(image1, image2, bins=bins)

    # Normalize to get joint probability distribution
    joint_prob = joint_hist / joint_hist.sum()

    # Compute marginal probabilities
    prob_image1 = np.sum(joint_prob, axis=1)  # Sum along rows
    prob_image2 = np.sum(joint_prob, axis=0)  # Sum along columns

    # Compute joint entropy
    joint_entropy = calculate_entropy(joint_prob.flatten())

    # Compute marginal entropies
    entropy_image1 = calculate_entropy(prob_image1)
    entropy_image2 = calculate_entropy(prob_image2)

    # Calculate Normalized Mutual Information
    nmi = (entropy_image1 + entropy_image2) / joint_entropy
    return nmi

# # Example Usage
# image1_path = "path_to_image1.nii"
# image2_path = "path_to_image2.nii"


# print(f"Normalized Mutual Information: {nmi:.4f}")



#################### APPLICATION ###############################
# Example usage
def call_evaluation_metric_calculation(image1_path,image2_path,mask1_path,mask2_path):
    # image1_path = sys.argv[1] #"path_to_image1.nii"
    # image2_path = sys.argv[2] #"path_to_image2.nii"
    # Calculate Mutual Information
    mi_value = calculate_mutual_information(image1_path, image2_path)
    nmi = calculate_normalized_mutual_information(image1_path, image2_path)
    # Print the result
    print(f"Mutual Information: {mi_value:.4f}")
    # Example Usage
    # mask1_path = sys.argv[3] #"path_to_mask1.nii"
    # mask2_path = sys.argv[4] #"path_to_mask2.nii"
    # Load masks
    mask1 = load_nifti_mask(mask1_path)
    mask2 = load_nifti_mask(mask2_path)
    # Compute metrics
    dice = dice_coefficient(mask1, mask2)
    jaccard = jaccard_index(mask1, mask2)
    hausdorff = hausdorff_distance(mask1, mask2)
    overlapratio_den_session=overlap_ratio(mask2, mask1)
    overlapratio_den_template=overlap_ratio(mask1, mask2)
    # semi_hausdorff_distance_3d(mask2, mask1)
    # mean_directed_hausdorff_distance_3d(mask2, mask1)
    # warped_csf_mask=f'input/warped_1_mov_{SCAN_NAME_no_ext}_resaved_csf_unet_fixed_COLIHM620406202215542_lin1_BET.nii.gz'
    moving_image_basename=os.path.basename(mask2_path).split('_resaved')[0].split('warped_1_mov_')[1]
    # Save metrics
    csv_output = image2_path.split('.nii')[0]+"_metrics_results.csv"
    header = ["Fixed Image Basename", "Moving Image Basename","overlapratio_den_session","overlapratio_den_template", "Dice Similarity Coefficient", "Jaccard Index", "Hausdorff Distance","Mutual Information","Normalized Mutual Information"]
    listofmetrics=[os.path.basename(image1_path).split('.nii')[0], moving_image_basename,overlapratio_den_session,overlapratio_den_template,dice, jaccard, hausdorff,mi_value,nmi]
    try:
        # Add header only if file doesn't exist
        with open(csv_output, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    except FileExistsError:
        pass  # File exists, do nothing
    save_metrics_to_csv(csv_output, listofmetrics )

def ratio_twomasks(mask1,mask2):
    mask1_nib=nib.load(mask1)
    mask1_nib_data=mask1_nib.get_fdata()
    mask1_nib_data[mask1_nib_data>np.min(mask1_nib_data)]=1
    mask1_nib_data[mask1_nib_data<1]=0
    mask2_nib=nib.load(mask2)
    mask2_nib_data=mask2_nib.get_fdata()
    mask2_nib_data[mask2_nib_data>np.min(mask2_nib_data)]=1
    mask2_nib_data[mask2_nib_data<1]=0
    if np.sum(mask2_nib_data)!=0:
        return np.sum(mask1_nib_data)/np.sum(mask2_nib_data)
    else:
        print("mask2 should be bigger than mask1")



def superimpose_single_mask(grayscale_img_path, mask_path, output_dir, mask_color=(255, 0, 0), image_prefix="superimposed", threshold=0.5):
    """
    Superimpose a single binary mask on a grayscale image with a specified color.

    Parameters:
    - grayscale_img_path: Path to the grayscale NIfTI image.
    - mask_path: Path to the binary mask NIfTI image.
    - output_dir: Directory to save the superimposed images.
    - mask_color: RGB color for the mask (default is red).
    - image_prefix: Prefix for the output image filenames.
    - threshold: Threshold to binarize the mask image (default is 0.5).

    Output:
    - Superimposed images for each slice saved as PNG files in the output directory.
    """
    # Load grayscale image and normalize intensity
    grayscale_img = nib.load(grayscale_img_path).get_fdata()
    grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)

    # Load and binarize the mask
    mask = nib.load(mask_path).get_fdata()
    mask = (mask > threshold).astype(np.uint8)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop through each slice
    for i in range(grayscale_img.shape[2]):
        # Extract the slice from the grayscale image
        grayscale_slice = grayscale_img[:, :, i]

        # Convert grayscale slice to RGB
        grayscale_rgb = np.dstack([grayscale_slice] * 3)

        # Extract the corresponding slice from the mask
        mask_slice = mask[:, :, i]

        # Overlay the mask (in mask_color)
        mask_indices = np.where(mask_slice > 0)
        grayscale_rgb[mask_indices] = mask_color

        # Save the superimposed image as PNG
        output_path = os.path.join(output_dir, f"{image_prefix}_slice_{i:03d}.png")
        cv2.imwrite(output_path, grayscale_rgb)

    print(f"Superimposed images saved in {output_dir}")

def superimpose_two_masks(grayscale_img_path, mask1_path, mask2_path, output_dir, mask1_color=(255, 0, 0), mask2_color=(0, 255, 0), image_prefix="superimposed", threshold=0.5):
    """
    Superimpose two binary masks on a grayscale image with different colors for visualization.

    Parameters:
    - grayscale_img_path: Path to the grayscale NIfTI image.
    - mask1_path: Path to the first binary mask NIfTI image.
    - mask2_path: Path to the second binary mask NIfTI image.
    - output_dir: Directory to save the superimposed images.
    - mask1_color: RGB color for the first mask (default is red).
    - mask2_color: RGB color for the second mask (default is green).
    - image_prefix: Prefix for the output image filenames.
    - threshold: Threshold to binarize the mask images (default is 0.5).

    Output:
    - Superimposed images for each slice saved as PNG files in the output directory.
    """
    # Load grayscale image and normalize intensity
    grayscale_img = nib.load(grayscale_img_path).get_fdata()
    grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)

    # Load and binarize masks
    mask1 = nib.load(mask1_path).get_fdata()
    mask2 = nib.load(mask2_path).get_fdata()
    mask1 = (mask1 > threshold).astype(np.uint8)
    mask2 = (mask2 > threshold).astype(np.uint8)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop through each slice
    for i in range(grayscale_img.shape[2]):
        # Extract the slice from the grayscale image
        grayscale_slice = grayscale_img[:, :, i]

        # Convert grayscale slice to RGB
        grayscale_rgb = np.dstack([grayscale_slice] * 3)

        # Extract corresponding slices from masks
        mask1_slice = mask1[:, :, i]
        mask2_slice = mask2[:, :, i]

        # Overlay mask1 (in mask1_color)
        mask1_indices = np.where(mask1_slice > 0)
        grayscale_rgb[mask1_indices] = mask1_color

        # Overlay mask2 (in mask2_color), ensuring overlap regions are visible
        mask2_indices = np.where(mask2_slice > 0)
        grayscale_rgb[mask2_indices] = mask2_color

        # Save the superimposed image as PNG
        output_path = os.path.join(output_dir, f"{image_prefix}_slice_{i:03d}.png")
        cv2.imwrite(output_path, grayscale_rgb)

    print(f"Superimposed images saved in {output_dir}")


def superimpose_masks_on_grayscale(grayscale_img_path, mask1_path, mask2_path, output_dir, mask1_color=(255, 0, 0), mask2_color=(0, 255, 0), overlap_color=(255, 255, 0), threshold=0.5, image_prefix="superimposed"):
    """
    Superimpose two binary masks on a grayscale image with distinct colors for masks and overlapping regions.

    Parameters:
    - grayscale_img_path: Path to the grayscale NIfTI image.
    - mask1_path: Path to the first binary mask NIfTI image.
    - mask2_path: Path to the second binary mask NIfTI image.
    - output_dir: Directory to save the superimposed images.
    - mask1_color: RGB color for the first mask (default is red).
    - mask2_color: RGB color for the second mask (default is green).
    - overlap_color: RGB color for overlapping regions (default is yellow).
    - threshold: Threshold to binarize the mask images (default is 0.5).
    - image_prefix: Prefix for the output image filenames.

    Output:
    - Superimposed images for each slice saved as PNG files in the output directory.
    """
    # Load grayscale image and normalize intensity
    grayscale_img = nib.load(grayscale_img_path).get_fdata()
    grayscale_img = ((grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min()) * 255).astype(np.uint8)

    # Load and binarize masks
    mask1 = nib.load(mask1_path).get_fdata()
    mask2 = nib.load(mask2_path).get_fdata()
    mask1 = (mask1 > threshold).astype(np.uint8)
    mask2 = (mask2 > threshold).astype(np.uint8)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop through each slice
    for i in range(grayscale_img.shape[2]):
        # Extract the slice from the grayscale image
        grayscale_slice = grayscale_img[:, :, i]

        # Convert grayscale slice to RGB
        grayscale_rgb = np.dstack([grayscale_slice] * 3)

        # Extract corresponding slices from masks
        mask1_slice = mask1[:, :, i]
        mask2_slice = mask2[:, :, i]

        # Create separate color layers for each mask
        mask1_layer = np.zeros_like(grayscale_rgb)
        mask2_layer = np.zeros_like(grayscale_rgb)

        # Apply colors to masks
        mask1_indices = np.where(mask1_slice > 0)
        mask2_indices = np.where(mask2_slice > 0)

        mask1_layer[mask1_indices] = mask1_color
        mask2_layer[mask2_indices] = mask2_color

        # Add mask layers to the grayscale image
        combined_image = cv2.addWeighted(grayscale_rgb, 1.0, mask1_layer, 0.5, 0)
        combined_image = cv2.addWeighted(combined_image, 1.0, mask2_layer, 0.5, 0)

        # Highlight overlapping regions
        overlap_indices = np.where((mask1_slice > 0) & (mask2_slice > 0))
        combined_image[overlap_indices] = overlap_color

        # Save the superimposed image as PNG
        output_path = os.path.join(output_dir, f"{image_prefix}_slice_{i:03d}.png")
        cv2.imwrite(output_path, combined_image)

    print(f"Superimposed images saved in {output_dir}")

def get_points_from_mask(mask):
    """Extract the indices of nonzero voxels from a 3D mask."""
    return np.array(np.nonzero(mask)).T  # Get indices of all nonzero points (as an Nx3 array)

def semi_hausdorff_distance_3d(mask_a, mask_b):
    """
    Compute the directed Hausdorff Distance from mask A to mask B in 3D.
    mask_a and mask_b are binary masks loaded from NIfTI files.
    """
    points_a = get_points_from_mask(mask_a)
    points_b = get_points_from_mask(mask_b)
    distances = cdist(points_a, points_b)  # Compute pairwise distances between all points
    min_distances = np.min(distances, axis=1)  # Find the shortest distance to B for each point in A
    return np.max(min_distances)  # Take the maximum of the shortest distances

def mean_directed_hausdorff_distance_3d(mask_a, mask_b):
    """
    Compute the Mean Directed Hausdorff Distance from mask A to mask B in 3D.
    """
    points_a = get_points_from_mask(mask_a)
    points_b = get_points_from_mask(mask_b)
    distances = cdist(points_a, points_b)
    min_distances = np.min(distances, axis=1)
    return np.mean(min_distances)


def binarymask_to_convexhull_mask(input_nii_path,output_nii_path):
    # Step 1: Load the input binary mask from a NIfTI file
    # input_nii_path = 'workinginput/ventricle.nii'
    binary_mask, affine, header = load_nii_mask(input_nii_path)

    # Step 2: Create 3D model from binary mask and save the STL file
    surface_mesh_stl = 'surface_model.stl'
    surface_mesh = create_3d_model_from_mask(binary_mask, surface_mesh_stl)

    # Step 3: Create convex hull from the 3D model and fix the normals
    convex_hull_stl = 'convex_hull_fixed_normals.stl'
    convex_hull_mesh = create_convex_hull_and_fix_normals(surface_mesh, convex_hull_stl)
    scale_mesh_fixed_center(convex_hull_stl, 'convex_hull_stl_1.stl', 1.05)
    # Step 4: Create binary mask from convex hull aligned with the original mask
    # convex_hull_binary_mask = create_binary_mask_from_hull(convex_hull_mesh, binary_mask.shape, affine)

    # # Step 5: Save the binary mask as a new NIfTI file
    # output_nii_path = 'convex_hull_binary_mask.nii'
    # save_nii_mask(convex_hull_binary_mask, affine, header, output_nii_path)
    #
    # print(f"Convex hull binary mask saved to: {output_nii_path}")

    convex_hull_mesh = trimesh.load('convex_hull_stl_1.stl') #'convex_hull_fixed_normals.stl')
    stl_to_binary_mask('convex_hull_stl_1.stl',input_nii_path, output_nii_path, binary_mask.shape)
def create_3d_model_from_mask(binary_mask, stl_filename):
    """
    Step 1: Create a 3D model (STL) from the binary mask using Marching Cubes
    """
    verts, faces, _, _ = marching_cubes(binary_mask, level=0) #measure.marching_cubes_lewiner(binary_mask, level=0) ##marching_cubes(binary_mask, level=0)

    # Create a trimesh object
    mesh = trimesh.Trimesh(vertices=verts, faces=faces)

    # Save the mesh as an STL file
    mesh.export(stl_filename)
    print(f"3D surface model saved as {stl_filename}")

    return mesh
def create_convex_hull_and_fix_normals(mesh, output_stl_filename):
    """
    Step 2: Compute the convex hull and ensure that all normals are pointing outwards.
    """
    # Create the convex hull of the mesh
    hull_mesh = mesh.convex_hull

    # Ensure normals are outward
    hull_mesh.fix_normals()

    # Save the convex hull mesh as an STL file
    hull_mesh.export(output_stl_filename)
    print(f"Convex hull with fixed normals saved as {output_stl_filename}")

    return hull_mesh
def scale_mesh_fixed_center(stl_filename, output_filename, scale_factor):
    """
    Scales a 3D mesh from an STL file, keeping the center fixed, and saves the scaled mesh as a new STL file.

    Parameters:
    - stl_filename: str, path to the input STL file.
    - output_filename: str, path to save the scaled STL file.
    - scale_factor: float or list of 3 floats (x, y, z scaling factors).
                    If a single float is provided, it scales uniformly in all directions.
    """
    # Load the STL file
    mesh = trimesh.load_mesh(stl_filename)

    # Find the centroid of the mesh
    centroid = mesh.centroid

    # Translate the mesh to the origin (centroid becomes [0, 0, 0])
    mesh.vertices -= centroid

    # Apply scaling to the mesh
    if isinstance(scale_factor, (float, int)):  # Uniform scaling
        mesh.apply_scale(scale_factor)
    elif isinstance(scale_factor, (list, tuple)) and len(scale_factor) == 3:  # Non-uniform scaling (x, y, z)
        mesh.vertices *= scale_factor
    else:
        raise ValueError("scale_factor must be a float (uniform scaling) or a list of 3 floats (x, y, z scaling).")

    # Translate the mesh back to its original position
    mesh.vertices += centroid

    # Save the scaled mesh as an STL file
    mesh.export(output_filename)
    print(f"Scaled mesh (with fixed center) saved as {output_filename}")
def stl_to_binary_mask(stl_filename,inputniftifilename, output_nifti_filename, volume_shape):
    """
    Converts an STL file to a binary mask and saves it as a NIfTI file (no affine required).

    Parameters:
    - stl_filename: str, path to the input STL file.
    - output_nifti_filename: str, path to save the binary mask as a NIfTI file.
    - volume_shape: tuple, shape of the output binary mask (e.g., (x, y, z)).
    """
    # Load the STL file
    inputniftifilename_nib=nib.load(inputniftifilename)
    mesh = trimesh.load_mesh(stl_filename)

    # Create an empty binary mask with the given volume shape
    binary_mask = np.zeros(volume_shape, dtype=bool)

    # Create a grid of voxel coordinates
    grid = np.indices(volume_shape).reshape(3, -1).T

    # Check which of the voxel grid coordinates are inside the mesh (assuming voxel size is 1 unit)
    inside = mesh.contains(grid)

    # Update the binary mask with the points that are inside the mesh
    binary_mask[tuple(grid[inside].T)] = 1

    # Save the binary mask as a NIfTI file
    nifti_img = nib.Nifti1Image(binary_mask.astype(np.uint8), affine=inputniftifilename_nib.affine,header=inputniftifilename_nib.header) #np.eye(4))  # Identity affine (default)
    nib.save(nifti_img, output_nifti_filename)

    print(f"Binary mask saved as {output_nifti_filename}")
def create_convex_hull_mask_3d(input_nii_path):
    """
    Create a 3D convex hull mask for a given binary mask.

    Parameters:
        binary_mask (numpy.ndarray): Input binary mask (3D).

    Returns:
        convex_hull_mask (numpy.ndarray): Convex hull mask (3D).
    """
    # Get the coordinates of non-zero points in the binary mask
    binary_mask, affine, header = load_nii_mask(input_nii_path)
    points = np.argwhere(binary_mask > 0)

    # Compute the 3D convex hull
    hull = ConvexHull(points)

    # Create an empty mask
    convex_hull_mask = np.zeros_like(binary_mask, dtype=np.uint8)

    # Fill the convex hull by iterating over simplices
    for simplex in hull.simplices:
        simplex_points = points[simplex]
        # Approximate a filled convex hull by marking the vertices in the mask
        for point in simplex_points:
            convex_hull_mask[tuple(point)] = 1

    return convex_hull_mask


def create_convex_hull_mask_filled_3d(input_nii_path,output_nifti_filename):
    """
    Create a 3D convex hull mask for a given binary mask and fill it.

    Parameters:
        binary_mask (numpy.ndarray): Input binary mask (3D).

    Returns:
        convex_hull_mask (numpy.ndarray): Filled convex hull mask (3D).
    """
    # Get the coordinates of non-zero points in the binary mask
    binary_mask, affine, header = load_nii_mask(input_nii_path)
    points = np.argwhere(binary_mask > 0)

    # Compute the 3D convex hull
    hull = ConvexHull(points)

    # Create a Delaunay triangulation for efficient point inclusion checks
    delaunay = Delaunay(points[hull.vertices])

    # Create a grid of all voxel indices in the binary mask
    x, y, z = np.indices(binary_mask.shape)

    # Flatten the grid into a list of points
    grid_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

    # Check which grid points are inside the convex hull
    inside_hull = delaunay.find_simplex(grid_points) >= 0

    # Create the convex hull mask
    convex_hull_mask = np.zeros_like(binary_mask, dtype=np.uint8)
    convex_hull_mask[x.ravel()[inside_hull], y.ravel()[inside_hull], z.ravel()[inside_hull]] = 1
    nifti_img = nib.Nifti1Image(convex_hull_mask.astype(np.uint8), affine=nib.load(input_nii_path).affine,header=nib.load(input_nii_path).header) #np.eye(4))  # Identity affine (default)
    nib.save(nifti_img, output_nifti_filename)
    return convex_hull_mask
