# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os
import subprocess
import shlex
from typing import List

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

# Logging
from loguru import logger as log

class TerminalRunner(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

        self.command_as_list: List[str] = []
        self.background_run: bool = True
        
    def on_ready(self) -> None:
        # Load persisted settings
        settings = self.get_settings()

        # Restore the last set command
        self.command_as_list = self._parse_command_string_cfg(settings.get("command_string_cfg", ""))

        # Retore background run option
        self.background_run = settings.get("background_run_cfg", True)

        log.info("Terminal Runner ready")
        
    def get_config_rows(self):
        # The actual command to be running
        self.command_string_cfg = Adw.EntryRow(title="Command to run")
        # Whether or not the command should be ran in the background (appending & to the end)
        self.background_run_cfg = Adw.SwitchRow(title="Run command in background")
        # TODO: Should I add an output handler setting?

        # Load default settings
        self.load_defaults()

        # Connect all events to their handlers
        self.command_string_cfg.connect("changed", self.on_command_string_cfg_changed)
        self.background_run_cfg.connect("notify::active", self.background_run_cfg_changed)

        # Return all rows as a list
        return [self.command_string_cfg, self.background_run_cfg]

    def load_defaults(self) -> None:
        """Load the default settings and persisted command string."""
        # Load the settings
        settings = self.get_settings()

        # Fill out config fields based on loaded settings
        self.command_string_cfg.set_text(settings.get("command_string_cfg", ""))
        self.background_run_cfg.set_active(settings.get("background_run_cfg", True))

    def on_command_string_cfg_changed(self, entry, *args):
        """Event handler for when the command string changes."""
        # Change the setting for persistence 
        settings = self.get_settings()
        settings["command_string_cfg"] = entry.get_text()
        self.set_settings(settings)

        # Parse it
        self.command_as_list = self._parse_command_string_cfg(entry.get_text())

    def _parse_command_string_cfg(self, command_string_cfg: str) -> List[str]:
        """Returns a parsed string list for the input command, following normal guidelines for BASH command argument processing."""
        return shlex.split(command_string_cfg)

    def background_run_cfg_changed(self, switch, *args):
        """Event handler for when the 'Run in Background' option changes."""
        # Change the setting for persistence 
        settings = self.get_settings()
        settings["background_run_cfg"] = switch.get_active()
        self.set_settings(settings)

        # Change local attribute
        self.background_run = switch.get_active()

    def on_key_down(self) -> None:
        """StreamController key press handler."""
        log.debug("TerminalRunner button pressed")
        log.debug(f"Running Command: '{self.command_as_list}'")

        if self.background_run:
            subprocess.run(self.command_as_list + ['&'])
        else:
            subprocess.run(self.command_as_list)