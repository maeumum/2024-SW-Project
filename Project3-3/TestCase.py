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

    def test_engine_toggle1(self):
        """엔진 시동"""

        # 시동 on 조건
        self.car._Car__speed = 0
        self.car._Car__lock = False
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__left_door_lock = "LOCKED"  # 좌측 도어 잠김 상태
        self.car._Car__right_door_lock = "LOCKED"  # 우측 도어 잠김 상태
        self.car._Car__trunk_status = True

        self.gui.simultaneous_input_active = True  # 동시 입력 상태로 지정
        self.car._Car__brake_pedal = True

        # ENGINE_BTN 시그널
        self.car_controller.toggle_engine(self.gui)

        # 차량의 상태가 제대로 변경되었는지 확인
        self.assertTrue(self.car.is_brake_pedal_pressed())  # break가 True로 바뀌었는지
        self.assertTrue(self.car.engine_on)  # 엔진이 켜졌는지
        self.assertEqual(self.car.gear_status, "D")

    def test_engine_toggle2(self):
        #시동 off 조건
        self.car._Car__speed = 0
        self.car._Car__engine_on = True
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__left_door_lock = "LOCKED"  # 좌측 도어 잠김 상태
        self.car._Car__right_door_lock = "LOCKED"  # 우측 도어 잠김 상태
        self.car._Car__trunk_status = True

        # ENGINE_BTN 시그널
        self.car_controller.toggle_engine(self.gui)

        self.assertEqual(self.car.gear_status, "P")
        self.assertFalse(self.car.engine_on) # 엔진이 꺼졌는지

    def test_accelerate(self):

        #엑셀 조건
        self.car._Car__speed=0
        self.car._Car__engine_on = True
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__trunk_status = True
        self.car._Car__lock=False
        self.car._Car__brake_pedal=True

        # ACCELERATE 시그널
        self.car_controller.accelerate() #5초 후 증가
        self.assertEqual(self.car.speed, 10)


    def test_acceleration_without_engine(self):
        """엔진이 꺼진 상태에서 가속 실패"""
        # 초기 상태
        self.car._Car__engine_on = False

        # ACCELERATE 시도
        self.car_controller.accelerate()

        # 상태 확인
        self.assertEqual(self.car.speed, 0, "Speed should remain 0 when engine is OFF.")


if __name__ == "__main__":
    unittest.main()

