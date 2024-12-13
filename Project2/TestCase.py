import unittest
from car import Car
from car_controller import CarController


class TestCarController(unittest.TestCase):

    def setUp(self):
        """테스트를 위한 준비 작업"""
        self.car = Car()  # Car 객체 생성
        self.car_controller = CarController(self.car)  # CarController 객체 생성

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

        # ENGINE_BTN 시그널
        self.car_controller.toggle_engine()

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
        self.car_controller.toggle_engine()

        self.assertEqual(self.car.gear_status, "P")
        self.assertFalse(self.car.engine_on) # 엔진이 꺼졌는지

    def test_accelerate(self):

        #엑셀 조건
        self.car._Car__engine_on = True
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__trunk_status = True
        self.car._Car__lock=False

        # ACCELERATE 시그널
        self.car_controller.accelerate() #5초 후 증가
        self.car._increase_speed() #직접 호출로 즉각 실행 
        self.assertEqual(self.car.speed, 10)


if __name__ == "__main__":
    unittest.main()

