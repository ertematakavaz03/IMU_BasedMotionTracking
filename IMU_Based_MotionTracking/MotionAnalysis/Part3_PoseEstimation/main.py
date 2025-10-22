# main.py:
# python main.py --file data/mergedWalk.csv --fs 100 --gyro-unit rad --alpha 0.98
import argparse

# Local Imports:
from modules.poseEstimator import estimate_pose

def main():

    # 1) Creating argument parser for command-line interface!
    parser = argparse.ArgumentParser(description="Pose Estimation (with plot)")
    
    # 1.1) Adding required and optional arguments for user input!
    parser.add_argument("--file", required=True, help="Path to merged IMU CSV (e.g., data/mergedWalk.csv)")
    parser.add_argument("--fs", type=int, required=True, help="Sampling rate in Hz (e.g., 100)")
    parser.add_argument("--gyro-unit", default="rad", help="Gyro unit: 'rad' or 'deg' (default: rad)")
    parser.add_argument("--alpha", type=float, default=0.98, help="Complementary filter alpha (default=0.98)")
    
    # 1.2) Parsing command-line arguments!
    args = parser.parse_args()

    # 2) Calling the main pose estimation function with parsed arguments!
    res = estimate_pose(
        csvPath=args.file,
        sampleRate=args.fs,
        gyroUnit=args.gyro_unit,
        alpha=args.alpha,
        outputDir="outputs",
        plot=True
    )

    print("\n========== Pose Estimation Summary ==========")
    print(f"File          : {args.file}")
    print(f"Sampling Rate : {args.fs} Hz")
    print(f"Gyro Unit     : {args.gyro_unit}")
    print(f"Alpha (α)     : {args.alpha}")
    print(f"Output CSV    : {res['csv_path']}")
    print(f"Output Plot   : {res['plot_path']}")
    print("=============================================\n")

if __name__ == "__main__":
    main()
