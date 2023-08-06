===============
Getting Started
===============
Installation Instructions
-------------------------

1. Install python 3.7
2. The package is available via pip. pip install Maxar-OGC
3. Create a credentials file called `.ogc-config`
 
   The file should look like

| [ogc]
| user_name=<your-user-name>
| user_password=<your-password>
| user_tenant=https://securewatch.digitalglobe.com/
| user_connectid=<your-desired-connectid>



Usage Instructions
------------------
 
>>> from Maxar_OGC import Interface
    try:
     sw_ogc = Interface() # if .ogc-config was created
    except:
     sw_ogc = Interface('https://securewatch.maxar.com/','<connect_id>') # if .ogc-config was not created
>>> print(help(sw_ogc))
