import random
import math
import bpy
import bpy_extras.object_utils

X_MIN, X_MAX = 0, 3.0
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
    print("Camara activa: ",scene.camera)
    camera = bpy.data.objects[camera_name]
    print("Camara para renderizar: ", camera)
    print(object_name)
    scene.camera = camera
    print("Camara para activa actualizada: ", scene.camera)
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
    print("Objeto Activo: ",obj)
    if not obj:
        return

    #obj = bpy.data.objects["Dado"]
    #print("Objeto Activo: ",obj)
    obj.hide_render = False
    #obj.hide_viewport = False
    x, y, z = 1.0, 1.0, 1.0
    for _ in range(50):
        colision = False
        # Generar las posiciones aleatorias dentro de la sala
        x = random.uniform(X_MIN + MARGEN_OBJETOS, X_MAX - MARGEN_OBJETOS)
        y = random.uniform(Y_MIN + MARGEN_OBJETOS, Y_MAX - MARGEN_OBJETOS)
        z = random.uniform(Z_MIN + MARGEN_OBJETOS, Z_MAX - MARGEN_OBJETOS)

        # Verificar que no existan colisiones del objeto con el escenario
        for obstaculo in OBSTACULOS:
            for ox, oy, o_radio in obstaculo:
                distancia = math.sqrt((x - ox)**2 + (y - oy)**2)
                if distancia < (o_radio + MARGEN_OBJETOS):
                    colision = True
                    break

        if not colision:
            # Trasladar el objeto
            obj.location = (x, y, z)

            # Rotar el objeto
            obj.rotation_euler = (
                random.uniform(0, 2 * math.pi),
                random.uniform(0, 2 * math.pi),
                random.uniform(0, 2 * math.pi)
            )
            break

    print("Ubicacion Objeto: " + str(x) + ", " + str(y) + ", " + str(z))
    # Forzar la actualizacion de las transformaciones del objeto
    #bpy.context.view_layer.update()
    #DrawBorder(camera, scene, obj)

def DrawBorder(camera, scene, obj):
    print("\nRenderizar con borde. Frame "+str(scene.frame_current))
    print("Objeto Activo Para el bounding box: ", obj)
    render = scene.render
    print("Bordes de renderizado: ",
          scene.frame_current,
          render.border_min_x,
          render.border_min_y,
          render.border_max_x,
          render.border_max_y
          )
    #ubicacion = obj.location
    #print("Ubicacion Objeto: " + str(ubicacion[0]) + ", " + str(ubicacion[1]) + ", " + str(ubicacion[2]))

    margen_borde = 0.005

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

    render.use_border = True
    #render.use_crop_to_border = True

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
    print("Coordenadas del borde  ("+pMinX+", "+pMinY+") - ("+pMaxX+", "+pMaxY+")")

    print("Borde nuevo: ",
          minX,
          minY,
          maxX,
          maxY
          )


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

def Renderizado(camera_name="Camera", object_name="Dado"):
    scene = bpy.context.scene
    frame_end = scene.frame_end
    ruta_original = scene.render.filepath
    print("\n Renderizando Secuencia ")
    print("\n Frames totales: " + str(frame_end))
    for frame in range(0, 10 + 1):
        scene.frame_set(frame)
        MoveObjects(scene, camera_name, object_name)
        scene.render.filepath = ruta_original + str(frame).zfill(4)
        print(f"Renderizando frame {frame}")
        bpy.ops.render.render(write_still = True)

    scene.render.filepath = ruta_original

def frame_handler(scene):
    random.seed(scene.frame_current)
    MoveObjects(scene, "Camera.001", "Dado")

print("Cantidad de handlers: ", len(bpy.app.handlers.frame_change_post))
for h in bpy.app.handlers.frame_change_post:
    print("Handler: ", h)

#Renderizado("Camera.001", "Puff_01")
if frame_handler not in bpy.app.handlers:
    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_post.append(frame_handler)
