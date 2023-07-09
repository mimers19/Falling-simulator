import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


g = 9.81        #przyspieszenie ziemskie
dt = 0.1       #rozdzielczość czasu
v0 = 0          #prędkość początkowa
f_time = 0.0
a = [g]
v = [0]
y = []
t = [0]


def make_window():
    layout = [
        [sg.Text("Initial height:")],
        [sg.InputText(key='y0')],
        [sg.Text("Mass:")],
        [sg.InputText(key='m')],
        [sg.Text("Air resistance:")],
        [sg.InputText(key='b')],
        [sg.Button("OK")]
    ]

    window = sg.Window(title="Skydiving Simulator", layout=layout)

    while True:
        event, values = window.read()

        if event == "OK":
            work(values)

        if event == sg.WIN_CLOSED:
            break

    window.close()


def falling_time(b, m, y0, time):     #funkcja obliczająca czas spadania metodą Eulera
    v_t = v0
    y_t = float(y0)

    t = 0
    while y_t > 0:
        a_t = (m * g - b * v_t**2) / m
        a.append(a_t)
        v_t += a_t * dt
        v.append(v_t)
        y_t -= v_t * dt
        y.append(y_t)
        t += dt
        time.append(t)
    return t


def paint_charts(i):

    plt.title(f'Falling time:{f_time}   v_end:{v[len(v)-1]}')
    x = [0] * len(y)
    plt.subplot(1, 4, 1)
    plt.plot(x[0:i], y[0:i], scalex=False, color='red')
    plt.ylabel('y(t)')
    plt.xlabel('x(t) = 0')
    plt.xlim([-1, 1])
    plt.ylim([0, max(y)])

    plt.subplot(1, 4, 2)
    plt.plot(t[0:i], y[0:i], scalex=False, color='red')
    plt.ylabel('y(t)')
    plt.xlabel('t')
    plt.xlim([0, f_time])
    plt.ylim([0, max(y)])

    plt.subplot(1, 4, 3)
    plt.plot(t[0:i], v[0:i], scalex=False, color='green')
    plt.ylabel('v(t)')
    plt.xlabel('t')
    plt.xlim([0, f_time])

    plt.subplot(1, 4, 4)
    plt.plot(t[0:i], a[0:i], scalex=False, color='blue')
    plt.ylabel('a(t)')
    plt.xlabel('t')
    plt.xlim([0, f_time])


def work(values):                   #główna funkcja zarządzająca kolejnością obliczeń
    global f_time
    y.append(float(values['y0']))
    f_time = float(falling_time(float(values['b']), float(values['m']), float(values['y0']), time=t))
    print("Czas spadania wynosi:", f_time, "sekund")
    fig = plt.figure(figsize=(17, 6))
    ani = FuncAnimation(fig=fig, func=paint_charts, interval=dt, cache_frame_data=False)
    plt.show()

make_window()