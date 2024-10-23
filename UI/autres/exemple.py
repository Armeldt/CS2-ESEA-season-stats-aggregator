from customtkinter import *

win = CTk()
win.geometry("300x300")


def hide_all():
    """ Hides all the pages """
    page1.hide()
    page2.hide()


def show_page1():
    page1.show()


def show_page2():
    page2.show()


class Page1:
    def __init__(self):
        self.label1 = CTkLabel(win, text="I'm on the first page")
        self.button1 = CTkButton(win, text="Change to the second page", command=show_page2)

    def show(self):
        hide_all()
        self.label1.pack()
        self.button1.pack()

    def hide(self):
        self.label1.pack_forget()
        self.button1.pack_forget()


class Page2:
    def __init__(self):
        self.label1 = CTkLabel(win, text="I'm on the second page")
        self.button1 = CTkButton(win, text="Change to the first page", command=show_page1)

    def show(self):
        hide_all()
        self.label1.pack()
        self.button1.pack()

    def hide(self):
        self.label1.pack_forget()
        self.button1.pack_forget()


page1 = Page1()
page2 = Page2()

page1.show()

win.mainloop()