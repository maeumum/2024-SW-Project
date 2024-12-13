class Car:
    def __init__(self, engine_on=False, speed=0, lock=True, trunk_status=True):
        self.__engine_on = engine_on  # True = ON / False = OFF
        self.__speed = speed  # km/h
        self.__lock = lock  # True = Locked / False = Unlocked
        self.__trunk_status = trunk_status  # True = Closed / False = Opened
        self.__left_door_status = "CLOSED"  # "OPEN" or "CLOSED"
        self.__right_door_status = "CLOSED"  # "OPEN" or "CLOSED"
        self.__left_door_lock = "LOCKED"  # "LOCKED" or "UNLOCKED"8
        self.__right_door_lock = "LOCKED"  # "LOCKED" or "UNLOCKED"
        self.__gear_status = "P"
        self.__brake_pedal = False
        self.gui = None  # GUI 참조를 저장할 변수

    # 엔진 상태 읽기
    @property
    def engine_on(self):
        return self.__engine_on

    # 속도 읽기
    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        if value >= 0:  # 속도는 음수일 수 없으므로, 음수로 설정하려 하면 무시
            self.__speed = value
        else:
            print("Speed cannot be negative!")

    def set_gui(self, gui):
        """GUI 참조를 설정하는 메서드"""
        self.gui = gui

    # 기어
    @property
    def gear_status(self):
        return self.__gear_status

    # lock
    @property
    def lock(self):
        return self.__lock

    # 차량 전체 잠금/잠금 해제
    def lock_vehicle(self):
        if self.__speed == 0:
            self.__lock = True

    def unlock_vehicle(self):
        if self.__speed == 0:
            self.__lock = False

    # 트렁크 상태 읽기
    @property
    def trunk_status(self):
        return self.__trunk_status

    # 좌측 도어 상태 읽기
    @property
    def left_door_status(self):
        return self.__left_door_status

    # 우측 도어 상태 읽기
    @property
    def right_door_status(self):
        return self.__right_door_status

    # 좌측 도어 잠금 상태 읽기
    @property
    def left_door_lock(self):
        return self.__left_door_lock

    # 우측 도어 잠금 상태 읽기
    @property
    def right_door_lock(self):
        return self.__right_door_lock

        # 엔진 토글

    def toggle_engine(self):
        if not self.__engine_on \
                and self.__left_door_status == "CLOSED" \
                and self.__right_door_status == "CLOSED" \
                and self.__trunk_status and not self.__lock:
            self.__brake_pedal = True
            if not self.__lock and self.__brake_pedal:
                self.__engine_on = True
                self.set_gear_to_drive()  # 엔진 ON 시 자동으로 Drive 모드 설정
                print("Engine started, gear set to Drive.")
        elif self.__engine_on:
            if self.__speed == 0:
                self.__engine_on = False
                self.set_gear_to_park()  # 엔진 OFF 시 자동으로 Park 모드 설정
                print("Engine stopped, gear set to Park.")

    def accelerate(self):
        """엑셀 페달 입력 후 5초 후에 속도를 증가시키고 GUI를 업데이트합니다."""
        if self.__engine_on and self.gui:
            print("엑셀이 입력되었습니다. 5초 후에 속도가 증가됩니다.")
            # 5초 후에 속도 증가 및 GUI 업데이트
            self.gui.window.after(5000, self._increase_speed)

    def _increase_speed(self):
        if self.__engine_on:
            self.__speed += 10
            if self.gui:
                self.gui.update_gui()  # GUI 업데이트

    def brake(self):
        if self.__engine_on and self.gui:
            print("브레이크가 입력되었습니다. 5초 후에 속도가 감소됩니다.")
            self.gui.window.after(5000, self._decrease_speed)

    def _decrease_speed(self):
        if self.__engine_on:
            self.__speed = max(0, self.__speed - 10)
            print(f"5초 후 속도 감소: 현재 속도는 {self.__speed} km/h입니다.")
            if self.gui:
                self.gui.update_gui()  # GUI 업데이트

    def is_brake_pedal_pressed(self):
        return self.__brake_pedal

    # 기어 상태 변경
    def set_gear_to_drive(self):
        if self.__engine_on and not self.__lock:
            self.__gear_status = "D"

    def set_gear_to_park(self):
        if self.__speed == 0:
            self.__gear_status = "P"

    # 트렁크 상태 변경
    def open_trunk(self):
        if not self.__engine_on:
            self.__trunk_status = False
            print("Trunk opened.")

    def close_trunk(self):
        self.__trunk_status = True
        print("Trunk closed.")

    # 좌측 도어 상태 변경
    def open_left_door(self):
        if not self.__engine_on:
            self.__left_door_status = "OPEN"
            print("Left door opened.")

    def close_left_door(self):
        self.__left_door_status = "CLOSED"
        print("Left door closed.")

    # 우측 도어 상태 변경
    def open_right_door(self):
        if not self.__engine_on:
            self.__right_door_status = "OPEN"
            print("Right door opened.")

    def close_right_door(self):
        self.__right_door_status = "CLOSED"
        print("Right door closed.")

    # 좌측 도어 잠금/잠금 해제
    def lock_left_door(self):
        self.__left_door_lock = "LOCKED"

    def unlock_left_door(self):
        self.__left_door_lock = "UNLOCKED"

    # 우측 도어 잠금/잠금 해제
    def lock_right_door(self):
        self.__right_door_lock = "LOCKED"

    def unlock_right_door(self):
        self.__right_door_lock = "UNLOCKED"
