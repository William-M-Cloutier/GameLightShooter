# GameLightShooter
Repository for my game that uses light sensor triangulation data to control the player characters

Game mechanics itself was made using python and the turtle library. An Ardunio was in charge of IO for the photoresistors.
There are three photoresistors in the following configuration:
*
|
|
|
|
*------------*

Where the * represents a photoresistor. These photoresistors were connected to a breadboard, which then connected them to the Arduino.
The spacing and location for the photoresistors was chosen to mimic the video game arena, which is rectangular, as closely as possible.

To play a game, a light is shined on a table that houses the photoresistor.
The data from the photoresistors are collected by the Arduino and sent to the python script. 
The python script would then use triangulation to determine the coordinates of where the light was shined. 
From here, the python script would send these coordinates to the video game logic where they would be mapped to the video game arena appropriately.
The code calibrates the photoresistors to ensure natural lighting does not interfere with game mechanics.
Threshold values for calibration can be altered accordingly within code. 

The game itself is a two-player game where one player must build blocks to defend their homebases while the other player must shoot the defender's homebase.
The defender wins if the timer runs out, the attacker wins if all three homebases are destroyed.

The arena is divided up into vertical halves, where the top half is the defender and the other half is the attacker. 
Current implementation is meant for players to quickly flash lights on and off to control their character. 
A player's character will move to the spot where the light was flashed and will either build a defensive block or shoot a bullet is possible. 


