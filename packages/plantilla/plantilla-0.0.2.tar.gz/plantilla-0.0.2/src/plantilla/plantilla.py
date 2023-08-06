def plantilla(proyecto=None, subproyecto=None):
    import os
    # from sfi import Macro

    # proyecto = Macro.getGlobal("proyecto")

    try:
        from sfi import Macro
        proyecto = Macro.getGlobal("proyecto")
        subproyecto = Macro.getGlobal("subproyecto")
    except:
        if proyecto==None:
            raise NameError("Error. Globales no definidas.")
        else:   
            proyecto = proyecto
            subproyecto = subproyecto

    path_user = ''
    
    test_path = fr"C:\Users\Administrador\Documents\MECON\{proyecto}"


    if os.path.isdir(test_path):
        path_user = test_path

    else:
        path = os.path.normpath(os.getcwd() + os.sep + os.pardir) # Get padre de la ruta del archivo

        path_user = path + '\\' + str(proyecto)

        if os.path.isdir(path_user)==False:
            raise NameError("Error 404. Directorio no encontrado, revisar nombre del proyecto")
    
    folders = []

                    

    if os.path.isdir(path_user + fr'\scripts\{subproyecto}'):
        
        print("El directorio en Script existe. Creando carpetas.")
        
        try:
            folders = [r'\data',
                        r'\data\data_in',
                        r'\data\data_out',
                        r'\docs',
                        r'\scripts',
                        fr'\scripts\{subproyecto}',
                        r'\outputs',
                        r'\outputs\figures',
                        fr'\outputs\figures\{subproyecto}',
                        r'\outputs\maps',
                        fr'\outputs\maps\{subproyecto}',
                        r'\outputs\tables',
                        fr'\outputs\tables\{subproyecto}']

        except:
            folders = [ r'\data',
                        r'\data\data_in',
                        r'\data\data_out',
                        r'\docs',
                        r'\scripts',
                        r'\outputs',
                        r'\outputs\figures',
                        r'\outputs\maps',
                        r'\outputs\tables']


        for folder in folders:

            mkdir = path_user + folder
            if os.path.isdir(mkdir)==False:
                os.mkdir(mkdir)
                print(mkdir, 'Creado')
            else:
                print(mkdir, 'ya existe')

    else:
        raise NameError("El directorio en Script no existe. Por favor, crear una carpeta en Script con el nombre del subproyecto.")
            
    path_datain	 = path_user + r'\data\data_in'
    path_dataout = path_user + r'\data\data_out'
    path_scripts = path_user + fr'\scripts\{subproyecto}'
    path_figures = path_user + fr'\outputs\figures\{subproyecto}'
    path_maps	 = path_user + fr'\outputs\maps\{subproyecto}'
    path_tables	 = path_user + fr'\outputs\tables\{subproyecto}'

    try:
        from sfi import Macro
        Macro.setGlobal('path_user', path_user)
        Macro.setGlobal('path_datain', path_datain)
        Macro.setGlobal('path_dataout', path_dataout)
        Macro.setGlobal('path_scripts', path_scripts)
        Macro.setGlobal('path_figures', path_figures)
        Macro.setGlobal('path_maps', path_maps)
        Macro.setGlobal('path_tables', path_tables)

    except:
        pass
    
if __name__ == "__main__":
    plantilla(sys.argv[1], sys.argv[2])
