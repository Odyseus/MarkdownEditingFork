#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re

import sublime
import sublime_plugin

from . import MDETextCommand
from . import is_desired_scope

__all__ = [
    "MarkFootnotes",
    "MdeGatherMissingFootnotesCommand",
    "MdeGoToFootnoteDefinitionCommand",
    "MdeGoToFootnoteReferenceCommand",
    "MdeInsertFootnoteCommand",
    "MdeMagicFootnotesCommand",
    "MdeSortFootnotesCommand",
    "MdeSwitchToFromFootnoteCommand"
]

DEFINITION_KEY = "MarkdownEditingFork-footnote-definitions"
REFERENCE_KEY = "MarkdownEditingFork-footnote-references"
REFERENCE_REGEX = r"\[\^([^\]]*)\]"
DEFINITION_REGEX = r"^ *\[\^([^\]]*)\]:"


def get_footnote_references(view):
    ids = {}
    for ref in view.get_regions(REFERENCE_KEY):
        if not re.match(DEFINITION_REGEX, view.substr(view.line(ref))):
            id = view.substr(ref)[2:-1]
            if id in ids:
                ids[id].append(ref)
            else:
                ids[id] = [ref]
    return ids


def get_footnote_definition_markers(view):
    ids = {}
    for defn in view.get_regions(DEFINITION_KEY):
        id = view.substr(defn).strip()[2:-2]
        ids[id] = defn
    return ids


def get_footnote_identifiers(view):
    ids = sorted(get_footnote_references(view).keys())
    return ids


def get_last_footnote_marker(view):
    ids = sorted([int(a) for a in get_footnote_identifiers(view) if a.isdigit()])
    if len(ids):
        return int(ids[-1])
    else:
        return 0


def get_next_footnote_marker(view):
    return get_last_footnote_marker(view) + 1


def is_footnote_definition(view):
    line = view.substr(view.line(view.sel()[-1]))
    return re.match(DEFINITION_REGEX, line)


def is_footnote_reference(view):
    refs = view.get_regions(REFERENCE_KEY)
    for ref in refs:
        if ref.contains(view.sel()[0]):
            return True
    return False


def strip_trailing_whitespace(view, edit):
    tws = view.find(r"\s+\Z", 0)
    if tws:
        view.erase(edit, tws)


class MarkFootnotes(sublime_plugin.EventListener):

    def update_footnote_data(self, view):
        if is_desired_scope(view):
            view.add_regions(
                REFERENCE_KEY,
                view.find_all(REFERENCE_REGEX),
                "",
                "cross",
                sublime.HIDDEN)
            view.add_regions(
                DEFINITION_KEY,
                view.find_all(DEFINITION_REGEX),
                "",
                "cross",
                sublime.HIDDEN)

    def on_modified_async(self, view):
        self.update_footnote_data(view)

    def on_load(self, view):
        self.update_footnote_data(view)


class MdeGatherMissingFootnotesCommand(MDETextCommand):

    def run(self, edit):
        refs = get_footnote_identifiers(self.view)
        defs = get_footnote_definition_markers(self.view)
        missingnotes = [note_token for note_token in refs if note_token not in defs]
        if len(missingnotes):
            self.view.insert(edit, self.view.size(), "\n")
            for note in missingnotes:
                self.view.insert(edit, self.view.size(), "\n [^%s]: " % note)


class MdeInsertFootnoteCommand(MDETextCommand):

    def run(self, edit):
        view = self.view
        markernum = get_next_footnote_marker(view)
        markernum_str = "[^%s]" % markernum
        for sel in view.sel():
            startloc = sel.end()
            if bool(view.size()):
                targetloc = view.find(r"(\s|$)", startloc).begin()
            else:
                targetloc = 0
            view.insert(edit, targetloc, markernum_str)
        if len(view.sel()) > 0:
            view.insert(edit, view.size(), "\n" + markernum_str + ": ")
            view.sel().clear()
            view.sel().add(sublime.Region(view.size(), view.size()))
            view.run_command(
                "set_motion", {
                    "inclusive": True, "motion": "move_to", "motion_args": {
                        "extend": True, "to": "eof"}})
            if view.settings().get("command_mode"):
                view.run_command(
                    "enter_insert_mode", {
                        "insert_command": "move", "insert_args": {
                            "by": "characters", "forward": True}})


class MdeGoToFootnoteDefinitionCommand(MDETextCommand):

    def run(self, edit):
        defs = get_footnote_definition_markers(self.view)
        regions = self.view.get_regions(REFERENCE_KEY)

        sel = self.view.sel()
        if len(sel) == 1:
            target = None
            selreg = sel[0]

            for region in regions:
                if selreg.intersects(region):
                    target = self.view.substr(region)[2:-1]
            if not target:
                try:
                    target = self.view.substr(self.view.find(REFERENCE_REGEX, sel[-1].end()))[2:-1]
                except BaseException:
                    pass
            if target:
                self.view.sel().clear()
                self.view.sel().add(defs[target])
                self.view.show(defs[target])


class MdeGoToFootnoteReferenceCommand(MDETextCommand):

    def run(self, edit):
        refs = get_footnote_references(self.view)
        match = is_footnote_definition(self.view)
        if match:
            target = match.groups()[0]
            self.view.sel().clear()
            [self.view.sel().add(a) for a in refs[target]]
            self.view.show(refs[target][0])


class MdeMagicFootnotesCommand(MDETextCommand):

    def run(self, edit):
        if (is_footnote_definition(self.view)):
            self.view.run_command("mde_go_to_footnote_reference")
        elif (is_footnote_reference(self.view)):
            self.view.run_command("mde_go_to_footnote_definition")
        else:
            self.view.run_command("mde_insert_footnote")


class MdeSwitchToFromFootnoteCommand(MDETextCommand):

    def run(self, edit):
        if (is_footnote_definition(self.view)):
            self.view.run_command("mde_go_to_footnote_reference")
        else:
            self.view.run_command("mde_go_to_footnote_definition")


class MdeSortFootnotesCommand(MDETextCommand):

    def run(self, edit):
        strip_trailing_whitespace(self.view, edit)
        defs = get_footnote_definition_markers(self.view)
        notes = {}
        erase = []
        keyorder = map(lambda x: self.view.substr(x)[2:-1], self.view.get_regions(REFERENCE_KEY))
        keys = []
        [keys.append(r) for r in keyorder if r not in keys]

        for (key, item) in defs.items():
            fnend = self.view.find(r"(\s*\Z|\n\s*\n(?!\ {4,}))", item.end())
            fnreg = sublime.Region(item.begin(), fnend.end())
            notes[key] = self.view.substr(fnreg).strip()
            erase.append(fnreg)
        erase.sort()
        erase.reverse()
        [self.view.erase(edit, reg) for reg in erase]

        for key in keys:
            self.view.insert(edit, self.view.size(), "\n\n " + notes[key])


if __name__ == "__main__":
    pass
