import bpy

col_objects = bpy.data.collections.get("Objetos_Detectar")
col_camaras = bpy.data.collections.get("Camaras")

if not col_objects or len(col_objects.objects) == 0:
    print("Error la colección Objetos_Detectar está vacía o no existe")
else:
    if not col_objects or len(col_objects.objects) == 0:
        print("Error la colección Camaras está vacía o no existe")
    else:
        scene = bpy.context.scene

        ruta_output = scene.render.filepath

        print(f"Lanzando Trabajos de Renderización - Total: {len(col_objects.objects)*len(col_camaras.objects)}")

        for obj in col_objects.objects:
            for camera in col_camaras.objects:
                objeto = obj.name
                camera_name = camera.name

                scene["object_name"] = objeto
                scene["camera_name"] = camera_name

                scene.flamenco_job_name = f"Trabajo_{objeto}_{camera_name}"

                scene.render.filepath = f"//outputs/{objeto}_{camera_name}/######"

                try:
                    print(f"Enviando '{objeto}' y '{camera_name}' a la cola...")
                    bpy.ops.flamenco.submit_job()
                    print(f"Trabajo creado 'Trabajo_{objeto}_{camera_name}'")
                except Exception as e:
                    print(f"Error creando el trabajo 'Trabajo_{objeto}_{camera_name}': {e}")

        scene.render.filepath = ruta_output
        print("Todo los trabajos han sido creados")
