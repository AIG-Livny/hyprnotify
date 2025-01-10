
import dbus
import gi

gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf, GLib

import dbus.service
import dbus.mainloop.glib
import subprocess
import datetime

def save_image_bytes(px_args):
    # gets image data and saves it to file
    # https://specifications.freedesktop.org/notification-spec/latest/
    save_path = f"/tmp/image-{datetime.datetime.now().strftime('%s')}.png"
    GdkPixbuf.Pixbuf.new_from_data(
        width=px_args[0],
        height=px_args[1],
        has_alpha=px_args[3],
        data=px_args[6],
        colorspace=GdkPixbuf.Colorspace.RGB,
        rowstride=px_args[2],
        bits_per_sample=px_args[4],
    ).savev(save_path, "png")
    return save_path

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
        message = f"{summary}{f'{chr(10)*2}{body}' if body else ''}"
        
        # Uncomment this, when Hyprland be able to show icons
        '''
        icon_path = ''
        if 'icon-data' in hints:
            icon_path = save_image_bytes(hints['icon-data'])
        elif 'icon_data' in hints:
            icon_path = save_image_bytes(hints['icon_data'])
        '''
        
        subprocess.run(f"hyprctl notify 2 {expire_timeout} 0 '{message}'",shell=True)
        NotifyObj.messageId += 1
        return NotifyObj.messageId
        
if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("org.freedesktop.Notifications", session_bus)
    object = NotifyObj(session_bus, '/org/freedesktop/Notifications')

    mainloop = GLib.MainLoop()
    mainloop.run()
