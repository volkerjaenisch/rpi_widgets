from zope.interface import Interface, Attribute


class IGUI(Interface):
    pass


class IWidget(Interface):

    content = Attribute("""Content of widget""")
    pos_x = Attribute("""X position of widget""")
    pos_y = Attribute("""Y position of widget""")
    parent = Attribute("""X,Y position of widget""")

    def length(self):
        pass

    def init(self):
        pass


class ILineWidget(IWidget):
    pass


class ILinesWidget(IWidget):
    pass


class ISelectWidget(IWidget):
    pass


class IPageWidget(IWidget):
    pass


class IRenderer(Interface):

    def render(self):
        pass


class IDisplay(Interface):

    def init(self):
        pass

    def run(self):
        pass

    def done(self):
        pass

    def write(self, value):
        pass

    def set_cursor_pos(self, x, y):
        pass


class IRPLCD(IDisplay):
    pass


class ICharLCD(IDisplay):
    pass


class ICurses(IDisplay):
    pass


class IInput(Interface):

    def init(self):
        pass

    def run(self):
        pass

    def donw(self):
        pass


class IWidgetController(Interface):
    pass


class ILayout(Interface):

    focus = Attribute("""Focussed widget""")


class INotify(Interface):
    pass