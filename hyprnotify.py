
from gi.repository import GLib

import dbus
import dbus.service
import dbus.mainloop.glib
import subprocess

class NotifyObj(dbus.service.Object):
    messageId = 0

    @dbus.service.method("org.freedesktop.Notifications",in_signature='', out_signature='ssss')
    def GetServerInformation(self):
        return ("hyprnotify", "AIG", "0.1", "0.1")

    @dbus.service.method("org.freedesktop.Notifications",in_signature='susssasa{sv}i', out_signature='u')
    def Notify (
        self,
        app_name,    
        replaces_id,    
        app_icon,    
        summary,    
        body,    
        actions,    
        hints,    
        expire_timeout
    ):
        if expire_timeout < 0:
            expire_timeout = 5000
        subprocess.run(f"hyprctl notify 2 {expire_timeout} 0 '{summary}'",shell=True)
        NotifyObj.messageId += 1
        return NotifyObj.messageId
     
if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("org.freedesktop.Notifications", session_bus)
    object = NotifyObj(session_bus, '/org/freedesktop/Notifications')

    mainloop = GLib.MainLoop()
    mainloop.run()
