import os


class PluginManager:
    def __init__(self, plugin_dir):
        self.plugin_list = [plugin for plugin in os.listdir(plugin_dir) if plugin.endswith(".py")]

    def get_plugin_list(self):
        return self.plugin_list
