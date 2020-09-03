from inqbus.rpi.widgets.base.controller import WidgetController
from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.base.signals import InputClick
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer, IWidgetController
from inqbus.rpi.widgets.interfaces.widgets import IButtonWidget
from inqbus.rpi.widgets.line import Line
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(IButtonWidget)
class Button(Line):
    """
    Button Widget. Representing a single line button.
    """

    # The click_handler for the button
    _click_handler = None

    @property
    def width(self):
        """
        The width of the widget in characters
        """
        if self._desired_width is None:
            # The button adds two braces
            # so we have to add 2 to the width of the content itself
            return len(self.content) + 2
        else:
            return self._desired_width

    @width.setter
    def width(self, value):
        """
        Set the width to a fixed value

        Args:
            value: width
        """
        self._desired_width = value

    def init_content(self):
        # The initial content of the button should
        # be empty as long as no content is set
        self._content = ''

    @property
    def click_handler(self):
        """
        Property to get the click_handler

        Returns:
            The click_handler
        """
        return self._click_handler

    @click_handler.setter
    def click_handler(self, handler):
        """
        Property to set the click_handler
        Args:
            handler: The handler
        """
        self._click_handler = handler


@implementer(IRenderer)
class ButtonRenderer(Renderer):
    """
    Renderer for a LineWidget
    """
    __used_for__ = (IButtonWidget, Interface)

    def render(self):
        """
        Render the Button at the given position

        Returns: the new x, y position
        """
        pos_x = self.widget.pos_x
        pos_y = self.widget.pos_y
        # if a button width is set truncate the content
        if self.widget.width:
            # when we render the button
            # we have to substract two characters for the braces to determine
            # the amount of characters to use from the content.
            content = self.widget.content[:self.widget.width-2]
        else:
            content = self.widget.content

        # If the button is focussed
        # indicate this by changing the braces to angles
        if self.widget.has_focus:
            out_str = '>' + content + '<'
        else:
            out_str = '[' + content + ']'
        self.display.write_at_pos(pos_x, pos_y, out_str)
        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1

    def clear(self):
        """
        Erase the button from the frame_buffer
        """
        self.display.write_at_pos(
                self.widget.pos_x,
                self.widget.pos_y,
                ' ' * (len(self.widget.content) + 2)
        )


@implementer(IWidgetController)
class ButtonController(WidgetController):
    """
    Controller for IButtonWidgets.
    """
    __used_for__ = IButtonWidget

    def dispatch(self, signal):
        """
        Dispatcher for Signals. Displaytches only the InputClick signal

        Args:
            signal: Incoming Signal

        Returns:
            True if the widget consumes the Signal,
            False if the widget cannot consume the signal
        """
        if signal == InputClick:
            return self.widget.click_handler()
        else:
            return False


# Register the adapters
gsm = getGlobalSiteManager()
gsm.registerAdapter(ButtonRenderer, (IButtonWidget, Interface), IRenderer)
gsm.registerAdapter(ButtonController, (IButtonWidget,), IWidgetController)
