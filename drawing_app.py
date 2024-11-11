import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, OptionMenu
from PIL import Image, ImageDraw


class DrawingApp:

    def __init__(self, root):

        self.clicks = 0

        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.canvas_color = 'white'
        self.canvas = tk.Canvas(root, width=600, height=400, bg=self.canvas_color)
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color_in = 'black'
        self.pen_color = self.pen_color_in

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.canvas.bind('<Button-3>', self.pick_color)

        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)


    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(control_frame, text="Ластик", command=self.erase)
        self.eraser_button.pack(side=tk.RIGHT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        sizes = [1, 2, 5, 10]

        self.brush_size_menu = OptionMenu(control_frame,
                                             self.brush_size_scale,
                                             *sizes)
        self.brush_size_menu.pack(side=tk.LEFT)

    def paint(self, event):
        """ Функция вызывается при движении мыши с нажатой левой кнопкой по холсту. Она рисует линии на холсте Tkinter
        и параллельно на объекте Image из Pillow:
        - event: Событие содержит координаты мыши, которые используются для рисования.
        - Линии рисуются между текущей и последней зафиксированной позициями курсора, что создает непрерывное
        изображение."""

        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def erase(self):
        """ Эта функция вызывается при однократном нажатии кнопки "Ластик".
        Активирует счетчик нажатий. Значение счетчика  НЕЧЕТНОЕ - кнопка активирована. Цвет чернил соответствует
        цвету канваса. Значение счетчика  ЧЕТНОЕ - кнопка дезактивирована. Цвет чернил соответствует цвету,
        действующему до момента активации кнопки "ЛАСТИК"

        """

        self.clicks += 1
        if self.clicks % 2 == 0:
            self.pen_color = self.pen_color_in
        else:
            self.pen_color = self.canvas_color

    def reset(self, event):
        """ Сбрасывает последние координаты кисти. Это необходимо для корректного начала новой линии после того,
        как пользователь отпустил кнопку мыши и снова начал рисовать."""

        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """ Эта функция вызывается при однократном нажатии кнопки "Очистить".
        Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDraw для нового изображения."""

        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event):
        """ Эта функция вызывается при однократном нажатии кнопки "Выбрать цвет".
        Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти."""

        self.clicks = 0
        self.pen_color_in = colorchooser.askcolor(color=self.pen_color_in)[1]
        self.pen_color = self.pen_color_in

    def pick_color(self, event):
        """ Эта функция вызывается при однократном нажатии ПРАВОЙ кнопки мышки.

        Переназначает цвет чернил пера по соответствующему пикселю канваса, на который (пиксель) указывает курсор.

        При этом, кнопка "ЛАСТИК" переводится в дезактивированное состояние.
        """
        r = '';  g = ''; b = ''

        self.clicks = 0   # кнопка "ЛАСТИК" переводится в дезактивированное состояние
        x = event.x
        y = event.y

        r_g_b = self.image.getpixel((x, y))  # получаем кортеж трех целых чисел, например (255, 0, 0) КРАСНЫЙ
        for i in range(3):
            x = str(hex(r_g_b[i]))   # преобразуем полученные значения в шестнадцатиричную систему, приводим к строке
            if len(x) == 3:
                x = x + '0'
            x = x[2:4]
            if i == 0:
                r = x
            elif i == 1:
                g = x
            else:
                b = x
        r_g_b = '#' + r + g + b     # формируем итоговую строку - значение цвета
        self.pen_color_in = r_g_b
        self.pen_color = self.pen_color_in

    def save_image(self, event):
        """ Эта функция вызывается при однократном нажатии кнопки "Сохранить".
        Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
        Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении."""

        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
