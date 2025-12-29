# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport

# Import actions
from .actions.TerminalRunner.TerminalRunner import TerminalRunner

class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__()

        ## Register actions
        self.terminal_runner_action_holder = ActionHolder(
            plugin_base = self,
            action_core = TerminalRunner,
            action_id_suffix = "TerminalRunner", # Change this to your own plugin id
            action_name = "Terminal Runner",
            action_support = {
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.terminal_runner_action_holder)

        # Register plugin
        self.register(
            plugin_name = "Terminal Runner",
            github_repo = "https://github.com/Leanspeed/StreamController-TerminalRunner",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )