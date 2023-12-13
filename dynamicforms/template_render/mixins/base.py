from dynamicforms.fields import DFField

from .render_mode_enum import ViewModeEnum


class ViewModeBase(object):
    view_mode = None

    def set_view_mode(self, view_mode: "ViewModeEnum"):
        self.view_mode = view_mode

    def set_bound_value(self, *args):
        """
        Used to set the bound value. However, implementation is class-specific, so we only declare this so that
        implementations are checked to contain the method
        """
        raise NotImplementedError()

    def render(self: "_ViewModeBoundField"):
        view_mode_name = f"render_{self.view_mode.name.lower()}"
        render_func = getattr(self, view_mode_name, None)
        if render_func is None:
            raise NotImplementedError(
                f'ViewMode object {self.__class__.__name__}{(" " + self.label) if self.label else ""} has view_mode '
                f"set to {self.view_mode.name}, but doesn't handle rendering for it"
            )
        return render_func()

    def __str__(self):
        return self.render()


# noinspection PyAbstractClass
class _ViewModeBoundField(ViewModeBase, DFField):
    """
    Dummy class just for type hinting
    """

    pass
