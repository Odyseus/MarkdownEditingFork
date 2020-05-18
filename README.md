
# MarkdownEditing fork for Sublime Text 3

Fork of the Sublime Text plugin called [MarkdownEditing](https://packagecontrol.io/packages/MarkdownEditing).

## Packages that need to be disabled

- Markdown (default Sublime Text package).
- The original MarkdownEditing plugin.

## Modifications to the original plugin

- Renamed all internal commands.
- Converted all syntax files to **sublime-syntax**.
- Removed all editor settings from the syntax setting files.
- Removed all commands.
- Removed all color schemes and color scheme facilities.
- Removed all context menu items.
- Removed several key bindings.
- Removed linter. There is only SublimeLinter.
- Removed all wiki features.
- Renamed **Markdown** syntax to **Markdown GFM** and **Markdown (standard)** to **Markdown**.
- Changed all settings menu items to open the default and the user's settings in the same view and with just one click.

## Why fork the plugin?

- The **36** commands added by the original plugin were just polluting the command palette.
- The **9** context menu items added by the original plugin were just polluting the context menu.
- The original plugin added **86** key bindings. I just left **34** of the less annoying ones.
- One command was interfering with a command from another plugin. Specifically, the `IndentListItemCommand` class (`indent_list_item` command) interfered with the command of the same name provided by the **Restructured Text (RST) Snippets** plugin. So I renamed all command classes with the **Mde** prefix (**mde_** when they are *translated* to commands).
