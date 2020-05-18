#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sublime_plugin

from .st_plugins import settings
from python_utils.sublime_text_utils import events
from python_utils.sublime_text_utils import utils

# NOTE: Import last.
from .st_plugins.completions import *             # noqa
from .st_plugins.decide_title import *            # noqa
from .st_plugins.find_under_expand import *       # noqa
from .st_plugins.folding import *                 # noqa
from .st_plugins.footnotes import *               # noqa
from .st_plugins.headers import *                 # noqa
from .st_plugins.lists import *                   # noqa
from .st_plugins.quote_indenting import *         # noqa
from .st_plugins.references import *              # noqa
from .st_plugins.preview import *              # noqa


class ProjectSettingsController(utils.ProjectSettingsController,
                                sublime_plugin.EventListener):
    """docstring for ProjectSettingsController.
    """

    def _on_post_save_async_callback(self):
        settings.load()


def plugin_loaded():
    """On plugin loaded callback.
    """
    events.broadcast("plugin_loaded")


def plugin_unloaded():
    """On plugin unloaded.
    """
    events.broadcast("plugin_unloaded")


if __name__ == "__main__":
    pass
