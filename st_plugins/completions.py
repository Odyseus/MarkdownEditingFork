#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sublime_plugin

from . import logger
from . import settings
from python_utils.sublime_text_utils import events
from python_utils.sublime_text_utils import utils

__all__ = [
    "MdeCompletions"
]


class MdeCompletions(utils.CompletionsSuperClass, sublime_plugin.ViewEventListener):
    _completions_scope = "text.html.markdown"
    _completions = []
    _settings = settings
    _logger = logger

    def on_query_completions(self, *args, **kwargs):
        return super().on_query_completions(*args, **kwargs)


@events.on("plugin_loaded")
def on_plugin_loaded():
    MdeCompletions.update_completions()


@events.on("plugin_unloaded")
def on_plugin_unloaded():
    events.off(on_settings_changed)


@events.on("settings_changed")
def on_settings_changed(settings, **kwargs):
    """On settings changed.

    Parameters
    ----------
    settings : object
        A ``settings_utils.Settings`` instance.
    **kwargs
        Keyword arguments.
    """
    if settings.has_changed("completions"):
        MdeCompletions.update_completions()


if __name__ == "__main__":
    pass
