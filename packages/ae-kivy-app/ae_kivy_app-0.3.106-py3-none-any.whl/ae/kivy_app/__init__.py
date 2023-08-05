"""
main application classes and widgets for GUIApp-conform Kivy apps
=================================================================

this ae portion is providing additional :ref:`config-variables` and some useful constants, various enhanced widget
classes, two application classes (:class:`FrameworkApp` and :class:`KivyMainApp`) and an i18n wrapper (:func:`get_txt`),
adding translatable f-strings to the python and kv code of your app.


kivy app constants and config variables
---------------------------------------

with the optional :ref:`config-variables` `win_min_width` and `win_min_height`, added by this portion, you can restrict
the minimum size of the kivy main window of your app. their default values are set on app startup in the method
:meth:`~KivyMainApp.on_app_start`.

more constants provided by this portion are in the constant declaration section starting with :data:`MAIN_KV_FILE_NAME`.

additionally, all the :ref:`config-variables` and app constants inherited from the base app classes are available.

.. hint::
    please see the documentation of the namespace portions/modules :mod:`ae.console` and :mod:`ae.gui_app` for more
    detailed information on all the inherited :ref:`config-variables`, :ref:`config-options`, :ref:`config-files` and
    :ref:`app-state-constants`.


enhanced widget classes
-----------------------

the widgets provided by this portion are based on the kivy widgets and are respecting the :ref:`app-state-variables`
specifying the desired app style (dark or light) and font size. most of them also change automatically the
:ref:`application flow`.

the following widgets provided by this portion will be registered in the kivy widget class maps by importing this module
to be available for your app:

* :class:`AppStateSlider`: :class:`~kivy.uix.slider.Slider` changing the value of :ref:`app-state-variables`.
* :class:`FlowButton`: button to change the application flow.
* :class:`FlowDropDown`: attachable popup, based on :class:`~kivy.uix.dropdown.DropDown`.
* :class:`FlowInput`: dynamic kivy widget based on :class:`~kivy.uix.textinput.TextInput` with application flow support.
* :class:`FlowPopup`: dynamic auto-content-sizing popup to query user input or to show messages.
* :class:`FlowToggler`: toggle button based on :class:`ImageLabel` and :class:`~kivy.uix.behaviors.ToggleButtonBehavior`
  to change the application flow or any flag or application state.
* :class:`ImageLabel`: dynamic kivy widget extending the Kivy :class:`~kivy.uix.label.Label` widget with an image.
* :class:`MessageShowPopup`: simple message box widget based on :class:`FlowPopup`.
* :class:`OptionalButton`: dynamic kivy widget based on :class:`FlowButton` which can be dynamically hidden.
* :class:`TouchableBehavior`: extends toggle-/touch-behavior of :class:`~kivy.uix.behaviors.ButtonBehavior`.
* :class:`UserNameEditorPopup`: popup window used e.g. to enter new user, finally registered in the app config files.


kivy app classes
----------------

the class :class:`KivyMainApp` is implementing a main app class that is reducing the amount of code needed to create
a Python application based on the `kivy framework <https://kivy.org>`_.

:class:`KivyMainApp` is based on the following classes:

* the abstract base class :class:`~ae.gui_app.MainAppBase` which adds :ref:`application status`,
  :ref:`app-state-variables`, :ref:`app-state-constants`, :ref:`application flow` and :ref:`application events`.
* :class:`~ae.console.ConsoleApp` is adding :ref:`config-files`, :ref:`config-variables` and :ref:`config-options`.
* :class:`~ae.core.AppBase` is adding :ref:`application logging` and :ref:`application debugging`.

this namespace portion is also encapsulating the :class:`Kivy App class <kivy.app.App>` within the :class:`FrameworkApp`
class. this Kivy app class instance can be directly accessed from the main app class instance via the
:attr:`~ae.gui_app.MainAppBase.framework_app` attribute.


kivy application events
^^^^^^^^^^^^^^^^^^^^^^^

this portion is firing :ref:`application events` additional to the ones provided by :class:`~ae.gui_app.MainAppBase` by
redirecting events of Kivy's :class:`~kivy.app.App` class (the Kivy event/callback-method name is given in brackets).
these framework app events get fired after :meth:`~ae.gui_app.MainAppBase.on_app_run` in the following order:

* on_app_build (kivy.app.App.build, after the main kv file get loaded).
* on_app_built (kivy.app.App.build, after the root widget get build).
* on_app_started (kivy.app.App.on_start)
* on_app_pause (kivy.app.App.on_pause)
* on_app_resume (kivy.app.App.on_resume)
* on_app_stopped (kivy.app.App.on_stop)


i18n support
------------

translatable f-strings are provided via the helper function :func:`get_txt` and the :class:`_GetTextBinder` class.


unit tests
----------

unit tests need at least V 2.0 of OpenGL and the kivy framework installed.

.. note::
    unit tests does have 100 % coverage but are currently not passing the gitlab CI tests because were failing in set up
    a proper running window system on the python image that all ae portions are using.
"""
import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from plyer import vibrator                                                                  # type: ignore

import kivy                                                                                 # type: ignore
from kivy.animation import Animation                                                        # type: ignore
from kivy.app import App                                                                    # type: ignore
from kivy.clock import Clock                                                                # type: ignore
from kivy.core.audio import SoundLoader                                                     # type: ignore
from kivy.core.window import Window                                                         # type: ignore
from kivy.factory import Factory, FactoryException                                          # type: ignore
from kivy.graphics import Ellipse                                                           # type: ignore
from kivy.input import MotionEvent                                                          # type: ignore
from kivy.lang import Builder, Observable, global_idmap                                     # type: ignore
from kivy.metrics import dp, sp                                                             # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import (                                                               # type: ignore
    BooleanProperty, ColorProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty)
from kivy.uix.boxlayout import BoxLayout                                                    # type: ignore
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior                         # type: ignore
from kivy.uix.bubble import BubbleButton                                                    # type: ignore
from kivy.uix.dropdown import DropDown                                                      # type: ignore
from kivy.uix.label import Label                                                            # type: ignore
from kivy.uix.popup import Popup                                                            # type: ignore
from kivy.uix.slider import Slider                                                          # type: ignore
import kivy.uix.textinput                                                                   # type: ignore
# noinspection PyProtectedMember
from kivy.uix.textinput import TextInput, TextInputCutCopyPaste as OriTextInputCutCopyPaste
from kivy.uix.widget import Widget                                                          # type: ignore
from kivy.utils import escape_markup, get_hex_from_color                                    # type: ignore

from ae.base import os_platform                                                             # type: ignore
from ae.files import CachedFile                                                             # type: ignore
from ae.paths import app_docs_path                                                          # type: ignore
from ae.i18n import default_language, get_f_string                                          # type: ignore
from ae.core import DEBUG_LEVELS, DEBUG_LEVEL_ENABLED                                       # type: ignore

# id_of_flow not used here - added for easier import in app project
from ae.gui_app import (                                                                    # type: ignore
    APP_STATE_SECTION_NAME, MAX_FONT_SIZE, MIN_FONT_SIZE,
    THEME_LIGHT_BACKGROUND_COLOR, THEME_LIGHT_FONT_COLOR, THEME_DARK_BACKGROUND_COLOR, THEME_DARK_FONT_COLOR,
    ensure_tap_kwargs_refs, replace_flow_action)
from ae.gui_help import HelpAppBase                                                         # type: ignore
from ae.kivy_glsl import ShaderIdType, ShadersMixin                                         # type: ignore
from ae.kivy_auto_width import ContainerChildrenAutoWidthBehavior                           # type: ignore
from ae.kivy_dyn_chi import DynamicChildrenBehavior                                         # type: ignore
from ae.kivy_help import (                                                                  # type: ignore
    ANI_SINE_DEEPER_REPEAT3, HelpBehavior, HelpToggler, ModalBehavior, Tooltip, TourOverlay)
from ae.kivy_relief_canvas import relief_colors, ReliefCanvas                               # type: ignore


__version__ = '0.3.106'


MAIN_KV_FILE_NAME = 'main.kv'  #: default file name of the main kv file

