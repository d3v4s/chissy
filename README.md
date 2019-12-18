# Chissy
  
Chissy is SSH server for GNU/Linux that reject all access request and sniff the username, password and address of the client.

### ALERT: This project is under development. Test it and report a [issue](https://github.com/d3v4s/chissy/issues/new).

## Install
Download the [master](https://github.com/d3v4s/chissy/archive/master.zip) and extract it, or clone with `git`:  
`git clone https://github.com/d3v4s/chissy.git`  

Enter in the chissy directory and install the requirements:  
`pip3 install -r requirements.txt`  

Now install Chissy, than execute:  
`./install.py`

## Usage
You can run Chissy as _daemon_ through:  
`systemctl start|stop|restart|status chissy.service`

or use:  
`chissy start|get-log|remove-log|version|help [options]`  
  
Read the out of sniffing on `/var/log/chissy/`.

## Help

```
Usage: chissy start|get-log|remove-log|version|help [option]

Arguments:

    start
        starting a fake ssh server.

    get-log [options]
        show the logs create. You can specify the get-log options.

    remove-log [options]
        remove the logs. You can specify the get-log options.

    version
        get the Chissy version.

    help
        show this helps.


Options:

    get-log:
        -a --address ADDRESS
            specify the IP address
    
        -f --from-date DATE
            get only the logs before the date specified. DATE format yyyy-mm-dd.
    
        -t --to-date DATE
            get only the logs after the date specified. Use the same DATE format to -f.

    remove-log:
        -f --from-date DATE
            delete the logs before the date specified. Use the same DATE format to get-log options.
    
        -t --to-date DATE
            delete the logs after the date specified. Use the same DATE format to get-log options.

Examples:
    chissy start
    chissy get-log -a 127.0.0.1
```

## Config
Manage the configurations with the files `log.json` and `server.json` on `config` directory.  
If you have installed Chissy, you can find the configurations on `/etc/chissy/`.
