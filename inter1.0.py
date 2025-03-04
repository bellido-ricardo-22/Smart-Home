import serial
import tkinter as tk
from tkinter import PhotoImage, messagebox

class Cuenta:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SMART HOME")
        self.root.geometry("300x200")
        self.root.config(bg="black")

        # usuario y contraseña
        self.usuario_valido = "usuario"
        self.contrasena_valida = "12345678"

        # entrada
        tk.Label(self.root, text="Usuario:", font=("TIMES NEW ROMAN", 12), bg="black", fg="white").pack(pady=5)
        self.usuario_entry = tk.Entry(self.root, font=("TIMES NEW ROMAN", 12))
        self.usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("TIMES NEW ROMAN", 12), bg="black", fg="white").pack(pady=5)
        self.contrasena_entry = tk.Entry(self.root, show="*", font=("TIMES NEW ROMAN", 12))
        self.contrasena_entry.pack(pady=5)

        # Botón de inicio de sesión
        tk.Button(self.root, text="Iniciar Sesión", command=self.verificar_credenciales, bg="green", fg="white", width=15).pack(pady=10)

        self.root.mainloop()

    def verificar_credenciales(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        if usuario == self.usuario_valido and contrasena == self.contrasena_valida:
            self.root.destroy()  # cierra  ventana login
            app = SmartHome()    # abre ventana principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


class SmartHome:
    def __init__(self, puerto="COM6", baudrate=115200):
        self.puerto = puerto
        self.baudrate = baudrate
        try:
            self.ser = serial.Serial(self.puerto, self.baudrate, timeout=1)
        except Exception as e:
            print(f"Error al conectar con {self.puerto}: {e}")
            self.ser = None

        # Ventana principal
        self.root = tk.Tk()
        self.root.title("SMART HOME")
        self.root.geometry("800x800")
        self.root.config(bg="black")

        # Cargar imágenes
        self.logo = PhotoImage(file=r"C:\Users\RICARDO\Desktop\smarthome-poo\Logo-fiee.png").subsample(4, 4)
        self.second_logo = PhotoImage(file=r"C:\Users\RICARDO\Desktop\smarthome-poo\uni.png").subsample(1, 1)

        # Mostrar imágenes
        image_frame = tk.Frame(self.root, bg="black")
        image_frame.pack(pady=10, fill="x")
        
        tk.Label(image_frame, image=self.second_logo, bg="black").pack(side="left", padx=10)
        tk.Label(image_frame, image=self.logo, bg="black").pack(side="right", padx=10)

        # Título
        tk.Label(self.root, text="INTERFAZ", font=("TIMES NEW ROMAN", 16, "bold"), bg="white", padx=10).pack(pady=10)

        # frame  para organizar las secciones
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(fill="both", expand=True)

        # Frame para la izquierda 
        left_frame = tk.Frame(main_frame, bg="black")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame para la derecha 
        right_frame = tk.Frame(main_frame, bg="black")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Sensor
        sensor_frame = tk.Frame(left_frame, bg="black")
        sensor_frame.pack(anchor="w", padx=10, pady=5, fill="x")
        
        tk.Label(sensor_frame, text="Sensor", font=("TIMES NEW ROMAN", 14, "bold"), bg="white", padx=10).pack(pady=5)
        
        self.temp_label = tk.Label(sensor_frame, text="Temperatura: --°C", font=("TIMES NEW ROMAN", 12), bg="white", padx=10)
        self.temp_label.pack(pady=5)
        self.hum_label = tk.Label(sensor_frame, text="Humedad: --%", font=("TIMES NEW ROMAN", 12), bg="white", padx=10)
        self.hum_label.pack(pady=5)

        #  Iluminación
        iluminacion_frame = tk.Frame(left_frame, bg="black")
        iluminacion_frame.pack(anchor="w", padx=10, pady=5, fill="x")
        
        tk.Label(iluminacion_frame, text="Iluminación", font=("TIMES NEW ROMAN", 14, "bold"), bg="white", padx=10).pack(pady=5)
        
        self.iluminacion = Iluminacion(self.ser, iluminacion_frame)

        # Ventilación
        ventilacion_frame = tk.Frame(right_frame, bg="black")
        ventilacion_frame.pack(anchor="e", padx=10, pady=5, fill="x")
        
        tk.Label(ventilacion_frame, text="Ventilación", font=("TIMES NEW ROMAN", 14, "bold"), bg="white", padx=10).pack(pady=5)
        
        self.ventilacion = Ventilacion(self.ser, ventilacion_frame)

        # Cerradura
        cerradura_frame = tk.Frame(right_frame, bg="black")
        cerradura_frame.pack(anchor="e", padx=10, pady=5, fill="x")
        
        tk.Label(cerradura_frame, text="Cerradura", font=("TIMES NEW ROMAN", 14, "bold"), bg="white", padx=10).pack(pady=5)
        
        self.cerradura = Cerradura(self.ser, cerradura_frame)

        # Inicializar componentes
        self.sensor = Sensor(self.ser)
        
        # Actualizar datos periódicamente
        self.actualizar_datos()

        self.root.mainloop()

    def enviar_comando(self, comando):
        if self.ser:
            try:
                self.ser.write((comando + "\n").encode())
            except Exception as e:
                print(f"Error al enviar comando: {e}")

    def actualizar_datos(self):
        # Leer datos del sensor
        temp, hum = self.sensor.leer_sensor()
        self.temp_label.config(text=f"Temperatura: {temp}°C")
        self.hum_label.config(text=f"Humedad: {hum}%")
        self.root.after(2000, self.actualizar_datos)  # Actualizar cada 2 segundos


class Sensor:
    def __init__(self, serial_port):
        self.ser = serial_port

    def leer_sensor(self):
        if self.ser:
            self.ser.write(b"READ\n")
            datos = self.ser.readline().decode().strip()
            if "," in datos:
                temp, hum = datos.split(",")
                return temp, hum
        return "--", "--"


class Iluminacion:
    def __init__(self, serial_port, root):
        self.ser = serial_port
        self.root = root

        # Configuración de luces
        self.leds = [
            {"nombre": "LUZ 1", "on": "LED1_ON", "off": "LED1_OFF"},
            {"nombre": "LUZ 2", "on": "LED2_ON", "off": "LED2_OFF"},
            {"nombre": "LUZ 3", "on": "LED3_ON", "off": "LED3_OFF"}
        ]

        # Crear botones para cada luz
        for led in self.leds:
            frame = tk.Frame(root, bg="black")
            frame.pack(pady=5, anchor="w")
            
            tk.Label(frame, text=led["nombre"], font=("TIMES NEW ROMAN", 12), bg="white", padx=10).pack(side="left")
            tk.Button(frame, text="ON", command=lambda cmd=led["on"]: self.enviar_comando(cmd), bg="green", fg="white", width=12).pack(side="left", padx=5)
            tk.Button(frame, text="OFF", command=lambda cmd=led["off"]: self.enviar_comando(cmd), bg="red", fg="white", width=12).pack(side="left", padx=5)

    def enviar_comando(self, comando):
        if self.ser:
            try:
                self.ser.write((comando + "\n").encode())
            except Exception as e:
                print(f"Error al enviar comando: {e}")


class Ventilacion:
    def __init__(self, serial_port, root):
        self.ser = serial_port
        self.root = root

        # ventilación
        frame = tk.Frame(root, bg="black")
        frame.pack(pady=5, anchor="e")
        
        tk.Label(frame, text="VENTILADOR", font=("TIMES NEW ROMAN", 12), bg="white", padx=10).pack(side="left")
        tk.Button(frame, text="ON", command=lambda: self.enviar_comando("MOTOR_ON"), bg="green", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(frame, text="OFF", command=lambda: self.enviar_comando("MOTOR_OFF"), bg="red", fg="white", width=12).pack(side="left", padx=5)

    def enviar_comando(self, comando):
        if self.ser:
            try:
                self.ser.write((comando + "\n").encode())
            except Exception as e:
                print(f"Error al enviar comando: {e}")


class Cerradura:
    def __init__(self, serial_port, root):
        self.ser = serial_port
        self.root = root

        # cerradura
        frame = tk.Frame(root, bg="black")
        frame.pack(pady=5, anchor="e")
        
        tk.Label(frame, text="Cerradura", font=("TIMES NEW ROMAN", 12), bg="white", padx=10).pack(side="left")
        tk.Button(frame, text="Abrir", command=lambda: self.enviar_comando("ABRIR_CERRADURA"), bg="green", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(frame, text="Cerrar", command=lambda: self.enviar_comando("CERRAR_CERRADURA"), bg="red", fg="white", width=12).pack(side="left", padx=5)

    def enviar_comando(self, comando):
        if self.ser:
            try:
                self.ser.write((comando + "\n").encode())
            except Exception as e:
                print(f"Error al enviar comando: {e}")


if __name__ == "__main__":
    cuenta = Cuenta()