# HeraEngine

## Core

La classe Core est le points centrale du game engine, permettant la mise en place de la fenetre,  du clavier, de la souris et du render.

Il peut etre initialise ainsi: 

```PYTHON
    from HeraEngine import Core

    core = Core(start_func: Fonction,update_fonction: Fonction, asset_path: Str)
```

Il utilise deux fonctions: 

```PYTHON
    self.core.start = func()
    self.core.update = func(core: Core)
```

La fonction start est appeler a l'initialisiation du projet, et l'update tout les ticks.

L'asset_path represente le dossier des textures pour les charger a l'avance.

## Types

Voici les differents types de données du projet, utilisés par l'enssemble des modules:

```PYTHON
    from HeraEngine.types import ...
```

### Vec2 

L'unite initial du projet, permetant la representation de deux valeurs, une valeur x et une valeur y.


```PYTHON
    data = Vec2(x=12,y=3.1)
    print(data.x) #12
    print(data.y) #3
```

Ils peuvent etre aditionés, soustraits, multiplies et divises, avec un autre Vec2, ou un int ou un float
### Collection

Une collection d'entite, facilitant la creation et la destruction d'entites ou de text.

```PYTHON
    collection = Collection(core: Core)
    collection.Entity(...) #Parametre identiques a l'entite classique, plus un "name" : name = entity_name
    collection.Text(...) #Idem

    collection.entity_name.position = Vec2(1,1)

    collection.quit() #Supprime toutes les entités.
```

### Texture

Represente une texture

```PYTHON
    texture = Texture(path,core: Core) #le core est optionel mais permet d'utiliser les textures pre-charges, sans lui la texture va etre recharger depuis le fichier.

    texture.size = Vec2(1,2) #redimentionne la texture, garder le meme ratio que l'original est idéal.
```


## Cursor

Cette classe represente la souris de l'utilisateur.



