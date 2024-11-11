import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# Directory containing the text files (replace with your actual directory path)
directory_path = "The path to the directory containing YOLOv8 prediction output text files."
output_directory = "The path to the directory where the analyzed results will be saved."
# Define the body part names
body_parts = ['head', 'thorax', 'abdomen', 'left_wing', 'right_wing']
min_threshold = 2  # Minimum frames for detecting behavior

def parse_predictions(file_path):
    with open(file_path, 'r') as f:
        predictions = []
        for line in f:
            elements = list(map(float, line.split()))
            label = int(elements[0])
            roi = elements[1:5]
            keypoints = np.array(elements[5:]).reshape(-1, 3)
            predictions.append((label, roi, keypoints))
    return predictions

def analyze_keypoints(predictions):
    results = {'Fly_m': [], 'Fly_F': []}
    for label, roi, keypoints in predictions:
        fly_type = "Fly_m" if label == 0 else "Fly_F"
        result = {body_parts[i]: keypoints[i] for i in range(len(body_parts))}
        results[fly_type].append(result)
    return results

def calculate_direction(keypoints):
    head = keypoints['head']
    thorax = keypoints['thorax']
    direction = np.arctan2(thorax[1] - head[1], thorax[0] - head[0])
    return direction

def calculate_speed(keypoints, prev_keypoints):
    dist = np.linalg.norm(keypoints['thorax'][:2] - prev_keypoints['thorax'][:2])
    return dist

def calculate_distance(keypoints1, keypoints2):
    dist = np.linalg.norm(keypoints1['thorax'][:2] - keypoints2['thorax'][:2])
    return dist

def detect_behaviors(results, min_threshold):
    pointing_towards = 0
    chasing = 0
    frame_count_towards = 0
    frame_count_chasing = 0
    total_frames = len(results['Fly_m'])
    distances = []

    for i in range(1, total_frames):  # Start from frame 1 to avoid index error
        male = results['Fly_m'][i]
        female = results['Fly_F'][i]
        prev_male = results['Fly_m'][i-1]
        prev_female = results['Fly_F'][i-1]

        male_direction = calculate_direction(male)
        female_direction = calculate_direction(female)
        male_speed = calculate_speed(male, prev_male)
        female_speed = calculate_speed(female, prev_female)
        distance = calculate_distance(male, female)
        distances.append(distance)

        # Check if they are pointing towards each other
        if np.abs(male_direction - female_direction) < np.pi / 2:
            frame_count_towards += 1
        else:
            if frame_count_towards >= min_threshold:
                pointing_towards += 1
            frame_count_towards = 0

        # Check if the male is chasing the female
        if np.abs(male_direction - female_direction) > np.pi / 2 and female_speed > male_speed:
            frame_count_chasing += 1
        else:
            if frame_count_chasing >= min_threshold:
                chasing += 1
            frame_count_chasing = 0

    average_distance = np.mean(distances)
    return pointing_towards, chasing, average_distance, distances

def save_to_csv(results, output_directory):
    for fly_type, data in results.items():
        file_path = os.path.join(output_directory, f"{fly_type}_data.csv")
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header
            header = ['frame', 'body_part', 'x', 'y', 'confidence']
            writer.writerow(header)
            for frame_index, frame_data in enumerate(data):
                for body_part, coords in frame_data.items():
                    row = [frame_index, body_part, coords[0], coords[1], coords[2]]
                    writer.writerow(row)

def visualize_data(distances, results, total_frames):
    male_directions = [calculate_direction(results['Fly_m'][i]) for i in range(1, total_frames)]
    female_directions = [calculate_direction(results['Fly_F'][i]) for i in range(1, total_frames)]

    plt.figure(figsize=(10, 5))

    plt.subplot(2, 1, 1)
    plt.plot(range(1, total_frames), male_directions, label='Male Fly Direction')
    plt.plot(range(1, total_frames), female_directions, label='Female Fly Direction')
    plt.xlabel('Frame')
    plt.ylabel('Direction (radians)')
    plt.legend()
    plt.title('Fly Directions Over Time')

    plt.subplot(2, 1, 2)
    plt.plot(range(1, total_frames), distances, label='Distance Between Flies')
    plt.xlabel('Frame')
    plt.ylabel('Distance')
    plt.legend()
    plt.title('Distance Between Flies Over Time')

    plt.tight_layout()
    plt.show()

def process_directory(directory_path, output_directory):
    all_results = {'Fly_m': [], 'Fly_F': []}
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            predictions = parse_predictions(file_path)
            analysis_results = analyze_keypoints(predictions)
            for fly_type in ['Fly_m', 'Fly_F']:
                all_results[fly_type].extend(analysis_results[fly_type])
    save_to_csv(all_results, output_directory)
    
    pointing_towards, chasing, average_distance, distances = detect_behaviors(all_results, min_threshold)
    total_frames = len(all_results['Fly_m'])
    print(f"Number of times pointing towards each other: {pointing_towards}")
    print(f"Duration of chasing behavior: {chasing} frames")
    print(f"Average distance between flies: {average_distance:.2f}")
    
    visualize_data(distances, all_results, total_frames)

def main():
    os.makedirs(output_directory, exist_ok=True)
    process_directory(directory_path, output_directory)

if __name__ == "__main__":
    main()
