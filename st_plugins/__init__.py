#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

root_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir)))))

import sublime_plugin

from python_utils import log_system
from python_utils.sublime_text_utils import events
from python_utils.sublime_text_utils import logger as logger_utils
from python_utils.sublime_text_utils import settings as settings_utils

package_name = os.path.basename(root_folder)
plugin_name = "MarkdownEditingFork"

_log_file = log_system.generate_log_path(storage_dir=os.path.join(root_folder, "tmp", "logs"),
                                         prefix="LOG")
logger = logger_utils.SublimeLogger(logger_name=plugin_name, log_file=_log_file)
settings = settings_utils.Settings(name_space=plugin_name, logger=logger)


@events.on("plugin_loaded")
def on_plugin_loaded():
    settings.load()


@events.on("plugin_unloaded")
def on_plugin_unloaded():
    settings.unobserve()


def is_desired_scope(view):
    """Summary

    Parameters
    ----------
    view : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    if view and len(view.sel()) > 0:
        return len(view.sel()) > 0 and bool(
            view.score_selector(view.sel()[0].a, settings.get("commands_scope", ""))
        )
    else:
        return False


class MDETextCommand(sublime_plugin.TextCommand):
    """Summary
    """

    def is_enabled(self):
        """Summary

        Returns
        -------
        TYPE
            Description
        """
        return is_desired_scope(self.view)

    def is_visible(self):
        """Summary

        Returns
        -------
        TYPE
            Description
        """
        return is_desired_scope(self.view)


if __name__ == "__main__":
    pass
