class CarController:
    def __init__(self, car):
        self.car = car

    def toggle_engine(self):
        self.car.toggle_engine()
        print("Engine state changed.")

    #페달
    def accelerate(self):
        self.car.accelerate()

    def brake(self):
        self.car.brake()

    #차량 잠금
    def lock_vehicle(self):
        self.car.lock_vehicle()
        print("Vehicle locked.")

    def unlock_vehicle(self):
        self.car.unlock_vehicle()
        print("Vehicle unlocked.")

    def open_trunk(self):
        if self.car.speed > 0:  # 차량이 주행 중일 경우
            print("Cannot open the trunk while driving.")
            self.car._Car__trunk_status = True  # 트렁크를 닫힌 상태로 유지
            return
        elif self.car.lock:  # 차량이 잠겨 있을 경우
            print("Cannot open the trunk while the car is locked.")
            self.car._Car__trunk_status = True  # 트렁크를 닫힌 상태로 유지
            return

            # 정상적인 조건에서만 트렁크를 열림 상태로 설정
        else :
            self.car._Car__trunk_status = False
            print("Trunk opened.")

    def close_trunk(self):
        self.car.close_trunk()
        print("Trunk closed.")

    #기어 설정
    def set_gear_to_drive(self):
        self.car.set_gear_to_drive()
        print("Gear set to Drive.")

    def set_gear_to_park(self):
        self.car.set_gear_to_park()
        print("Gear set to Park.")

    # 좌/우 도어 열기/닫기
    def open_left_door(self):
        self.car.open_left_door()

    def close_left_door(self):
        self.car.close_left_door()

    def open_right_door(self):
        self.car.open_right_door()

    def close_right_door(self):
        self.car.close_right_door()

    # 좌/우 도어 잠금/잠금 해제
    def lock_left_door(self):
        self.car.lock_left_door()

    def unlock_left_door(self):
        self.car.unlock_left_door()

    def lock_right_door(self):
        self.car.lock_right_door()

    def unlock_right_door(self):
        self.car.unlock_right_door()

    def get_engine_status(self):
        return self.car.engine_on

    def get_lock_status(self):
        return self.car.lock

    def get_speed(self):
        return self.car.speed

    def get_trunk_status(self):
        return self.car.trunk_status

    # 좌/우 도어 상태 및 잠금 상태 읽기
    def get_left_door_status(self):
        return self.car.left_door_status

    def get_right_door_status(self):
        return self.car.right_door_status

    def get_left_door_lock(self):
        return self.car.left_door_lock

    def get_right_door_lock(self):
        return self.car.right_door_lock

    def set_sos(self):
        if self.car.speed > 0:
            self.car.speed = 0
        self.car.unlock_vehicle()  # 차량 잠금 해제
        self.car._Car__left_door_lock = "UNLOCKED" #좌측 도어 잠금 해제
        self.car._Car__right_door_lock = "UNLOCKED" #우측 도어 잠금 해제
        self.car.open_left_door()   # 좌측 도어 열기
        self.car.open_right_door()  # 우측 도어 열기
        self.car.open_trunk()       # 트렁크 열기


