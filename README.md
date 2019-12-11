# Chissy

Fake SSH server to defensive analysis.

### ALERT: This project is under development. Test it and report a [issue](https://github.com/d3v4s/chissy/issues/new).

## Install
Before install paramiko:  
`pip install paramiko`  
  
Next download the [master](https://github.com/d3v4s/chissy/archive/master.zip), extract it and run `./install.py`.

## Usage
You can run Chissy as _daemon_ through:  
`systemctl start|stop|restart chissy.service`

or use:  
`chissy start|get-log|version|help [options]`
