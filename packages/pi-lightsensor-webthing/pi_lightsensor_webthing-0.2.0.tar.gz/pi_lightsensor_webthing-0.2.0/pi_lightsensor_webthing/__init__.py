from string import Template
from pi_lightsensor_webthing.app import App
from pi_lightsensor_webthing.lightsensor_webthing import run_server

PACKAGENAME = 'pi_lightsensor_webthing'
ENTRY_POINT = "lightsensor"
DESCRIPTION = "A web connected digital light sensor measuring the intensity of ambient light on Raspberry Pi"

UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=syslog.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --verbose $verbose --port $port
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')



class LightSensorApp(App):


    def do_process_command(self, command:str, port: int, verbose: bool, args) -> bool:
        if command == 'listen' and (args.gpio is not None):
            print("running " + self.packagename + " on port " + str(port))
            run_server(port, description=self.description)
            return True
        elif args.command == 'register':
            print("register " + self.packagename + " on port " + str(port) + " and starting it")
            unit = UNIT_TEMPLATE.substitute(packagename=self.packagename, entrypoint=self.entrypoint, port=port, verbose=verbose)
            self.unit.register(port, unit)
            return True
        else:
            return False


def main():
    LightSensorApp(PACKAGENAME, ENTRY_POINT, DESCRIPTION).handle_command()


if __name__ == '__main__':
    main()
