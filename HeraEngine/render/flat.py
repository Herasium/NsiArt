from HeraEngine.types.Vec2 import Vec2
from HeraEngine.childs.Entity import Entity

class FlatRenderer():
    def __init__(self):
        pass

    def render(self,size: Vec2,buffer,zmap,entityList: list[Entity],z:int):
        for entity in entityList:
            if not isinstance(entity,Entity):
                raise TypeError(f"Entity {entity} is not(?) an entity. ({entity.__class__.__name__})")
            if not entity.flat:
                raise TypeError(f"Entity {entity} is not a flat entity (Mais je l'avais pourtant securisé avec le cadenas)")
            
            buffer,zmap = self.render_square(entity,size,buffer,zmap,z)

        return buffer, zmap

    def render_square(self,entity: Entity,size: Vec2,buffer,zmap,z:int):
            
        start_x = max(0, entity.position.x)
        end_x   = min(size.x, entity.position.x + entity.size.x)
        start_y = max(0, entity.position.y)
        end_y   = min(size.y, entity.position.y + entity.size.y)
            

        if start_x >= end_x or start_y >= end_y:
            return  

        for y in range(start_y, end_y):
            row_start = y * size.y
            buffer[row_start + start_x : row_start + end_x] = [entity.color.value] * (end_x - start_x)
            zmap[row_start + start_x : row_start + end_x] = [z] * (end_x - start_x)

        return buffer,zmap