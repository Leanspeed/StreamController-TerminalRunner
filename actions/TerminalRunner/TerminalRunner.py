# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os
import subprocess
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

        self.command_as_list = []
        
    def on_ready(self) -> None:
        # Load persisted settings
        settings = self.get_settings()

        # Restore the last set command
        self.command_as_list = self._parse_command_string(settings.get("command_string", ""))

        log.info("My action is ready")
        
    def get_config_rows(self):
        # The actual command to be running
        # self.command_string = Adw.EntryRow(title=self.plugin_base.locale_manager.get("actions.TerminalRunner.command.string"))
        self.command_string = Adw.EntryRow(title="Command to Run")

        # TODO: Should I add an output handler setting?

        # Load default settings
        self.load_defaults()

        # Connect all events to their handlers
        self.command_string.connect("changed", self.on_command_string_changed)

        # Return all rows as a list
        return [self.command_string]

    def load_defaults(self) -> None:
        """
        Load the default settings and persisted command string.
        """
        # Load the settings
        settings = self.get_settings()

        # Fill out config fields based on loaded settings
        self.command_string.set_text(settings.get("command_string", ""))

    def on_command_string_changed(self, entry, *args):
        """
        Event handler for when the command string changes.
        """
        # Change the setting for persistence 
        settings = self.get_settings()
        settings["command_string"] = entry.get_text()
        self.set_settings(settings)

        # Parse it
        self.command_as_list = self._parse_command_string(entry.get_text())

    def _parse_command_string(self, command_string: str) -> List[str]:
        """
        Returns a parsed string list for the input command, following normal guidelines for BASH command argument processing.
        """

        # TODO: Fix parsing so it funcitons like a normal terminal command argument parser
        return command_string.split(" ")

    def on_key_down(self) -> None:
        log.info("TerminalRunner button pressed")
        log.info(f"Running Command: '{self.command_as_list}'")
        # Use subprocess to run the Command in silent mode TODO: Add configuration settings for run mode?
        # TODO: Clean this up
        subprocess.run(self.command_as_list)