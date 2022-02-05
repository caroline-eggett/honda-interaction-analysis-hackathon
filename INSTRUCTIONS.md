# Instruction Documentation

## HOST Table
### Host Vehichle System States (CAN)
- Headlamp (cnt: 4)
- Wiper (cnt: 4)
- Turnsignal (cnt: 4)
- Transition State (N, P, D, R)
- Stability Control Status (Binary): keep you on course when steering
- Traction Control (cnt: 8 ?): keep traction between tires and road in sleepery/dangerous conditions

### Host Vehicle Kinematic State (CAN*)
- Brakestatus (Binary)
- ~~Global Positioning System (GPS) Speed* (cnt: 77,229): **figure out why so high**~~
- Yaw Rate (cnt: 210, 434): determines how fast you turn (degrees/s)
- Speed (cnt: 76, 015): m/s

### Host Vehicle Localization (GPS)
- Nothing

## SUMMARY Table

### DSRC & CAN Versioning
- Nothing

### System Outage Counts
- Nothing

### RvBSM Event Counts
- numnormalbsmrx (cnt: 342): number of recieved singals from remote vehicles

### Evt Warn Event Counts
- numwinforms (cnt: 7): count of informed warnings // definitely categorical

### SPaT Event Counts
- numshadowbsmrx (Binary): number of vehicles passed in front of host vehicle
- numspatrx (cnt: 1,135): number of received signals for intersetions passed for all vehicles
- numintersectionencounters (cnt: 17): number of received signals for intersections passed for host

### Trip Endpoints
- Difference b|t StartLocalTime and EndLocalTime
- Additional Columns for avg. mileage: Latitude and Longitude (use triangle theory)
