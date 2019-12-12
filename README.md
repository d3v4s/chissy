# Chissy
  
Chissy is SSH server for GNU/Linux that reject all access request and sniff the username, password and address of the client.

### ALERT: This project is under development. Test it and report a [issue](https://github.com/d3v4s/chissy/issues/new).

## Install
Before install paramiko:  
`pip install paramiko`  
or  
`pip3 install paramiko`
  
Next download the [master](https://github.com/d3v4s/chissy/archive/master.zip), extract it and run `./install.py`.

## Usage
You can run Chissy as _daemon_ through:  
`systemctl start|stop|restart chissy.service`

or use:  
`chissy start|get-log|version|help [options]`  
  
Read the out of sniffing on `/var/log/chissy/`.

## Config
Manage the configurations with the files `log.json` and `server.json` on `config` directory.  
If you have installed Chissy, you can find the configurations on `/etc/chissy/`.
