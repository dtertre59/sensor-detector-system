"""
coordinator.py
"""

import threading
import queue
import time
import numpy as np
import cv2

from src.sensor.computer_camera import ComputerCamera
from src.detector.color_detector import ColorDetector
# from src.factory import Factory


class Classifier:
    """
    Classifer
    """

    MATERIALS = {
        'zinc': (200, 196, 186),
        'brass': (110, 193, 225),
        'copper': (51, 87, 255)
    }

    @staticmethod
    def which_material(color: tuple) -> str:
        """
        which material it is
        """
        distances = {material: np.linalg.norm(np.array(color) - np.array(m_color)) for material, m_color in Classifier.MATERIALS.items()}
        # Find the material with the smallest distance
        closest_material = min(distances, key=distances.get)
        return closest_material


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

        self.sensor_queue = queue.Queue(maxsize=2)
        self.detector_queue = queue.Queue(maxsize=2)

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
                print('detector')
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
            if self.sensor._name == 'Computer Camera':
                frame = self.sensor_queue.get()
                cv2.imshow('Computer CAM live video feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop_event.set()
                    print("Stopping coordinator...")
                    return -1
            if self.detector:
                data = self.detector_queue.get()
                cv2.imshow('detector', data)
            

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


        print("Coordinator stopped.")
