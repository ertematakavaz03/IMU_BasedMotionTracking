# dataloader.py: Loading Inertial Measurement Unit data from a CSV file, separating accelerometer and gyroscope readings for further signal processing.
import csv

def load_imu(file_path):
    timestamp, xAccel, yAccel, zAccel, xGyro, yGyro, zGyro = [], [], [], [], [], [], []

    # 1) Opening the CSV file for reading!
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  
        
        # 2) Iterating through each row in the CSV!
        for row in reader:
            if not row:
                continue
            try:
                # 3) Converting each sensor reading to float and storing them!
                timestamp.append(float(row[0]))
                xAccel.append(float(row[1]))
                yAccel.append(float(row[2]))
                zAccel.append(float(row[3]))
                xGyro.append(float(row[4]))
                yGyro.append(float(row[5]))
                zGyro.append(float(row[6]))
            
            except ValueError:
                continue

    return timestamp, xAccel, yAccel, zAccel, xGyro, yGyro, zGyro