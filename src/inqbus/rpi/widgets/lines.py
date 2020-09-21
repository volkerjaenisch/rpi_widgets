from inqbus.rpi.widgets.base.render import Renderer
from inqbus.rpi.widgets.base.widget import Widget
from inqbus.rpi.widgets.interfaces.interfaces import IRenderer
from inqbus.rpi.widgets.interfaces.widgets import ILinesWidget
from inqbus.rpi.widgets.line import Line
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implementer


@implementer(ILinesWidget)
class Lines(Widget):
    """
    Lines Widget.
    Representing one or more lines.
    This widget contains a list of lines which will
    be rendered left_bounded.
    """
    def init_content(self):
        self._content = []

    def handle_new_content(self, value):
        # accept only a list of ether strings or Line Instances
        assert isinstance(value, list)
        # for all given lines
        for line_val in value:
            # if line is string
            if isinstance(line_val, str):
                # .. then transform it into a line instance
                line = Line()
                line.render_on_content_change = False
                line.content = line_val
                self._content.append(line)
            else:
                # .. else just append to the content
                self._content.append(line_val)

        # if render on content_change
        if self.render_on_content_change:
            # .. render the widget
            self.render()

    @property
    def height(self):
        """
        The height of the widget in characters
        """
        if self._desired_height is None:
            return len(self._content)
        else:
            return self._desired_height

    @height.setter
    def height(self, value):
        """
        Set the height to a fixed value

        Args: value: height
        """
        self._desired_height = value


@implementer(IRenderer)
class LinesRenderer(Renderer):
    """
    Renderer for a LinesWidget
    """
    __used_for__ = (ILinesWidget, Interface)

    def render(self):
        pos_x = self.widget.pos_x
        pos_y = self.widget.pos_y
        if self.widget.height == 1:
            renderer = self.get_display_renderer_for(self.widget.content[0])
            _pos_x, pos_y = renderer.render(
                    pos_x=pos_x,
                    pos_y=pos_y
            )
        else:

            for line in self.widget.content:
                renderer = self.get_display_renderer_for(line)
                pos_x, pos_y = renderer.render(pos_x=pos_x, pos_y=pos_y)
                pos_y += 1

        # return the coordinate after the content
        # ToDo width, height handling
        return pos_x, pos_y + 1


# Register the render adapter
gsm = getGlobalSiteManager()
gsm.registerAdapter(LinesRenderer, (ILinesWidget, Interface), IRenderer)
