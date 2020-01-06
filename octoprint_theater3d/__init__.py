# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

import sys, os
cd = os.getcwd()
sys.path.append(cd)

from .libs.servo_ctrlr import PanTilt_Ctrlr
import octoprint.plugin
from octoprint.events import eventManager, Events
from flask import jsonify, request, make_response, Response
from octoprint.server.util.flask import restricted_access
from datetime import datetime
from datetime import timedelta
import octoprint.util
import requests
import inspect
import threading
import json


class Theater3dPlugin(octoprint.plugin.StartupPlugin,
                      octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.BlueprintPlugin, 
                      octoprint.plugin.EventHandlerPlugin):

	##~~ Creates an instance of the Pan/Tilt Servo Controller & sets the default values
	pt_ctrlr = PanTilt_Ctrlr()
	
	def on_after_startup(self):
		self._logger.info("Theater3d is now starting.")

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]
		
	##~~ AssetPlugin mixin
	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/theater3d.js"],
			css=["css/theater3d.css"]
		)
		
	@octoprint.plugin.BlueprintPlugin.route("/pan_fxn", methods=["GET"])
	def pan_fxn(self):
		direction = request.values["direction"]
		if (direction == "L"):
			self.pt_ctrlr.pan_left()
		elif (direction == "R"):
			self.pt_ctrlr.pan_right()
		return jsonify(success=True)

	@octoprint.plugin.BlueprintPlugin.route("/tilt_fxn", methods=["GET"])
	def tilt_fxn(self):
		direction = request.values["direction"]
		if (direction == "U"):
			self.pt_ctrlr.tilt_up()
		elif (direction == "D"):
			self.pt_ctrlr.tilt_down()
		return jsonify(success=True)	

	@octoprint.plugin.BlueprintPlugin.route("/swap_fxn", methods=["GET"])
	def swap_fxn(self):
		opt = request.values["opt"]
		if (opt == "servos"):
			self.pt_ctrlr.swap_ServoAssignments()
		elif (opt == "dir_b"):
			self.pt_ctrlr.swap_pan_rotations()
			self.pt_ctrlr.swap_tlt_rotations()
                elif (opt == "dir_p"):
                        self.pt_ctrlr.swap_pan_rotations()
                elif (opt == "dir_t"):
                        self.pt_ctrlr.swap_tlt_rotations()
                elif (opt == "all"):
                        self.pt_ctrlr.swap_all()
		return jsonify(success=True)

	@octoprint.plugin.BlueprintPlugin.route("/reset_fxn", methods=["GET"])
	def reset_fxn(self):
		self.pt_ctrlr.reset_Servos()
		return jsonify(success=True)
	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			theater3d=dict(
				displayName="Theater3d Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="nerdboyq",
				repo="OctoPrint-Theater3d",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/nerdboyq/OctoPrint-Theater3d/archive/{target_version}.zip"
			)
		)
	



# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Theater3d"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Theater3dPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

