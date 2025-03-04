from machine import Pin, PWM
import dht
import time
import sys
import select

# DHT11 en el pin GPIO5
sensor = dht.DHT11(Pin(5))


led1 = Pin(32, Pin.OUT)  # GPIO32
led2 = Pin(25, Pin.OUT)  # GPIO25
led3 = Pin(27, Pin.OUT)  # GPIO27

# 28BYJ-48
motor_pins = [Pin(pin, Pin.OUT) for pin in (14, 12, 13, 15)]  # pines del motor

# Secuencia de pasos para el motor paso a paso (medio paso)
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# SG90 
servo = PWM(Pin(16), freq=50)  

# 
def mover_servo(angulo):
    duty = int(40 + (angulo / 180) * 115)  
    servo.duty(duty)
    time.sleep(1)  # Esperar a que el servomotor llegue a la posición

# abrir la cerradura 
def abrir_cerradura():
    mover_servo(90)

# cerrar la cerradura 
def cerrar_cerradura():
    mover_servo(0)

# motor
def motor_step(direction):
    step = 0
    while True:
        for pin in range(4):
            motor_pins[pin].value(step_sequence[step][pin])
        step += direction
        if step >= len(step_sequence):
            step = 0
        elif step < 0:
            step = len(step_sequence) - 1
        time.sleep_ms(10)

def motor_stop():
    for pin in motor_pins:
        pin.value(0)

while True:
    try:
        
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        # imprime datos
        print(f"{temp},{hum}")

        # Leer comandos desde la PC
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            comando = sys.stdin.readline().strip()
            if comando == "LED1_ON":
                led1.value(1)
            elif comando == "LED1_OFF":
                led1.value(0)
            elif comando == "LED2_ON":
                led2.value(1)
            elif comando == "LED2_OFF":
                led2.value(0)
            elif comando == "LED3_ON":
                led3.value(1)
            elif comando == "LED3_OFF":
                led3.value(0)
            elif comando == "MOTOR_ON":
                motor_step(1)  # Girar en una dirección
            elif comando == "MOTOR_OFF":
                motor_stop()  # Detener el motor
            elif comando == "ABRIR_CERRADURA":
                abrir_cerradura()
            elif comando == "CERRAR_CERRADURA":
                cerrar_cerradura()

    except Exception as e:
        print("Error:", e)
    
time.sleep(2)


