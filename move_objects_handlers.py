### Este script mueve un objeto que recibimos como parametro mediante hadlers, para cuando se realiza el renderizado normal de blender+flamenco

import random
import bpy
import sys
import argparse

X_MIN, X_MAX = 0, 3.0
#Y_MIN, Y_MAX = 0, 6.0
Y_MIN, Y_MAX = 0, 5.3
Z_MIN, Z_MAX = 0, 3.0

RX_MAX = 360
RY_MAX = 360
RZ_MAX = 360

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

APERTURA = (3.237, 6.0, 2.68, 2.99, 0.0, 3.0)

OBSTACULOS = [COLUMNAS]

MARGEN_OBJETOS = 0.6

COLECCION = "Objetos_Detectar"

collection = bpy.data.collections.get(COLECCION)
if collection:
    NOMBRES_OBJETOS = [obj.name for obj in collection.objects]
else:
    NOMBRES_OBJETOS = ["Dado", "Puff_01", "Puff_02"]

def MoveObjects(scene, camera_name, object_name):
    print("HANDLER: Camara activa: ",scene.camera)
    camera = bpy.data.objects[camera_name]
    print("HANDLER: Camara para renderizar: ", camera)
    #print(object_name)
    scene.camera = camera
    print("HANDLER: Camara para activa actualizada: ", scene.camera)
    #frame = scene.frame_current
    #random.seed(frame)
    #objeto_activo = scene.get(object_name, "Dado")
    #print(objeto_activo)

    for nombre in NOMBRES_OBJETOS:
        obj_comprobar = bpy.data.objects.get(nombre)
        if obj_comprobar:
            obj_comprobar.hide_render = (nombre != object_name)
            #obj_comprobar.hide_viewport = (nombre != object_name)

    obj = bpy.data.objects.get(object_name)
    print("HANDLER: Objeto Activo: ",obj)
    if not obj:
        return

    #obj = bpy.data.objects["Dado"]
    #print("Objeto Activo: ",obj)
    obj.hide_render = False
    #obj.hide_viewport = False
    # Constantes para calcular las posiciones del objeto
    Q_X = 3
    Q_Y = 3
    Q_Z = 2
    # Constantes para calcular las rotaciones del objeto
    QR_X = 2
    QR_Y = 2
    QR_Z = 2

    frame = scene.frame_current
    x = (frame%Q_X * (X_MAX/Q_X)) + random.uniform(-0.3, 0.3)
    y = ((frame//Q_X)%Q_Y * (Y_MAX/Q_Y)) + random.uniform(-0.3, 0.3)
    z = ((frame//(Q_X*Q_Y))%Q_Z * (Z_MAX/Q_Z)) + random.uniform(-0.2, 0.2)

    r_x = ((frame//(Q_X*Q_Y*Q_Z))%QR_X * (RX_MAX/QR_X)) + random.uniform(-5, 5)
    r_y = ((frame//(Q_X*Q_Y*Q_Z*QR_X))%QR_Y * (RY_MAX/QR_Y)) + random.uniform(-5, 5)
    r_z = ((frame//(Q_X*Q_Y*Q_Z*QR_X*QR_Y))%QR_Z * (RZ_MAX/QR_Z)) + random.uniform(-5, 5)

    # Trasladar el objeto
    obj.location = (x, y, z)
    # Rotar el objeto
    obj.rotation_euler = (r_x, r_y, r_z)
    #obj.rotation_euler = (
    #    random.uniform(0, 2 * math.pi),
    #    random.uniform(0, 2 * math.pi),
    #    random.uniform(0, 2 * math.pi)
    #)
    print(f"HANDLER: Ubicacion del objeto: {x}; {y}; {z}")
    print(f"HANDLER: Rotacion del objeto: {obj.rotation_euler}")
    print(f"HANDLER: Rotaciones calculadas: {r_x}; {r_y}; {r_z}")

# Randomizar las luces de la pared de golpes
def PunchingLightsRandom(scene):
    col_lights = bpy.data.collections.get("Luces_Pared_Golpes")
    for light in col_lights.objects:
        # print("HANDLER: Luz actual: ", light)
        # print("HANDLER: Luz actual ubicacion: ", light.location)
        location = light.location
        x = location.x
        z = location.z
        state = random.randint(0, 10)
        if (state >= 8):
            y = 1
            print("HANDLER: Luz Prendida")
        else:
            y = 0
            print("HANDLER: Luz Apagada")

        light.location = (x, y, z)

argv = sys.argv
argv = argv[argv.index("--")+1:]

if argv:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--format", type=str, required=True)
    parser.add_argument("--frame", type=int, required=True)
    parser.add_argument("--frames_total", type=int, required=True)
    parser.add_argument("--camera", type=str, required=True)
    parser.add_argument("--object", type=str, required=True)
    args, unknow = parser.parse_known_args(argv)
    print("HANDLER: output: ", args.output);
    print("HANDLER: format: ", args.format);
    print("HANDLER: frame: ", args.frame)
    print("HANDLER: frames_total: ", args.frames_total)
    print("HANDLER: camera: ", args.camera)
    print("HANDLER: object: ", args.object)

def frame_handler(scene):
    random.seed(scene.frame_current)
    MoveObjects(scene, "Camera.001", "Dado")
    PunchingLightsRandom(scene)

print("HANDLER: Cantidad de handlers: ", len(bpy.app.handlers.frame_change_post))
for h in bpy.app.handlers.frame_change_post:
    print("Handler: ", h)

#Renderizado("Camera.001", "Puff_01")
if frame_handler not in bpy.app.handlers:
    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_post.append(frame_handler)
