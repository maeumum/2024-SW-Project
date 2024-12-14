import unittest
from car import Car
from car_controller import CarController

class TestCarControllerTrunk(unittest.TestCase):

    def setUp(self):
        """테스트 준비 작업"""
        self.car = Car()  # Car 객체 생성
        self.car_controller = CarController(self.car)  # CarController 객체 생성
        # 차량 초기 상태 설정
        self.car._Car__speed = 0  # 속도 0 (정지 상태)
        self.car._Car__lock = True  # 차량 잠금 상태
        self.car._Car__trunk_status = True  # 트렁크 닫힘 상태

    def test_open_trunk_while_driving(self):
        """차량이 주행 중일 때 트렁크를 열 수 없는지 테스트"""
        self.car._Car__speed = 60  # 차량 주행 중 상태
        self.car_controller.open_trunk()  # 트렁크 열기 시도
        self.assertTrue(
            self.car.trunk_status  # 트렁크는 열리지 않아야 한다.
        )

    def test_open_trunk_when_locked(self):
        """차량이 잠겨 있을 때 트렁크를 열 수 없는지 테스트"""
        self.car._Car__lock = True  # 차량 잠금 상태
        self.car_controller.open_trunk()  # 트렁크 열기 시도
        self.assertTrue(
            self.car.trunk_status # 차량이 잠겨 있으면 트렁크는 열리지 않아야 한다.
        )

    def test_open_trunk_when_unlocked_and_parked(self):
        """차량이 잠금 해제되고 정지 상태일 때 트렁크를 열 수 있는지 테스트"""
        self.car._Car__lock = False  # 잠금 해제
        self.car._Car__speed = 0  # 차량 정지 상태
        self.car_controller.open_trunk()  # 트렁크 열기 시도
        self.assertFalse(
            self.car.trunk_status  # 잠금 해제, 정지 상태에서는 트렁크가 열려야 한다.
        )

    def test_open_trunk_under_normal_conditions(self):
        """정상적인 조건에서 트렁크를 열 수 있는지 테스트"""
        self.car._Car__lock = False  # 잠금 해제
        self.car._Car__speed = 0  # 차량 정지 상태
        self.car_controller.open_trunk()  # 트렁크 열기 시도
        self.assertFalse(
            self.car.trunk_status # 정상적인 상태에서는 트렁크가 열려야 한다.
        )

if __name__ == "__main__":
    unittest.main()
