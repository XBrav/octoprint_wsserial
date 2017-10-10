from __future__ import absolute_import

import os
import time
import websocket
import thread
import time
import multiprocessing
import octoprint.plugin

# master for pty, slave for tty

class WebSocketSerialBridge(octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.SimpleApiPlugin):
    m,s = os.openpty()
    ws = websocket.WebSocketApp
    status = ""
        
    def on_event(self, event, payload):
        self._logger.info("EVENT!: " + str(event))
    
    def get_settings_defaults(self):
        return dict(url="ws://127.0.0.1:81")
    
    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]
    
    def processText(self, string):
        string = string.strip('\n')
        string = string.strip('\r')
        return string
    
    def on_message(self, ws, message):
        message = self.processText(message)
        os.write(self.m,message + '\n')
        return
    
    def on_error(self, ws, error):
        print(error)
        return
    
    def on_close(self, ws):
        print("### closed ###")
        return
    
    def on_api_command(self, command, data):
        if command == "reload":
            self.ws_connect()
    
    def ws_connect(self):
        #Close old ws, just in case
        try:
            self.ws.close()
        except:
            self._logger.info("No active websocket found. This is normal at startup.")
        self.ws = websocket.WebSocketApp(self._settings.get(["url"]),
                          on_message = self.on_message,
                          on_error = self.on_error,
                          on_close = self.on_close)
        self.ws.on_open = self.on_open
        #self.ws.run_forever(skip_utf8_validation=False)    
    
    def read(self, ws):
        while True:
            command = ' '
            while command[len(command)-1] <> '\n':
                command = command + os.read(self.m,1)
                time.sleep(0.0001)
            command = self.processText(command)
            ws.send(command + '\n')
    
    def on_open(self,ws):
        self._logger.info("On Open Launched! m = " + str(self.m) + " ws = " + str(ws))
        rThread = multiprocessing.Process(target=self.read, args=(self.ws,))
        rThread.start()
    
    def on_after_startup(self):
        self._logger.info("Opened on " + os.ttyname(self.s))
        websocket.enableTrace(False)
        self.ws_connect()

__plugin_name__ = "WebSocket Serial Bridge"
__plugin_version__ = "0.1.0"
__plugin_description__ = "Emulates a serial port and pipes the data over websockets"
__plugin_implementation__ = WebSocketSerialBridge()


