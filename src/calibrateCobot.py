from cartesian_acquisition import CobotCalibrator, getRTMatrix

if __name__ == '__main__':
    calibrator = CobotCalibrator(callback)
    calibrator.calibrateCobot()
    
