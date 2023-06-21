import cv2
import numpy as np
import csv
import pywavefront

print("Hello World")
def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames



def find_correspondences(image1, image2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Initialize feature detector and descriptor
    sift = cv2.SIFT_create()
    
    # Detect and compute keypoints and descriptors
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)
    
    # Initialize matcher
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    
    # Match keypoints
    matches = matcher.match(descriptors1, descriptors2)
    
    # Filter matches based on a distance threshold
    distance_threshold = 0.75
    good_matches = [match for match in matches if match.distance < distance_threshold * match.distance]
    
    # Extract corresponding points
    points1 = np.float32([keypoints1[match.queryIdx].pt for match in good_matches])
    points2 = np.float32([keypoints2[match.trainIdx].pt for match in good_matches])
    
    return points1, points2


def calculate_disparity_map(image1, image2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Initialize stereo block matching
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    
    # Compute disparity map
    disparity = stereo.compute(gray1, gray2)
    
    return disparity


def reconstruct_3d_points(disparity_map):
    # Define camera parameters
    focal_length = 1000.0  # Example focal length (adjust according to your setup)
    baseline = 0.1        # Example baseline distance (adjust according to your setup)
    
    # Calculate depth from disparity map
    depth = baseline * focal_length / (disparity_map + 1e-6)
    
    # Generate 3D point cloud
    height, width = disparity_map.shape[:2]
    u, v = np.meshgrid(np.arange(width), np.arange(height))
    points_3d = np.stack([u, v, depth], axis=-1)
    
    return points_3d

def export_points_to_obj(points_3d, output_path):
    scene = pywavefront.Wavefront()
    for point in points_3d:
        x, y, z = point
        scene.vertices.append((x, y, z))
    
    scene.save(output_path)
print("ok")