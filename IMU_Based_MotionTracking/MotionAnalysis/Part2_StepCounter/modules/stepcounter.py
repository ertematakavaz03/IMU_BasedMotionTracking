# stepcounter.py: Processes filtered accelerometer magnitudes to detect step peaks and compute walking metrics.
from typing import Dict, Optional, List

# Local Imports:
from modules.dataloader import loadMagnitude
from modules.filters import preprocessSteps
from modules.peaks import dynamicTreshold, peakDetection

def processFile(csvPath: str, samplingFrequency: Optional[int] = None, thresholdMode: str | float = "auto", sensitivityFactor: float = 0.8, minGapMiliseconds: int = 350,) -> Dict[str, object]:

    # 1) Loading of the accelometer magnitude data from the CSV file!
    mag: List[float] = loadMagnitude(csvPath)
    if not mag:
        return {
            "signal": [],
            "threshold": 0.0,
            "peaks": [],
            "steps": 0,
            "fs": samplingFrequency,
            "duration_s": None,
            "cadence_spm": None,
        }

    # 2) Applying of High pass (gravity removal) and Low pass (noise smoothing)!
    filteredSignal: List[float] = preprocessSteps(mag, samplingFrequency=samplingFrequency)

    # 3) Determining the threshold mode, automatic or fixed!
    if isinstance(thresholdMode, str) and thresholdMode.lower() == "auto":
        thresholdLevel = float(dynamicTreshold(filteredSignal, tresholdSensitivity=sensitivityFactor))
    else:
        thresholdLevel = float(thresholdMode)

    # 4) Converting of refractory gap from ms to samples!
    if samplingFrequency and samplingFrequency > 0:
        minPeakDistance = max(1, int(samplingFrequency * (minGapMiliseconds / 1000.0)))
    else:
        minPeakDistance = 15 # If sampling frequency is unknown then use a conservative default, which is around 15 samples

    # 5) Detecting of step peaks that are above the threshold!
    detectedPeaks = peakDetection(filteredSignal, thresholdLevel, minPeakDistance)
    stepCount = len(detectedPeaks)

    # 6) Calculating of total duration in seconds and cadence in steps per minute!
    if samplingFrequency and samplingFrequency > 0:
        durationSeconds = len(filteredSignal) / samplingFrequency
    else:
        durationSeconds = None

    if durationSeconds and durationSeconds > 0:
        cadenceSPM = (stepCount / durationSeconds) * 60.0
    else:
        cadenceSPM = None

    # 7) Returning of all computed results in dict. format!
    return {
        "signal": filteredSignal,
        "threshold": thresholdLevel,
        "peaks": detectedPeaks,
        "steps": stepCount,
        "fs": samplingFrequency,
        "duration_s": durationSeconds,
        "cadence_spm": cadenceSPM,
    }
