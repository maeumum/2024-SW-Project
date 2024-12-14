import unittest
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI

# 모든 하위 test 동시 실행 시 : gui 관련 image 로딩으로 인해 오류가 발생하므로 개별 실행 요망
class TestCarController(unittest.TestCase):

    def setUp(self):
        """테스트를 위한 준비 작업"""
        self.car = Car()  # Car 객체 생성
        self.car_controller = CarController(self.car)  # CarController 객체 생성
        self.gui = CarSimulatorGUI(self.car, self.car_controller, lambda command: None)

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

