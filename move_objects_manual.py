### Este script mueve un objeto y restringe el area de renderizado mediante funciones, se puede ejecutar junto al script de traslacion mediante handlers, produce una salida en la misma carpeta configurada en flamenco pero con sufijo _script.png

import random
import math
import bpy
import bpy_extras.object_utils
import sys
import argparse
import re

X_MIN, X_MAX = 0, 3.0
#Y_MIN, Y_MAX = 0, 6.0
Y_MIN, Y_MAX = 0, 6.0
Z_MIN, Z_MAX = 0, 2.0

RX_MAX = 360
RY_MAX = 360
RZ_MAX = 360

def MoveObjects(scene, camera, object_name, obj, frames_total):
    # Constantes para calcular las posiciones del objeto
    Q_X = 10
    Q_Y = 10
    Q_Z = 5
    # Constantes para calcular las rotaciones del objeto
    QR_X = 7
    QR_Y = 7
    QR_Z = 7

    if not obj:
        return

    frame = scene.frame_current
    x = (frame%Q_X * (X_MAX/Q_X)) + random.uniform(-0.3, 0.3)
    y = ((frame//Q_X)%Q_Y * (Y_MAX/Q_Y)) + random.uniform(-0.3, 0.3)
    z = ((frame//(Q_X*Q_Y))%Q_Z * (Z_MAX/Q_Z)) + random.uniform(-0.2, 0.2)

    r_x = ((frame//(Q_X*Q_Y*Q_Z))%QR_X * (RX_MAX/QR_X)) + random.uniform(-25, 25)
    r_y = ((frame//(Q_X*Q_Y*Q_Z*QR_X))%QR_Y * (RY_MAX/QR_Y)) + random.uniform(-25, 25)
    r_z = ((frame//(Q_X*Q_Y*Q_Z*QR_X*QR_Y))%QR_Z * (RZ_MAX/QR_Z)) + random.uniform(-25, 25)

    # Trasladar el objeto
    obj.location = (x, y, z)
    # Rotar el objeto
    obj.rotation_euler = (math.radians(r_x), math.radians(r_y), math.radians(r_z))
    #obj.rotation_euler = (
    #    random.uniform(0, 2 * math.pi),
    #    random.uniform(0, 2 * math.pi),
    #    random.uniform(0, 2 * math.pi)
    #)
    print(f"SCRIPT: Ubicacion del objeto: {x}; {y}; {z}")
    print(f"SCRIPT: Rotacion del objeto: {obj.rotation_euler}")
    print(f"SCRIPT: Rotaciones calculadas: {r_x}; {r_y}; {r_z}")

# Randomizar las luces de la pared de golpes
def PunchingLightsRandom(scene):
    col_lights = bpy.data.collection.get("Luces_Pared_Golpes")
    for light in col_lights.objects:
        print("SCRIPT: Luz actual: ", light)
        location = light.location
        x = location.x
        y = random.randint(0, 1)
        z = location.z
        if (y == 1):
            print("SCRIPT: Luz Prendida")
        else:
            print("SCRIPT: Luz Apagada")

        light.location = (x, y, z)

def DrawBorder(camera, scene, obj):
    print("\nHANDLER: Renderizar con borde. Frame "+str(scene.frame_current))
    print("SCRIPT: Objeto Activo Para el bounding box: ", obj)

    # Margen para el borde de renderizado
    margen_borde = 0.000000000000000000000000000000000001

    # Obtener los vertices del bounding box
    mesh = obj.bound_box

    # Obtener la matriz de las transformaciones del objeto
    matrix = obj.matrix_world
    col0 = matrix.col[0]
    col1 = matrix.col[1]
    col2 = matrix.col[2]
    col3 = matrix.col[3]

    minX = 1
    maxX = 0
    minY = 1
    maxY = 0

    numVertices = len(mesh)

    # Calcular las coordenadas de los vertices del recuadro
    for t in range(0, numVertices):
        co = mesh[t]
        pos = (col0 * co[0]) + (col1 * co[1]) + (col2 * co[2]) + col3
        pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, pos)
        if (pos.x < minX):
            minX = pos.x
        if (pos.y < minY):
            minY = pos.y
        if (pos.x > maxX):
            maxX = pos.x
        if (pos.y > maxY):
            maxY = pos.y

    render = scene.render
    render.use_border = True
    render.use_crop_to_border = False

    # Agregar un margen al borde
    minX -= margen_borde
    minY -= margen_borde
    maxX += margen_borde
    maxY += margen_borde

    # Obtener las coordenadas y la relacion con el recuado de renderizado
    pMinX = str(int(minX*render.resolution_x))
    pMinY = str(int(minY*render.resolution_y))
    pMaxX = str(int(maxX*render.resolution_x))
    pMaxY = str(int(maxY*render.resolution_y))
    print("SCRIPT: Coordenadas del borde  ("+pMinX+", "+pMinY+") - ("+pMaxX+", "+pMaxY+")")

    #render.border_min_x = minX
    #render.border_min_y = minY
    #render.border_max_x = maxX
    #render.border_max_y = maxY
    # Para asegurar que el recuadro se quede dentro de la pantalla de renderizado
    render.border_min_x = max(0.0, min(1.0, minX))
    render.border_min_y = max(0.0, min(1.0, minY))
    render.border_max_x = max(0.0, min(1.0, maxX))
    render.border_max_y = max(0.0, min(1.0, maxY))

def Renderizado(camera_name="Camera.002", object_name="Dado", frame=1, output=None, frames_total=1):
    scene = bpy.context.scene
    random.seed(scene.frame_current)
    print(f"SCRIPT: Frames a renderizar {scene.frame_end}")
    #frame_end = scene.frame_end
    #camera_name = scene.get("camera_name", "Camera")
    camera = bpy.data.objects[camera_name]
    scene.camera = camera
    obj = bpy.data.objects.get(object_name)
    print("SCRIPT: Objeto Activo: ",obj)
    print("SCRIPT: Objeto escondido vista render: ",obj.hide_render)
    print("SCRIPT: Objeto escondido vista viewport: ",obj.hide_viewport)
    obj.hide_render = False
    obj.hide_viewport = False
    obj.location = (1.5, 0.3, 1.0)
    ruta_original = scene.render.filepath
    #print("\n Renderizando Secuencia ")
    #print("\n Frames totales: " + str(frame_end))
    #for frame in range(0, 10 + 1):
    scene.frame_set(frame)
    #bpy.context.view_layer.update()
    #scene.view_layers[0].update()
    # Mover los objetos
    MoveObjects(scene, camera, object_name, obj, frames_total)
    PunchingLightsRandom(scene)
    #scene.view_layers[0].update()
    # Restringir los bordes del renderizado
    DrawBorder(camera, scene, obj)
    # Forzar la actualizacion de las transformaciones del objeto
    bpy.context.view_layer.update()

    output = output + "_script"
    match = re.search(r"#+", output)
    if match:
        hashes = match.group()
        frame_str = str(frame).zfill(len(hashes))
        scene.render.filepath = output.replace(hashes, frame_str)
    else:
        scene.render.filepath = output + str(frame).zfill(4)
    print(f"SCRIPT: Renderizado guardado en: {scene.render.filepath}")
    print(f"SCRIPT: Renderizando frame {frame}")
    bpy.ops.render.render(write_still = True)

    scene.render.filepath = ruta_original
    obj.location = (1.5, 0.3, 1.0)

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
    print("SCRIPT: output: ", args.output);
    print("SCRIPT: format: ", args.format);
    print("SCRIPT: frame: ", args.frame)
    print("SCRIPT: frames_total: ", args.frames_total)
    print("SCRIPT: camera: ", args.camera)
    print("SCRIPT: object: ", args.object)

    bpy.context.scene.render.image_settings.file_format = args.format

    Renderizado(args.camera, args.object, args.frame, args.output, args.frames_total)
else:
    Renderizado("Camera.001", "Dado", 5)

