import time
import RPi.GPIO as GPIO
from buildhat import Motor

motor_a = Motor('A')

start_t = time.time()

motor_a.run_for_seconds(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # 例外処理(Ctrl+C)
        pass
    finally:
        GPIO.cleanup()