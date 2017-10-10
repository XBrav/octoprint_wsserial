#Websocket Serial Bridge

Latest Release: 0.1.0 (Or, How I Learned to love Git)

#Project Description

This plugin creates a bridge to a compatible 3D printer such as the MonoPrice Select Mini / Malyan M200 over the WiFi link on the UI controller.

#Prerequisites

- Octoprint running on a Linux platform (tested on a Raspberry Pi 3)
- Python websocket-client installed: https://github.com/websocket-client/websocket-client
- Additional serial port /dev/pts/1 added in Octoprint Settings (Printer --> Serial Connection --> Additional serial ports)

#How To Use

Clone / download the repository to the Octoprint Plugins directory (ie/ ~/.octoprint/plugins/wsserial). Once installed, set up the WiFi URL of the printer under the WebSocket Serial Bridge settings (ws://{IP}:{PORT}). Restart Octoprint once the settings are saved. (Actually, for now, restart the entire system if possible. A reminder that this is a super early release).

If successful, you should see a serial port called "/dev/pts/1" on your Serial Port list. Hit Connect to connect through the link. It should operate identical to the USB link.

#Known Bugs

- So far, only tested on my enviroment. May be missing prerequisites (file a bug report)
- On the MP Select Mini, the UI controller has been known to get saturated from messages, resulting in a hang time waiting for new commands. The best temporary workaround is to reduce Octoprint's communication timeout to 5 seconds.
- No code in place to handle re-establishing the websocket link outside of restarting Octoprint

#Release Notes:

0.1.0:

- Initial Release
- It works for me, but there's a good chance it won't work for you!
