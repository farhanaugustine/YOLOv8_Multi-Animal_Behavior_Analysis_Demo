[![DOI](https://zenodo.org/badge/886500378.svg)](https://doi.org/10.5281/zenodo.14064613)
# Fly Behavior Analysis Using YOLOv8 Pose Estimation

|Multi-Animal Pose Estimations and Behavior Analysis|
|---|
|![Screenshot 2024-11-08 201406](https://github.com/user-attachments/assets/c834fd0c-2e0f-4d78-8937-e01d2186dd57)|



## Overview
This project utilizes YOLOv8 pose estimation to analyze the behavior of male and female flies in a video. The script processes the YOLOv8 model's prediction output, extracts keypoints, and analyzes the fly behavior. The behavior analysis includes detecting instances where flies point towards each other and when the male fly is chasing the female fly. The script also computes the average distance between flies and visualizes the orientation and distance over time.

## Directory Structure
### directory_path: The path to the directory containing YOLOv8 prediction output text files.

### output_directory: The path to the directory where the analyzed results will be saved.

### Body Part Definitions
The following body parts are analyzed:

`head`

`thorax`

`abdomen`

`left_wing`

`right_wing`

## Key Functions
parse_predictions(file_path)

1. Purpose: Parse the YOLOv8 prediction output text files.

2. Input: Path to a text file containing predictions.

3. Output: List of predictions with labels, regions of interest (ROI), and keypoints.

## analyze_keypoints(predictions)

1. Purpose: Categorize keypoints into male (Fly_m) and female (Fly_F) flies.

2. Input: List of predictions.

3. Output: Dictionary of keypoints categorized by fly type.

## calculate_direction(keypoints)

1. Purpose: Calculate the direction a fly is pointing based on its keypoints.

2. Input: Dictionary of keypoints.

3. Output: Direction in radians.

## calculate_speed(keypoints, prev_keypoints)

1. Purpose: Calculate the movement speed of a fly.

2. Input: Current and previous keypoints.

3. Output: Speed as a distance value.

## calculate_distance(keypoints1, keypoints2)

1. Purpose: Calculate the distance between two flies.

2. Input: Keypoints of two flies.

3. Output: Distance value.

## detect_behaviors(results, min_threshold)

1. Purpose: Detect behaviors such as pointing towards each other and chasing.

2. Input: Dictionary of results and minimum frame threshold for behaviors.

3. Output: Number of times flies point towards each other, duration of chasing behavior, average distance, and distances.

## save_to_csv(results, output_directory)

1. Purpose: Save the analyzed keypoints to CSV files.

2. Input: Dictionary of results and output directory path.

3. Output: CSV files for male and female flies.

## visualize_data(distances, results, total_frames)

1. Purpose: Visualize the orientation and distance of flies over time.

2. Input: List of distances, dictionary of results, and total number of frames.

3. Output: Visualization plots.

## process_directory(directory_path, output_directory)

1. Purpose: Process all prediction files in the specified directory and analyze behaviors.

2. Input: Directory paths for input and output.

3. Output: Analyzed results and visualizations.

## main()

1. Purpose: Main function to run the entire analysis pipeline.

2. Input: None.

3. Output: Processed results and visualizations.

# Usage
Set up directory paths:

```
directory_path = r"C:\Users\Farhan\Videos\Yolov8 MutliAnimal Poses\runs\pose\predict\labels"
output_directory = r"C:\Users\Farhan\Videos\Yolov8 MutliAnimal Poses\runs\pose\predict"
```
## Script Output
### CSV files containing keypoints data for male and female flies.

### Printed analysis results including the number of times flies point towards each other, the duration of chasing behavior, and the average distance between flies.

### Visualizations of fly directions and distances over time.

# Conclusion
This project provides a comprehensive analysis of fly behavior using YOLOv8 pose estimation. By categorizing keypoints, calculating directions and speeds, and detecting behaviors, this script helps in understanding the interactions between male and female flies. The visualizations further aid in interpreting the results, making this tool useful for behavioral studies and research.
