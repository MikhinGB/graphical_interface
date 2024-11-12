# graphical_interface
Программа для создания изображений на основе TKinter.
Данная программа представляет собой пример использования библиотеки TKinter для создания графического интерфейса.
Класс DrawingApp


Инициализация __init__(self, root)

Конструктор класса принимает один параметр:

- root: Это корневой виджет Tkinter, который служит контейнером для всего интерфейса приложения.



Внутри конструктора выполняются следующие ключевые действия:

- Устанавливается заголовок окна приложения.

- Создается объект изображения (self.image) с использованием библиотеки Pillow. Это изображение служит виртуальным холстом, на котором происходит рисование. Изначально оно заполнено белым цветом.

- Инициализируется объект ImageDraw.Draw(self.image), который позволяет рисовать на объекте изображения.

- Создается виджет Canvas Tkinter, который отображает графический интерфейс для рисования. Размеры холста установлены в 600x400 пикселей.

- Вызывается метод self.setup_ui(), который настраивает элементы управления интерфейса.

- Привязываются обработчики событий к холсту для отслеживания движений мыши при рисовании () и сброса состояния кисти при отпускании кнопки мыши ().



Метод setup_ui(self)

Этот метод отвечает за создание и расположение виджетов управления:


- Кнопки "Очистить", "Выбрать цвет" и "Сохранить" позволяют пользователю очищать холст, выбирать цвет кисти и сохранять текущее изображение соответственно.

- Слайдер для изменения размера кисти дает возможность выбирать толщину линии от 1 до 10 пикселей. Рядом - меню выбора толщины линии.
![Выбор толщины линии](https://github.com/MikhinGB/graphical_interface/blob/main/png3.png)  
- Кнопка "Ластик" позволяет пользователю частично подчищать нарисованное. Повторное нажатие кнопки (дезактивация кнопки) возвращает в состояние рисования цветом, что использовался до активации данной кнопки.


Метод paint(self, event)

Функция вызывается при движении мыши с нажатой левой кнопкой по холсту. Она рисует линии на холсте Tkinter и параллельно на объекте Image из Pillow:

- event: Событие содержит координаты мыши, которые используются для рисования.

- Линии рисуются между текущей и последней зафиксированной позициями курсора, что создает непрерывное изображение.



Метод reset(self, event)

Сбрасывает последние координаты кисти. Это необходимо для корректного начала новой линии после того, как пользователь отпустил кнопку мыши и снова начал рисовать.



Метод clear_canvas(self)

Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDrawдля нового изображения.



Метод choose_color(self)

Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.
![Выбор цвета кисти](https://github.com/MikhinGB/graphical_interface/blob/main/png5.png)


Методы, связанные с выбором цвета кисти, изменяют соответствуюшим образом цвет индикаторного окошка "ink" ("чернила").
![Изменение цвета окошка ink](https://github.com/MikhinGB/graphical_interface/blob/main/png6.png)




Метод save_image(self)

Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла. Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.



Обработка событий

- : Событие привязано к методу paint, позволяя рисовать на холсте при перемещении мыши с нажатой левой кнопкой.

- : Событие привязано к методу reset, который сбрасывает состояние рисования для начала новой линии.



Использование приложения

Пользователь может рисовать на холсте, выбирать цвет и размер кисти, очищать холст и сохранять в формате PNG.
