# Create RSA key pair

To create RSA kay pair, use this command:  
`openssl req -new -x509 -days 365 -nodes -keyout test.key`

Now open the created file and change the first and last line on:  
`-----BEGIN RSA PRIVATE KEY-----`  
and  
`-----END RSA PRIVATE KEY-----`

> Change the `host_key_filename` on `conf/server.json` file.