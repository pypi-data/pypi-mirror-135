# ![Magic icon](./icon.png?raw=true "Magic icon") Magic

[![Repository](https://img.shields.io/badge/repository-gray.svg?logo=github)](https://github.com/TatuArvela/magic)
[![GitHub issues](https://img.shields.io/github/issues/TatuArvela/magic)](https://github.com/TatuArvela/magic/issues)
[![Pipeline status](https://github.com/TatuArvela/magic/actions/workflows/verify.yml/badge.svg?event=push)](https://github.com/TatuArvela/magic/actions/workflows/verify.yml)
[![PyPI](https://img.shields.io/pypi/v/tatuarvela-magic)](https://pypi.org/project/tatuarvela-magic/)
[![License](https://img.shields.io/github/license/TatuArvela/magic)](https://github.com/TatuArvela/magic/blob/master/LICENSE)
[![Created at Nitor](https://img.shields.io/badge/created%20at-Nitor-informational.svg)](https://nitor.com/)

Magic is a tool for turning repeated command line tasks and long, hard to
remember commands into quickly callable simple commands, **spells**.

Spells provide a simple and managed alternative to manually created aliases or
scripts.

## 🏃 Quick tour

1. To add spells, run the built-in **wizard** `magic add`
2. Spells are written into the **spellbook** file (`~/.spellbook.json`)
3. Each spell is available as a command under `magic`, which can be listed
   with `magic --help`
4. A spell can have one or several command names, which are called **magic
   words**  
   e.g. `magic build-app` and `magic ba`
5. Spells can have **arguments** passed to them  
   e.g. `magic say abra kadabra`

## 💻 Installation

Magic is designed for macOS and common Linux distributions using Bash or Zsh.
Magic also works on Windows Subsystem for Linux.

Magic requires Python 3.7 or above, and can be installed using pip:

```console
python3 -m pip install tatuarvela-magic
```

## 🪄 Usage

```console
$ magic
✨ Magic v3.1.2 © 2021 Tatu Arvela
A tool for simplifying repeated command line tasks

Usage: magic [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  add      Add spell to spellbook
  e        Example echo spell with arguments '$a0' and '$a1'
  edit     Open spellbook in editor
  example  Example echo spell with arguments '$a0' and '$a1'
```

Editing the spellbook is currently done with an external editor (**Visual Studio
Code** by default).

## 📚 Documentation

### Spell options

Spell options can be listed with the `-h` or `--help` option.

```console
$ magic example --help
Usage: magic example [OPTIONS]

  Example echo spell with arguments '$a0' and '$a1'

Options:
  -d, --delete  Delete this spell.
  -s, --show    Show details of this spell.
  -h, --help    Show this message and exit.
```

`-d` or `--delete` option can be used to delete a spell.

`-s` or `--show` option can be used to show the details of a spell.

Other options are interpreted as arguments for spells.

### Spell arguments

Spells can have an array of arguments, which are populated according to their
index, starting from 0.

Example:

```json
{
  "description": "Example echo spell with arguments '$a0' and '$a1'",
  "magicWords": [
    "e",
    "example"
  ],
  "commands": [
    "echo $a0",
    "echo $a1"
  ],
  "argumentCount": 2
}
```

```console
$ magic example cat dog
✨ Example echo spell with arguments 'cat' and 'dog'
cat
dog
✅ 12:30:43 | ⏱ 0:00:00
```

The arguments can be used in the spell description and commands.

The description arguments are replaced when displaying the spell message.

`argumentCount` property is automatically inferred from the description and
commands.

Excessive usage of arguments is considered to be an anti-pattern, it is
recommended to create separate spells instead.

#### Advanced usage: Empty arguments

Argument are handled as an ordered array. If necessary, it is possible to make
an argument an empty string: `''`.

### Messages

#### Message

Magic can print the description of a spell, filled with the provided arguments

```console
✨ Example echo spell with arguments 'cat' and 'dog'
```

`showMessage` property defaults to `true`.

#### Success message

Magic can show a success message which reports the starting time and duration of
a spell. This may be useful for longer operations.

```console
✅ 23:46:43 | ⏱ 0:00:00
```

`showSuccessMessage` property defaults to `true`.

## ⚙️ Development

Development instructions and notes can be found
in [DEVELOPMENT.md](./DEVELOPMENT.md)
