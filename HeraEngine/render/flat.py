from HeraEngine.types.Vec2 import Vec2
from HeraEngine.types.Font import Font

from HeraEngine.childs.Entity import Entity

import numpy as np

class FlatRenderer():
    def __init__(self):
        pass

    def render(self, size: Vec2, buffer, zmap, entityList: list[Entity], z: int):
        buffer_np = np.frombuffer(buffer, dtype=np.uint32).reshape(size.y, size.x)
        zmap_np = np.frombuffer(zmap, dtype=np.int32).reshape(size.y, size.x)
        
        for entity in entityList:
            if not isinstance(entity, Entity):
                raise TypeError(f"Target is not an Entity (type: {type(entity).__name__})")
            
            pos = entity.position
            ent_size = entity.size

            if entity.is_text == True:
                self.render_text(entity, buffer_np, zmap_np, z, size, pos)
                continue
            
            if entity.textured:
                self.render_textured(entity, buffer_np, zmap_np, z, size, pos, ent_size)
                continue
                
            self.render_square(buffer_np, zmap_np, z, size, pos, ent_size, entity.color.value)

        return buffer, zmap

    def render_text(self, entity, buffer_np, zmap_np, z, size, pos):
        font = entity.font
        if not isinstance(font,Font):
            raise TypeError("Entity doesn't have valid Font.")
        
        font_size = font.size
        offset = 0

        for i in entity.text:
            texture_data = font.get_char(i).data
        
            buf_y_start, buf_y_end = np.clip([pos.y, pos.y + font_size.y], 0, size.y)
            buf_x_start, buf_x_end = np.clip([pos.x + offset, pos.x + font_size.x + offset], 0, size.x)
    
            small_y_start = max(0, -pos.y)
            small_y_end = small_y_start + (buf_y_end - buf_y_start)
            small_x_start = max(0, -pos.x)
            small_x_end = small_x_start + (buf_x_end - buf_x_start)

            buffer_view = buffer_np[buf_y_start:buf_y_end, buf_x_start:buf_x_end]
            texture_patch = texture_data[small_y_start:small_y_end, small_x_start:small_x_end]

            non_zero_mask = texture_patch != 0
            np.copyto(buffer_view, texture_patch, where=non_zero_mask)
            np.copyto(zmap_np[buf_y_start:buf_y_end, buf_x_start:buf_x_end], z, where=non_zero_mask)
            offset += font_size.x


    def render_textured(self, entity, buffer_np, zmap_np, z, size, pos, ent_size):
        texture_data = entity.texture.data
        
        buf_y_start, buf_y_end = np.clip([pos.y, pos.y + ent_size.y], 0, size.y)
        buf_x_start, buf_x_end = np.clip([pos.x, pos.x + ent_size.x], 0, size.x)
   
        small_y_start = max(0, -pos.y)
        small_y_end = small_y_start + (buf_y_end - buf_y_start)
        small_x_start = max(0, -pos.x)
        small_x_end = small_x_start + (buf_x_end - buf_x_start)

        buffer_view = buffer_np[buf_y_start:buf_y_end, buf_x_start:buf_x_end]
        texture_patch = texture_data[small_y_start:small_y_end, small_x_start:small_x_end]

        non_zero_mask = texture_patch != 0
        np.copyto(buffer_view, texture_patch, where=non_zero_mask)
        np.copyto(zmap_np[buf_y_start:buf_y_end, buf_x_start:buf_x_end], z, where=non_zero_mask)

    def render_square(self, buffer_np, zmap_np, z, size, pos, ent_size, color):
        y_start, y_end = np.clip([pos.y, pos.y + ent_size.y], 0, size.y)
        x_start, x_end = np.clip([pos.x, pos.x + ent_size.x], 0, size.x)
        
        if y_start >= y_end or x_start >= x_end:
            return

        buffer_slice = buffer_np[y_start:y_end, x_start:x_end]
        buffer_slice[:] = color
        zmap_np[y_start:y_end, x_start:x_end] = z