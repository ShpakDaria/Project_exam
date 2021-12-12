#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Button, messagebox, Canvas, filedialog, Label, Menu, CENTER, Scale
from PIL import ImageTk, Image, ImageFilter, ImageDraw, ImageOps
import random

class Example(Frame):
    def __init__(self, parent):  # Создание окна __init__ - инициализация окна
        Frame.__init__(self, parent) #self - аргумент позволяющий остальным функциям ссылаться к этому окну, parent - агрумент для наследования, обозначает родительский класс

        self.parent = parent
        self.create_menu()

        self.image = None
        self.photo = None

        self.display = Canvas(self.parent, bg="#706f6f")  # Создаём холст куда будем загружать изображение
        self.display.bind_all("<MouseWheel>", self._on_mousewheel)#Назнчаение колёсика мишы для функции скрола экрана
        self.display_img = self.display.create_image(0, 0)
        self.display.place(relx=0, rely=0, relwidth=0.88, relheight=1)

    def open(self):  # Подпрограмма для отрытия изображения
        self.filename = filedialog.askopenfilename()
        if self.filename:
            self.image = Image.open(self.filename)
            self.photo = ImageTk.PhotoImage(self.image)
            self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

            self.file_menu.entryconfig("Save", state='active')
            self.file_menu.entryconfig("Clear", state='active')

            self.btn_yar.config(state="normal")
            self.btn_contr.config(state="normal")
            self.btn_cvb.config(state="normal")
            self.btn_neg.config(state="normal")
            self.btn_shy.config(state="normal")
            self.btn_sep.config(state="normal")
            self.btn_blu.config(state="normal")
            self.btn_con.config(state="normal")

    def save(self): # Функция для сохранения изображения
        path = filedialog.asksaveasfilename(initialdir="D:\БГПУ\Курсовая работа\Photo editor\desktop.ini",
                                            title="Select file",
                                            filetypes=(
                                            ("PNG files", "*.png"), ("JPG files", "*.jpg"), ("JPG 2000 files", "*.jp2"),
                                            ("TIFF files", "*.tiff"), ("BMP files", "*.bmp"), ("All files", "*.*")),
                                            defaultextension=((".png"), (".jpg"), (".jp2"), (".tiff"), (".bmp")))
        if path:
            try:
                self.image.save(path)
                messagebox.showinfo('Preservation', 'File saved.')
            except KeyError:
                messagebox.showerror('Error', 'No extension specified')

    def clear(self):  # Попрограмма для отчистки
        self.image = Image.open(self.filename)
        self.photo = ImageTk.PhotoImage(self.image)
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def close(self):  # Блок программы который будет запускаться по нажатию кнопки "Выход" и выдавать модальное окно с подтверждением
        if messagebox.askyesno('Exit', 'Are you sure??'):
            self.parent.destroy()

    def _on_mousewheel(self, event):
        self.display.yview_scroll((event.delta // 120), "units")


    def brightness(self):  # Функция изменения яркости изображения
        draw = ImageDraw.Draw(self.image)
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        factor = self.scale.get()
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0] + factor
                b = pix[i, j][1] + factor
                c = pix[i, j][2] + factor
                if (a < 0):
                    a = 0
                if (b < 0):
                    b = 0
                if (c < 0):
                    c = 0
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
        self.photo = ImageTk.PhotoImage(self.image)
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def brightness_click(self):  # Функция для создания окна изменения яркости изображения
        root = Tk()
        root.geometry('%dx%d+%d+%d' % (150, 100, 400, 400))
        label = Label(root, text='Select the brightness value')
        label.pack(anchor=CENTER)

        self.scale = Scale(root, from_=-100, to=100, orient="horizontal")
        self.scale.pack(anchor=CENTER)

        def reset_brightness():
            self.brightness()

        def close():
            root.destroy()

        button_rnd = Button(root, text="Ok", command=reset_brightness)
        button_rnd.place(x=25, y=62)
        button_close = Button(root, text="Close", command=close)
        button_close.place(x=70, y=62)

    def blur(self):  # Функция для наложения фильтра BLUR на изображение
        self.image = self.image.filter(ImageFilter.BLUR)
        self.photo = ImageTk.PhotoImage(self.image)
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def contour(self):  # Подпрограмма для Контура
        self.image = self.image.filter(ImageFilter.CONTOUR)
        self.photo = ImageTk.PhotoImage(self.image)
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def contrast(self):  # Подпрограмма для изменения контраста
        draw = ImageDraw.Draw(self.image)  # Получаем изображение и информацию по нему
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        factor = self.scale_contrast.get()  # Получаем значение которое было указано в одпрограмме contrast_click()
        contrast1 = (259 * (factor + 255)) / (255 * (259 - factor))
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                a = round(contrast1 * (a - 128) + 128)
                b = round(contrast1 * (b - 128) + 128)
                c = round(contrast1 * (c - 128) + 128)
                if (a < 0):
                    a = 0
                if (b < 0):
                    b = 0
                if (c < 0):
                    c = 0
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def contrast_click(self):  # Подпрограмма для создания окна  Контраста
        root_contrast = Tk()  # Открываем новое окно
        root_contrast.geometry('%dx%d+%d+%d' % (150, 100, 400, 400))  # Создаём горизонтальну полос со значениями от -100 до 100
        label_contrast = Label(root_contrast, text='Choose a contrast value')
        label_contrast.pack(anchor=CENTER)
        self.scale_contrast = Scale(root_contrast, from_=-100, to=100, orient="horizontal")
        self.scale_contrast.pack(anchor=CENTER)

        def reset_contrast():  # Подпрограмма отвечающая за кномку ОК
            self.contrast()

        def close():  # Подпрограмма отвечающая за кномку Закрыть
            root_contrast.destroy()

        button_rnd = Button(root_contrast, text="Ok", command=reset_contrast)  # Создание кнопки при нажатие на которую будет обрабатываться программа contrast
        button_rnd.place(x=25, y=62)
        button_close = Button(root_contrast, text="Close", command=close)  # Создание кнопки при нажатие на которую окно закроеться
        button_close.place(x=70, y=62)

    def rgb_balans(self): # Подпрограмма для изменения rgb баланса
        draw = ImageDraw.Draw(self.image)  # Получаем изображение и информацию по нему
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        for i in range(width):  # Начинаем цикл, чтобы пройти по каждому пикселю изображения
            for j in range(height):
                a = pix[i, j][0] + self.scale_r.get()  # К полученному значению каждого цветового канала пикселя, прибавляются значения из rgb_balans_click
                b = pix[i, j][1] + self.scale_g.get()
                c = pix[i, j][2] + self.scale_b.get()
                if (a < 0):  # Устанавливаем ограничения, чтобы при покраске рисунка у нас не было ошибок
                    a = 0
                if (b < 0):
                    b = 0
                if (c < 0):
                    c = 0
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))  # Переносим результат на изображение,  i, j - это координаты пикселя, а переменные a, b, c - это каналы RGB
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def rgb_balans_click(self):  # Подпрограмма для создания окна rgb баланса
        root_rgb_balans = Tk()  # Открываем новое окно
        root_rgb_balans.geometry('%dx%d+%d+%d' % (200, 225, 400, 400))

        label_r = Label(root_rgb_balans, text='Choose the value of red')  # Создаём горизонтальные полосы со значениями от -256 до 256
        label_r.pack(anchor=CENTER)
        self.scale_r = Scale(root_rgb_balans, from_=-256, to=256, orient="horizontal")
        self.scale_r.pack(anchor=CENTER)

        label_g = Label(root_rgb_balans, text='Choose the green value')
        label_g.pack(anchor=CENTER)
        self.scale_g = Scale(root_rgb_balans, from_=-256, to=256, orient="horizontal")
        self.scale_g.pack(anchor=CENTER)

        label_b = Label(root_rgb_balans, text='Choose the blue value')
        label_b.pack(anchor=CENTER)
        self.scale_b = Scale(root_rgb_balans, from_=-256, to=256, orient="horizontal")
        self.scale_b.pack(anchor=CENTER)

        def reset_rgb_balans():  # Подпрограмма отвечающая за кномку ОК
            self.rgb_balans()

        def close():  # Подпрограмма отвечающая за кномку Закрыть
            root_rgb_balans.destroy()

        button_rnd = Button(root_rgb_balans, text="Ok", command=reset_rgb_balans)  # Создание кнопку при нажатие на которую будет обрабатываться программа rgb_balans
        button_rnd.place(x=45, y=190)
        button_close = Button(root_rgb_balans, text="Close", command=close)  # Создание кнопку при нажатие на которую окно закроеться
        button_close.place(x=100, y=190)

    def negativ_clic(self):  # Подпрограмма для фильтра негатив
        draw = ImageDraw.Draw(self.image)  # Получаем изображение и информацию по нему
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        for i in range(width):  # Начинаем цикл, чтобы пройти по каждому пикселю изображения
            for j in range(height):
                a = pix[i, j][0]  # Записываем значение звета пиксельно
                b = pix[i, j][1]
                c = pix[i, j][2]
                draw.point((i, j), ( 255 - a, 255 - b, 255 - c))  # Вычитаем из 255 значение нашего цветного канала для текущего пикселя
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def rnd_noise(self): # Подпрограмма для фильтра шум
        draw = ImageDraw.Draw(self.image)  # Получаем изображение и информацию по нему
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        factor = self.scale_rnd.get()  # Получаем значение которое было указано в одпрограмме rnd_noise_click
        for i in range(width):
            for j in range(height):
                rand = random.randint(-factor, factor)
                a = pix[i, j][0] + rand
                b = pix[i, j][1] + rand
                c = pix[i, j][2] + rand
                if (a < 0):
                    a = 0
                if (b < 0):
                    b = 0
                if (c < 0):
                    c = 0
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def rnd_noise_click(self):  # Попрограмма для создания окна шума
        root = Tk()  # Открываем новое окно
        root.geometry('%dx%d+%d+%d' % (150, 100, 400, 400))  # Создаём горизонтальную полосу со значениями от 0 до 100

        label_rnd = Label(root, text='Choose a noise value')
        label_rnd.pack(anchor=CENTER)

        self.scale_rnd = Scale(root, from_=0, to=100, orient="horizontal")
        self.scale_rnd.pack(anchor=CENTER)

        def reset_rnd():  # Подпрограмма отвечающая за кномку ОК
            self.rnd_noise()

        def close():  # Подпрограмма отвечающая за кномку Закрыть
            root.destroy()

        button_rnd = Button(root, text="Ok", command=reset_rnd)  # Создание кнопку при нажатие на которую будет обрабатываться программа rnd_noise
        button_rnd.place(x=25, y=62)
        button_close = Button(root, text="Close", command=close)  # Создание кнопку при нажатие на которую окно закроеться
        button_close.place(x=70, y=62)

    def sepia_click(self):  # Попрограмма для сепии
        depth = 30  # Создаём пременную (коэффициент) со значение 30
        draw = ImageDraw.Draw(self.image)  # Получаем изображение и информацию по нему
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                a = S + depth * 2
                b = S + depth
                c = S
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def black_white_click(self):  # Попрограмма для чёрно-белого фильтра
        draw = ImageDraw.Draw(self.image)  # Получаем изображение и информацию по нему
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = a + b + c
                if (S > (((255) // 2) * 3)):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                draw.point((i, j), (a, b, c))
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def gray_click(self):  # Попрограмма для серого фильтра
        draw = ImageDraw.Draw(self.image)  # Получаем изображение и информацию по нему
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        for i in range(width):  # Начинаем цикл, чтобы пройти по каждому пикселю изображения
            for j in range(height):
                a = pix[i, j][0]  # Записываем значение звета пиксельно
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3  # Значения цветовых каналов равняется среднему арифметическому
                draw.point((i, j), (S, S, S))  # Переносим результат на изображение,  i, j - это координаты пикселя, а переменные S - это среднее арифметическое значение RGB каналов
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def rnd_red_click(self):  # Попрограмма для красного фильтра
        draw = ImageDraw.Draw(self.image)  # Получаем изображение и информацию по нему
        width = self.image.size[0]
        height = self.image.size[1]
        pix = self.image.load()
        for i in range(width):  # Начинаем цикл, чтобы пройти по каждому пикселю изображения
            for j in range(height):
                a = pix[i, j][0]  # Записываем значение цвета пиксельно
                b = pix[i, j][1]
                c = pix[i, j][2]
                Red = (255 - (255 - a))  # к цветовому каналу, отвечающему за красный цвет, прибавляется случайное значение из диапазона от 0 до 255. Если результирующее значение больше 255, то оно равняется 255
                if b > 10:
                    b = b // 100
                if c > 10:
                    c = c // 100
                draw.point((i, j), (Red, b, c))  # Переносим результат на изображение,  i, j - это координаты пикселя, а переменные Red, b, c - это каналы RGB
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def rnd_green_click(self):  # Попрограмма для зелёного фильтра
        draw = ImageDraw.Draw(self.image)  # Создаем инструмент для рисования # Получаем изображение и информацию по нему
        width = self.image.size[0]  # Определяем ширину
        height = self.image.size[1]  # Определяем высоту
        pix = self.image.load()  # Выгружаем значения пикселей
        for i in range(width):  # Начинаем цикл, чтобы пройти по каждому пикселю изображения
            for j in range(height):
                a = pix[i, j][0]  # Записываем значение цвета пиксельно
                b = pix[i, j][1]
                c = pix[i, j][2]
                Green = (255 - (255 - b))
                if a > 10:
                    a = a // 100
                if c > 10:
                    c = c // 100
                draw.point((i, j), (a, Green, c))
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def rnd_blue_click(self):  # Попрограмма для синего фильтра
        draw = ImageDraw.Draw(self.image)  # Создаем инструмент для рисования # Получаем изображение и информацию по нему
        width = self.image.size[0]  # Определяем ширину
        height = self.image.size[1]  # Определяем высоту
        pix = self.image.load()  # Выгружаем значения пикселей
        for i in range(width):  # Начинаем цикл, чтобы пройти по каждому пикселю изображения
            for j in range(height):
                a = pix[i, j][0]  # Записываем значение цвета пиксельно
                b = pix[i, j][1]
                c = pix[i, j][2]
                Blue = (255 - (255 - c))
                if a > 10:
                    a = a // 100
                if b > 10:
                    b = b // 100
                draw.point((i, j), (a, b, Blue))
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")
        del draw

    def detall(self): #Фильтр детализации
        self.image = self.image.filter(ImageFilter.DETAIL)
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def edge_enhance(self): #Фильтр улучшение краёв
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def emboss(self): #Фильтр рельеф
        self.image = self.image.filter(ImageFilter.EMBOSS)
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def find_edges(self): #Фильтр поиск по краю
        self.image = self.image.filter(ImageFilter.FIND_EDGES)
        self.photo = ImageTk.PhotoImage(self.image)  # Показываем результат.
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def rotate(self, degrees): #Функция для поворота
        self.image = self.image.rotate(degrees, expand=1)
        self.photo = ImageTk.PhotoImage(self.image)
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def flip(self, flip_type): #Функция для флипа
        if flip_type == "horizontally":
            self.image = ImageOps.mirror(self.image)
        elif flip_type == "vertically":
            self.image = ImageOps.flip(self.image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def resize(self, percents): #Функция для изменения размера изображения
        width = self.image.size[0]
        height = self.image.size[1]
        width = (width * percents) // 100
        height = (height * percents) // 100
        self.image = self.image.resize((width, height), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.display.itemconfigure(self.display_img, image=self.photo, anchor="nw")

    def create_menu(self):  # Главное меню
        menu = Menu(self.parent)  # Обозначаем создание меню

        self.file_menu = Menu(menu)  # Присваеваем меню 4 вкладки
        self.transform_menu = Menu(menu)
        self.filters_menu = Menu(menu)
        self.parametr_menu = Menu(menu)

        self.rotate_menu = Menu(self.transform_menu)
        self.flip_menu = Menu(self.transform_menu)
        self.resize_menu = Menu(self.transform_menu)
        self.color_menu = Menu(self.filters_menu)

        menu.add_cascade(label="File", menu=self.file_menu)  # Присваеваем вкладкам название
        menu.add_cascade(label="Transformation", menu=self.transform_menu)
        self.transform_menu.add_cascade(label="Rotation", menu=self.rotate_menu)
        self.transform_menu.add_cascade(label="Flip", menu=self.flip_menu)
        self.transform_menu.add_cascade(label="Scaling", menu=self.resize_menu)
        menu.add_cascade(label="Options", menu=self.parametr_menu)
        menu.add_cascade(label="Filters", menu=self.filters_menu)
        self.filters_menu.add_cascade(label="Color", menu=self.color_menu)

        self.file_menu.add_command(label="Open", command=self.open)  # Создаём подкатегории в меню во вкладке Фаил
        self.file_menu.add_command(label="Save", command=self.save, state='disabled')
        self.file_menu.add_command(label="Clear", command=self.clear, state='disabled')
        self.file_menu.add_separator()  # Разделяющая линия
        self.file_menu.add_command(label="Exit", command=self.close)

        self.rotate_menu.add_command(label="Rotation left on 90", command=lambda: self.rotate(90))
        self.rotate_menu.add_command(label="Rotation left on 180", command=lambda: self.rotate(180))
        self.rotate_menu.add_command(label="Rotation right on 90", command=lambda: self.rotate(-90))
        self.rotate_menu.add_command(label="Rotation right on 180", command=lambda: self.rotate(-180))

        self.flip_menu.add_command(label="Flip horizontally", command=lambda: self.flip("horizontally"))
        self.flip_menu.add_command(label="Flip vertically", command=lambda: self.flip("vertically"))

        self.resize_menu.add_command(label="25% of original size", command=lambda: self.resize(25))
        self.resize_menu.add_command(label="50% of original size", command=lambda: self.resize(50))
        self.resize_menu.add_command(label="75% of original size", command=lambda: self.resize(75))
        self.resize_menu.add_command(label="125% of original size", command=lambda: self.resize(125))
        self.resize_menu.add_command(label="150% of original size", command=lambda: self.resize(150))
        self.resize_menu.add_command(label="200% of original size", command=lambda: self.resize(200))

        self.parametr_menu.add_command(label="Brightness", command=self.brightness_click)  # Создаём подкатегории в меню во вкладке Параметры
        self.parametr_menu.add_command(label="Contrast", command=self.contrast_click)
        self.parametr_menu.add_command(label="RGB balance", command=self.rgb_balans_click)

        self.filters_menu.add_command(label="Negative", command=self.negativ_clic)  # Создаём подкатегории в меню во вкладке Фильтры
        self.filters_menu.add_command(label="Noise", command=self.rnd_noise_click)
        self.filters_menu.add_command(label="Sepia", command=self.sepia_click)
        self.filters_menu.add_command(label="Blur", command=self.blur)
        self.filters_menu.add_command(label="Contour", command=self.contour)
        self.filters_menu.add_command(label="Detall", command=self.detall)
        self.filters_menu.add_command(label="Edge Enhance", command=self.edge_enhance)
        self.filters_menu.add_command(label="Emboss", command=self.emboss)
        self.filters_menu.add_command(label="Find Edges", command=self.find_edges)
        self.color_menu.add_command(label="Black and white", command=self.black_white_click)
        self.color_menu.add_command(label="Gray filter", command=self.gray_click)
        self.color_menu.add_command(label="Red filter", command=self.rnd_red_click)
        self.color_menu.add_command(label="Green filter", command=self.rnd_green_click)
        self.color_menu.add_command(label="Blue filter", command=self.rnd_blue_click)

        label_fail_par = Label(root, bg="#585858", font="Berlin 16", text='Options', fg="#ffffff")
        label_fail_par.place(relx=0.905, rely=0.03)
        self.btn_yar = Button(text="Brightness", height=2, width=12, command=self.brightness_click)
        self.btn_yar.place(relx=0.899, rely=0.09)
        self.btn_contr = Button(text="Contrast", height=2, width=12, command=self.contrast_click)  # Создание кнопки Контрастность
        self.btn_contr.place(relx=0.899, rely=0.16)  # Размещение кнопки
        self.btn_cvb = Button(text="RGB balance", height=2, width=12, command=self.rgb_balans_click)  # Создание кнопки RGB баланс
        self.btn_cvb.place(relx=0.899, rely=0.23)  # Размещение кнопки
        label_fail_par = Label(root, bg="#585858", font="Berlin 16", text='Filters', fg="#ffffff")
        label_fail_par.place(relx=0.91, rely=0.32)
        self.btn_neg = Button(text="Negative", height=2, width=12, command=self.negativ_clic)
        self.btn_neg.place(relx=0.899, rely=0.38)  # Размещение кнопки
        self.btn_shy = Button(text="Noise", height=2, width=12, command=self.rnd_noise_click)
        self.btn_shy.place(relx=0.899, rely=0.45)
        self.btn_sep = Button(text="Sepia", height=2, width=12, command=self.sepia_click)
        self.btn_sep.place(relx=0.899, rely=0.52)
        self.btn_blu = Button(text="Blur", height=2, width=12, command=self.blur)
        self.btn_blu.place(relx=0.899, rely=0.59)
        self.btn_con = Button(text="Contour", height=2, width=12, command=self.contour)
        self.btn_con.place(relx=0.899, rely=0.66)

        self.parent.config(menu=menu)  # Передаём окну параметр того что будет создано меню

if __name__ == '__main__':
    root = Tk()
    root.title("Photo editor")
    root.geometry("1200x650+150+70")
    root["bg"] = "#585858"
    app = Example(root)
    root.mainloop()
