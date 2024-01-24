```
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
-------------------------------------
```
An async request library which requests data by utilizing various proxy servers.

Automatically rotates bad proxy servers, preserves data which failed to request.
Makes scraping API's easy and fun. Written with `py-3.12.1`.


## Compiling to package

    python setup.py sdist bdist_wheel

The command above should compile the lib to a `dist` folder.


## Development dependencies
Make sure to run this command in a virtual environment

    pip install . && pip uninstall aproxyrelay -y

