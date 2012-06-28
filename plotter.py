#!/usr/bin/python

import sys
import cairo
import math 

class Plotter:
  """Draw osm map and routing"""
  def __init__(self, nodes, filename = "plot.png"):
    self.nodes  = nodes
    self.filename = filename
    self.minLon = 180
    self.minLat = 90
    self.maxLon = -180
    self.maxLat = -90
    self.init_maximum_lat_and_long()

  def init_maximum_lat_and_long(self):
    for id, n in self.nodes.items():
      """Nodes need to be stored"""
      lat = float(n[0])
      lon = float(n[1])
      if lon < self.minLon:
        self.minLon = lon
      if lat < self.minLat:
        self.minLat = lat
      if lon > self.maxLon:
        self.maxLon = lon
      if lat > self.maxLat:
        self.maxLat = lat

  def init_coordinates(self,w,h, lat,lon, scale=1):
    """Setup an image coordinate system"""
    self.w = w
    self.h = h
    self.clat = lat
    self.clon = lon
    self.dlat = (self.maxLat - self.minLat) / scale
    self.dlon = (self.maxLon - self.minLon) / scale

  def latlong_to_coordinates(self, lat, lon):
    """Convert from lat/long to image coordinates"""
    x = self.w * (0.5 + 0.5 * (lon - self.clon) / (0.5 * self.dlon))
    y = self.h * (0.5 - 0.5 * (lat - self.clat) / (0.5 * self.dlat))
    return(x,y)

  def draw(self, route_from, route_to, route):
    """Wrapper around the routing function, which creates the output image, etc"""
    size = 1690
    scalemap = 10 # the bigger this is, the more the map zooms-in
    # Centre the map halfway between start and finish
    ctrLat = (self.nodes[route_from][0] + self.nodes[route_to][0]) / 2
    ctrLon = (self.nodes[route_from][1] + self.nodes[route_to][1]) / 2
    
    self.init_coordinates(size, size, ctrLat, ctrLon, scalemap)
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.w, self.h)
    
    self.ctx = cairo.Context(surface)
    # Dump all the nodes onto the map, to give the routes some context
    self.ctx.set_source_rgb(1.0, 0.0, 0.0)
    self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    for id,n in self.nodes.items():
      x,y = self.latlong_to_coordinates(*n)
      self.ctx.move_to(x,y)
      self.ctx.line_to(x,y)
      self.ctx.stroke()
    
    # Highlight the route
    self.draw_route(route)
    
    # Highlight which nodes were the start and end
    self.mark_node(route_from,1,1,1)
    self.mark_node(route_to,1,1,0)
    
    # Image is complete
    print "Drawing %s..." % self.filename
    surface.write_to_png(self.filename)

  def draw_route(self, route):
    """Draw the found route"""
    last = -1
    for node in route:
      if last != -1:
        self.mark_line(last,node,0.5,1.0,0.5)
      
      self.mark_node(node,0.5,1.0,0.5)
      last = node

  def mark_node(self, node, r, g, b):
    """Mark a node on the map"""
    self.ctx.set_source_rgb(r,g,b)
    lat,lon = node if isinstance(node, tuple) else self.nodes[node]
    x,y = self.latlong_to_coordinates(lat,lon)
    self.ctx.arc(x,y,2, 0,2*3.14)
    self.ctx.fill()
  
  def mark_line(self, n1, n2, r, g, b):
    """Draw a line on the map between two nodes"""
    self.ctx.set_source_rgba(r,g,b,0.3)
    lat,lon = n1 if isinstance(n1, tuple) else self.nodes[n1]
    x,y = self.latlong_to_coordinates(lat,lon)
    self.ctx.move_to(x,y)
    lat,lon = n2 if isinstance(n2, tuple) else self.nodes[n2]
    x,y = self.latlong_to_coordinates(lat,lon)
    self.ctx.line_to(x,y)
    self.ctx.stroke()

