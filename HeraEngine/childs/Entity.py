from HeraEngine.types.Vec2 import Vec2
from HeraEngine.types.Vec3 import Vec3
from HeraEngine.types.Color import Color

class Entity:
    def __init__(self, layer, size, position, **kwargs):
        if layer not in {1, 2, 3, 4}:
            raise ValueError("Unknown Layer")

        if None in {size, position}:
            raise ValueError("Missing Size or Position")

        is_flat = layer in {1, 3, 4}
        expected_type = Vec2 if is_flat else Vec3

        if not isinstance(size, expected_type) or not isinstance(position, expected_type):
            raise TypeError(f"Size and Position should be of type {expected_type.__name__}")

        self.layer = layer
        self.size = size
        self.position = position
        self.dimentional = not is_flat
        self.flat = is_flat
        self.color = Color(255,255,255)
        
        for key, value in kwargs.items():
            setattr(self, key, value)

        
