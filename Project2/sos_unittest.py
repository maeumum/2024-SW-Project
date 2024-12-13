import unittest
from car import Car
from car_controller import CarController


class TestCarControllerSOS(unittest.TestCase):

    def setUp(self):
        """테스트를 위한 준비 작업"""
        self.car = Car()  # Car 객체 생성
        self.car_controller = CarController(self.car)  # CarController 객체 생성

    def test_sos_button_functionality_during_driving(self):
        """주행 중일 때 SOS 버튼을 눌렀을 때의 기능이 제대로 작동하는지 확인"""

        # 자동차가 주행 중일 때 (속도 100, 문과 트렁크는 닫혀있고, 차량은 잠금 상태)
        self.car._Car__speed = 100
        self.car._Car__lock = True
        self.car._Car__left_door_status = "CLOSED"
        self.car._Car__right_door_status = "CLOSED"
        self.car._Car__left_door_lock = "LOCKED"  # 좌측 도어 잠김 상태
        self.car._Car__right_door_lock = "LOCKED"  # 우측 도어 잠김 상태
        self.car._Car__trunk_status = True

        # SOS 버튼을 누름
        self.car_controller.set_sos()

        # 차량의 상태가 제대로 변경되었는지 확인
        self.assertEqual(self.car.speed, 0)  # 속도가 0으로 변경되었는지 확인
        self.assertEqual(self.car.left_door_status, "OPEN")  # 좌측 도어가 열린지 확인
        self.assertEqual(self.car.right_door_status, "OPEN")  # 우측 도어가 열린지 확인
        self.assertEqual(self.car.left_door_lock, "UNLOCKED")  # 좌측 도어 잠금이 해제되었는지 확인
        self.assertEqual(self.car.right_door_lock, "UNLOCKED")  # 우측 도어 잠금이 해제되었는지 확인
        self.assertFalse(self.car.lock)  # 차량 잠금이 해제되었는지 확인
        self.assertFalse(self.car.trunk_status)  # 트렁크가 열린지 확인


if __name__ == "__main__":
    unittest.main()