CRITICAL_VIBRATE_PATTERN = (0.00, 0.12, 0.12, 0.12, 0.12, 0.12,
                            0.12, 0.24, 0.12, 0.24, 0.12, 0.24,
                            0.12, 0.12, 0.12, 0.12, 0.12, 0.12)
""" very long/~2.4s vibrate pattern for critical error notification (sending SOS to the mobile world;) """

ERROR_VIBRATE_PATTERN = (0.0, 0.09, 0.09, 0.18, 0.18, 0.27, 0.18, 0.36, 0.27, 0.45)
""" long/~2s vibrate pattern for error notification. """

LOVE_VIBRATE_PATTERN = (0.0, 0.12, 0.12, 0.21, 0.03, 0.12, 0.12, 0.12)
""" short/~1.2s vibrate pattern for fun/love notification. """

TOUCH_VIBRATE_PATTERN = (0.0, 0.09, 0.09, 0.06, 0.03, 0.03)
""" very short/~0.3s vibrate pattern for button and toggler touch. """

# load/declare base widgets with integrated app flow and observers ensuring change of app states (e.g. theme and size)
Builder.load_file(os.path.join(os.path.dirname(__file__), "widgets.kv"))


class AppStateSlider(HelpBehavior, Slider, ShadersMixin):
    """ slider widget with help text to change app state value. """
    app_state_name = StringProperty()  #: name of the app state to be changed by this slider value


class ImageLabel(ReliefCanvas, Label, ShadersMixin):
    """ base label used for all labels and buttons - declared in widgets.kv and also in this module to inherit from.

    .. note::
        hide-able label needs extra handling, because even setting width/height to zero the text can still be visible,
        especially in dark mode and even with having the text-color-alpha==0. to fully hide the texture in all cases,
        set either the text to an empty string or the opacity to zero.
    """


