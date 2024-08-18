import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

# Calculo de la posicion
def posiciones(x, y, xmin, ymin, xmax, ymax):
    recta = INSIDE
    if x < xmin:     
        recta |= LEFT
    elif x > xmax:   
        recta |= RIGHT
    if y < ymin:      
        recta |= BOTTOM
    elif y > ymax:    
        recta |= TOP
    return recta

def cohenSutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    punto1 = posiciones(x1, y1, xmin, ymin, xmax, ymax)
    punto2 = posiciones(x2, y2, xmin, ymin, xmax, ymax)
    accept = False

    while True:
        if punto1 == 0 and punto2 == 0:
            # Trivialmente aceptada
            accept = True
            break
        elif punto1 & punto2 != 0:
            # Trivialmente rechazada
            break
        else:
            # Recorte necesario
            if punto1 != 0:
                puntoFuera = punto1
            else:
                puntoFuera = punto2

            if puntoFuera & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif puntoFuera & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif puntoFuera & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif puntoFuera & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if puntoFuera == punto1:
                x1, y1 = x, y
                punto1 = posiciones(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                punto2 = posiciones(x2, y2, xmin, ymin, xmax, ymax)

    if accept:
        return [(x1, y1), (x2, y2)]
    else:
        return []

class CortadorLinea:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax
        self.fig, self.ax = plt.subplots()
        self.rect = Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, linewidth=2, edgecolor='black', facecolor='none')
        self.ax.add_patch(self.rect)
        self.x0, self.y0 = None, None
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.linea = None

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        self.x0, self.y0 = event.xdata, event.ydata

    def on_release(self, event):
        if event.inaxes != self.ax:
            return
        x1, y1 = self.x0, self.y0
        x2, y2 = event.xdata, event.ydata
        lineaCortada = cohenSutherland(x1, y1, x2, y2, self.xmin, self.ymin, self.xmax, self.ymax)
        if lineaCortada:
            (cx1, cy1), (cx2, cy2) = lineaCortada
            self.ax.plot([cx1, cx2], [cy1, cy2], 'g')
        else:
            self.ax.plot([x1, x2], [y1, y2], 'r')
        self.fig.canvas.draw()
        self.x0, self.y0 = None, None
        self.linea = None

    def on_motion(self, event):
        if event.inaxes != self.ax or self.x0 is None or self.y0 is None:
            return
        if self.linea:
            self.linea.remove()
        self.linea, = self.ax.plot([self.x0, event.xdata], [self.y0, event.ydata], 'r',linewidth=2)
        self.fig.canvas.draw()

    def show(self):
        plt.xlim(0, 300)
        plt.ylim(0, 300)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

xmin, ymin, xmax, ymax = 50, 50, 250, 250 
CortadorLinea(xmin, ymin, xmax, ymax).show()

