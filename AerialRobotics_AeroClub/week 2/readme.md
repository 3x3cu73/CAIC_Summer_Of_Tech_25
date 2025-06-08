# 🚁 Week 2: Manual Control via Python in Webots

---

## 1. 🎯 Objectives 
- Develop a Python controller that issues direct motion commands to the quadrotor.
- Implement a predefined flight pattern (square) at a fixed altitude.
- Record and verify position data throughout the mission.

---

## 2. 🧭 Prerequisites
- Completion of Week 1 setup (Webots installation, Python virtual environment, mavic sample world).
- Active virtual environment with the Webots controller package installed.

---

## 3. 🚀 Concepts Covered
- ### Velocity vs. Position Control
 Understanding the difference between setting a target velocity (setVelocity) and commanding a target position (setPosition).


- ### Coordinate Frames
 Interpreting world-frame coordinates (X, Y, Z) and body-frame commands.


- ### Time-Stepped Control Loop
 Using Webots’ basic time step to regulate update frequency and ensure consistent control.


- ### Data Logging
 Capturing simulated sensor output or state estimates (e.g., GPS coordinates) to a CSV file for verification.



## 4. 📋 Tasks
- Load Week 2 World and copy mavic_2_pro.wbt into the week2/ directory.
- Ensure the controllers/ directory contains your Week 1 controller for reference.
- Implement Square Flight Controller


### 🔄 Create controllers/square_flight.py with the following behavior:
- Take off to 1 m altitude.
- Fly a square of side 1 m at constant speed.
- Return to the starting point.
- Land and disarm.


Use a time-stepped loop to:
- Read current position from the GPS or tracking node.
- Compute required velocity vector to reach the next waypoint.
- Issue setVelocity commands to the motors.
- Append timestamped position data to a CSV file.


### 🔧 Sample Code Skeleton
```bash 
from controller import Robot, Motor, InertialUnit, GPS, Gyro
import math

# Initialize robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Devices
imu = robot.getDevice("inertial unit")
imu.enable(timestep)

gps = robot.getDevice("gps")
gps.enable(timestep)

gyro = robot.getDevice("gyro")
gyro.enable(timestep)


# Motor setup (as in Week 1)
motors = []


# Parameters
altitude = 1.0
side_length = 1.0
speed = 0.5  # m/s
waypoints = [
    (0.0, 0.0),
    (side_length, 0.0),
    (side_length, side_length),
    (0.0, side_length),
    (0.0, 0.0)
]

# CSV logging setup
csv_file = open('position_log.csv', 'w', newline='')
logger = csv.writer(csv_file)
logger.writerow(['time', 'x', 'y', 'z'])

def set_lift(value):
    for m in motors:
        m.setVelocity(value)

# Take off


# Fly square


# Land


# Apply stabilization and control


supervisor.simulationQuit(0)
 (Note: adapt field updates to your controller API if needed.)
```

### Execution and Verification


- In Webots, assign square_flight.py as the controller for MAVIC_2_PRO.
- Press Run and observe the square trajectory at 1 m altitude.
- Confirm that position_log.csv records timestamped coordinates.

---

## 5. Expected Deliverables
- Controller Script: controllers/square_flight.py with in-code comments.
- Position Log: position_log.csv containing columns time, x, y, z.
- Demonstration Video: ≤2 minutes showing the executed square flight and landing.
- README Update: A section in week2/README.md summarizing your implementation approach and any observations.

---

## 6. 🎯 Bonus Challenge (Optional)
- Parameterization: Modify your controller to accept command-line arguments for side_length, altitude, and speed.
- Dynamic Waypoints: Read a list of waypoints from an external JSON file and execute them in sequence.

---

## 7. 📚 Resources
- Webots Python API Reference: https://cyberbotics.com/doc/reference/python-api
- Quadcopter Tutorial: https://cyberbotics.com/doc/guide/tutorial-8-drone
- CSV Module Documentation: https://docs.python.org/3/library/csv.html
- Webots Sample Worlds: Use additional sample worlds to test navigation in more complex environments.

---

## 8. SUBMISSION
- Submit your work through the google form attached below
- https://forms.office.com/Pages/ResponsePage.aspx?id=S1xNYsVFIkGM0ETw-E6UXcue0fDziu5KmhlObRm5LTlUM01KRjNWVUxIOEpTUUpVQzgyQ1FXQjhTNy4u

---
