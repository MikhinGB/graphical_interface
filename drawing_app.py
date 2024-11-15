import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, OptionMenu, Label, Text
from tkinter.simpledialog import askinteger, askstring
from PIL import Image, ImageDraw, ImageFont


class DrawingApp:

    def __init__(self, root):

        self.clicks = 0

        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.canvas_color = 'white'
        self.width = 600
        self.height = 400
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg=self.canvas_color)
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

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color_button)
        color_button.pack(side=tk.LEFT)

        color_canvas_button = tk.Button(control_frame, text="Изменить фон", command=self.change_canvas_color)
        color_canvas_button.pack(side=tk.LEFT)

        text_button = tk.Button(control_frame, text="Текст", command=self.create_text_user)
        text_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(control_frame, text="Ластик", command=self.erase)
        self.eraser_button.pack(side=tk.RIGHT)

        self.canvas_sizes_button = tk.Button(control_frame, text=f"Холст {self.width}x{self.height}",
                                             command=self.canvas_resize)
        self.canvas_sizes_button.pack(side=tk.RIGHT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        sizes = [1, 2, 5, 10]

        self.brush_size_menu = OptionMenu(control_frame,
                                          self.brush_size_scale,
                                          *sizes)
        self.brush_size_menu.pack(side=tk.LEFT)

        self.lbl_color = Label(control_frame, text="ink")
        self.lbl_color.configure(bg="black")
        self.lbl_color.pack(side=tk.LEFT)

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

    def choose_color_button(self):
        """ Эта функция вызывается при однократном нажатии кнопки "Выбрать цвет".
        Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти."""

        self.clicks = 0
        self.pen_color_in = colorchooser.askcolor(color=self.pen_color_in)[1]
        self.pen_color = self.pen_color_in
        self.lbl_color.configure(bg=self.pen_color)

    def choose_color(self, event):
        """ Эта функция вызывается  горячими клавишами "Control-c".
        Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти."""

        self.clicks = 0
        self.pen_color_in = colorchooser.askcolor(color=self.pen_color_in)[1]
        self.pen_color = self.pen_color_in
        self.lbl_color.configure(bg=self.pen_color)

    def create_text_user(self):
        """ Эта функция вызывается при однократном нажатии кнопки "Текст".
        Открывает стандартное диалоговое окно для ввода текста.
        Далее вызывет функцию text_placement  для размещения текста в указанное курсором место канваса по клику левой
        кнопки мышки"""
        self.user_text = askstring('Ввод текста', 'подсказка')
        self.canvas.bind('<Button-1>', self.text_placement)

    def text_placement(self, event):
        """ Эта функция вызывается при однократном нажатии левой кнопки мышки.
            Размещает текст, набранный пользователем по вызову функции create_text_user, в указанное курсором место
            канваса.
            """
        x = event.x
        y = event.y
        fnt = ImageFont.truetype("FreeMono.ttf", 40)
        self.canvas.create_text(x, y, text=self.user_text, fill=self.pen_color)
        self.draw.text((x, y), self.user_text, font=fnt, fill=self.pen_color)

    def change_canvas_color(self):
        """ Эта функция вызывается при однократном нажатии кнопки "Изменить фон".
                Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий фон."""

        self.canvas_color = colorchooser.askcolor(color=self.canvas_color)[1]
        self.canvas.configure(bg=self.canvas_color)

    def canvas_resize(self):
        """ Эта функция вызывается нажатием кнопки "Холст w * h".
                Открывает стандартное диалоговое окно выбора ширины холста. После нажатия кнопки "ОК" открывается
                стандартное диалоговое окно выбора высоты холста. После нажатия кнопки "ОК" холст изменяется в размерах
                в соответствии с введенными значениями. На кнопке "Холст w * h"  отражаются  новые значения  размеров
                ширины и высоты холста"""
        size_image = ()
        self.width = askinteger("Ширина", "Целое, pix")
        size_image += (self.width,)
        self.height = askinteger("Высота", "Целое, pix")
        size_image += (self.height,)

        self.image = Image.new("RGB", size=size_image, color='white')
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.config(width=self.width, height=self.height)
        self.canvas_sizes_button.configure(text=f"Холст {self.width}x{self.height}")

    def pick_color(self, event):
        """ Эта функция вызывается при однократном нажатии ПРАВОЙ кнопки мышки.

        Переназначает цвет чернил пера по соответствующему пикселю канваса, на который (пиксель) указывает курсор.

        При этом, кнопка "ЛАСТИК" переводится в дезактивированное состояние.
        """

        self.clicks = 0  # кнопка "ЛАСТИК" переводится в дезактивированное состояние
        x = event.x
        y = event.y

        r_g_b = self.image.getpixel((x, y))  # получаем кортеж трех целых чисел, например (255, 0, 0) КРАСНЫЙ

        self.pen_color_in = self.get_rgb(r_g_b)
        self.pen_color = self.pen_color_in
        self.lbl_color.configure(bg=self.pen_color)

    def save_image(self, event):
        """ Эта функция вызывается при однократном нажатии кнопки "Сохранить" или горячими клавишами "Control-s".
        Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
        Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении."""

        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def get_rgb(self, rgb):
        """  Функция преобразует (конвертирует) кортеж трех целых чисел RGB-составляющих, например (255, 0, 0) КРАСНЫЙ в
        шестнадцатеричный код цвета в формате #RRGGBB """
        return "#%02x%02x%02x" % rgb

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
