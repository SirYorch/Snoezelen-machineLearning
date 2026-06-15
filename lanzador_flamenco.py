import bpy

COLECCION = "Objetos_Detectar"
collection = bpy.data.collections.get(COLECCION)

if not collection or len(collection.objects) == 0:
    print(f"Error la colección '{COLECCION}' está vacía o no existe")
else:
    scene = bpy.context.scene

    ruta_output = scene.render.filepath

    print(f"Lanzando Trabajos de Renderización - Total: {len(collection.objects)}")

    for obj in collection.objects:
        objeto = obj.name

        scene["objeto_activo"] = objeto

        scene.flamenco_job_name = f"Trabajo_{objeto}"

        scene.render.filepath = f"//outputs/{objeto}/######"

        try:
            print(f"Enviando '{objeto}' a la cola...")
            bpy.ops.flamenco.submit_job()
            print(f"Trabajo creado 'Trabajo_{objeto}'")
        except Exception as e:
            print(f"Error creando el trabajo 'Trabajo_{objeto}': {e}")

    scene.render.filepath = ruta_output
    print("Todo los trabajos han sido creados")
