import csv
import math
import matplotlib.pyplot as plt
import os
import shutil


def load_data(file_path):
    ax, ay, az = [], [], []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        headers = [h.strip().lower() for h in headers]

        # X, Y, Z kolonlarını bul
        x_idx = next((i for i, h in enumerate(headers) if 'x' in h), None)
        y_idx = next((i for i, h in enumerate(headers) if 'y' in h), None)
        z_idx = next((i for i, h in enumerate(headers) if 'z' in h and 'abs' not in h), None)

        if None in (x_idx, y_idx, z_idx):
            raise ValueError(f"Cannot find X/Y/Z columns in {file_path}. Found: {headers}")

        for row in reader:
            try:
                fx = float(row[x_idx])
                fy = float(row[y_idx])
                fz = float(row[z_idx])
                ax.append(fx)
                ay.append(fy)
                az.append(fz)
            except (ValueError, IndexError):
                continue

    # Magnitude (Amplitude)
    magnitude = [math.sqrt(x**2 + y**2 + z**2) for x, y, z in zip(ax, ay, az)]
    return ax, ay, az, magnitude


def plot_magnitude(name, magnitude):
    plt.figure(figsize=(10,4))
    plt.plot(magnitude[:1000], label="Amplitude (√x²+y²+z²)", color='black')
    plt.title(f"{name.capitalize()} - Acceleration Magnitude")
    plt.xlabel("Sample Index (Time)")
    plt.ylabel("Acceleration (m/s²)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{name}_plot.png")
    plt.close()


def plot_combined(name, ax, ay, az, magnitude):
    plt.figure(figsize=(10,5))
    plt.plot(ax[:1000], label='X-axis', alpha=0.7)
    plt.plot(ay[:1000], label='Y-axis', alpha=0.7)
    plt.plot(az[:1000], label='Z-axis', alpha=0.7)
    plt.plot(magnitude[:1000], label='Amplitude', color='black', linewidth=2)
    plt.title(f"{name.capitalize()} - X, Y, Z and Total Acceleration")
    plt.xlabel("Sample Index (Time)")
    plt.ylabel("Acceleration (m/s²)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{name}_combined_plot.png")
    plt.close()


def compute_stats(data):
    n = len(data)
    mean = sum(data)/n
    var = sum((x - mean)**2 for x in data)/n
    std = math.sqrt(var)
    return mean, std, max(data), min(data)


activities = ["standing", "sitting", "walking", "running"]

for act in activities:
    file_path = f"data/{act}.csv"
    ax, ay, az, magnitude = load_data(file_path)

    plot_magnitude(act, magnitude)
    plot_combined(act, ax, ay, az, magnitude)

    mean, std, maxv, minv = compute_stats(magnitude)
    print(f"{act}: mean={mean:.2f}, std={std:.2f}, max={maxv:.2f}, min={minv:.2f}")

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

for file in os.listdir():
    if file.endswith(".png"):
        shutil.move(file, os.path.join(output_dir, file))

print(f"\n All plots have moved to '{output_dir}/' successfully.")
