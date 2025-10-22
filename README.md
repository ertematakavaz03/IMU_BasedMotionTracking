# IMU Based Motion Tracking:
Contributors:
Ertem Ata Kavaz 
Şevval Ecenaz Çelik
Enes Coşkun 
Kağan Ali Korkmaz

# Overview:
This project demonstrates human activity recognition and orientation tracking using smartphone IMU sensors (accelerometer and gyroscope).
It includes three stages:

- **Activity Visualization** – Analyze and compare accelerometer patterns for sitting, standing, walking, and running.

- **Step Detection** – Count steps using signal filtering and adaptive peak detection.

- **Pose Estimation** – Estimate 3D orientation (roll, pitch, yaw) using a complementary filter that fuses accelerometer and gyroscope data.

All experiments were conducted using Phyphox app on an iPhone 11, with the device placed in the left pant pocket (screen facing outward).

# Part 1 – Data Visualization & Feature Inspection:
**Goal:** Visualize and interpret accelerometer signals for different human activities. 

**Run Command:** *python inspect_data.py --file data/walking.csv*

**Methodology:** 
- **Data Acquisition:** Accelerometer readings were collected using the Phyphox app for four activities — sitting, standing, walking, and running.
- **Data Processing:** Each CSV file (X, Y, Z axes) was read and combined to compute the total acceleration magnitude.
- **Signal Visualization:** Individual axis plots were created for each activity and combined magnitude plots were generated to observe rhythmic patterns.
- **Analysis:** The flatness, periodicity, and variance of the signal were compared across activities. Results were interpreted to show clear separations between static and dynamic actions.

**Outputs:** 
- **running_plot.png:** X–Y–Z axis data for running
- **running_combined_plot.png:** Combined acceleration magnitude for running
- **sitting_plot.png:** X–Y–Z axis data for sitting
- **sitting_combined_plot.png:** Combined acceleration magnitude for sitting
- **standing_plot.png:** X–Y–Z axis data for standing
- **standing_combined_plot.png:** Combined acceleration magnitude for standing
- **walking_plot.png:** X–Y–Z axis data for walking
- **walking_combined_plot.png:** Combined acceleration magnitude for walking

**Conclusion:** Sitting and standing show nearly flat signals (~9.8 m/s²), while walking introduces rhythmic oscillations and running shows high-amplitude, dense peaks (up to 70–80 m/s²). The distinct amplitude and frequency characteristics allow visual classification of human activity.


# Part 2 – Step Detection:
**Goal:** Detect and count steps from accelerometer magnitude using adaptive peak detection.

**Run Command:** *python main.py --file data/walking.csv*

**Methodology:** 
- **Data Loading:** The walking dataset was loaded through dataloader.py, extracting the X, Y, and Z acceleration components.
- **Signal Preprocessing:** A high-pass filter was applied to remove the gravity component, and a low-pass filter was used to suppress high-frequency noise.
- **Peak Detection:** The filtered magnitude signal was analyzed using peaks.py to identify local maxima that exceeded an adaptive threshold. Each detected peak represented one step.
- **Temporal Filtering:** A refractory period of approximately 350 ms was enforced to prevent false double-counting of steps.
- **Integration:** All detected step indices and timestamps were saved to a CSV file, while a visual representation of detected peaks was plotted for verification.

**Outputs:**
- **steps.csv:** Index and timestamp of each detected step
- **steps_detected.png:** Filtered signal with detected peaks marked in red

**Conclusion:** The implemented pipeline accurately detected step events using minimal computation. The combination of adaptive thresholding and noise-filtering provided a reliable step count even under small signal variations, making the method suitable for embedded IoT applications.


# Part 3 – Pose Estimation:
**Goal:** Estimate the device’s 3D orientation (roll, pitch, yaw) by fusing accelerometer and gyroscope data using a complementary filter.

**Run Command:** 

1) If the accelerometer and gyroscope data are saved separately, first merge them using:  *python modules/mergedata.py*

2) If you already have merged dataset:  *python main.py --file data/mergedWalk.csv --fs 100 --gyro-unit rad --alpha 0.98*


**Methodology:** 
- **Data Loading:** Accelerometer and gyroscope recordings were merged into mergedWalk.csv using mergedata.py, ensuring synchronized timestamps for accurate sensor fusion.
- **Preprocessing:** A low-pass filter was applied to the accelerometer data to smooth high-frequency noise and a high-pass filter was applied to the gyroscope data to reduce long-term drift.
- **Sensor Fusion:** The complementary filter was implemented in poseEstimator.py to blend the two data sources according to the formula:
  **θt ​= α(θt−1​+ωt​⋅Δt) + (1−α)at**​, where α = 0.98 controls the balance between gyroscope responsiveness and accelerometer stability.
- **Computation & Visualization** The calculated roll, pitch, and yaw angles were plotted over time. Optional animation scripts rendered 3D coordinate frames and a simplified human-body motion to visualize orientation changes.

**Outputs:**
- **orientation_output.csv:** Estimated roll, pitch, and yaw values over time
- **pose_plot.png** Visualization of orientation (roll & pitch curves)

There are also two animations simulating the motion that are provided in the IMU_MotionTracking.pdf:
- **pose_animation.mp4** 3D coordinate frame animation of the device: *https://drive.google.com/file/d/1o5XfhFY7EC1f9sqGGo1FjgBQki3KLVH1/view?usp=drive_link*
- **pose_human_animation.mp4** Simplified human motion synchronized with orientation angles:
- *https://drive.google.com/file/d/1hkkAtpc-g8JGnY1tZfutBhJKKY2XeFPf/view?usp=drive_link*

**Conclusion:** The complementary filter successfully combined accelerometer and gyroscope data to provide smooth, accurate, and drift-free orientation estimation. When accelerometer and gyroscope files are stored separately, merging them before processing ensures correct synchronization and reliable 3D pose tracking suitable for real-time IMU applications.
