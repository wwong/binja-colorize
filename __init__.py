from binaryninja import *
from color import run_plugin_globally, run_plugin_on_function

PluginCommand.register_for_function("Colorize Suspicious Instructions in Function", "Highlight suspicious instructions. Based on setColorsSiko.py from the Practical Malware Analysis blog.", run_plugin_on_function)
PluginCommand.register("Colorize All Suspicious Instructions", "Highlight suspicious instructions. Based on setColorsSiko.py from the Practical Malware Analysis blog. Runs at start-up on all known functions.", run_plugin_globally)