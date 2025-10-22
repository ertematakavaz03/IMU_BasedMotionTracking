# dataloader.py: Reads accelometer CSV data and computes the magnitude '√(x² + y² + z²)' for each row:
import csv, math

def loadMagnitude(csvPath):

    magnitudes = []

    # 1) Including filename as input and cleaning the headers
    with open(csvPath, "r", newline="") as csvFile:
        csvReader = csv.reader(csvFile)
        rawHeaders = next(csvReader)
        normalizedHeaders = [h.strip().lower() for h in rawHeaders]

        # 2) Finding the 'x', 'y', and 'z' columns:
        xColumnIndex = next(i for i,h in enumerate(normalizedHeaders) if 'x' in h)
        yColumnIndex = next(i for i,h in enumerate(normalizedHeaders) if 'y' in h)
        zColumnIndex = next(i for i,h in enumerate(normalizedHeaders) if 'z' in h)

        # 3) Reading line by line while calculating the vector magnitude of 'x', 'y', and 'z' values:
        for row in csvReader:
            try:
                xAcceleration = float(row[xColumnIndex]); yAcceleration = float(row[yColumnIndex]); zAcceleration = float(row[zColumnIndex])
                magnitudes.append(math.sqrt(xAcceleration*xAcceleration + yAcceleration*yAcceleration + zAcceleration*zAcceleration))
            
            except Exception:
                continue

    return magnitudes