import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI
import tkinter as tk


# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):
    print(f"Executing command: {command}")  # 로그 출력

    if car_controller.car.speed > 0:  # 주행 시, 문&트렁크 open, unlock 명령 무시
        if command == "UNLOCK": return  # 주행 시 차량의 모든 문 unlock 명령 무시
        if command == "LEFT_DOOR_OPEN": return  # 주행 시 왼쪽문 open 명령 무시
        if command == "RIGHT_DOOR_OPEN": return  # 주행 시 오른쪽 문 open 명령 무시
        if command == "LEFT_DOOR_UNLOCK": return  # 주행 시 왼쪽문 unlock 명령 무시
        if command == "RIGHT_DOOR_UNLOCK": return  # 주행 시 오른쪽 문 unlock 명령 무시
        if command == "TRUNK_OPEN":
            if car_controller.car.speed > 0:
                print("[TRUNK_OPEN] Command ignored: Cannot open trunk while driving.")
                return
            car_controller.open_trunk()
            print("[TRUNK_OPEN] Trunk opened successfully.")  # 주행 시 트렁크 open 명령 무시

    if command == "ENGINE_BTN":
        # 시동 ON 조건
        if car_controller.car.left_door_status == "CLOSED" \
                and car_controller.car.right_door_status == "CLOSED" and car_controller.car.trunk_status \
                and car_controller.car.left_door_lock == "LOCKED" and car_controller.car.right_door_lock == "LOCKED":
            car_controller.toggle_engine()  # 시동 ON / OFF

    elif command == "ACCELERATE":
        if (car_controller.car._Car__left_door_status == "CLOSED" and
                car_controller.car._Car__right_door_status == "CLOSED" and car_controller.car._Car__engine_on == True and
                car_controller.car._Car__lock == False and car_controller.car._Car__trunk_status == True):
            car_controller.car.accelerate()
    elif command == "BRAKE":
        if car_controller.car._Car__speed == 0:
            # 속도가 0일 때: 엔진 상태와 관계없이 브레이크 상태 변경
            car_controller.car._Car__brake_pedal = True
            print("Brake state is changed.")
            print(f"Brake pedal status: {car.is_brake_pedal_pressed()}")

        elif 0 < car_controller.car._Car__speed < 150:
            # 속도가 0 초과 150 미만일 때: 기존 처리 방식 유지
            if (car_controller.car._Car__left_door_status == "CLOSED" and
                    car_controller.car._Car__right_door_status == "CLOSED" and
                    car_controller.car._Car__engine_on and
                    car_controller.car._Car__lock == False and
                    car_controller.car._Car__trunk_status == True):
                car_controller.car.brake()


    elif command == "LOCK":
        car_controller.lock_vehicle()  # 차량잠금
    elif command == "UNLOCK":
        if car_controller.car.speed > 0: return  # 주행 시 무시
        car_controller.unlock_vehicle()  # 차량잠금해제
    elif command == "LEFT_DOOR_LOCK":
        car_controller.lock_left_door()  # 왼쪽문 잠금
    elif command == "LEFT_DOOR_UNLOCK":
        if car_controller.car.speed > 0: return  # 주행 시 무시
        car_controller.unlock_left_door()  # 왼쪽문 잠금해제
    elif command == "LEFT_DOOR_OPEN":
        if car_controller.car.speed > 0: return  # 주행 시 무시
        car_controller.open_left_door()  # 왼쪽문 열기
    elif command == "LEFT_DOOR_CLOSE":
        car_controller.close_left_door()  # 왼쪽문 닫기
    elif command == "TRUNK_OPEN":
        if car_controller.car.speed > 0: return  # 주행 시 무시
        car_controller.open_trunk()  # 트렁크 열기
    elif command == "SOS":
        car_controller.set_sos()

# 파일 경로를 입력받는 함수
# -> 가급적 수정하지 마세요.
#    테스트의 완전 자동화 등을 위한 추가 개선시에만 일부 수정이용하시면 됩니다. (성적 반영 X)
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        # 파일 경로를 받은 후 GUI의 mainloop에서 실행할 수 있도록 큐에 넣음
        gui.window.after(0, lambda: gui.process_commands(file_path))


# 메인 실행
# -> 가급적 main login은 수정하지 마세요.
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)

    # GUI는 메인 스레드에서 실행
    gui = CarSimulatorGUI(car,car_controller, lambda command: execute_command_callback(command, car_controller))

    # SOS 버튼을 GUI에 추가
    sos_button = tk.Button(
        gui.window,
        text="SOS",
        command=lambda: execute_command_callback("SOS", car_controller),
        bg="red",
        fg="white",
        font=("Arial", 16, "bold"),
        width=10,
        height=2
    )
    sos_button.place(x=10, y=10)  # 왼쪽 상단에 배치하여 ready와 대칭

    # 파일 입력 스레드는 별도로 실행하여, GUI와 병행 처리
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 메인 스레드가 종료되면 서브 스레드도 종료되도록 설정
    input_thread.start()

    # GUI 시작 (메인 스레드에서 실행)
    gui.start()
