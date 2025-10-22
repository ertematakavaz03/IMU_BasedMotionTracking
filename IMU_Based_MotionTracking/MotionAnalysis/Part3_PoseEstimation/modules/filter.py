# filter.py: Combining accelerometer and gyroscope data using a complementary filterto estimate orientation (for roll, pitch, and yaw) in degrees.
from math import atan2, sqrt, pi

# Helper function that ensures alpha value stays within [0-1] to maintain valid complementary filter weighting!
def alphaLimit(alpha: float) -> float:
    if alpha < 0.0: return 0.0
    if alpha > 1.0: return 1.0
    return alpha

# Helper function that converts radians to degrees!
def radToDegree(x: float) -> float:
    return x * 180.0 / pi

# Helper function that calculates roll and pitch angles (in degrees) using only accelerometer data!
def computeAccelTilt(xAccel: float, yAccel: float, zAccel: float):
    rollAccel  = atan2(yAccel, zAccel)                        
    pitchAccel = atan2(-xAccel, sqrt(yAccel*yAccel + zAccel*zAccel))    
    return radToDegree(rollAccel), radToDegree(pitchAccel)

# Main function: 
def combineIMUData(xAccel, yAccel, zAccel, xGyro, yGyro, zGyro, samplingRate: float, alpha: float = 0.98, gyroUnit: str = "rad", includeYAW: bool = False):
    
    # 1) Validating data length and sampling rate!
    sampleCount = min(len(xAccel), len(yAccel), len(zAccel), len(xGyro), len(yGyro), len(zGyro))
    if sampleCount == 0 or samplingRate <= 0:
        return ([] , []) if not includeYAW else ([], [], [])

    # 2) Normalizing parameters by...
    alpha = alphaLimit(alpha) # ..keeping alpha in [0,1]
    dt = 1.0 / float(samplingRate) # ..sample perios in seconds

    # 3) Converting gyro units to deg/s for the combination process for roll/pitch!
    if gyroUnit.lower().startswith("deg"):
        xGyroDegree = xGyro[:sampleCount]
        yGyroDegree = yGyro[:sampleCount]
        zGyroDegree = zGyro[:sampleCount]
    else:
        xGyroDegree = [g * 180.0 / pi for g in xGyro[:sampleCount]]
        yGyroDegree = [g * 180.0 / pi for g in yGyro[:sampleCount]]
        zGyroDegree = [g * 180.0 / pi for g in zGyro[:sampleCount]]
    
    # 4) Initializing angles (roll, pitch and partially yaw) using accelerometer
    rollInitial, pitchInitial = computeAccelTilt(xAccel[0], yAccel[0], zAccel[0])
    rollDegree  = [rollInitial]
    pitchDegree = [pitchInitial]
    yawDegree   = [0.0]  

    # 5) Iterating through all samples to: (1) integrate gyro for angle prediction, (2)compute instantaneous tilt from accelerometer, (3) combine them using filter equation
    for i in range(1, sampleCount):

        # 5.1) integrate gyro for angle prediction,
        rollGyro  = rollDegree[-1]  + xGyroDegree[i] * dt
        pitchGyro = pitchDegree[-1] + yGyroDegree[i] * dt
        yawGyro   = yawDegree[-1]   + zGyroDegree[i] * dt  

        # 5.2) compute instantaneous tilt from accelerometer,
        rollAccel, pitchAccel = computeAccelTilt(xAccel[i], yAccel[i], zAccel[i])

        # 5.3) combine (high-freq from gyro and low-freq from accel) with filter equation,
        rollTotal = alpha * rollGyro  + (1.0 - alpha) * rollAccel
        pitchTotal = alpha * pitchGyro + (1.0 - alpha) * pitchAccel

        # 5.4) append to output arrays!
        rollDegree.append(rollTotal)
        pitchDegree.append(pitchTotal)
        yawDegree.append(yawGyro)

    if includeYAW:
        return rollDegree, pitchDegree, yawDegree
    else:
        return rollDegree, pitchDegree
