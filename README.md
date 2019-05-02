# delta_robot
Integrated delta robot code

Overall structure of code:

START
1) Vision
  - Move delta robot to place not blocking camera
  - Run vision code
    - See what toppings we can distinguish
    - See where they are
    - See where pizza is
  - Decide what toppings we want to put on pizza
  - For 1st topping in list of toppings:
    - Path plan, get coordinates
    - Pass these coordinates (x, y, z) as "goal" to IK

2) Inverse kinematics
  - Take in (x, y, z) goal coords
  - Solve desired thetas
  - Pass (theta1, theta2, theta3) to Odrives

3) Odrives
  - Move motors to goal thetas
  - Check that end-effector is at correct location after moving
 
4) Pneumatics
  - Once odrives are done, start pumping (blow up balloon)
  - Done pumping
  - Move down to preset z for picking up topping (reverse pumping)
  - Move up to preset z, move to x-y of pizza hole
  - Pump a little again to drop topping
  - Go back to run vision code again
  
5) Repeat x times until all the pizza is full with at least 1 of each topping

6) Move to pick up salt shaker and shake

7) Push pizza off to mobile robot

8) Flatten play-doh

END
