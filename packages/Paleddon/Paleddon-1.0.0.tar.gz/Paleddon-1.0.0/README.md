# Paleddon

This command line interface allows you to quickly generate the basic structure of an extension so that you have a starting point to start developing. Although basic, the generated extension can be perfectly packaged and installed in Pale Moon.

# Install

```
pip install paleddon
```

# Usage

In command line type: `paleddon`

```
Usage: paleddon [OPTIONS] COMMAND [ARGS]...

  Paleddon CLI

Options:
  --help  Show this message and exit.

Commands:
  custom  Create addon manually
  fast    Create fast addon with default values
```

## custom command

```
paleddon custom --help

Usage: paleddon custom [OPTIONS]

  Create addon manually

Options:
  --id TEXT                    Addon ID
  --version TEXT               Initial version
  --name TEXT                  Name of extension
  --description TEXT           Addon description
  --creator TEXT               Creator of the addon
  --homepage TEXT              Repository/Addon Support Page
  --minVersion TEXT            Minimun supported browser version
  --maxVersion TEXT            Maximum supported browser version
  --existing / --not-existing  Replace addon folder if this already exist
  --help                       Show this message and exit.
```

You can run `paleddon custom` and you will be prompted for such data.

Or you can pass parameters manually, for example:

`paleddon custom --name Addonamazing`.

Parameters that are not passed will be left with their default values.

In this command, you will be asked if the extension will have a toolbar button.

## fast command

```
paleddon fast --help

Usage: paleddon fast [OPTIONS]

  Create fast addon with default values

Options:
  --existing / --not-existing  Replace addon folder if this already exist
  --help                       Show this message and exit.
```

The button on the taskbar will be added by default.