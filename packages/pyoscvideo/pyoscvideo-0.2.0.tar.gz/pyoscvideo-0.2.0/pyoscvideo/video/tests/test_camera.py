from pyoscvideo.video.camera import Camera
import time


def test_basic_image_update():
    camera = Camera(0, 25)
    for i in range(1000):
        time.sleep(0.001)
    print(camera.model.frame_counter)
    camera.cleanup()


test_basic_image_update()
