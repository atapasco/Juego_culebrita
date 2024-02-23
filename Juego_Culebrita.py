import tkinter as tk
import random

# Dimensiones de la ventana
ANCHO = 800
ALTO = 600

# Tamaño de las bolitas
TAM_BOLA = 20

# Velocidad de la serpiente
VELOCIDAD = 150  # milisegundos

class JuegoSerpiente(tk.Tk):
    def __init__(self):
        super().__init__()

        self.canvas = tk.Canvas(self, width=ANCHO, height=ALTO, bg='white')
        self.canvas.pack()

        self.serpiente = [(100, 100), (80, 100), (60, 100)]
        self.direccion = "Derecha"
        self.comida = self.crear_comida()
        self.obstaculos = self.crear_obstaculos()

        self.bind("<KeyPress>", self.cambiar_direccion)

        self.mover_serpiente()

    def crear_comida(self):
        x = random.randint(0, (ANCHO - TAM_BOLA) / TAM_BOLA) * TAM_BOLA
        y = random.randint(0, (ALTO - TAM_BOLA) / TAM_BOLA) * TAM_BOLA

        return self.canvas.create_oval(x, y, x+TAM_BOLA, y+TAM_BOLA, fill="red")

    def crear_obstaculos(self):
        obstaculos = []
        for _ in range(10):  # Crear 10 obstáculos
            x = random.randint(0, (ANCHO - TAM_BOLA) / TAM_BOLA) * TAM_BOLA
            y = random.randint(0, (ALTO - TAM_BOLA) / TAM_BOLA) * TAM_BOLA
            obstaculos.append((x, y))
            self.canvas.create_rectangle(x, y, x+TAM_BOLA, y+TAM_BOLA, fill="black")
        return obstaculos

    def mover_serpiente(self):
        cabeza_x, cabeza_y = self.serpiente[0]

        if self.direccion == "Izquierda":
            cabeza_x -= TAM_BOLA
        elif self.direccion == "Derecha":
            cabeza_x += TAM_BOLA
        elif self.direccion == "Arriba":
            cabeza_y -= TAM_BOLA
        elif self.direccion == "Abajo":
            cabeza_y += TAM_BOLA

        self.serpiente.insert(0, (cabeza_x, cabeza_y))
        self.canvas.delete("serpiente")

        for x, y in self.serpiente:
            self.canvas.create_oval(x, y, x+TAM_BOLA, y+TAM_BOLA, fill="green", tag="serpiente")

        if self.verificar_colisiones() or self.verificar_colisiones_con_obstaculo():
            self.fin_del_juego()
            return

        if cabeza_x == self.canvas.coords(self.comida)[0] and cabeza_y == self.canvas.coords(self.comida)[1]:
            self.canvas.delete(self.comida)
            self.comida = self.crear_comida()
        else:
            self.serpiente.pop()

        self.after(VELOCIDAD, self.mover_serpiente)

    def cambiar_direccion(self, event):
        if event.keysym == "Left" and self.direccion != "Derecha":
            self.direccion = "Izquierda"
        elif event.keysym == "Right" and self.direccion != "Izquierda":
            self.direccion = "Derecha"
        elif event.keysym == "Up" and self.direccion != "Abajo":
            self.direccion = "Arriba"
        elif event.keysym == "Down" and self.direccion != "Arriba":
            self.direccion = "Abajo"

    def verificar_colisiones(self):
        cabeza_x, cabeza_y = self.serpiente[0]

        return (
            cabeza_x < 0 or
            cabeza_x >= ANCHO or
            cabeza_y < 0 or
            cabeza_y >= ALTO or
            (cabeza_x, cabeza_y) in self.serpiente[1:]
        )

    def verificar_colisiones_con_obstaculo(self):
        cabeza_x, cabeza_y = self.serpiente[0]

        return (cabeza_x, cabeza_y) in self.obstaculos

    def fin_del_juego(self):
        self.canvas.create_text(ANCHO/2, ALTO/2 - 50, text="Fin del Juego", fill="black", font=("Arial", 30, "bold"))
        boton_jugar_nuevo = tk.Button(self, text="Jugar de Nuevo", font=("Arial", 20, "bold"), bg="green", fg="white", command=self.reiniciar_juego)
        boton_jugar_nuevo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def reiniciar_juego(self):
        self.destroy()
        juego = JuegoSerpiente()
        juego.title("Juego de la Serpiente")
        juego.mainloop()

if __name__ == "__main__":
    juego = JuegoSerpiente()
    juego.title("Juego de la Serpiente")
    juego.mainloop()