import tkinter as tk
import tkinter.font as ft

class ButtonActor:
    def __init__(self, gui, char):
        self.char = str(char)
        self.gui = gui

    def act(self):
        self.gui.act(self.char)


class Calculator:
    def __init__(self):
        self.first_argument = None
        self.second_argument = None
        self.operator = None

    def compute(self):
        self.first_argument, self.second_argument = int(self.first_argument), int(self.second_argument)
        if self.operator == '+':
            result = self.first_argument + self.second_argument
        elif self.operator == '-':
            result = self.first_argument - self.second_argument
        elif self.operator == '*':
            result = self.first_argument * self.second_argument
        elif self.operator == '/':
            if self.second_argument != 0:
                result = int(self.first_argument / self.second_argument)
            else:
                result = 0
        else:
            result = 0
        self.refresh()
        return result

    def computable(self):
        return self.first_argument is not None and self.operator is not None and self.second_argument is not None

    def refresh(self):
        self.first_argument = self.second_argument = self.operator = None


class Gui:
    def __init__(self):
        self.main_frame = tk.Tk()
        self.main_frame.title("계산기")
        self.text = ''
        self.__make_screen()
        self.__make_buttons()
        self.calculator = Calculator()

    def __make_screen(self):
        self.screen_text = tk.StringVar()
        screen = tk.Entry(self.main_frame, state='readonly', textvariable=self.screen_text,
                          readonlybackground='#ffffff', relief='solid',
                          font=ft.Font(family='맑은 고딕', size=13))
        screen.pack(fill='x', padx=15, pady=10)

    def __make_buttons(self):
        button_frame = tk.Frame(self.main_frame, bd=10)
        button_frame.pack()
        leftcolumn = ['+', '-', '*']
        lastline = ['C', '0', '=', '/']
        ncnt = 0
        for i in range(16):
            if i >= 12:  # number
                cr = lastline[i - 12]
            elif i % 4 != 3:  # operator
                ncnt += 1
                cr = str(ncnt)
            else:  # lastline
                cr = leftcolumn[i // 4]

            button_actor = ButtonActor(self, cr)
            if cr.isdigit():
                button = tk.Button(button_frame, command=button_actor.act, text=cr, width=5, height=2)
            elif cr == 'C':
                button = tk.Button(button_frame, command=button_actor.act, text=cr, width=5, height=2,
                                   bg='#ffff88')
            else:
                button = tk.Button(button_frame, command=button_actor.act, text=cr, width=5, height=2, bg='#ddddff')
            button.grid(row=(i // 4), column=(i % 4), padx=1, pady=1)

    def act(self, char):
        if char == 'C':
            self.text = ''
            self.screen_text.set('0')
            self.calculator.refresh()
        elif char == '=':
            if self.text:
                text = self.text
            elif self.screen_text.get():
                text = self.screen_text.get()
            else:
                text = '0'
            self.calculator.second_argument = int(text)
            if self.calculator.computable():
                self.screen_text.set(str(self.calculator.compute()))
                self.text = ''
            else:
                self.screen_text.set(self.calculator.second_argument)
                self.calculator.refresh()
                self.text = ''
        else:
            if char.isdigit():
                if self.screen_text.get() != '0':
                    self.text += char
                else:
                    self.text = char
                self.screen_text.set(self.text)
            else:  # operator
                if not self.text:
                    screen_number = self.screen_text.get()
                    if screen_number:
                        self.calculator.first_argument = int(screen_number)
                        self.calculator.operator = char
                elif self.calculator.first_argument is None:
                    self.calculator.first_argument = int(self.text)
                    self.calculator.operator = char
                else:
                    self.calculator.second_argument = int(self.text)
                    result = self.calculator.compute()
                    self.calculator.first_argument = result
                    self.calculator.operator = char
                    self.screen_text.set(result)
                self.text = ''

        print(char)

    def mainloop(self):
        self.main_frame.mainloop()


if __name__ == '__main__':
    a = Gui()
    a.mainloop()
