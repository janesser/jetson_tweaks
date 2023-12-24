import abc
import typing
import datetime

class CameraDriver(abc.ABC):
    '''CameraDriver provides real-time or recorded images'''    

    @abc.abstractmethod
    def register(
        self, 
        observer: typing.Callable[[typing.Sequence[int], datetime.datetime], None], 
        transform: typing.Callable[[typing.Sequence[int]], typing.Sequence[int]]
    ):
        ...
        
    @abc.abstractmethod
    def release():
        ...

class CsiCameraDriver(CameraDriver):

    def __init__(self, width, height, deviceId):
        from jetcam.csi_camera import CSICamera        
        self.camera = CSICamera(width=width, height=height, capture_device=deviceId)
        
    def register(self, observer, transform):
        def obs(change):
            raw_image = change['new']
            transformed_image = transform(raw_image)
            observer(transformed_image, datetime.now())
        self.camera.observe(obs, names='value')
        self.camera.running = True
        
    def release(self):
        self.camera.running = False
        self.camera.cap.release()
        
class CompositeCameraDriver(CameraDriver):
    def __init__(self, *drivers: CameraDriver):
        self.drivers = drivers
        
    def register(self, observer, transform):
        for d in self.drivers:
            d.register(observer, transformer)
            
    def release(self):
        for d in self.drivers:
            d.release()