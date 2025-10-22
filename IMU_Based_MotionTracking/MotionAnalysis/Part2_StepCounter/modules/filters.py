# filters.py: Processes accelerometer magnitudes with custom high-pass and low-pass filters to isolate step-related motion:
from typing import List, Optional

# 1) Sliding Window mechanism that computes a moving average:
def movingAvg(signalValues: List[float], windowLength: int) -> List[float]:
    if not signalValues or windowLength <= 1:
        return signalValues[:]
    smoothedSignal, sumWindow = [], 0.0
    buffer = []
    for v in signalValues:
        buffer.append(v); sumWindow += v
        if len(buffer) > windowLength:
            sumWindow -= buffer.pop(0)
        smoothedSignal.append(sumWindow / len(buffer))
    return smoothedSignal

# 2) High Pass filter, removing the slow gravity signals to highlight walking motion:
def highpassGravityRemoval(magnitude: List[float], fs: Optional[int] = None) -> List[float]:
    windowLength = int(fs * 1.0) if (fs and fs > 0) else 25
    gravityTrend = movingAvg(magnitude, windowLength)
    return [rawAcceleration - gravityEstimate for rawAcceleration, gravityEstimate in zip(magnitude, gravityTrend)]


# 3) Low Pass Filter, smoothing the high frequency noise signals to highlight clearer step patterns:
def lowpassSmoother(filteredSignals: List[float], samplingFrequency: Optional[int] = None) -> List[float]:
    if samplingFrequency and samplingFrequency > 0:
        windowLength = int(samplingFrequency * 0.25)
    else:
        windowLength = 5

    return movingAvg(filteredSignals, max(1, windowLength))


# 4) Combining both the filters:
def preprocessSteps(magnitude: List[float], samplingFrequency: Optional[int] = None) -> List[float]:
    return lowpassSmoother(highpassGravityRemoval(magnitude, fs=samplingFrequency), samplingFrequency=samplingFrequency)