# Create RSA key pair

To create RSA kay pair, use this command:  
`openssl req -new -x509 -nodes -keyout new_rsa.key`
  
Now execute:  
`ssh-keygen -p -m PEM -f new_rsa.key`

> Change the `host-key-filename` on `conf/server.json` file.