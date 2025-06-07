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


class Classifier:
    """
    Classifer
    BGR
    """
    MATERIALS = {
        # Dataset 1
        # 'zinc': (200, 196, 186),
        # 'brass': (110, 193, 225),
        # 'copper': (51, 87, 255),

        # Dataset 2
        # "copper": (152, 180, 210),
        # "zinc": (203, 209, 211),
        # "brass": (157, 199, 213),
        # "pcb": (183, 204, 192),

        # Manual
        "copper": (160, 180, 210),
        "zinc": (185, 185, 185),
        "brass": (160, 200, 210),
        "pcb": (170, 204, 170)
    }

    @staticmethod
    def which_material(color: tuple) -> str:
        """
        which material it is
        """
        print(color)
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
    def __init__(self, material: int, timestamp: int):
        self.material = material
        self.timestamp = timestamp

    def pack(self) -> bytes:
        return struct.pack('II', self.material, self.timestamp)


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

    def run(self) -> None:
        """
        Run the coordinator
        """
        self.sensor.initialize()
        self.detector.initialize()

        self.transmitter.initialize()

        # flat field
        flag = False
        while True:
            frame = self.sensor.read()

            # flat field
            if flag:
                self.detector.flat_field = frame
                flag = False

            threshold_image, pieces = self.detector.detect(frame)
            released_pieces = self.tracker.update_3(pieces)

            # Classify the pieces
            for piece in self.tracker._pieces:
                material = Classifier.which_material(piece.calculate_mean_color())
                piece.name = f"{material}-{piece.id}"

            # Send the released pieces to the peers
            if released_pieces:
                print('Released pieces:', [released_piece.name for released_piece in released_pieces])
                for piece in released_pieces:

                    material = Classifier.which_material(piece.calculate_mean_color())
                    material_id = 0
                    if material == 'zinc':
                        material_id = 1

                    data_raw = RawPiece(material_id, int(piece.positions[-1]['time'])).pack()
                    self.transmitter.send_multicast(data_raw)
                    print('Sent:', data_raw)

            # Draw the tracker
            self.tracker.draw(frame)
            final_img = cv2.vconcat([threshold_image, frame])

            cv2.imshow('Video', final_img)
            cv2.moveWindow('Video', 10, 10)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

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
