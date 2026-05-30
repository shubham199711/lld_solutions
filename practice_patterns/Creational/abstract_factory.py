from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass

class MacButton(Button):
    def render(self):
        print("Mac Button")

class WindowsButton(Button):
    def render(self):
        print("Windows Button")

class MacCheckbox(Checkbox):
    def render(self):
        print("Mac Checkbox")

class WindowsCheckbox(Checkbox):
    def render(self):
        print("Windows Checkbox")

class UIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass


class MacFactory(UIFactory):
    @abstractmethod
    def create_button(self):
        return MacButton()

    @abstractmethod
    def create_checkbox(self):
        return MacCheckbox()


class WindowFactory(UIFactory):
    @abstractmethod
    def create_button(self):
        return WindowsButton()

    @abstractmethod
    def create_checkbox(self):
        return WindowsCheckbox()