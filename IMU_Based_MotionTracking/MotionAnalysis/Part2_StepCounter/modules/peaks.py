# peaks.py: Detects step peaks from filtered acceleration signals using a custom local-maximum method with adaptive thresholding and refractory gap control:
from typing import List

# 1) Computing a dynamic threshold:
def dynamicTreshold(signalMagnitude: List[float], tresholdSensitivity: float = 0.8) -> float:
    if not signalMagnitude:
        return 0.0
    
    # 1.1) Calculating the total number of samples and their average value
    sampleCount = float(len(signalMagnitude))
    avgValue = sum(signalMagnitude) / sampleCount

    # 1.2) Calculating the variance and standard deviation
    variance = sum((x - avgValue) * (x - avgValue) for x in signalMagnitude) / max(1.0, (sampleCount - 1.0))
    standardDeviation = variance ** 0.5

    # 1.3) Computing the adaptive treshold
    return avgValue + tresholdSensitivity * standardDeviation


# 2) Finding local maxima above the threshold while enforcing a refractory gap to prevent double counting.
def peakDetection(signalMagnitude: List[float], threshold: float, minGapDistance: int) -> List[int]:
    
    # 2.1) Validating input and ensure a minimum gap value:
    sampleCount = len(signalMagnitude)
    if sampleCount < 3:
        return []

    if minGapDistance < 1:
        minGapDistance = 1

    # 2.2) Initialize peak list and the last accepted peak idx:
    peaks: List[int] = []

    # initialize to negative infinity so the first detected peak is always accepted
    lastPeak = -float('inf') 

    # 2.3) Main iteration through signal, excluding first and last signals:
    for i in range(1, sampleCount - 1):
        prevVal = signalMagnitude[i - 1]
        currVal = signalMagnitude[i]
        nextVal = signalMagnitude[i + 1]

        # 2.4) Checking for local maximum that are above the treshold:
        if prevVal < currVal >= nextVal and currVal > threshold:
            
            # 2.5) Applying of refractory rule, accepting only if far enough from the last peak
            if i - lastPeak >= minGapDistance:
                peaks.append(i)
                lastPeak = i
    return peaks



# 3) Merging closely spaced peaks, keeping the stronger one to handle twin-peak artifacts.
def peakDetectionWithMerge(signalMagnitude: List[float], threshold: float, minGapDistance: int) -> List[int]:
    
    # 3.1) Collecting all local maxima above the threshold!
    candidateIndex: List[int] = []
    n = len(signalMagnitude)
    for i in range(1, n - 1):
        if signalMagnitude[i - 1] < signalMagnitude[i] >= signalMagnitude[i + 1] and signalMagnitude[i] > threshold:
            candidateIndex.append(i)
    if not candidateIndex:
        return []

    # 3.2) Merging the peaks that are too close, then keeping the stronger one!
    mergedPeaks: List[int] = [candidateIndex[0]]
    for currentIndex in candidateIndex[1:]:
        
        if currentIndex - mergedPeaks[-1] < minGapDistance:
            if signalMagnitude[currentIndex] > signalMagnitude[mergedPeaks[-1]]:
                mergedPeaks[-1] = currentIndex
        
        else:
            mergedPeaks.append(currentIndex)
    return mergedPeaks
