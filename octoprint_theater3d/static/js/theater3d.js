/*
 * View model for OctoPrint-Theater3d
 *
 * Author: Princton Brennan
 * License: AGPLv3
 */
$(function() {
    function Theater3dViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
         self.loginStateViewModel = parameters[0];
         self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

        self.tilt_camera_u = function (){
            console.log("running");
            var request = {
                "direction": "U"
            };

            $.ajax({
                type: "GET",
                dataType: "json",
                url: "plugin/theater3d/tilt_fxn",
                data: request,
                success: function(data){
                    console.log("success")
                }
            });

        };

        self.tilt_camera_d = function (){
            console.log("running");
            var request = {
                "direction": "D"
            };

            $.ajax({
                type: "GET",
                dataType: "json",
                url: "plugin/theater3d/tilt_fxn",
                data: request,
                success: function(data){
                    console.log("success")
                }
            });

        };
        self.pan_camera_l = function (){
            console.log("running");
            var request = {
                "direction": "L"
            };

            $.ajax({
                type: "GET",
                dataType: "json",
                url: "plugin/theater3d/pan_fxn",
                data: request,
                success: function(data){
                    console.log("success")
                }
            });

        };

        self.pan_camera_r = function (){
            console.log("running");
            var request = {
                "direction": "R"
            };

            $.ajax({
                type: "GET",
                dataType: "json",
                url: "plugin/theater3d/pan_fxn",
                data: request,
                success: function(data){
                    console.log("success")
                }
            });

        };

        self.swap_servos = function (){
            console.log("running");
            var request = {
                "opt": "servos"
            };

            $.ajax({
                type: "GET",
                dataType: "json",
                url: "plugin/theater3d/swap_fxn",
                data: request,
                success: function(data){
                    console.log("success")
                }
            });

        };

        self.swap_rotation = function (){
            console.log("running");
            var request = {
                "opt": "dir_b"
            };

            $.ajax({
                type: "GET",
                dataType: "json",
                url: "plugin/theater3d/swap_fxn",
                data: request,
                success: function(data){
                    console.log("success")
                }
            });

        };

    self.reset_servos = function (){
        console.log("running");

        $.ajax({
            type: "GET",
            dataType: "json",
            url: "plugin/theater3d/reset_fxn",
            success: function(data){
                console.log("success")
            }
        });

    };
    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: Theater3dViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_theater3d, #tab_plugin_theater3d, ...
        elements: [ /* ... */ ]
    });
});