class TouchableBehavior:  # pragma: no cover
    """ touch-/toggle-button mix-in class with shaders, animations and additional events for double/triple/long touches.

    :Events:
        `on_double_tap`:
            fired with the touch down MotionEvent instance arg when a button get tapped twice within short time.
        `on_triple_tap`:
            fired with the touch down MotionEvent instance arg when a button get tapped three times within short time.
        `on_long_tap`:
            fired with the touch down MotionEvent instance arg when a button get tapped more than 2.4 seconds.
        `on_alt_tap`:
            fired with the touch down MotionEvent instance arg when a button get either double, triple or long tapped.

    .. note::
        has to be inherited (to be in the MRO) before :class:`~kivy.uix.behaviors.ButtonBehavior`, respectively
        :class:`~kivy.uix.behaviors.ToggleButtonBehavior`, for the touch event get grabbed properly.
    """
    # abstracts of mixing-in class; e.g. from :class:`~kivy.widget.Widget`, :class:`~ae.kivy_glsl.ShadersMixin`
    # and :class:`~kivy.uix.behaviors.ButtonBehavior`
    add_shader: Callable
    center_x: float
    center_y: float
    collide_point: Callable
    del_shader: Callable
    disabled: bool
    dispatch: Callable
    state: str

    # Kivy properties and events
    down_shader = DictProperty()        #: shader running if button is in pressed state `'down'`
    normal_shader = DictProperty()      #: shader running if button is in pressed state `'normal'`

    _touch_anim = NumericProperty(1.0)  #: widget-got-touched-animation
    _touch_x = NumericProperty()        #: x pos moving from touch to center pos
    _touch_y = NumericProperty()        #: y pos moving from touch to center pos

    __events__ = ('on_alt_tap', 'on_double_tap', 'on_long_tap', 'on_triple_tap')

    def __init__(self, **kwargs):
        """ set normal pressed state shader on widget initialization. """
        # noinspection PyUnresolvedReferences
        super().__init__(**kwargs)      # pylint: disable=no-member

        self._app = App.get_running_app()
        self._state_shader_id: ShaderIdType = {}
        self.down_shader = dict(shader_code='=fire_storm', render_shape=Ellipse,
                                tint_ink=self._app.main_app.flow_path_ink)
        self.normal_shader = dict(shader_code='=plunge_waves', render_shape=Ellipse, add_to='before',
                                  alpha=0.36, contrast=0.09, tex_col_mix=0.87,  time=lambda: -Clock.get_boottime(),
                                  tint_ink=self._app.main_app.flow_id_ink)

    @staticmethod
    def _cancel_long_touch_clock(touch: MotionEvent) -> bool:
        long_touch_handler = touch.ud.pop('long_touch_handler', None)
        if long_touch_handler:
            Clock.unschedule(long_touch_handler)  # alternatively: long_touch_handler.cancel()
        return bool(long_touch_handler)

    def on_alt_tap(self, touch: MotionEvent):
        """ default handler for alternative tap (double, triple or long tap/click).

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_double_tap(self, touch: MotionEvent):
        """ double tap/click default handler.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_down_shader(self, *_args):
        """ button down state shader changed event handler. """
        self._update_shader()

    def on_long_tap(self, touch: MotionEvent):
        """ long tap/click default handler.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """
        # remove 'long_touch_handler' key from touch.ud dict although just fired to signalize that
        # the long tap event got handled in self.on_touch_up (to return True)
        self._cancel_long_touch_clock(touch)

        # reset button state to normal - if state is still down (to replace down_shader with normal_shader)
        if self.state == 'down':
            self.state = 'normal'

        # to prevent dismiss via super().on_touch_up: exclusive receive of this touch up event in self.on_touch_up
        touch.grab(self, exclusive=True)

        # also dispatch as alternative tap
        self.dispatch('on_alt_tap', touch)  # pylint: disable=no-member

    def on_normal_shader(self, *_args):
        """ button normal state shader changed event handler. """
        self._update_shader()

    def on_state(self, _widget: Any, _value: str):
        """ button pressed state changed event handler, switching between `'normal'` and `'down'` state shader.

        :param _widget:         button widget (is self).
        :param _value:          new state value (either 'normal' or 'down').
        """
        self._update_shader()

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ check for additional double/triple/alt touch events and add sound, vibration and animation.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        if not self.disabled and self.collide_point(touch.x, touch.y):
            self._touch_anim = 0.0
            self._touch_x, self._touch_y = touch.pos
            # pylint: disable=no-member # false positive
            Animation(_touch_anim=1.0, _touch_x=self.center_x, _touch_y=self.center_y, t='out_quad', d=0.69).start(self)
            is_triple = touch.is_triple_tap
            if is_triple or touch.is_double_tap:
                # pylint: disable=maybe-no-member
                self.dispatch('on_triple_tap' if is_triple else 'on_double_tap', touch)
                self.dispatch('on_alt_tap', touch)
                return True
            # pylint: disable=maybe-no-member
            touch.ud['long_touch_handler'] = long_touch_handler = lambda dt: self.dispatch('on_long_tap', touch)
            Clock.schedule_once(long_touch_handler, 0.99)
            main_app = self._app.main_app
            main_app.play_vibrate(TOUCH_VIBRATE_PATTERN)
            main_app.play_sound('touched')
        # noinspection PyUnresolvedReferences
        return super().on_touch_down(touch)  # type: ignore # pylint: disable=no-member; does touch.grab(self)

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger moves.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        # alternative method to calculate touch.pos distances is (from tripletap.py):
        # Vector.distance(Vector(ref.sx, ref.sy), Vector(touch.osx, touch.osy)) > 0.009
        if abs(touch.ox - touch.x) > 9 and abs(touch.oy - touch.y) > 9 and self.collide_point(touch.x, touch.y):
            self._cancel_long_touch_clock(touch)
        # noinspection PyUnresolvedReferences
        return super().on_touch_move(touch)     # type: ignore # pylint: disable=no-member

    def on_touch_up(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger up.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        if touch.grab_current is self and not self._cancel_long_touch_clock(touch):
            touch.ungrab(self)
            return True                     # prevent popup/dropdown dismiss
        # noinspection PyUnresolvedReferences
        return super().on_touch_up(touch)   # type: ignore # pylint: disable=no-member; does touch.ungrab(self)

    def on_triple_tap(self, touch: MotionEvent):
        """ triple tap/click default handler.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def _update_shader(self):
        """ update shader on changed shader or button state. """
        if self._state_shader_id:
            self.del_shader(self._state_shader_id)
            self._state_shader_id = {}

        add_shader_kwargs = self.down_shader if self.state == 'down' else self.normal_shader
        if add_shader_kwargs:
            self._state_shader_id = self.add_shader(**add_shader_kwargs)


class FlowButton(HelpBehavior, TouchableBehavior, ButtonBehavior, ImageLabel):  # pragma: no cover
    """ button to change the application flow. """
    tap_flow_id = StringProperty()  #: the new flow id that will be set when this button get tapped
    tap_kwargs = ObjectProperty()   #: kwargs dict passed to event handler (change_flow) when button get tapped

    def __init__(self, **kwargs):
        ensure_tap_kwargs_refs(kwargs, self)
        super().__init__(**kwargs)


class FlowDropDown(ContainerChildrenAutoWidthBehavior, DynamicChildrenBehavior, ReliefCanvas,
                   DropDown):  # pragma: no cover
    """ dropdown widget used for user selections from a list of items (represented by the children-widgets). """
    close_kwargs = DictProperty()               #: kwargs passed to all close action flow change event handlers
    parent_popup_to_close = ObjectProperty()    #: parent popup widget instance to be closed if this dropdown closes

    def dismiss(self, *args):
        """ override DropDown method to prevent dismiss of any dropdown/popup while clicking on activator widget.

        :param args:            args to be passed to DropDown.dismiss().
        """
        app = App.get_running_app()
        if app.help_layout is None or not isinstance(app.help_layout.targeted_widget, HelpToggler):
            super().dismiss(*args)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ prevent the processing of a touch on the help activator widget by this dropdown.

        :param touch:           motion/touch event data.
        :return:                True if event got processed/used.
        """
        if App.get_running_app().main_app.help_activator.collide_point(*touch.pos):
            return False  # allow help activator button to process this touch down event
        return super().on_touch_down(touch)

    def _reposition(self, *args):
        """ fixing Dropdown bug - see issue #7382 and PR #7383. TODO: remove if PR gets merged and distributed. """
        if self.attach_to and not self.attach_to.parent:
            return
        super()._reposition(*args)


class ExtTextInputCutCopyPaste(OriTextInputCutCopyPaste):  # pragma: no cover
    """ overwrite/extend :class:`kivy.uix.textinput.TextInputCutCopyPaste` w/ translatable and autocomplete options. """
    def __init__(self, **kwargs):
        """ create :class:`~kivy.uix.Bubble` instance to display the cut/copy/paste options.

        the monkey patch of :class:`~kivy.uix.textinput.TextInputCutCopyPaste` which was done in
        :meth:`FlowInput._show_cut_copy_paste` has to be temporarily reset before the super() call below, to prevent
        endless recursion because else the other super(cls, instance) call (in python2 style within
        :meth:`TextInputCutCopyPaste.__init__`) results in the same instance (instead of the overwritten instance).
        """
        kivy.uix.textinput.TextInputCutCopyPaste = OriTextInputCutCopyPaste
        self.fw_app = App.get_running_app()
        super().__init__(**kwargs)

    def on_parent(self, instance: Widget, value: Widget):
        """ overwritten to translate BubbleButton texts and to add extra menus to add/delete ac texts.

        :param instance:        self.
        :param value:           kivy main window.
        """
        super().on_parent(instance, value)
        textinput = self.textinput
        if not textinput:
            return

        cont = self.content
        font_size = self.fw_app.main_app.font_size

        for child in cont.children:
            child.font_size = font_size
            child.text = get_txt(child.text)

        if not textinput.readonly:
            # memorize/forget complete text to/from autocomplete because dropdown is not visible if this bubble is
            self.add_widget(BubbleButton(text=get_txt("Memorize"), font_size=font_size,
                                         on_release=textinput.extend_ac_with_text))
            self.add_widget(BubbleButton(text=get_txt("Forget"), font_size=font_size,
                                         on_release=textinput.delete_text_from_ac))

        # estimate container size (exact calc not possible because button width / texture_size[0] is still 100 / 0)
        width = cont.padding[0] + cont.padding[2] + len(cont.children) * (cont.spacing[0] + sp(126))
        height = cont.padding[1] + cont.padding[3] + self.fw_app.button_height
        self.size = width, height   # pylint: disable=attribute-defined-outside-init # false positive


class FlowInput(HelpBehavior, TextInput, ShadersMixin):  # pragma: no cover
    """ text input/edit widget with optional autocompletion.

    until version 0.1.43 of this portion the background and text color of :class:`FlowInput` did automatically
    get switched by a change of the light_theme app state. now all colors left unchanged (before only the ones
    with <unchanged>)::

    * background_color: Window.clearcolor            # default: 1, 1, 1, 1
    * cursor_color: app.font_color                   # default: 1, 0, 0, 1
    * disabled_foreground_color: <unchanged>         # default: 0, 0, 0, .5
    * foreground_color: app.font_color               # default: 0, 0, 0, 1
    * hint_text_color: <unchanged>                   # default: 0.5, 0.5, 0.5, 1.0
    * selection_color: <unchanged>                   # default: 0.1843, 0.6549, 0.8313, .5

   to implement a dark background for the dark theme we would need also to change the images in the properties:
    background_active, background_disabled_normal and self.background_normal.

    the images/colors of the bubble that is showing e.g. on long press of the TextInput widget (cut/copy/paste/...)
    kept unchanged - only the font_size get adapted and the bubble button texts get translated. for that the class
    :class:`ExtTextInputCutCopyPaste` provided by this portion inherits from the original bubble class
    :class:`~kivy.uix.textinput.TextInputCutCopyPaste`.

    the original bubble class is getting monkey patched shortly/temporarily in the moment of the instantiation to
    translate the bubble menu options, change the font sizes and add additional menu options to memorize/forget
    auto-completion texts.
    """
    focus_flow_id = StringProperty()        #: flow id that will be set when this widget get focus
    unfocus_flow_id = StringProperty()      #: flow id that will be set when this widget lost focus

    auto_complete_texts: List[str] = ListProperty()  #: list of autocompletion texts
    auto_complete_selector_index_ink: Tuple[float, float, float, float] = ListProperty((0.69, 0.69, 0.69, 1))
    """ color and alpha used to highlight the currently selected text of all matching autocompletion texts """

    _ac_dropdown: Any = None                #: singleton FlowDropDown instance for all TextInput instances
    _matching_ac_texts: List[str] = []      #: one list instance for all TextInput instances is enough
    _matching_ac_index: int = 0             #: index of selected text in the dropdown matching texts list

    def __init__(self, **kwargs):
        # changed to kivy properties so no need to pop them from kwargs:
        # self.auto_complete_texts = kwargs.pop('auto_complete_texts', [])
        # self.auto_complete_selector_index_ink = kwargs.pop('auto_complete_selector_index_ink', (0.69, 0.69, 0.69, 1))

        super().__init__(**kwargs)

        self.main_app = App.get_running_app().main_app

        if not FlowInput._ac_dropdown:
            FlowInput._ac_dropdown = FlowDropDown()  # widget instances cannot be created in class var declaration

    def _change_selector_index(self, delta: int):
        """ change/update/set the index of the matching texts in the opened autocompletion dropdown.

        :param delta:           index delta value between old and new index (e.g. pass +1 to increment index).
                                set index to zero if the old/last index was on the last item in the matching list.
        """
        cnt = len(self._matching_ac_texts)
        if cnt:
            chi = list(reversed(self._ac_dropdown.container.children))
            idx = self._matching_ac_index
            chi[idx].square_fill_ink = Window.clearcolor
            self._matching_ac_index = (idx + delta + cnt) % cnt
            chi[self._matching_ac_index].square_fill_ink = self.auto_complete_selector_index_ink
            # suggestion_text will be removed in Kivy 2.1.0 - see PR #7437
            # self.suggestion_text = self._matching_ac_texts[self._matching_ac_index][len(self.text):]  # type: ignore

    def _delete_ac_text(self, ac_text: str = ""):
        if not ac_text and self._matching_ac_texts:
            ac_text = self._matching_ac_texts[self._matching_ac_index]
        if ac_text in self.auto_complete_texts:
            self.auto_complete_texts.remove(ac_text)
            self.on_text(self, self.text)   # redraw autocompletion dropdown

    def delete_text_from_ac(self, *_args):
        """ check if current text is in autocompletion list and if yes then remove it.

        called by FlowInput kbd event handler and from menu button added by ExtTextInputCutCopyPaste.on_parent().

        :param _args:           unused event args.
        """
        self._delete_ac_text(self.text)

    def extend_ac_with_text(self, *_args):
        """ add non-empty text to autocompletion texts.

        :param _args:           unused event args.
        """
        if self.text:
            self.auto_complete_texts.insert(0, self.text)

    def keyboard_on_key_down(self, window: Any, keycode: Tuple[int, str], text: str, modifiers: List[str]) -> bool:
        """ overwritten TextInput/FocusBehavior kbd event handler.

        :param window:          keyboard window.
        :param keycode:         pressed key as tuple of (numeric key code, key name string).
        :param text:            pressed key value string.
        :param modifiers:       list of modifier keys (pressed or locked).
        :return:                True if key event get processed/used by this method.
        """
        key_name = keycode[1]
        if self._ac_dropdown.attach_to:
            if key_name in ('enter', 'right') and len(self._matching_ac_texts) > self._matching_ac_index:
                # suggestion_text will be removed in Kivy 2.1.0 - see PR #7437
                # self.suggestion_text = ""
                self.text = self._matching_ac_texts[self._matching_ac_index]
                self._ac_dropdown.close()
                return True

            if key_name == 'down':
                self._change_selector_index(1)
            elif key_name == 'up':
                self._change_selector_index(-1)
            elif key_name == 'delete' and 'ctrl' in modifiers:
                self._delete_ac_text()

        if key_name == 'insert' and 'ctrl' in modifiers:
            self.extend_ac_with_text()

        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def keyboard_on_textinput(self, window: Window, text: str):
        """ overridden to suppress any user input if tour is running/active. """
        if not self.main_app.tour_layout:
            super().keyboard_on_textinput(window, text)

    def on_focus(self, _self: Widget, focus: bool):
        """ change flow on text input change of focus.

        :param _self:           unused dup ref to self.
        :param focus:           True if this text input got focus, False on unfocus.
        """
        flow_id = self.focus_flow_id if focus else self.unfocus_flow_id
        if flow_id:
            self.main_app.change_flow(flow_id)

    def on_text(self, _self: Widget, text: str):
        """ TextInput.text change event handler.

        :param _self:           unneeded duplicate reference to TextInput/self.
        :param text:            new/current text property value.
        """
        if text:
            matching = [txt for txt in self.auto_complete_texts if txt[:-1].startswith(text)]
        else:
            matching = []
        self._matching_ac_texts[:] = matching
        self._matching_ac_index = 0

        if matching:
            cdm = []
            for txt in matching:
                cdm.append(dict(cls='FlowButton', kwargs=dict(text=txt, on_release=self._select_ac_text)))
            self._ac_dropdown.child_data_maps[:] = cdm
            if not self._ac_dropdown.attach_to:
                self.main_app.change_flow(replace_flow_action(self.focus_flow_id, 'suggest'))
                self._ac_dropdown.open(self)
            self._change_selector_index(0)
            # suggestion_text will be removed in Kivy 2.1.0 - see PR #7437
            # self.suggestion_text = matching[self._matching_ac_index][len(self.text):]
        elif self._ac_dropdown.attach_to:
            self._ac_dropdown.close()

    def _select_ac_text(self, selector: Widget):
        """ put selected autocompletion text into text input and close _ac_dropdown """
        self.text = selector.text
        self._ac_dropdown.close()

    def _show_cut_copy_paste(self, *args, **kwargs):    # pylint: disable=signature-differs
        kivy.uix.textinput.TextInputCutCopyPaste = ExtTextInputCutCopyPaste  # reset in ExtTextInputCutCopyPaste.__init_
        super()._show_cut_copy_paste(*args, **kwargs)
        kivy.uix.textinput.TextInputCutCopyPaste = OriTextInputCutCopyPaste  # reset here too if already instantiated


class FlowPopup(ModalBehavior, DynamicChildrenBehavior, ReliefCanvas, BoxLayout):                   # pragma: no cover
    """ popup for dynamic and auto-content-sizing dialogs and other top-most or modal windows.

    the scrollable :attr:`container` (a :class:`~kivy.uix.scrollview.ScrollView` instance) can only have one child,
    the content. use a layout as content to display multiple widgets. set :attr:`content_optimal_width` and/or
    :attr:`content_optimal_height` to make the popup size as small as possible, using e.g. `minimum_width` respectively
    `minimum_height` if the content is a layout that is providing and updating this property, or
    :meth:`~KivyMainApp.text_size_guess` if the content is a label or button widget.

    .. hint::
        :attr:`~kivy.uix.label.Label.texture_size` could provide a more accurate content size than
        :meth:`~KivyMainApp.text_size_guess`, but should be used with care to prevent recursive property change loops.

    this class is compatible to :class:`~kivy.uix.popup.Popup` and can be used as replacement, unsupported are only
    the following attributes of :class:`~kivy.uix.popup.Popup` and :class:`~kivy.uix.modalview.ModalView`:

    * :attr:`~kivy.uix.modalview.ModalView.background`: FlowPopup has no :class:`BorderImage`.
    * :attr:`~kivy.uix.modalview.ModalView.border`: FlowPopup is using a :class:`RoundedRectangle`.
    * :attr:`~kivy.uix.popup.Popup.title_align`: is 'center' and could be changed via the `title_bar` id.
    * :attr:`~kivy.uix.popup.Popup.title_color` is the `app.font_color`.
    * :attr:`~kivy.uix.popup.Popup.title_font` is the default font.
    * :attr:`~kivy.uix.popup.Popup.title_size` is the default button height (:attr:`FrameworkApp.button_height`).

    :Events:
        `on_pre_open`:
            fired before the FlowPopup is opened and got added to the main window.
        `on_open`:
            fired when the FlowPopup is opened.
        `on_pre_dismiss`:
            fired before the FlowPopup is closed.
        `on_dismiss`:
            fired when the FlowPopup is closed. if the callback returns True, the popup will stay opened.

    """

    background_color = ColorProperty()
    """ background ink tuple in the format (red, green, blue, alpha).

    the :attr:`background_color` is a :class:`~kivy.properties.ColorProperty` and defaults to
    :attr:`~kivy.core.window.Window.clearcolor`.
    """

    close_kwargs = DictProperty()
    """ kwargs passed to all close action flow change event handlers.

    :attr:`close_kwargs` is a :class:`~kivy.properties.DictProperty`. the default depends the action of the penultimate
    flow id in the :attr:`ae.gui_app.flow_path`: is empty or 'enter' dict then it defaults to an empty flow, else to an
    empty dict.
    """

    container = ObjectProperty()
    """ popup scrollable layout underneath the title bar and content container (parent widget of :attr:`content`).

    :attr:`container` is an :class:`~kivy.properties.ObjectProperty` and is read-only.
    """

    content = ObjectProperty()
    """ popup main content, displayed in the scrollable layout :attr:`container`.

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and has to be specified either in the kv language
    as children or via the `content` kwarg.
    """

    optimal_content_width = NumericProperty()
    """ width of the content to be fully displayed/visible.

    :attr:`optimal_content_width` is a :class:`~kivy.properties.NumericProperty`. if `0` or `None` or not explicitly set
    then it defaults to the main window width and - in landscape orientation - minus the :attr:`side_spacing` and the
    width needed by the :attr:`query_data_maps` widgets.
    """

    optimal_content_height = NumericProperty()
    """ height of the content to be fully displayed/visible.

    :attr:`optimal_content_height` is a :class:`~kivy.properties.NumericProperty`. if `0` or `None` or not explicitly
    set then it defaults to the main window height minus the height of :attr:`title` and - in portrait orientation -
    minus the :attr:`side_spacing` and the height needed by the :attr:`query_data_maps` widgets.
    """

    overlay_color = ColorProperty()
    """ ink (color + alpha) tuple in the format (red, green, blue, alpha) used for dimming of the main window.

    :attr:`overlay_color` is a :class:`~kivy.properties.ColorProperty` and defaults to the current color value
    :attr:`~kivy.core.window.Window.clearcolor` with an alpha of 0.6 (set in :meth:`.__init__`).
    """

    parent_popup_to_close = ObjectProperty()
    """ parent popup widget instance to be closed if this popup closes.

    :attr:`parent_popup_to_close` is a :class:`~kivy.properties.ObjectProperty` and defaults to None.
    """

    query_data_maps: List[Dict[str, Any]] = ListProperty()
    """ list of child data dicts to instantiate the query widgets (most likely :class:`FlowButton`) of this popup.

    :attr:`query_data_maps` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    """

    separator_color = ColorProperty()
    """ color used by the separator between title and the content-/container-layout.

    :attr:`separator_color` is a :class:`~kivy.properties.ColorProperty` and defaults to the current value of the
    :attr:`~FrameworkApp.font_color` property.
    """

    separator_height = NumericProperty('3sp')
    """ height of the separator.

    :attr:`separator_height` is a :class:`~kivy.properties.NumericProperty` and defaults to 3sp.
    """

    side_spacing = NumericProperty('192sp')
    """
    :attr:`side_spacing` is a :class:`~kivy.properties.NumericProperty` and defaults to 192sp.
    """

    title = StringProperty("")
    """ title string of the popup.

    :attr:`title` is a :class:`~kivy.properties.StringProperty` and defaults to an empty string.
    """

    _anim_alpha = NumericProperty()                         #: internal opacity/alpha for fade-in/-out animations
    _anim_duration = NumericProperty(.3)                    #: internal time in seconds for fade-in/-out animations
    _max_height = NumericProperty()                         #: popup max height (calculated from Window/side_spacing)
    _max_width = NumericProperty()                          #: popup max width (calculated from Window/side_spacing)

    __events__ = ('on_pre_open', 'on_open', 'on_pre_dismiss', 'on_dismiss')

    def __init__(self, **kwargs):
        self.fw_app = app = App.get_running_app()

        clr_ink = Window.clearcolor
        self.background_color = clr_ink
        self.overlay_color = tuple(clr_ink[:3]) + (.6, )
        self.relief_square_outer_colors = relief_colors(app.font_color)
        self.relief_square_outer_lines = sp(9)
        self.separator_color = app.font_color

        super().__init__(**kwargs)

    def add_widget(self, widget: Widget, index: int = 0, canvas: Optional[str] = None):
        """ add container and content widgets (first call set container from kv rule, 2nd the content, 3rd raise error).

        :param widget:          widget instance to be added.
        :param index:           index kwarg of :meth:`kivy.uix.widget.Widget`.
        :param canvas:          canvas kwarg of :meth:`kivy.uix.widget.Widget`.
        """
        if self.container:      # None until FlowPopup kv rule in widgets.kv is fully built (before user kv rule build)
            if self.content:
                raise ValueError("FlowPopup has already a children, set via this method, kv or the content property")
            self.fw_app.main_app.vpo(f"FlowPopup: add content widget {widget} to container", index, canvas)
            self.container.add_widget(widget, index=index)  # ScrollView.add_widget does not have canvas parameter
            self.content = widget
        else:
            self.fw_app.main_app.vpo(f"FlowPopup: add container {widget} from internal kv rule", index, canvas)
            super().add_widget(widget, index=index, canvas=canvas)

    def close(self, *_args, **kwargs):
        """ close/dismiss container/layout (ae.gui_app popup handling compatibility for all GUI frameworks).

        .. note:: prevents close/dismiss of any dropdown/popup while clicking on help activator widget.

        :param _args:           arguments (to have compatible signature for DropDown/Popup/ModalView widgets).
        :param kwargs:          keyword arguments (compatible signature for DropDown/Popup/ModalView widgets).
        """
        if self._window is None:
            return

        app = self.fw_app
        if app.help_layout is not None and isinstance(app.help_layout.targeted_widget, HelpToggler):
            return

        self.dispatch('on_pre_dismiss')                                                     # pylint: disable=no-member

        if self.dispatch('on_dismiss') is True and kwargs.get('force', False) is not True:  # pylint: disable=no-member
            return

        if kwargs.get('animation', True):
            Animation(_anim_alpha=0.0, d=self._anim_duration).start(self)
        else:
            self._anim_alpha = 0.0
            self.deactivate_modal()

    dismiss = close     #: alias method of :meth:`~FlowPopup.close`

    def on__anim_alpha(self, _instance: Widget, value: float):
        """ _anim_alpha changed event handler. """
        if value == 0.0 and self._window is not None:
            self.deactivate_modal()

    def on_content(self, _instance: Widget, value: Widget):
        """ optional single widget (to be added to the container layout) set directly or via FlowPopup kwargs. """
        self.fw_app.main_app.vpo(f"FlowPopup.on_content adding content {value} to container {self.container}")
        self.container.clear_widgets()
        self.container.add_widget(value)

    def on_dismiss(self) -> Optional[bool]:
        """ dismiss/close event handler. """

    def on_open(self):
        """ open default event handler. """

    def on_pre_dismiss(self):
        """ pre close/dismiss event handler. """

    def on_pre_open(self):
        """ pre open default event handler. """

    def open(self, *_args, **kwargs):
        """ start optional open animation after calling open method if exists in inheriting container/layout widget.

        :param _args:           unused argument (to have compatible signature for Popup/ModalView and DropDown
                                widgets passing the parent widget).
        :param kwargs:          extra arguments that are removed before to be passed to the inheriting open method:

                                * 'animation': `False` will disable the fade-in-animation (default=True).
        """
        app = self.fw_app
        if not self.optimal_content_width:
            self.optimal_content_width = self._max_width * (0.69 if self.query_data_maps and app.landscape else 1.0)
        if not self.optimal_content_height:
            self.optimal_content_height = self._max_height \
                - (app.button_height + self.ids.title_bar.padding[1] * 2 if self.title else 0.0) \
                - (len(self.query_data_maps) * app.button_height if not app.landscape else 0.0)
        self.center = Window.center

        self.dispatch('on_pre_open')                                            # pylint: disable=no-member
        self.activate_modal()
        if kwargs.get('animation', True):
            ani = Animation(_anim_alpha=1.0, d=self._anim_duration)
            ani.bind(on_complete=lambda *_args: self.dispatch('on_open'))       # pylint: disable=no-member
            ani.start(self)
        else:
            self._anim_alpha = 1.0
            self.dispatch('on_open')                                            # pylint: disable=no-member


class FlowToggler(HelpBehavior, TouchableBehavior, ToggleButtonBehavior, ImageLabel):  # pragma: no cover
    """ toggle button changing flow id. """
    tap_flow_id = StringProperty()  #: the new flow id that will be set when this toggle button get released
    tap_kwargs = DictProperty()     #: kwargs dict passed to event handler (change_flow) when button get tapped

    def __init__(self, **kwargs):
        ensure_tap_kwargs_refs(kwargs, self)
        super().__init__(**kwargs)
        self.down_shader = dict(add_to='before', shader_code='=circled_alpha', render_shape=Ellipse)


class FrameworkApp(App):
    """ kivy framework app class proxy redirecting events and callbacks to the main app class instance. """

    app_states = DictProperty()                         #: duplicate of MainAppBase app state for events/binds
    button_height = NumericProperty('45sp')             #: default button height, dynamically calculated from font size
    displayed_help_id = StringProperty()                #: help id of the currently explained/help-target widget
    font_color = ObjectProperty(THEME_DARK_FONT_COLOR)  #: rgba color of the font used for labels/buttons/...
    help_layout = ObjectProperty(allownone=True)        #: layout widget if help mode is active else None
    landscape = BooleanProperty()                       #: True if app win width is bigger than the app win height
    max_font_size = NumericProperty(MAX_FONT_SIZE)      #: maximum font size in pixels bound to window size
    min_font_size = NumericProperty(MIN_FONT_SIZE)      #: minimum - " -
    mixed_back_ink = ListProperty((.69, .69, .69, 1.))  #: background color mixed from available back inks
    tour_layout = ObjectProperty(allownone=True)        #: overlay layout widget if tour is active else None

    def __init__(self, main_app: 'KivyMainApp', **kwargs):
        """ init kivy app """
        super().__init__(**kwargs)

        self.main_app = main_app                            #: set reference to KivyMainApp instance

        self.title = main_app.app_title                     #: set kivy.app.App.title
        self.icon = os.path.join("img", "app_icon.png")     #: set kivy.app.App.icon
        self.use_kivy_settings = main_app.debug             #: set kivy.app.App.use_kivy_settings

    def build(self) -> Widget:
        """ kivy build app callback.

        :return:                root widget (Main instance) of this app.
        """
        self.main_app.vpo("FrameworkApp.build")
        self.main_app.call_method('on_app_build')

        Window.bind(on_resize=self.win_pos_size_change,
                    left=self.win_pos_size_change,
                    top=self.win_pos_size_change,
                    on_key_down=self.key_press_from_kivy,
                    on_key_up=self.key_release_from_kivy)

        def _set_button_height(*_args):
            new_height = round(self.main_app.font_size * 1.95)
            if self.button_height != new_height:
                self.button_height = new_height
        self.bind(app_states=_set_button_height)

        self.main_app.framework_root = root = Factory.Main()
        self.main_app.framework_win = Window    # == root.parent (after the calling method has finished)
        self.main_app.call_method('on_app_built')
        return root

    def key_press_from_kivy(self, keyboard: Any, key_code: int, _scan_code: int, key_text: Optional[str],
                            modifiers: List[str]) -> bool:
        """ convert and redistribute key down/press events coming from Window.on_key_down.

        :param keyboard:        used keyboard.
        :param key_code:        key code of pressed key.
        :param _scan_code:      key scan code of pressed key.
        :param key_text:        key text of pressed key.
        :param modifiers:       list of modifier keys (including e.g. 'capslock', 'numlock', ...)
        :return:                True if key event got processed used by the app, else False.
        """
        return self.main_app.key_press_from_framework(
            "".join(_.capitalize() for _ in sorted(modifiers) if _ in ('alt', 'ctrl', 'meta', 'shift')),
            keyboard.command_keys.get(key_code) or key_text or str(key_code))

    def key_release_from_kivy(self, keyboard, key_code, _scan_code) -> bool:
        """ key release/up event.

        :return:                return value of call to `on_key_release` (True if ke got processed/used).
        """
        return self.main_app.call_method('on_key_release', keyboard.command_keys.get(key_code, str(key_code)))

    def on_pause(self) -> bool:
        """ app pause event automatically saving the app states.

        emits the `on_app_pause` event.

        :return:                True.
        """
        self.main_app.vpo("FrameworkApp.on_pause")
        self.main_app.save_app_states()
        self.main_app.call_method('on_app_pause')
        return True

    def on_resume(self) -> bool:
        """ app resume event automatically loading the app states.

        emits the `on_app_resume` event.

        :return:                True.
        """
        self.main_app.vpo("FrameworkApp.on_resume")
        self.main_app.load_app_states()
        self.main_app.call_method('on_app_resume')
        return True

    def on_start(self):
        """ kivy app start event.

        called after :meth:`~ae.gui_app.MainAppBase.run_app` method and :meth:`~ae.gui_app.MainAppBase.on_app_start`
        event and after Kivy created the main layout (by calling its :meth:`~kivy.app.App.build` method) and has
        attached it to the main window.

        emits the `on_app_started` event.
       """
        self.main_app.vpo("FrameworkApp.on_start")
        self.win_pos_size_change()  # init. app./self.landscape (on app startup and after build)
        self.main_app.call_method('on_app_started')

    def on_stop(self):
        """ quit app event automatically saving the app states.

        emits the `on_app_stopped` event whereas the method :meth:`~ae.gui_app.MainAppBase.stop_app`
        emits the `on_app_stop` event.
        """
        self.main_app.vpo("FrameworkApp.on_stop")
        self.main_app.save_app_states()
        self.main_app.call_method('on_app_stopped')

    def win_pos_size_change(self, *_):
        """ resize handler updates: :attr:`~ae.gui_app.MainAppBase.win_rectangle`, :attr:`~FrameworkApp.landscape`. """
        self.main_app.win_pos_size_change(Window.left, Window.top, Window.width, Window.height)


class MessageShowPopup(FlowPopup):
    """ flow popup to display info or error messages. """
    message = StringProperty()  #: popup window message text to display
    title = StringProperty()    #: popup window title text to display


class _GetTextBinder(Observable):
    """ redirect :func:`ae.i18n.get_f_string` to an instance of this class.

    kivy currently only support a single one automatic binding in kv files for all function names ending with `_`
    (see `watched_keys` extension in kivy/lang/parser.py line 201; e.g. `f_` would get recognized by the lang_tr
    re pattern, but kivy will only add the `_` symbol to watched_keys and therefore `f_` not gets bound.)
    to allow both - f-strings and simple get_text messages - this module binds :func:`ae.i18n.get_f_string`
    to the `get_txt` symbol (instead of :func:`ae.i18n.get_text`).

    :data:`get_txt` can be used as translation callable, but also to switch the current default language.
    additionally :data:`get_txt` is implemented as an observer that automatically updates any translations
    messages of all active/visible kv rules on switch of the language at app run-time.

    inspired by (see also discussion at https://github.com/kivy/kivy/issues/1664):

    - https://github.com/tito/kivy-gettext-example
    - https://github.com/Kovak/kivy_i18n_test
    - https://git.bluedynamics.net/phil/woodmaster-trainer/-/blob/master/src/ui/kivy/i18n.py

    """
    observers: List[Tuple[Callable, tuple, dict]] = []  #: list of bound observer tuples (func, args, kwargs)
    _bound_uid = -1

    def fbind(self, name: str, func: Callable, *args, **kwargs) -> int:
        """ override fbind (fast bind) from :class:`Observable` to collect and separate `_` bindings.

        :param name:            attribute name to be bound.
        :param func:            observer notification function (to be called if attribute changes).
        :param args:            args to be passed to the observer.
        :param kwargs:          kwargs to be passed to the observer.
        :return:                unique id of this binding.
        """
        if name == "_":
            # noinspection PyUnresolvedReferences
            self.observers.append((func.__call__, args, kwargs))  # type: ignore  # __call__ to prevent weakly-ref-err
            # Observable.bound_uid - initialized in _event.pyx/Observable.cinit() - is not available in python:
            # uid = self.bound_uid      # also not available via getattr(self, 'bound_uid')
            # self.bound_uid += 1
            # return uid
            uid = self._bound_uid
            self._bound_uid -= 1
            return uid  # alternative ugly hack: return -len(self.observers)

        return super().fbind(name, func, *args, **kwargs)

    def funbind(self, name: str, func: Callable, *args, **kwargs):
        """ override fast unbind.

        :param name:            bound attribute name.
        :param func:            observer notification function (called if attribute changed).
        :param args:            args to be passed to the observer.
        :param kwargs:          kwargs to be passed to the observer.
        """
        if name == "_":
            # noinspection PyUnresolvedReferences
            key = (func.__call__, args, kwargs)  # type: ignore  # __call__ to prevent ReferenceError: weakly-ref
            if key in self.observers:
                self.observers.remove(key)
        else:
            super().funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang_code: str):
        """ change language and update kv rules properties.

        :param lang_code:       language code to switch this app to.
        """
        default_language(lang_code)

        app = App.get_running_app()

        for func, args, _kwargs in self.observers:
            app.main_app.vpo(f"_GetTextBinder.switch_lang({lang_code}) calling observer {str(args[0])[:45]}")
            try:
                func(args[0], None, None)
            except ReferenceError as ex:  # pragma: no cover # ReferenceError: weakly-referenced object no longer exists
                app.main_app.dpo(f"_GetTextBinder.switch_lang({lang_code}) exception {ex}")

        app.title = get_txt(app.main_app.app_title)

    def __call__(self, text: str, count: Optional[int] = None, language: str = '',
                 loc_vars: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """ translate text into the current-default or the passed language.

        :param text:            text to translate.
        :param count:           optional count for pluralization.
        :param language:        language code to translate the passed text to (def=current default language).
        :param loc_vars:        local variables used in the conversion of the f-string expression to a string.
                                the `count` item of this dict will be overwritten by the value of the
                                :paramref:`~_GetTextBinder.__call__.count` parameter (if this argument got specified).
        :param kwargs:          extra kwargs (e.g. :paramref:`~ae.i18n.get_f_string.glo_vars` or
                                :paramref:`~ae.i18n.get_f_string.key_suffix` - see :func:`~ae.i18n.get_f_string`).
        :return:                translated text.
        """
        if count is not None:
            if loc_vars is None:
                loc_vars = {}
            loc_vars['count'] = count
        return get_f_string(text, language=language, loc_vars=loc_vars, **kwargs)


get_txt = _GetTextBinder()              #: instantiate global i18n translation callable and language switcher helper
get_txt.__qualname__ = 'GetTextBinder'  # hide sphinx build warning (build crashes if the get_txt var get documented)
global_idmap['_'] = get_txt             # bind as function/callable with the name `_` to be used in kv files


class KivyMainApp(HelpAppBase):
    """ Kivy application """
    documents_root_path: str = "."                      #: root file path for app documents, e.g. for import/export
    get_txt_: Any = get_txt                             #: make i18n translations available via main app instance
    kbd_input_mode: str = 'scale'                       #: optional app state to set Window[Base].softinput_mode
    tour_overlay_class: Optional[Any] = TourOverlay     #: Kivy main app tour overlay class

    _debug_enable_clicks: int = 0

    # implementation of abstract methods

    def init_app(self, framework_app_class: Type[FrameworkApp] = FrameworkApp
                 ) -> Tuple[Optional[Callable], Optional[Callable]]:
        """ initialize framework app instance and prepare app startup.

        :param framework_app_class:     class to create app instance (optionally extended by app project).
        :return:                        callable to start and stop/exit the GUI event loop.
        """
        self.documents_root_path = app_docs_path()

        self.framework_app = framework_app_class(self)
        if os.path.exists(MAIN_KV_FILE_NAME):
            self.framework_app.kv_file = MAIN_KV_FILE_NAME

        return self.framework_app.run, self.framework_app.stop

    # overwritten and helper methods

    def app_env_dict(self) -> Dict[str, Any]:
        """ collect run-time app environment data and settings.

        :return:                dict with app environment data/settings.
        """
        app_env_info = super().app_env_dict()

        app_env_info['dpi_factor'] = self.dpi_factor()

        if self.debug:
            app_env_info['image_files'] = self.image_files
            app_env_info['sound_files'] = self.sound_files

            app_states_data = dict(app_state_version=self.app_state_version, app_state_keys=self.app_state_keys())
            if self.verbose:
                app_states_data["framework app states"] = self.framework_app.app_states
                app_states_data['kbd_input_mode'] = self.kbd_input_mode

                app_env_info['help data'] = {
                    'displayed_help_id': self.displayed_help_id,
                    'global_variables': self.global_variables(),
                    '_last_focus_flow_id': self._last_focus_flow_id,
                    '_next_help_id': self._next_help_id,
                }

                app_env_info['app data']['documents_root_path'] = self.documents_root_path
            app_env_info['app states data'] = app_states_data

        return app_env_info

    def call_method_delayed(self, delay: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ delayed call of passed callable/method with args/kwargs catching and logging exceptions preventing app exit.

        :param delay:           delay in seconds before calling the callable/method specified by
                                :paramref:`~call_method_delayed.callback`.
        :param callback:        either callable or name of the main app method to call.
        :param args:            args passed to the callable/main-app-method to be called.
        :param kwargs:          kwargs passed to the callable/main-app-method to be called.
        :return:                delayed call event (in Kivy of Type[ClockEvent]) providing a `cancel` method to allow
                                the cancellation of the delayed call within the delay time.
        """
        return Clock.schedule_once(lambda dt: self.call_method(callback, *args, **kwargs), timeout=delay)

    def change_light_theme(self, light_theme: bool):
        """ change font and window clear/background colors to match 'light'/'black' themes.

        :param light_theme:     pass True for light theme, False for black theme.
        """
        Window.clearcolor = THEME_LIGHT_BACKGROUND_COLOR if light_theme else THEME_DARK_BACKGROUND_COLOR
        self.framework_app.font_color = THEME_LIGHT_FONT_COLOR if light_theme else THEME_DARK_FONT_COLOR

    @staticmethod
    def class_by_name(class_name: str) -> Optional[Type]:
        """ resolve kv widgets """
        try:
            return Factory.get(class_name)
        except (FactoryException, AttributeError):
            return None

    @staticmethod
    def dpi_factor() -> float:
        """ dpi scaling factor - overridden to use Kivy's dpi scaling. """
        return dp(1.0)

    def ensure_top_most_z_index(self, widget: Widget):
        """ ensure visibility of the passed widget to be the top most in the z index/order.

        :param widget:          widget to check and possibly correct to be the top most one.

        if other dropdown/popup opened after the passed widget/layout, then only correct z index/order to show this
        widget/layout in front (as top-most widget). if the passed widget has a method named `activate_modal` (like e.g.
        :meth:`ae.kivy_help.ModalBehavior.activate_modal`) then its `activate_modal` method will be called instead.
        """
        if self.framework_win.children[0] != widget:
            reactivate_modal = getattr(widget, 'activate_modal', None)
            if callable(reactivate_modal):
                reactivate_modal()
            else:
                self.framework_win.remove_widget(widget)
                self.framework_win.add_widget(widget)

    def global_variables(self, **patches) -> Dict[str, Any]:
        """ overridden to add Kivy-specific globals. """
        return super().global_variables(escape_markup=escape_markup, get_hex_from_color=get_hex_from_color, **patches)

    def help_activation_toggle(self):  # pragma: no cover
        """ button tapped event handler to switch help mode between active and inactive (also inactivating tour). """
        activator = self.help_activator
        help_layout = self.help_layout
        tour_layout = self.tour_layout
        activate = help_layout is None and tour_layout is None
        help_id = ''
        help_vars = {}
        if activate:
            target, help_id = self.help_target_and_id(help_vars)
            help_layout = Tooltip(targeted_widget=target)
            self.framework_win.add_widget(help_layout)
        else:
            if help_layout:
                activator.ani_stop()
                ANI_SINE_DEEPER_REPEAT3.stop(help_layout)
                help_layout.ani_value = 0.99
                self.framework_win.remove_widget(help_layout)
                help_layout = None
                self.change_observable('displayed_help_id', '')

            if tour_layout:
                tour_layout.stop_tour()

        self.change_observable('help_layout', help_layout)

        if activate:
            self.help_display(help_id, help_vars)  # show found/initial help text (after self.help_layout got set)
            ANI_SINE_DEEPER_REPEAT3.start(help_layout)
            activator.ani_start()

    def load_sounds(self):
        """ override to preload audio sounds from app folder snd into sound file cache. """
        super().load_sounds()  # load from sound file paths all files into :class:`~ae.files.RegisteredFile` instances
        self.sound_files.reclassify(object_loader=lambda f: SoundLoader.load(f.path))  # :class:`~ae.files.CachedFile`

    def on_app_build(self):
        """ kivy App build event handler called at the beginning of :meth:`kivy.app.App.build`. """
        super().on_app_build()
        self.vpo("KivyMainApp.on_app_build - reload image resources from kv file late imports, e.g. ae.kivy_user_prefs")
        self.load_images()

    def on_app_built(self):
        """ kivy App build event handler called at the end of :meth:`kivy.app.App.build`. """
        self.vpo("KivyMainApp.on_app_built default/fallback event handler called")

    def on_app_pause(self):
        """ kivy :meth:`~kivy.app.App.on_pause` event handler. """
        self.vpo("KivyMainApp.on_app_pause default/fallback event handler called")

    def on_app_resume(self):
        """ kivy :meth:`~kivy.app.App.on_resume` event handler. """
        self.vpo("KivyMainApp.on_app_resume default/fallback event handler called")

    def on_app_start(self):  # pragma: no cover
        """ app start event handler - used to set the user preference app states and initial window pos and size. """
        super().on_app_start()
        self.vpo("KivyMainApp.on_app_start - setting lang, theme, win-pos/-size and softinput mode")

        get_txt.switch_lang(self.lang_code)
        self.change_light_theme(self.light_theme)
        Window.softinput_mode = self.kbd_input_mode
        Window.minimum_width = self.get_var('win_min_width', default_value=405)
        Window.minimum_height = self.get_var('win_min_height', default_value=303)

        if os_platform not in ('android', 'ios'):  # ignore last win pos on android/iOS, use always the full screen
            win_rect = self.win_rectangle or KivyMainApp.win_rectangle  # self val is empty tuple on first app start
            Window.left, Window.top = win_rect[:2]
            Window.size = win_rect[2:]

    def on_app_started(self):
        """ kivy :meth:`~kivy.app.App.on_start` event handler (called after on_app_build/on_app_built). """
        self.vpo("KivyMainApp.on_app_started event handler called - calling ae.gui_help.HelpAppBase.on_app_started")
        super().on_app_started()    # check user registration/onboarding tour start in ae.gui_help.HelpAppBase

    def on_app_stopped(self):
        """ kivy :meth:`~kivy.app.App.on_stop` event handler (called after on_app_stop). """
        self.vpo("KivyMainApp.on_app_stopped default/fallback event handler called")

    def on_flow_widget_focused(self):
        """ set focus to the widget referenced by the current flow id. """
        liw = self.widget_by_flow_id(self.flow_id)
        self.vpo(f"KivyMainApp.on_flow_widget_focused() '{self.flow_id}'"
                 f" {liw} has={getattr(liw, 'focus', 'unsupported') if liw else ''}")
        if liw and getattr(liw, 'is_focusable', False) and not liw.focus:
            liw.focus = True

    def on_kbd_input_mode_change(self, mode: str, _event_kwargs: Dict[str, Any]) -> bool:
        """ language app state change event handler.

        :param mode:            the new softinput_mode string (passed as flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                True to confirm the language change.
        """
        self.vpo(f"KivyMainApp.on_kbd_input_mode_change to {mode}")
        self.change_app_state('kbd_input_mode', mode)
        self.set_var('kbd_input_mode', mode, section=APP_STATE_SECTION_NAME)  # add optional app state var to config
        Window.softinput_mode = mode
        return True

    def on_lang_code(self):
        """ language code app-state-change-event-handler to refresh kv rules. """
        self.vpo(f"KivyMainApp.on_lang_code: language got changed to {self.lang_code}")
        get_txt.switch_lang(self.lang_code)

    def on_light_theme(self):
        """ theme app-state-change-event-handler. """
        self.vpo(f"KivyMainApp.on_light_theme: theme got changed to {self.light_theme}")
        self.change_light_theme(self.light_theme)

    def on_user_preferences_open(self, _flow_id: str, _event_kwargs: Dict[str, Any]) -> bool:
        """ enable debug mode after clicking 3 times within 6 seconds.

        :param _flow_id:        (unused).
        :param _event_kwargs:   (unused).
        :return:                False for :meth:`~.on_flow_change` get called, opening user preferences popup.
        """
        def _timeout_reset(_dt: float):
            self._debug_enable_clicks = 0

        if not self.debug:
            self._debug_enable_clicks += 1
            if self._debug_enable_clicks >= 3:
                self.on_debug_level_change(DEBUG_LEVELS[DEBUG_LEVEL_ENABLED], {})  # also enable for all sub-apps
                self._debug_enable_clicks = 0
            elif self._debug_enable_clicks == 1:
                Clock.schedule_once(_timeout_reset, 6.0)

        return False        # side-run:returning False (allowing user prefs dropdown to open)

    def play_beep(self):
        """ make a short beep sound. """
        self.play_sound('error')

    def play_sound(self, sound_name: str):
        """ play audio/sound file. """
        self.vpo(f"KivyMainApp.play_sound {sound_name}")
        file: Optional[CachedFile] = self.find_sound(sound_name)
        if file:
            try:
                sound_obj = file.loaded_object
                sound_obj.pitch = file.properties.get('pitch', 1.0)
                sound_obj.volume = (
                    file.properties.get('volume', 1.0) * self.framework_app.app_states.get('sound_volume', 1.))
                sound_obj.play()
            except Exception as ex:
                self.po(f"KivyMainApp.play_sound exception {ex}")
        else:
            self.dpo(f"KivyMainApp.play_sound({sound_name}) not found")

    def play_vibrate(self, pattern: Tuple = ERROR_VIBRATE_PATTERN):
        """ play vibrate pattern. """
        self.vpo(f"KivyMainApp.play_vibrate {pattern}")
        if self.framework_app.app_states.get('vibration_volume', 1.):  # no volume available, at least disable if 0.0
            try:  # added because it's crashing with current plyer version (master should work)
                vibrator.pattern(pattern)
            # except jnius.jnius.JavaException as ex:
            #    self.po(f"KivyMainApp.play_vibrate JavaException {ex}, update plyer to git/master")
            except Exception as ex:
                self.po(f"KivyMainApp.play_vibrate exception {ex}")

    def popups_opened(self, classes: Tuple[Widget, ...] = ()) -> List[Widget]:
        """ determine all popup-like container widgets that are currently opened.

        :param classes:         optional class filter - if not passed then only the widgets underneath win/root with an
                                `open` method will be yielded. pass tuple to restrict found popup widgets to certain
                                classes. like e.g. by passing `(Popup, DropDown, FlowPopup)` to get all popups of an
                                ae/Kivy app.
        :return:                list of opened/visible popup class instances that are children of either the
                                root layout or the app window, ordered by their z-coordinate (most upfront widget last).
                                overwritten because the children z-order is reversed in Kivy (topmost widget first).
        """
        return list(reversed(super().popups_opened(classes=classes)))

    def open_popup(self, popup_class: Type[Union[FlowPopup, Popup, DropDown]], **popup_kwargs) -> Widget:
        """ open Popup or DropDown using the `open` method. overwriting the main app class method.

        :param popup_class:     class of the Popup or DropDown widget.
        :param popup_kwargs:    args to be set as attributes of the popup class instance plus an optional
                                `parent` kwarg that will be passed as the popup parent widget arg
                                to the popup.open() method; if parent gets not specified then the root widget/layout
                                of self.framework_app will be passed into popup.open() as the widget argument.
        :return:                created and displayed/opened popup class instance.
        """
        self.dpo(f"KivyMainApp.open_popup {popup_class} {popup_kwargs}")

        # framework_win has absolute screen coordinates and lacks x, y properties, therefore use app.root as def parent
        parent = popup_kwargs.pop('parent', self.framework_root)
        popup_instance = popup_class(**popup_kwargs)
        popup_instance.open(parent)

        return popup_instance

    def text_size_guess(self, text: str, font_size: float = 0.0, padding: Tuple[float, float] = (0.0, 0.0)
                        ) -> Tuple[float, float]:
        """ quickly roughly pre-calculate texture size of a multi-line string without rendering.

        :param text:            text string which can contain line feed characters.
        :param font_size:       the font size to pseudo-render the passed text; using the value of
                                :attr:`~ae.gui_app.MainAppBase.font_size` as default if not passed.
        :param padding:         optional padding in pixels for x and y coordinate (totals for left+right/top+bottom).
        :return:                roughly the size (width, height) to display the string passed into
                                :paramref:`~text_size_guess.text`. more exactly size would need to use internal render
                                methods of Kivy, like e.g. :meth:`~kivy.uix.textinput.TextInput._get_text_width` and
                                :meth:`~kivy.core.text.LabelBase.get_extents`.
        """
        if not font_size:
            font_size = self.font_size

        char_width = font_size / 1.77
        line_height = font_size * 1.2 if text else 0
        max_width = lines_height = 0.0
        for line in text.split("\n"):
            line_width = len(line) * char_width
            if line_width > max_width:
                max_width = line_width
            lines_height += line_height

        return max_width + (padding[0] if text else 0.0), lines_height + (padding[1] if text else 0.0)

    def widget_children(self, wid: Any, only_visible: bool = False) -> List:
        """ determine the children of widget or its container (if exists) in z-order (top-most last).

        :param wid:             widget to determine the children from.
        :param only_visible:    pass True to only return visible widgets.
        :return:                list of children widgets of the passed widget.
        """
        return list(reversed(super().widget_children(wid, only_visible=only_visible)))

    @staticmethod
    def widget_pos(wid) -> Tuple[float, float]:
        """ return widget's window x/y position (overridden for absolute coordinates relative/scrollable layouts).

        :param wid:             widget to determine the position of.
        :return:                tuple of x and y screen coordinate.
        """
        return wid.to_window(*wid.pos)
