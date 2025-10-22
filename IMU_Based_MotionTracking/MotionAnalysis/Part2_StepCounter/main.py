# main.py: Running part of the Part 2 and saves all results in /outputs folder!
import argparse
import os
import csv
import matplotlib.pyplot as plt

# Local Imports:
from modules.stepcounter import processFile

def main():
    # 1) Parsing of the command-line arguments!
    ap = argparse.ArgumentParser(description="Offline Step Counter (Part 2)")
    ap.add_argument("--file", required=True, help="Path to walking.csv file")
    ap.add_argument("--fs", type=int, default=50, help="Sampling rate (Hz)")
    ap.add_argument("--threshold", default="auto",
                    help="Threshold value or 'auto' (mean + k*std)")
    ap.add_argument("--k-auto", type=float, default=0.8,
                    help="Multiplier for auto threshold (default=0.8)")
    ap.add_argument("--min-gap-ms", type=int, default=350,
                    help="Minimum gap between peaks in ms (default=350)")
    ap.add_argument("--plot", action="store_true",
                    help="If set, saves steps_detected.png in outputs/ folder")
    args = ap.parse_args()

    # 2) Executing of the full step counting pipeline!
    result = processFile(
        csvPath=args.file,
        samplingFrequency=args.fs,
        thresholdMode=args.threshold,
        sensitivityFactor=args.k_auto,
        minGapMiliseconds=args.min_gap_ms,
    )

    # 3) Creating of the output directory
    os.makedirs("outputs", exist_ok=True)

    # 4) Saving of detected step data as steps.csv
    steps_csv_path = os.path.join("outputs", "steps.csv")
    with open(steps_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step_index", "time_s"])
        for idx in result["peaks"]:
            t = idx / args.fs if args.fs > 0 else idx
            writer.writerow([idx, f"{t:.3f}"])
    print(f" Saved: {steps_csv_path}")

    # 5) Plotting and saving of the filtered signal and detected steps!
    if args.plot and result["signal"]:
        plt.figure(figsize=(10, 4))
        plt.plot(result["signal"], label="Filtered Signal", linewidth=1)
        plt.axhline(result["threshold"], color="green", linestyle="--",
                    label=f"Threshold ({result['threshold']:.2f})")
        if result["peaks"]:
            plt.scatter(result["peaks"],
                        [result["signal"][i] for i in result["peaks"]],
                        color="red", s=20, label="Detected Steps")
        plt.title("Step Detection Result")
        plt.xlabel("Sample Index")
        plt.ylabel("Magnitude (filtered)")
        plt.legend()
        plt.tight_layout()
        plt.savefig("outputs/steps_detected.png", dpi=160)
        plt.close()
        print(" Saved: outputs/steps_detected.png")

    # ---- Print summary ----
    print("\n********** Step Count Summary **********")
    print(f"File              : {args.file}")
    print(f"Sampling Rate (fs): {args.fs} Hz")
    print(f"Threshold used    : {result['threshold']:.2f}")
    print(f"Steps Detected    : {result['steps']}")
    
    if result["cadence_spm"] is not None:
        print(f"Mean Cadence      : {result['cadence_spm']:.1f} steps/min")
    
    else:
        print("Mean Cadence      : (fs not provided)")
    print("========================================\n")

if __name__ == "__main__":
    main()
