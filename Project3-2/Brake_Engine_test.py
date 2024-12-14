import unittest
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI

# 모든 하위 test 동시 실행 시 : gui 관련 image 로딩으로 인해 오류가 발생하므로 개별 실행 요망
class TestCarController(unittest.TestCase):

    def setUp(self):
        """테스트 전 초기화 작업"""
        self.car = Car()  # Car 객체 생성
        self.car_controller = CarController(self.car)  # CarController 객체 생성
        self.gui = CarSimulatorGUI(self.car, self.car_controller, lambda command: None)


    def test_success(self):
        self.car._Car__speed = 0
        self.car._Car__lock = False
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__left_door_lock = "LOCKED"  # 좌측 도어 잠김 상태
        self.car._Car__right_door_lock = "LOCKED"  # 우측 도어 잠김 상태
        self.car._Car__trunk_status = True

        self.gui.simultaneous_input_active=True #동시 입력 상태로 지정
        self.car._Car__brake_pedal=True
        self.car.toggle_engine(self.gui)

        # 테스트: 엔진이 시작되었고, 브레이크가 눌린 상태인지 확인
        self.assertTrue(self.car_controller.car._Car__brake_pedal, "Brake pedal should be pressed.")
        self.assertTrue(self.car_controller.car._Car__engine_on, "Engine should be on.")

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