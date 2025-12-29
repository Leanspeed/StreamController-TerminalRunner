# Import StreamController modules
from src.backend.PluginManager.ActionCore import ActionCore
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

# Logging
from loguru import logger as log

class TerminalRunner(ActionCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

        self.counter: int = 0
        
    def on_ready(self) -> None:
        log.info("My action is ready")
        self.set_center_label(str(self.counter))
        
    def on_key_down(self) -> None:
        self.counter += 1
        log.info(f"Counter incremented to {self.counter}")
        self.set_center_label(str(self.counter))
    
    # def on_key_up(self) -> None:
    #     print("Key up")