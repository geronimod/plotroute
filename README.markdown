PlotRoute
=========

PlotRoute is a combination between two versions of [pyroute library](http://wiki.openstreetmap.org/wiki/PyrouteLib), routing with differents transports and routing with graphical export of routing.

Usage:
>```python route.py osm-file start_node end_node [transport] [image_filename]```
  
>```python route.py osm/tandil.osm 448193247 1355523833 # transport default "cycle", image default "plot.png"```

>```python route.py osm/tandil.osm 448193247 1355523833 car```

>```python route.py osm/tandil.osm 448193247 1355523833 foot map.png```

License
=======

The pyroute library is under its own license. Any other code added here is released under the WTFPL license.