from typing import Dict, Optional
import os
import csv
import matplotlib.pyplot as plt

# Local Imports:
from modules.dataloader import load_imu        
from modules.filter import combineIMUData  

def estimate_pose(csvPath: str, sampleRate: int, gyroUnit: str = "rad", alpha: float = 0.98, outputDir: str = "outputs", plot: bool = True) -> Dict[str, object]:
    
    # 1) Loading IMU data from the CSV!
    timestamps, xAccel, yAccel, zAccel, xGyro, yGyro, zGyro = load_imu(csvPath)
    
    # 1.1) Aligning data by taking the minimum valid sample length across all channels
    sampleCount = min(len(timestamps), len(xAccel), len(yAccel), len(zAccel), len(xGyro), len(yGyro), len(zGyro))
    
    # 1.2) Checking for empty data or invalid sampling frequency
    if sampleCount == 0 or sampleRate <= 0:
        raise ValueError("Empty data or fs <= 0. Check file and arguments.")

    # 2) Running the complementary filter to estimate roll and pitch, in degrees!
    rollDegree, pitchDegree = combineIMUData(xAccel[:sampleCount], yAccel[:sampleCount], zAccel[:sampleCount], xGyro[:sampleCount], yGyro[:sampleCount], zGyro[:sampleCount], samplingRate=sampleRate, alpha=alpha, gyroUnit=gyroUnit, includeYAW=False)

    # 3) Creating output directory and saving orientation data to CSV!
    os.makedirs(outputDir, exist_ok=True)
    csvPath = os.path.join(outputDir, "orientation_output.csv")
    with open(csvPath, "w", newline="") as file:
        w = csv.writer(file)
        w.writerow(["time_s", "roll_deg", "pitch_deg"])
        for i in range(sampleCount):
            w.writerow([f"{timestamps[i]:.6f}", f"{rollDegree[i]:.4f}", f"{pitchDegree[i]:.4f}"])

    # 4) Plotting a PNG that shows roll and pitch over time!
    plotPath: Optional[str] = None
    if plot:
        plotPath = os.path.join(outputDir, "pose_plot.png")
        plt.figure(figsize=(10, 4))
        plt.plot(timestamps[:sampleCount], rollDegree, label="Roll (deg)")
        plt.plot(timestamps[:sampleCount], pitchDegree, label="Pitch (deg)")
        plt.title("Orientation (Complementary Filter)")
        plt.xlabel("Time (s)")
        plt.ylabel("Angle (deg)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(plotPath, dpi=160)
        plt.close()


    return {
        "time_s": timestamps[:sampleCount],
        "roll_deg": rollDegree,
        "pitch_deg": pitchDegree,
        "alpha": alpha,
        "fs": sampleRate,
        "gyro_unit": gyroUnit,
        "csv_path": csvPath,
        "plot_path": plotPath,
    }
