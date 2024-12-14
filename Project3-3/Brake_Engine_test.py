import unittest
from unittest.mock import MagicMock, patch
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


class TestCarController(unittest.TestCase):

    @patch("tkinter.PhotoImage")  # tkinter.PhotoImage를 모킹
    @patch("tkinter.Tk")  # tkinter.Tk 객체를 모킹
    def setUp(self, mock_tk, mock_photo_image):
        """테스트 전 초기화 작업"""
        self.car = Car()  # Car 객체 생성
        self.car_controller = CarController(self.car)  # CarController 객체 생성

        # GUI 객체를 생성하되, 이미지 로딩 및 캔버스 관련 요소는 모킹
        self.gui = CarSimulatorGUI(self.car, self.car_controller, lambda command: None)

        # 실제 GUI 관련 요소들을 모킹
        self.gui.canvas = MagicMock()  # canvas 모킹
        self.gui.canvas.create_image = MagicMock()  # create_image 메서드 모킹
        self.gui.load_image = MagicMock()  # load_image 메서드 모킹

        # 중요한 변수인 simultaneous_input_active만 유지
        self.gui.simultaneous_input_active = False


    def test_successful_sequence(self):
        """BRAKE → ENGINE_BTN → ACCELERATE 순서로 성공"""
        # 초기 상태
        self.car._Car__speed = 0
        self.car._Car__lock = False
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__trunk_status = True

        # 명령 실행
        self.gui.simultaneous_input_active = True  # 동시 입력 상태로 지정
        self.car._Car__brake_pedal = True  # 브레이크 눌림
        self.gui.simultaneous_input_active = True  # 동시 입력 상태로 지정

        self.car.toggle_engine(self.gui)  # 엔진 켜기
        self.car_controller.accelerate()  # 가속

        # 상태 확인
        self.assertTrue(self.car.engine_on, "Engine should be ON after correct sequence.")
        self.assertGreater(self.car.speed, 0, "Speed should increase after acceleration.")
        self.assertEqual(self.car.gear_status, "D")

    def test_failed_sequence(self):
        """ENGINE_BTN → BRAKE → ACCELERATE 순서로 실패"""
        # 초기 상태
        self.car._Car__speed = 0
        self.car._Car__lock = False
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__trunk_status = True

        # 명령 실행
        self.gui.simultaneous_input_active = True  # 동시 입력 상태로 지정

        self.car.toggle_engine(self.gui)  # 브레이크 없이 엔진 켜기 시도
        self.car._Car__brake_pedal = True  # 브레이크 눌림
        self.car_controller.accelerate()  # 가속 시도

        # 상태 확인
        self.assertFalse(self.car.engine_on, "Engine should remain OFF when brake is not pressed first.")
        self.assertEqual(self.car.speed, 0, "Speed should remain 0 when engine is OFF.")
        self.assertEqual(self.car.gear_status, "P")

    def test_failure1(self):
        self.car._Car__speed = 0
        self.car._Car__lock = False
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__left_door_lock = "LOCKED"  # 좌측 도어 잠김 상태
        self.car._Car__right_door_lock = "LOCKED"  # 우측 도어 잠김 상태
        self.car._Car__trunk_status = True

        self.gui.simultaneous_input_active = False  # 동시 입력 상태로 지정
        self.car.toggle_engine(self.gui)

        # 테스트 : BRAKE 명령 없이 ENGINE_BTN 실행
        self.assertFalse(self.car_controller.car._Car__brake_pedal, "Brake pedal should not be pressed.")
        self.assertFalse(self.car_controller.car._Car__engine_on, "Engine should not be on.")

    def test_failure2(self):
        self.car._Car__speed = 0
        self.car._Car__lock = False
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__left_door_lock = "LOCKED"  # 좌측 도어 잠김 상태
        self.car._Car__right_door_lock = "LOCKED"  # 우측 도어 잠김 상태
        self.car._Car__trunk_status = True

        self.gui.simultaneous_input_active = True  # 동시 입력 상태로 지정
        self.car.toggle_engine(self.gui)
        self.car._Car__brake_pedal = True

        # 테스트 : ENGINE_BTN>BRAKE 순으로 실행
        self.assertTrue(self.car_controller.car._Car__brake_pedal, "Brake pedal should be pressed.")
        self.assertFalse(self.car_controller.car._Car__engine_on, "Engine should not be on.")

    def test_failure3(self):
        self.car._Car__speed = 0
        self.car._Car__lock = False
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__left_door_lock = "LOCKED"  # 좌측 도어 잠김 상태
        self.car._Car__right_door_lock = "LOCKED"  # 우측 도어 잠김 상태
        self.car._Car__trunk_status = True

        self.gui.simultaneous_input_active = False  # 순차 입력 상태로 지정
        self.car._Car__brake_pedal = True
        self.car.toggle_engine(self.gui)

        # 테스트 : BRAKE>ENGINE_BTN 순으로 실행
        self.assertFalse(self.gui.simultaneous_input_active, "Simultaneous input not active. Engine toggle ignored.")
        self.assertTrue(self.car_controller.car._Car__brake_pedal, "Brake pedal should be pressed.")
        self.assertFalse(self.car_controller.car._Car__engine_on, "Engine should not be on.")


if __name__ == "__main__":
    unittest.main()