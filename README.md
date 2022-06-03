# callmon_fritzbox_7170
Get emails for missed calls on fritzbox 7170

Note: This most probably only works if the language of the web interface is set to German. If you need help adapting it to another language, just contact me.

## Worum geht es?

Dieses Tool ruft periodisch eine CSV-Liste mit Anrufen von der Fritzbox 7170 ab und informiert per Email über verpasste Anrufe. Moderne Fritzboxen können dies automatisch. Die 7170 kann leider nur Emails bei hinterlassener Nachricht auf dem Anrufbeantworter verschicken. Außerdem kann man sich einmal am Tag eine Zusammenfassung aller Anrufe per Email schicken lassen.


## Installation

Zunächst müssen verschiedene Einstellungen in settings.py vorgenommen werden, u.a. die URL zur Fritzbox und Daten zum Emailserver. Dann kann callmon.py gestartet werden.

Sollte der Callmonitor auf einem Linuxserver verwendet werden, empfiehlt es sich, diesen beim Booten automatisch zu starten, z.B. per Cronjob.

`crontab -e`

Dann unten einfügen:

`@reboot sleep 60 && sudo python3 /opt/callmon/callmon.py`

wenn der Callmonitor in `/opt/callmon' liegt.
