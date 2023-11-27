from arena import *

# this creates an object for scene 'example' at the given ARENA host
# scene = Scene(host="arenaxr.org", scene="example")
scene = Scene(host="localhost", scene="example")

# define a task that will add a box to the scene
@scene.run_once
def make_box():
    # Add a box at specific coordinates and adjust its properties
    box = Box(position=(0, 1, -3), scale=(1, 1, 1), color=(255, 0, 0),persist=True)
    scene.add_object(box)

# run the tasks defined for this scene
scene.run_tasks()
