from arena import *

# this creates an object for scene 'example' at the given ARENA host
# scene = Scene(host="arenaxr.org", scene="example")
scene = Scene(host="localhost", scene="example")

# define a task that will add a box to the scene
@scene.run_once
def make_box():
    # Add a box at specific coordinates and adjust its properties

    obj = Model(object_id="duck_1", position=(-1, 1, -3), url="store/models/Nessiekun.glb", persist=False)
    scene.add_object(obj)

# run the tasks defined for this scene
scene.run_tasks()
