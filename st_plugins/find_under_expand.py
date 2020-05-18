#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Re-implements `find_under_expand` command because ST refuses to use it inside macro
    definitions.

    Source: http://www.sublimetext.com/forum/viewtopic.php?f=3&t=5148
"""

import sublime
import sublime_plugin

__all__ = [
    "MdeCustomFindUnderExpandCommand"
]


class MdeCustomFindUnderExpandCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        regions = []

        for s in self.view.sel():
            word = self.view.word(sublime.Region(s.begin(), s.end()))
            regions.append(word)

        for r in regions:
            self.view.sel().add(r)


if __name__ == "__main__":
    pass
