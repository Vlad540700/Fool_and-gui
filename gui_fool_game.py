from pathlib import Path
from tkinter import (RAISED, SUNKEN, Button, Entry, Frame, Label, PhotoImage,
                     Radiobutton, StringVar, Tk, W)

from PIL import Image, ImageTk


class BaseApplication(Frame):
    def calculate_geometry(self):
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.master.geometry(f"+{x}+{y}")

class Application1(BaseApplication):
    def __init__(self, master):
        super(Application1, self).__init__(master)
        self.grid()
        self.new_widgets = []
        self.list_number_of_players = []
        self.number_players = 2
        self.error_labels = []
        self.players = []
        self.create_widgets()

    def create_widgets(self):
        Label(
            self,
            text="Добро пожаловать! Сейчас мы узнаем кто дурак)"
        ).grid(row=0, column=0, columnspan=3, sticky=W)

        Label(
            self,
            text='Сколько игроков участвует? (2-5):'
        ).grid(row=1, column=0, sticky=W)
        self.body_part = StringVar()
        self.body_part.set(None)
        body_parts = ['2', '3', '4', '5']
        column = 1
        for part in body_parts:
            Radiobutton(
                self,
                text=part,
                variable=self.body_part,
                value=part,
                command=self.additional_widgets
            ).grid(row=1, column=column)
            column += 1

    def limit_char_count(self, event, index):
        entry = self.list_number_of_players[index]
        text = entry.get()
        if len(text) > 20:
            entry.delete(20, 'end')

    def on_key_press(self, event):
        if event.keysym == 'space':
            return 'break'

    def additional_widgets(self):
        self.number_players = int(self.body_part.get())
        for widget in self.new_widgets:
            widget.destroy()
        for player in self.list_number_of_players:
            player.destroy()
        self.list_number_of_players = [0] * (self.number_players)
        for part in range(1, self.number_players+1):
            widget = Label(
                self,
                text=f'Имя {part} игрока:'
            )
            widget.grid(row=part+3, column=0, sticky=W)
            self.list_number_of_players[part-1] = Entry(self)
            self.list_number_of_players[part-1].grid(
                row=part+3,
                column=1,
                columnspan=4,
                sticky=W
            )
            self.list_number_of_players[part-1].bind(
                '<KeyRelease>',
                lambda event, index=part-1: self.limit_char_count(
                    event,
                    index
                )
            )
            self.list_number_of_players[part-1].bind(
                '<KeyPress>',
                lambda event: self.on_key_press(event)
            )
            self.new_widgets.append(widget)
            if part == int(self.number_players):
                btn = Button(self, text="Закрыть", command=self.click)
                btn.grid(row=part+4, column=0, columnspan=5)
                self.new_widgets.append(btn)

    def click(self):
        for label in self.error_labels:
            label.destroy()
        for player in range(self.number_players):
            person = self.list_number_of_players[player].get()
            if len(person) < 2:
                self.list_number_of_players[player].config(bg='red')
                error_label = Label(
                    self,
                    text='Имя должно быть больше 1 символов',
                    fg='red'
                )
                error_label.grid(row=player+4, column=6, sticky=W)
                self.error_labels.append(error_label)
            else:
                self.list_number_of_players[player].config(bg='white')
                self.players.append(person)

        if len(self.players) == self.number_players:
            self.master.destroy()
        else:
            self.players = []

    def return_number_and_list_players(self):
        return (self.number_players, self.players)


