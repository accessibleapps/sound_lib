from ctypes import pointer
from main import bass_call, update_3d_system
from pybass import *

class Listener(object):

 def get_3d_position(self):
  res = {
   'position': BASS_3DVECTOR(),
   'velocity': BASS_3DVECTOR(),
   'front': BASS_3DVECTOR(),
   'top': BASS_3DVECTOR()
  }
  bass_call(BASS_Get3DPosition, pointer(res['position']), pointer(res['velocity']), pointer(res['front']), pointer(res['top']))
  return res

 @update_3d_system
 def set_3d_position(self, position=None, velocity=None, front=None, top=None):
  """Sets the position, velocity, and orientation of the listener (ie. the player)."""
  old = self.get_3d_position()
  if position is None:
   position = old['position']
  if velocity is None:
   velocity = old['velocity']
  if front is None:
   front = old['front']
  if top is None:
   top = old['top']
  position = pointer(position)
  velocity = pointer(velocity)
  front = pointer(front)
  top = pointer(top)
  bass_call(BASS_Set3DPosition, position, velocity, front, top)

 def get_position(self):
  return self.get_3d_position()['position']

 def set_position(self, position):
  self.set_3d_position(position=position)

 position = property(fget=get_position, fset=set_position)

 def get_x(self):
  return self.position.x

 def set_x(self, val):
  old = self.position
  old.x = val
  self.position = old


 x = property(fget=get_x, fset=set_x)

 def get_y(self):
  return self.position.y

 def set_y(self, val):
  old = self.position
  old.y = val
  self.set_position(old)

 y = property(fget=get_y, fset=set_y)

 def get_z(self):
  return self.position.z

 def set_z(self, val):
  old = self.position
  old.z = val
  self.set_position(old)

 z = property(fget=get_z, fset=set_z)

 def get_velocity(self):
  return self.get_3d_position['velocity']

 def set_velocity(self, velocity):
  self.set_3d_position(velocity=velocity)

 velocity = property(fget=get_velocity, fset=set_velocity)

 def get_front(self):
  return self.get_3d_position()['front']

 def set_front(self, front):
  self.set_3d_position(front=front)

 front = property(fget=get_front, fset=set_front)

 def get_top(self):
  return self.get_3d_position()['top']

 def set_top(self, top):
  self.set_3d_position(top=top)

 top = property(fget=get_top, fset=set_top)
