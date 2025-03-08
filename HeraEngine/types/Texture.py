
from HeraEngine.files.raw_reader import BmpReader

from HeraEngine.types.Vec2 import Vec2

import numpy as np

class Texture():
    def __init__(self,path):
        self._original_size, self._original = BmpReader().read_file(path)
        self._original_array = np.array(self._original, dtype=np.uint32).reshape(self._original_size.y, self._original_size.x)
        self._resized_array = self._original_array
        self._size = self._original_size

    @property
    def data(self):
        return self._resized_array
    
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self,size):
        if not isinstance(size,Vec2):
            raise TypeError("Size should be a Vec2")
        
        original_h, original_w = self._original_array.shape[:2]  
        new_h, new_w = size.y, size.x
        
        sy = max(1, (new_h + original_h - 1) // original_h)
        sx = max(1, (new_w + original_w - 1) // original_w)
        
        if self._original_array.ndim == 3:
            tiled = np.kron(self._original_array, np.ones((sy, sx, 1)))
        else:
            tiled = np.kron(self._original_array, np.ones((sy, sx)))

        self._resized_array = tiled[:new_h, :new_w].astype(np.uint32)
        self._size = size