class Application2(BaseApplication):
    def __init__(
            self,
            master,
            name_plaer,
            cards_on_table,
            cards_on_hand,
            number_cards_deck,
            trump_suit,
            option
    ):
        super(Application2, self).__init__(master)
        self.grid()
        self.array = [None] * 12
        self.array1 = [None] * 36
        self.name_plaer = name_plaer
        self.cards_on_table = cards_on_table
        self.cards_on_hand = cards_on_hand
        self.number_cards_deck = number_cards_deck
        self.trump_suit = trump_suit
        self.option = option
        self.select_card = None
        self.create_widgets()

    def create_widgets(self):
        Label(
            self,
            text=f'{self.name_plaer} твой ход'
        ).grid(row=0, column=0, columnspan=6)
        Label(
            self,
            text="На столе сейчас такие карты"
        ).grid(row=1, column=0, columnspan=6)
        self.image = PhotoImage(file=f'image/{self.trump_suit}.png')
        self.resized_image = self.image.subsample(5, 6)
        bg_logo = Label(self, image=self.resized_image)
        bg_logo.grid(row=0, column=6, rowspan=2, columnspan=2)
        Label(
            self,
            font=('Comic Sans MS', 10, 'bold'),
            text=f'В колоде: {self.number_cards_deck}',
        ).grid(row=3, column=6, sticky=W)
        if self.cards_on_table == []:
            Label(
                self,
                font=('Comic Sans MS', 15, 'bold'),
                text='<Пусто>',
            ).grid(row=3, column=0,  columnspan=6)
        else:
            column1 = 0
            for index, value in enumerate(self.cards_on_table):
                if index % 2 == 0:
                    self.array[index] = ImageTk.PhotoImage(
                        Image.open(
                            f'image/{value}.png'
                        ).resize((
                            int(Image.open(f'image/{value}.png').width * 0.7),
                            int(Image.open(f'image/{value}.png').height * 0.7)
                            ),
                            resample=Image.Resampling.LANCZOS
                        )
                    )
                    label = Label(self, image=self.array[index])
                    label.grid(row=3, column=column1, sticky=W)
                else:
                    self.array[index] = ImageTk.PhotoImage(
                        Image.open(
                            f'image/{value}.png'
                        ).resize((
                            int(Image.open(f'image/{value}.png').width * 0.7),
                            int(Image.open(f'image/{value}.png').height * 0.7)
                            ),
                            resample=Image.Resampling.LANCZOS
                        )
                    )
                    label = Label(self, image=self.array[index])
                    label.grid(row=4, column=column1)
                    column1 += 1
        Label(
            self,
            text="Твои карты:"
        ).grid(row=5, column=0, columnspan=6)
        row2 = 6
        column2 = 0
        if self.cards_on_hand == []:
            Label(
                self,
                font=('Comic Sans MS', 15, 'bold'),
                text='<Пусто>',
            ).grid(row=row2, column=0,  columnspan=6)
        else:
            def on_enter(event):
                event.widget.config(relief=SUNKEN)

            def on_leave(event):
                event.widget.config(relief=RAISED)
            for index, value in enumerate(self.cards_on_hand):
                if index % 6 == 0:
                    column2 = 0
                else:
                    column2 += 1
                if index % 6 == 0 and index != 0:
                    row2 += 1
                self.array1[index] = ImageTk.PhotoImage(
                        Image.open(
                            f'image/{value}.png'
                        ).resize((
                            int(Image.open(f'image/{value}.png').width * 0.7),
                            int(Image.open(f'image/{value}.png').height * 0.7)
                            ),
                            resample=Image.Resampling.LANCZOS
                        )
                    )
                button = Button(
                    self,
                    image=self.array1[index],
                    command=lambda value=value: self.click(value)
                )
                button.grid(row=row2, column=column2)

                button.bind("<Enter>", on_enter)
                button.bind("<Leave>", on_leave)

        if self.option == 1:
            Button(
                self,
                text='Бито',
                command=lambda answer='Bito': self.click(answer),
                height=2,
                width=30,
            ).grid(row=row2+1, column=0, columnspan=6, sticky="nsew")

        if self.option == 2:
            Button(
                self,
                text='Взять карты',
                command=lambda answer='Takecards': self.click(answer),
                height=2,
                width=30,
            ).grid(row=row2+1, column=0, columnspan=6, sticky="nsew")

    def click(self, value):
        self.select_card = value
        self.master.destroy()

    def return_selected_card(self):
        return self.select_card


class Application3(BaseApplication):
    def __init__(
            self,
            master,
            name_plaer
    ):
        super(Application3, self).__init__(master)
        self.grid()
        self.name_plaer = name_plaer
        self.create_widgets()

    def create_widgets(self):
        Label(
            self,
            text=f'Игрок {self.name_plaer} победил',
            font=('Comic Sans MS', 15, 'bold')
        ).grid(row=0, column=0, columnspan=6)
        Label(
            self,
            text="Хотите сыграть еще раз?",
            font=('Comic Sans MS', 15, 'bold')
        ).grid(row=1, column=0, columnspan=6)

        Button(
            self,
            text='Да',
            command=lambda answer='Yes': self.click(answer),
            height=2,
            width=30,
            ).grid(row=2, column=0, columnspan=3, sticky="nsew")
        Button(
            self,
            text='Нет',
            command=lambda answer='No': self.click(answer),
            height=2,
            width=30,
            ).grid(row=2, column=3, columnspan=3, sticky="nsew")

    def click(self, value):
        self.answer = value
        self.master.destroy()

    def return_answer_game(self):
        return self.answer


def display_window(app_class, *args, **kwargs):
    root = Tk()
    root.title('Игра в дурака')
    root.iconbitmap(Path(__file__).resolve().parent/'image/4.ico')
    app = app_class(root, *args, **kwargs)
    app.calculate_geometry()
    root.mainloop()
    return app

def set_number_players():
    app = display_window(Application1)
    return app.return_number_and_list_players()


def select_card_gui(name_plaer, cards_on_table, cards_on_hand, number_cards_deck, trump_suit, option=0):
    app = display_window(Application2, name_plaer, cards_on_table, cards_on_hand, number_cards_deck, trump_suit, option)
    return app.return_selected_card()


def answer_game(name_plaer):
    app = display_window(Application3, name_plaer)
    return app.return_answer_game()
