# https://github.com/NVIDIA-AI-IOT/jetcam/blob/master/jetcam/csi_camera.py

from jetcam.csi_camera import Camera
import traitlets
import cv2
import atexit

class MyCamera(Camera):
    
    capture_device = traitlets.Integer(default_value=0)
    capture_fps = traitlets.Integer(default_value=30)
    capture_width = traitlets.Integer(default_value=640)
    capture_height = traitlets.Integer(default_value=480)
    
    def __init__(self, *args, **kwargs):
        super(MyCamera, self).__init__(*args, **kwargs)
        try:
            self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)

            re, image = self.cap.read()

            if not re:
                raise RuntimeError('Could not read image from camera.')
        except:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.cap.release)
    
    def _read(self):
        re, image = self.cap.read()
        if re:
            return image
        else:
            raise RuntimeError('Could not read image from camera')

    def _gst_str(self):
        gstTemplate = 'nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'
        
        return gstTemplate % (
                self.capture_device, 
                self.capture_fps,    
                self.capture_width, 
                self.capture_height)
    
    def release(self):
        self.cap.release()
        self.cap = None
        
    def read_image(self):
        return transform_image(self.read())

def transform_image(image):
    return image.flatten().tobytes()
    
def update_image(image_widget, change):
    image = transform_image(change['new'])
    image_widget.value = image