import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# БАРДУШКО
# Если пеленгуют сигнал, то просто апдейтишь singals
# signals(size(signals)) = json_сигнала
signals ={
    "0": {
        "freq": 1800,
        "bandwidth": 20,
        "power": 70.0,
        "signal_type": "smooth",
        "mod": "None",
        "bearing": 105,
        "text": ".. ^ .. ^ .. ^ ..",
        "source": "RLC",
        "X": 4,
        "Y": 4,
	    "distance": 0.5
    },
    "1": {
        "freq": 1850,
        "bandwidth": 20.200,
        "power": 65.0,
        "signal_type": "ragged",
        "mod": "am",
        "bearing": 120,
        "text": ".. ^ .. ^ .. ^ ..",
        "source": "radio",
        "X": 0.5,
        "Y": -0.3,
	    "distance": 1
    }
}

# БАРДУШКО
# То же самое, только местоположения еще наших комплексов ларандитов
# А так же наших чуваков, которые общаются
# Забираем из работы, а так же из автоматического определения
our_signals = {"1": {
        "freq": 1850,
        "bandwidth": 20.200,
        "power": 65.0,
        "signal_type": "ragged",
        "mod": "am",
        "bearing": 120,
        "text": ".. ^ .. ^ .. ^ ..",
        "source": "radio",
        "name": "Ольха",
        "X": -0.2,
        "Y": -0.2,
	    "distance": 1}
}

scale = 1
draw_path=True
image_path = "img/image_50000.jpg"


def plot_xy_graph(data_enemy=signals, data_ours = our_signals):
    
    # Загружаем карту под графиком
    img = Image.open(image_path)
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Прячем все подписи графика
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    # Отрисовка карты
    ax.imshow(img, extent=[-1, 1, -1, 1], aspect='auto')
    
    # Рисуем центральную точку
    center_x, center_y = 0, 0
    ax.plot(center_x, center_y, 'r^', markersize=8, label="Center")
    
    # Для своих сигналов
    for key in data_ours:
        entry = data_ours[key]
        # Высчитываем координаты относительно масштаба 
        x = entry["X"] / scale
        y = entry["Y"] / scale
        
        # Проверяем что точно находится в границах отображаемой карты
        # Иначе рисуем на границе карты
        if abs(x) > (1) or abs(y) > (1):
            factor = max(abs(x) + 0.1*scale, abs(y) + 0.1*scale)
            x /= factor
            y /= factor
        
        ax.plot(x, y, 'r.', markersize=10)  # ставим точку

        # подписываем координаты и позывной
        ax.text(x, y, f"({entry["X"]:.2f}, {entry["Y"]:.2f})", fontsize=10, color='red', ha='left', va='bottom')
        ax.text(x, y+0.04, f"{entry["name"]}", fontsize=14, color='red', ha='left', va='bottom')
        last_x, last_y = x, y
    
    # Для чужих сигналов
    last_x, last_y = None, None
    
    for key in data_enemy:
        entry = data_enemy[key]
        # Высчитываем координаты относительно масштаба 
        x = entry["X"] / scale
        y = entry["Y"] / scale
        
        # Проверяем что точно находится в границах отображаемой карты
        # Иначе рисуем на границе карты
        if abs(x) > 1 or abs(y) > 1:
            factor = max(abs(x) + 0.1, abs(y) + 0.1)
            x /= factor
            y /= factor
        
        ax.plot(x, y, 'bo', markersize=6)  # ставим точку

        # подписываем координаты
        ax.text(x, y, f"({entry["X"]:.2f}, {entry["Y"]:.2f})", fontsize=10, color='blue', ha='left', va='bottom')
        last_x, last_y = x, y
    
    # Если поставлена галочка на отрисовку пеленга на карте
    if draw_path and last_x is not None:
        ax.plot([center_x, last_x], [center_y, last_y], 'r-', linewidth=2)
        ax.text(center_x, center_y, f"{np.degrees(np.arctan2(last_y, last_x)):.1f}°", 
                fontsize=12, color='red', ha='left', va='bottom')
    
    plt.show()


# БАРДУШКО
# Очищаем карту (позже сделать, что свои точки остаются)
def clear_signals():
    signals.clear()
    plot_xy_graph()


# БАРДУШКО
# Меняем масштаб карты (если нажата кнопка масштаба)
def change_scale(scale_changed):
    global scale
    scale = scale_changed
    if scale == 1:
        image_path = "img/image_50000.jpg"
    elif scale == 2:
        image_path = "img/image_100000.jpg"
    else:
        image_path = "img/image_250000.jpg"
 
    plot_xy_graph()




# БАРДУШКО
# Изменения tickbox с отображением пеленга на карте
def change_draw_path():
    global draw_path
    if draw_path == True:
        draw_path = False
    else:
        draw_path = True
    plot_xy_graph()


change_scale(scale_changed = 1)
change_scale(2)
change_scale(scale_changed = 5)