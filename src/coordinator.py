"""
coordinator.py
"""

import threading
import queue
import time
import struct
import numpy as np
import cv2

from src.sensor.computer_camera import ComputerCamera
from src.detector.color_detector import ColorDetector

from src.tracker import Tracker

# from src.transmitter import Transmitter
from src.transmitter import MulticastTransmitter

from src.factory import SensorFactory, DetectorFactory
from src.sensor.sensor_type import SensorType
from src.detector.detector_type import DetectorType
import src.config_vars as cfv

class PairCoordinator:
    """
    Pair Coordinator class
    """

    def __init__(self, sensor_name: str = 'ccamera', detector_name: str = 'cdetector'):
        """
        Coordinator constructor
        """
        self.sensor = ComputerCamera()
        self.detector = ColorDetector()

        self.sensor_queue = queue.Queue(maxsize=100)
        self.detector_queue = queue.Queue(maxsize=100)

        self.stop_event = threading.Event()
        # self.lock = threading.Lock()

    def sensor_thread(self):
        """
        Sensor
        """
        self.sensor.initialize()
        while not self.stop_event.is_set():
            data = self.sensor.read()
            self.sensor_queue.put(data)
            time.sleep(0.01)
        self.sensor.release()

    def detector_thread(self):
        """
        Detector
        """
        self.detector.initialize()
        while not self.stop_event.is_set():
            
            try:
                time.sleep(0.1)
                data = self.sensor_queue.get(timeout=1)
                # print('detector')
                detection = self.detector.detect(data)
                self.detector_queue.put(detection, timeout=1)
                # print(1)
            except queue.Empty:
                continue
        self.detector.release()

    def main_thread(self):
        """
        Displays the live video feed from the computer's webcam until
        a key is pressed.
        """
        while not self.stop_event.is_set():
            # if self.sensor._name == 'Computer Camera':
            #     frame = self.sensor_queue.get()
            #     cv2.imshow('Computer CAM live video feed', frame)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         self.stop_event.set()
            #         print("Stopping coordinator...")
            #         return -1
            if self.detector:
                pieces = self.detector_queue.get()
                print('Pieces:', [piece.name for piece in pieces])

        # if self.detector:
        #     detection = self.detector_queue.get()
        #     print(detection)

    def run_t(self):
        """
        Run the coordinator
        """

        sensor_thread = threading.Thread(target=self.sensor_thread)
        detector_thread = threading.Thread(target=self.detector_thread)

        sensor_thread.start()
        detector_thread.start()

        self.main_thread()

        print('Stop', self.stop_event)
        detector_thread.join()
        sensor_thread.join()

        cv2.destroyAllWindows()
        print("Coordinator stopped.")



class RawPiece():
    def __init__(self, material: int, timestamp_ms: int, speed: float):
        self.material = material
        self.timestamp_ms = timestamp_ms
        self.speed = speed  # mm/s

    def pack(self) -> bytes:
        return struct.pack('ILf', self.material, self.timestamp_ms, self.speed)


class Coordinator:
    """
    Coordinator class
    """
    def __init__(self, sensor_name: str = 'computer_camera', detector_name: str = 'color_detector',
                 host: str = '224.0.0.1', port: int = 5007):
        """
        Coordinator constructor
        """
        self.sensor = SensorFactory.create(SensorType(sensor_name))
        self.detector = DetectorFactory.create(DetectorType(detector_name))

        self.tracker = Tracker()

        self.transmitter = MulticastTransmitter(host, port)

    def run(self, flat_field_flag: bool = False) -> None:
        """
        Run the coordinator
        """
        # Config parameters

        self.detector._thresh = cfv.RPI_CAM_THRESHOLD
        self.detector.min_area = cfv.DETECTOR_MIN_AREA
        self.tracker._x_addition_limit = cfv.X_ADDITION_LIMIT
        self.tracker._x_expulsion_limit = cfv.X_EXPULSION_LIMIT
        pixels_to_mm = cfv.PIXELS_TO_MM

        # Window
        window_name = 'CHS - Detector Machine - Video'
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        # Full screen mode
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        print()
        print('----- Init vars -----')
        print()

        self.sensor.initialize()
        self.detector.initialize()

        self.transmitter.initialize()
        
        print()
        print('----- Start Loop -----')
        print()
    
        while True:
            frame = self.sensor.read()

            # flat field
            if flat_field_flag:
                self.detector.flat_field = frame
                flat_field_flag = False

            threshold_image, pieces = self.detector.detect(frame, merge_pieces=False)
            released_pieces = self.tracker.update(pieces)

            # Send the released pieces to the peers
            if released_pieces:
                print('Released pieces:', self.tracker.get_short_description(released_pieces))
                for piece in released_pieces:
                    print('Clasification: ', f'{piece.category.name}({piece.category.value})', 'Speed:', piece.calculate_speed(pixels_to_mm=pixels_to_mm)[0])
                    data_raw = RawPiece(material=piece.category.value, 
                                        timestamp_ms=int(piece.positions[-1]['time'] * 1000),   # Convert to millis
                                        speed=piece.calculate_speed(pixels_to_mm=pixels_to_mm)[0]).pack()
                    self.transmitter.send_multicast(data_raw)
                    print('Sent:', data_raw)

            # Draw the tracker
            self.tracker.draw(frame)
            t_i = cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR)
            final_img = cv2.vconcat([t_i, frame])
            final_img = frame
            cv2.imshow(window_name, final_img)
            # cv2.moveWindow('Video', 20, 40)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print()
        print('----- Release resoures -----')
        print()

        self.sensor.release()
        self.detector.release()
        cv2.destroyAllWindows()

        print("Coordinator stopped.")



if __name__ == '__main__':

    # ----- pair Coordinator with threads
    # coordinator = PairCoordinator()
    # coordinator.run_t()

    # ----- Coordinator
    coordinator = Coordinator('rpi_camera')
    coordinator.run()
