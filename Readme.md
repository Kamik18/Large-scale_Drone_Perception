# Visual Slam - getting started document

To launch the visual slam system, ensure that the dependencies are installed.
These include:
- g2o-python
- opencv-python
- pillow
- pyopengl
- pygame

To launch the program, execute the following command on the command line
```
pipenv run python visual_slam.py path_to_directory_with_images
```

When the program is launched, it opens two windows.
The first window show the matches between the current and the previous frame.
The second window contains a 3D visualization of the camera locations and the reconstructed 3D points.

The window with the 3D visualization captures your mouse movements, and will not let you remove the mouse from its center.
To pause this behaviour press 'p'.
The camera placement can be altered using the keys: wsadqe
The camera orientation can be altered by moving the mouse.

To go to the next image press space.
To exit the program press escape.


## Running the program under Windows Subsystems for Linux (WSL)

To be able to run the program under Windows Subsystems for Linux (WSL), you 
need to install an X server on windows that supports xinput 2.

One option for this is the VcXsrv [https://sourceforge.net/projects/vcxsrv/].
After installing the X server, you need to let your WSL installation know the location of the X server.
This is achived by executing the following command in wsl.
	
```
export DISPLAY=$(ip route|awk '/^default/{print $3}'):0.0
```

You should now be able to launch the visual slam program as follows (assuming 
that your images are in the `input/frames_limited` directory.
```
pipenv run python visual_slam.py input/frames_limited/
```
