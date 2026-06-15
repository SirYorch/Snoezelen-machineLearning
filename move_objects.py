import random
import math
import bpy

X_MIN, X_MAX = 0, 6.0
Y_MIN, Y_MAX = 0, 6.0
Z_MIN, Z_MAX = 0, 3.0

COLUMNAS = [
    (3, 2.6, 0),
    (3, 3, 0),
    (6, 2.6, 0),
    (6, 3, 0),
    (3, 2.6, 1.95),
    (3, 3, 1.95),
    (6, 2.6, 1.95),
    (6, 3, 1.95)
]

OBSTACULOS = [COLUMNAS]

MARGEN_OBJETOS = 0.6

COLECCION = "Objetos_Detectar"

collection = bpy.data.collections.get(COLECCION)
if collection:
    NOMBRES_OBJETOS = [obj.name for obj in collection.objects]
else:
    NOMBRES_OBJETOS = ["Dado", "Puff_01", "Puff_02"]

def mover_objetos(scene):
    frame = scene.frame_current
    #random.seed(frame)
    #objeto_activo = random.choice(NOMBRES_OBJETOS]
    objeto_activo = scene.get("objeto_activo", NOMBRES_OBJETOS[0])
    #objeto_activo = NOMBRES_OBJETOS[2]
    print(objeto_activo)

    for nombre in NOMBRES_OBJETOS:
        obj_comprobar = bpy.data.objects.get(nombre)
        if obj_comprobar:
            obj_comprobar.hide_render = (nombre != objeto_activo)
            obj_comprobar.hide_viewport = (nombre != objeto_activo)

    obj = bpy.data.objects.get(objeto_activo)
    if not obj:
        return

    x, y, z = 0.0, 0.0, 1.0
    for _ in range(50):
        x = random.uniform(X_MIN + MARGEN_OBJETOS, X_MAX - MARGEN_OBJETOS)
        y = random.uniform(Y_MIN + MARGEN_OBJETOS, Y_MAX - MARGEN_OBJETOS)
        z = random.uniform(Z_MIN + MARGEN_OBJETOS, Z_MAX - MARGEN_OBJETOS)

        colision = False
        for obstaculo in OBSTACULOS:
            for ox, oy, o_radio in obstaculo:
                distancia = math.sqrt((x - ox)**2 + (y - oy)**2)
                if distancia < (o_radio + MARGEN_OBJETOS):
                    colision = True
                    break
            if not colision:
                break

        obj.location = (x, y, z)

        obj.rotation_euler = (
            random.uniform(0, 2 * math.pi),
            random.uniform(0, 2 * math.pi),
            random.uniform(0, 2 * math.pi)
        )

bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(mover_objetos)
