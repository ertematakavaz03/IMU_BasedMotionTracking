# merge_imu.py: Merges accelerometer and gyroscope data into a single time-synchronized CSV file for further analysis.
import csv

ACC_PATH = "data/Accelerometer.csv"
GYR_PATH = "data/Gyroscope.csv"
OUT_PATH = "data/mergedWalk.csv"

# 1) Loading the Accelerometer Data:
accelTime, xAccel, yAccel, zAccel = [], [], [], []
with open(ACC_PATH, "r") as file:
    reader = csv.reader(file); head = next(reader)
    for row in reader:
        try:
            accelTime.append(float(row[0])) # Time (s)
            xAccel.append(float(row[1])) # X (m/s^2)
            yAccel.append(float(row[2])) # Y (m/s^2)
            zAccel.append(float(row[3])) # Z (m/s^2)
        except:
            continue


# 2) Loading the Gyroscope Data:
gyroTime, xGyro, yGyro, zGyro = [], [], [], []
with open(GYR_PATH, "r") as file:
    reader = csv.reader(file); head = next(reader)
    for row in reader:
        try:
            gyroTime.append(float(row[0])) # Time (s)
            xGyro.append(float(row[1])) # X (rad/s)
            yGyro.append(float(row[2])) # Y (rad/s)
            zGyro.append(float(row[3])) # Z (rad/s)
        except:
            continue


# 3) Syncing the record lengths and normalizing the time
sampleCount = min(len(accelTime), len(gyroTime), len(xAccel), len(xGyro))
startTime = accelTime[0] if sampleCount > 0 else 0.0
timestamp = [accelTime[i] - startTime for i in range(sampleCount)] # Normalize timestamps relative to the first accelerometer sample

# 4) Writing the Merged Dataset to CSV
with open(OUT_PATH, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "ax", "ay", "az", "gx", "gy", "gz"])
    for i in range(sampleCount):
        writer.writerow([f"{timestamp[i]:.6f}", xAccel[i], yAccel[i], zAccel[i], xGyro[i], yGyro[i], zGyro[i]])

print(f" Created {OUT_PATH} ({sampleCount} samples). Duration ~ {timestamp[-1]:.2f}s")