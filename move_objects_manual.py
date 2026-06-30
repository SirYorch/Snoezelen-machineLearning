import random
import math
import bpy
import bpy_extras.object_utils
import mathutils
import sys
import argparse
import re

X_MIN, X_MAX = 0, 3.0
#Y_MIN, Y_MAX = 0, 6.0
Y_MIN, Y_MAX = 0, 5.3
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

APERTURA = (3.237, 6.0, 2.68, 2.99, 0.0, 3.0)

OBSTACULOS = [COLUMNAS]

MARGEN_OBJETOS = 0.6

COLECCION = "Objetos_Detectar"

collection = bpy.data.collections.get(COLECCION)
if collection:
    NOMBRES_OBJETOS = [obj.name for obj in collection.objects]
else:
    NOMBRES_OBJETOS = ["Dado", "Puff_01", "Puff_02"]

def MoveObjects(scene, camera, object_name, obj, frames_total):
    posiciones = mathutils.Vector.Linspace(0, Y_MAX, frames_total)
    #print("Camara activa: ",scene.camera)
    #camera = bpy.data.objects[camera_name]
    #print("Camara para renderizar: ", camera)
    #print(object_name)
    #scene.camera = camera
    #print("Camara para activa actualizada: ", scene.camera)
    #frame = scene.frame_current
    #random.seed(frame)
    #objeto_activo = scene.get(object_name, "Dado")
    #print(objeto_activo)

    for nombre in NOMBRES_OBJETOS:
        obj_comprobar = bpy.data.objects.get(nombre)
        if obj_comprobar:
            obj_comprobar.hide_render = (nombre != object_name)
            obj_comprobar.hide_viewport = (nombre != object_name)

    #obj = bpy.data.objects.get(object_name)
    print("Objeto Activo: ",obj)
    print("Objeto Vista Render: ",obj.hide_render)
    print("Objeto Vista Viewport: ",obj.hide_viewport)
    obj.hide_render = False
    obj.hide_viewport = False
    if not obj:
        return

    #obj = bpy.data.objects["Dado"]
    #print("Objeto Activo: ",obj)
    #obj.hide_render = False
    #obj.hide_viewport = False
    #colision = False
    locacion = obj.location
    #print("Vector de posiciones: ", posiciones)
    x, z = locacion.x, locacion.z
    #y = scene.frame_end * Y_MAX / scene.frame_current
    y = posiciones[scene.frame_current-1]
    obj.location = (x, y, z)
    obj.rotation_euler = (
        random.uniform(0, 2 * math.pi),
        random.uniform(0, 2 * math.pi),
        random.uniform(0, 2 * math.pi)
    )
    print(f"Ubicacion del objeto: {x}; {y}; {z}")
    print(f"Rotacion del objeto: {obj.rotation_euler}")
    #for _ in range(50):
    #    # Generar las posiciones aleatorias dentro de la sala
    #    x = random.uniform(X_MIN + MARGEN_OBJETOS, X_MAX - MARGEN_OBJETOS)
    #    y = random.uniform(Y_MIN + MARGEN_OBJETOS, Y_MAX - MARGEN_OBJETOS)
    #    z = random.uniform(Z_MIN + MARGEN_OBJETOS, Z_MAX - MARGEN_OBJETOS)

    #    # Verificar que no existan colisiones del objeto con el escenario
    #    for obstaculo in OBSTACULOS:
    #        for ox, oy, o_radio in obstaculo:
    #            distancia = math.sqrt((x - ox)**2 + (y - oy)**2)
    #            if distancia < (o_radio + MARGEN_OBJETOS):
    #                colision = True
    #                break
    #        if not colision:
    #            break

    #    # Trasladar el objeto
    #    obj.location = (x, y, z)

    #    # Rotar el objeto
    #    obj.rotation_euler = (
    #        random.uniform(0, 2 * math.pi),
    #        random.uniform(0, 2 * math.pi),
    #        random.uniform(0, 2 * math.pi)
    #    )
    # Forzar la actualizacion de las transformaciones del objeto
    bpy.context.view_layer.update()
    #scene.view_layers[0].update()
    DrawBorder(camera, scene, obj)

def DrawBorder(camera, scene, obj):
    print("\nRenderizar con borde. Frame "+str(scene.frame_current))
    print("Objeto Activo Para el bounding box: ", obj)
    #ubicacion = obj.location
    #print("Ubicacion Objeto: " + str(ubicacion[0]) + ", " + str(ubicacion[1]) + ", " + str(ubicacion[2]))

    margen_borde = 0

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
    render.use_crop_to_border = True

    # Agregar un margen al borde
    #minX -= margen_borde
    #minY -= margen_borde
    #maxX += margen_borde
    #maxY += margen_borde

    # Obtener las coordenadas y la relacion con el recuado de renderizado
    pMinX = str(int(minX*render.resolution_x))
    pMinY = str(int(minY*render.resolution_y))
    pMaxX = str(int(maxX*render.resolution_x))
    pMaxY = str(int(maxY*render.resolution_y))
    print("Coordenadas del borde  ("+pMinX+", "+pMinY+") - ("+pMaxX+", "+pMaxY+")")

    #render.border_min_x = minX
    #render.border_min_y = minY
    #render.border_max_x = maxX
    #render.border_max_y = maxY
    # Para asegurar que el recuadro se quede dentro de la pantalla de renderizado
    render.border_min_x = max(0.0, min(1.0, minX))
    render.border_min_y = max(0.0, min(1.0, minY))
    render.border_max_x = max(0.0, min(1.0, maxX))
    render.border_max_y = max(0.0, min(1.0, maxY))

# Creamos un recuadro al iniciar, para el primer frame
#scene = bpy.context.scene
#camera = bpy.data.objects['Camera.001']
#obj = bpy.data.objects["Dado"]
#DrawBorder(camera, scene, obj)

#bpy.app.handlers.frame_change_pre.clear()
#bpy.app.handlers.frame_change_pre.append(MoveObjects)

def Renderizado(camera_name="Camera", object_name="Dado", frame=1, output=None, frames_total=1):
    scene = bpy.context.scene
    print(f"Frames a renderizar {scene.frame_end}")
    #frame_end = scene.frame_end
    camera = bpy.data.objects[camera_name]
    scene.camera = camera
    obj = bpy.data.objects.get(object_name)
    obj.location = (1.5, 0.3, 1.0)
    ruta_original = scene.render.filepath
    #print("\n Renderizando Secuencia ")
    #print("\n Frames totales: " + str(frame_end))
    #for frame in range(0, 10 + 1):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    #scene.view_layers[0].update()
    MoveObjects(scene, camera, object_name, obj, frames_total)

    output = output + "_script"
    match = re.search(r"#+", output)
    if match:
        hashes = match.group()
        frame_str = str(frame).zfill(len(hashes))
        scene.render.filepath = output.replace(hashes, frame_str)
    else:
        scene.render.filepath = output + str(frame).zfill(4)
    print(f"Renderizado guardado en: {scene.render.filepath}")
    print(f"Renderizando frame {frame}")
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
    print("output: ", args.output);
    print("format: ", args.format);
    print("frame: ", args.frame)
    print("frames_total: ", args.frames_total)
    print("camera: ", args.camera)
    print("object: ", args.object)

    bpy.context.scene.render.image_settings.file_format = args.format

    Renderizado(args.camera, args.object, args.frame, args.output, args.frames_total)
else:
    Renderizado("Camera.001", "Dado", 5)

