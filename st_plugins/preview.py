#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import webbrowser

import sublime
import sublime_plugin

from . import MDETextCommand
from . import plugin_name
from . import settings
from python_utils.misc_utils import get_system_tempdir
from python_utils.mistune_utils import md
from python_utils.sublime_text_utils.utils import get_file_path
from python_utils.sublime_text_utils.utils import get_view_context
from python_utils.sublime_text_utils.utils import substitute_variables

__all__ = [
    "MdeMarkdownPreviewCommand",
    "MdeMarkdownPreviewListener"
]

_html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
<title>Markdown Editing Fork - Preview</title>
{stylesheets}
</head>
<body>
<div class="content boxed">
{content}
</div>
</body>
</html>
"""

_stylesheet_link_template = '<link rel="stylesheet" href="{href}" />'


class StorageClass():
    def __init__(self):
        self.open_previews = {}


Storage = StorageClass()


class MdeMarkdownPreviewCommand(MDETextCommand):

    def run(self, edit):
        file_path = get_file_path(self.view)
        text = self.view.substr(sublime.Region(0, self.view.size()))

        if not text or not file_path:
            sublime.status_message("No content to preview")
            return

        html_file_id = "%d-%d" % (self.view.window().id(), self.view.id())
        html_file_path = os.path.join(get_system_tempdir(), plugin_name, html_file_id + ".html")

        os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

        with open(html_file_path, "w", encoding="UTF-8") as temp_file:
            temp_file.write(_html_template.format(
                stylesheets=self._ody_get_stylesheets(),
                content=md(text))
            )

        if html_file_id not in Storage.open_previews:
            Storage.open_previews = html_file_id
            webbrowser.open(html_file_path, new=2, autoraise=True)
        else:
            sublime.status_message("Reload web page")

    def _ody_get_stylesheets(self):
        stylesheets = substitute_variables(get_view_context(
            self.view), settings.get("preview_stylesheets"))

        return "\n".join([_stylesheet_link_template.format(href=s)
                          for s in stylesheets]) if stylesheets else ""


class MdeMarkdownPreviewListener(sublime_plugin.EventListener):
    def on_close(self, view):
        if view and view.id() and view.window() and view.window().id():
            html_file_id = "%d-%d" % (view.window().id(), view.id())

            if html_file_id in Storage.open_previews:
                del Storage.open_previews[html_file_id]


if __name__ == "__main__":
    pass
