



## Overview
This repository contains my laboratory assignments for the CSE423 Computer Graphics course. The projects are implemented in Python using the PyOpenGL library, focusing on both 2D and 3D computer graphics principles, ranging from basic primitive rendering to complex 3D transformations, interactive gameplay, and algorithmic drawing techniques. 

## Technologies Used
**Language:** Python 
**Graphics Library:** PyOpenGL / OpenGL 
**Core Concepts:** 2D/3D Transformations, Midpoint Line Drawing Algorithm, Collision Detection (AABB), Perspective Projection, Delta Timing 

---

### Assignment 1: Introduction to OpenGL Primitives 
This assignment focuses on utilizing basic OpenGL primitives (`GL_POINTS`, `GL_LINES`, `GL_TRIANGLES`) to construct and animate 2D objects.

* **Task 1 - Building a House in Rainfall:**
  * Designed a 2D house with animated raindrops falling from top to bottom.
  * Implemented keyboard interactions: Left/Right arrows bend the direction of the rainfall.
  * Added day/night simulation keys that dynamically change the background and object visibility.
* **Task 2 - Building the Amazing Box:**
  * Right-clicking generates random, continuously moving points that bounce off the boundary walls.
  * Up/Down arrow keys control the speed of all generated points.
  * Left-clicking causes the points to blink (toggling between their original color and the background color).
  * Spacebar acts as a global freeze/unfreeze toggle for all animations.

### Assignment 2: Midpoint Line Drawing Algorithm - "Catch the Diamonds!" 
A fully functional 2D arcade game built strictly using the Midpoint Line Drawing Algorithm (only `GL_POINTS` primitive allowed).

* **Gameplay Mechanics:**
  * Control a catcher bowl at the bottom of the screen using the Left/Right arrow keys to catch falling diamonds[cite: 287].
  * [cite_start]Missing a diamond ends the game, turning the catcher red and freezing the screen[cite: 294, 295].
  * [cite_start]The game difficulty ramps up progressively as the falling speed of the diamonds increases over time[cite: 297].
* **Technical Highlights:**
  * [cite_start]Implemented the Midpoint Line Drawing algorithm to draw lines across all 8 zones by exploiting eight-way symmetry[cite: 187, 188].
  * [cite_start]Used Axis-Aligned Bounding Box (AABB) detection for collision logic between the catcher and the diamonds[cite: 327, 329].
  * [cite_start]Integrated real-time delta timing (Δt) to ensure consistent movement speeds regardless of hardware frame rates[cite: 345].
  * [cite_start]Built interactive on-screen UI buttons (Restart, Play/Pause, Terminate) drawn entirely with midpoint lines[cite: 298, 300, 305, 308].

### [cite_start]Assignment 3: 3D Transformations & Projections - "Bullet Frenzy" [cite: 42, 119]
[cite_start]A 3D first/third-person shooter game introducing complex 3D graphics concepts like translation, rotation, scaling, and perspective projection[cite: 47, 54, 121].

* **Gameplay Mechanics:**
  * [cite_start]Navigate a 3D grid and shoot expanding/shrinking spherical enemies that continuously track the player[cite: 122, 160, 162].
  * [cite_start]The game ends if the player's life hits zero (upon enemy contact) or if 10 bullets are missed[cite: 153, 154]. [cite_start]Hit enemies dynamically respawn[cite: 161].
* **Technical Highlights:**
  * [cite_start]Applied transformation matrices (`glTranslatef`, `glRotatef`, `glScalef`) to manipulate the gun, bullets, and enemies in 3D space[cite: 49, 50, 51, 61].
  * [cite_start]Implemented Perspective Projection using `gluPerspective` to create a realistic view frustum[cite: 54, 55, 103].
  * [cite_start]Created dynamic camera controls utilizing `gluLookAt` to toggle between first-person and third-person perspectives via right-click[cite: 56, 145].
  * [cite_start]Developed a "Cheat Mode" (toggled with 'C') that automatically detects enemy line-of-sight, auto-rotates the gun, and fires[cite: 148].
