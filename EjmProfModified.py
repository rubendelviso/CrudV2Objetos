#  Un banco tiene 50 cuentas. Se pide hacer un programa que realice las siguientes opciones: 

# ALTA: Permitir ingresa los siguientes datos de cada cuenta (Numero de cuenta--- entero. Tipo de cuenta --- carácter (C: cuenta corriente, A: caja de ahorro).
#  Saldo de la cuenta --- flotante. 
# MODICACION: Permite cambiar el saldo de una cuenta (se busca por número de cuenta).
# CONSULTA muestra los datos de todas las cuentas.
# CONSULTA POR NUMERO DE CUENTA muestra los datos de una cuenta cualquiera (se busca por número de cuenta).
# SALIR DEL PROGRAMA

#atributos: Numero de cuenta, Tipo de cuenta, Caracter


#CC-1 Se pide modificar el software  CRUD de cuentas bancarias para que permita la gestión de Clientes con los siguientes datos (CUIL, nombre, apellido,
#fecha de nacimiento, cuentas bancarias). Cada cliente del banco puede tener múltiples cuentas.

"Usuario = Cuil(OID)/nombre/ Apellido/ Fecha de nacimiento"
"Cuenta = Tipo de cuenta/ <---Moneda de la cuenta"

" SI hay que dividir el menu para dos tipos de logins solo para uno general"
"Descubrir como vincular un usuario con +de una  cuenta (CREO QUE VOY A HACER UNA LISTA PARA CUENTA Y OTRA PARA USUARIO DESPS UNA PARA LOS DOS)*"

""
# CC-2 Se pide agregar el tipo de cuenta "cuenta sueldo"

# CC-3 Se pide que cada cuenta sea en una moneda específica dentro de las cuales pueden estar: ARS (pesos argentinos), USD (dólares americanos), BRL(real brasileño

import re
from datetime import datetime


class Fecha:
    def __init__(self, fecha_str: str = None):
        if not fecha_str:
            hoy = datetime.now()
            self.dia = hoy.day
            self.mes = hoy.month
            self.anio = hoy.year
        else:
            # validar formato de fecha dd/mm/aaaa con expresiones regulres
            if not self.es_fecha_valida(fecha_str):
                raise ValueError(
                    'Formato de fecha no válido. Debe ser dd/mm/aaaa')
            partes = str(fecha_str).split('/')
            self.dia = int(partes[0])
            self.mes = int(partes[1])
            self.anio = int(partes[2])

    def es_fecha_valida(self, fecha: str):
        patron = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
        return re.match(patron, fecha)  

    def __str__(self):
        return f"{self.dia}/{self.mes}/{self.anio}"


class Menu:
    def __init__(self,opciones):
        self.opciones_menu = opciones

    def mostrar_menu(self) -> None:
        for opcion in self.opciones_menu:
            print(opcion)

    def pedir_opcion_de_menu_valida(self) -> int:
        opcion_seleccionada = ''
        while not opcion_seleccionada.isnumeric() or \
                int(opcion_seleccionada) not in range(1, len(self.opciones_menu)+1):
            opcion_seleccionada = input('Seleccione una opción del menú: ') 
            if not opcion_seleccionada.isnumeric() or \
                    int(opcion_seleccionada) not in range(1, len(self.opciones_menu)+1):
                print(
                    f'Opción no válida. Debe ser un número entre 1 y {len(self.opciones_menu)}')
        return int(opcion_seleccionada)

#atributos: Numero de cuenta, Tipo de cuenta, Caracter
"Usuario = Cuil(OID)/nombre/ Apellido/ Fecha de nacimiento"
"Cuenta = Tipo de cuenta/ <---Moneda de la cuenta  /Saldo de la cuenta"


class Usuario:
    "Atributos Nuevos: cuil,nombre,apellido,fecha de nacimiento, cuentas bancarias: Solo agregar la cuenta sueldo"  
    def __init__(self,listaDeCuentas:list,Cuil, Nombre:str,Apellido:str,fechaDeNacimiento:str):
        self.listaDeCuentas:list["Cuenta"]=listaDeCuentas  #va a contener la lista de todas mis cuentas
        self.Cuil = Cuil
        self.Nombre = Nombre
        self.fechaDeNacimiento = fechaDeNacimiento
        self.Apellido = Apellido
        

        

    def __str__(self):
        return f"N° De cuil {self.Cuil}  Nombre de titular:{self.Nombre} -Apellido: {self.Apellido} Fecha De Nacimiento: {self.fechaDeNacimiento} Cuentas asociadas:{self.listaDeCuentas}"


class Cuil:
    def __init__(self,cuil:str):
        
        if not self.VerificarPatron(cuil):
            raise ValueError("Cuil incorrecto o no valido")
            
    
    def VerificarPatron (self,cuil:str)->bool:
        patron =r'^(20|23|24|27|30|33|34)\d{8}\d$'
        if not re.match(patron,cuil):
            return None
        else:
            self.cuil = cuil
            return True

    
    # def __str__(self):
    #     return f"Cuil:{self.cuil}"

class Cuenta:
    acumulador = 1
    "Cuenta = Tipo de cuenta/ <---Moneda de la cuenta  /Saldo de la cuenta"
    def __init__(self,TipoDeCuenta:str,Moneda:str,Saldo:str,NumCuenta:int):
        
        self.NumCuenta= Cuenta.acumulador
        self.TipoDeCuenta = TipoDeCuenta
        self.Moneda = Moneda
        self.Saldo = Saldo

        Cuenta.acumulador+=1

    
    def __str__(self):
        return f"N° de la Cuenta{self.NumCuenta}\tTipo de Cuenta{self.TipoDeCuenta}\t Moneda:{self.Moneda}\tSaldo de la cuenta:{self.Saldo}"
class GestordeCuentas:
    def __init__(self):
        self.Cuentas:list[Cuenta]=[]
        
    #El verificador lo voy a utilizar para una sentencia mas adelante para que no ejecute lo que me aparece
    #cuando creo una cuenta por primera vez, distinto de cuando quiero directamente enlazar la cuenta
    def CrearCuenta (self,inst):
        
        moneda = float('inf')
        while True:
            try:
                TipoDeCuenta= self.validarCuenta(input("Ingrese por favor el Tipo de Cuenta que desea crear\nC_Cuenta Sueldo\nA_Caja de ahorro\nC_CuentaSueldo"))
                TipoDeCuenta = TipoDeCuenta.lower()
                break
            except ValueError as e :
                print(e)
            
        while True:
            try:
                TipoDeMoneda = self.validarMoneda(input("Ingrese por favor el tipo de moneda, que va a elegir para su cuenta\n\tBRS(Pesos brasileños)\n\tARS(Pesos Argentinos)\n\tUSD(Dolares Americanos)"))

                break
            except ValueError as e:
                print(e)
        while True:
            try:
                saldo = self.validarSaldo(input("Ingrese por favor un monto valido"))
                
                break
            except ValueError as e:
                print(e)

        NuevaCuenta = Cuenta(TipoDeCuenta,TipoDeMoneda,saldo,len(self.Cuentas))
        self.Cuentas.append(NuevaCuenta)
        
        if (input("Desea Enlazar su cuenta a un usuario?\nIngrese 1 si es asi"))=='1':


            self.EnlazarCuenta(inst,NuevaCuenta)

    def EnlazarCuentaDirecto (self,instUsuario)->None:
        "Muestro cuentas/ Elijo cuenta por cuil (empaqueto la cuenta y y la mando a enlazarcuenta)/"
        "Enlazo la cuenta/Muestro cambios"
        print(f"A continuacion se mostraran los usuarios{instUsuario.MostrarCliente()}\n\nA continuacion se mostraran las cuentas{self.mostrarCuentas()}")
        while True:
            try:
                cuenta = self.pedirNumeroValido()
                break
            except ValueError as e:
                print(e)
        self.EnlazarCuenta(instUsuario,cuenta)

    def desasociarCuenta(self,instUsuario):
        "Muestro los usuarios con instUsuario.MostrarCliente()/ Pregunto que usuario es con el que va a interactuar/ Obtengo el Objeto usuario/"
        "Trato de iterar las cuentas que tenga asociadas/remuevo la cuenta una vez que coincide con el numero de cuenta"
        print("A continuacion se mostraran los clientes")
        instUsuario.MostrarCliente()
        cuil = instUsuario.VerificarCuil()
        usuario = instUsuario.ver_alumnos(cuil)
        print(f"el cliente al que modificaremos es --> {usuario}") ##bandera1
        
        lista = usuario.listaDeCuentas 
        
        self.borrarCuenta(lista)
        print("Cambios mostrados a continuacion")
        self.solo_mostrar_cuentas(lista)


        # eliminar
    def solo_mostrar_cuentas(self,list:list)->None:
        for i in range(0,len(list)):
            print(list[i])
    def borrarCuenta(self,list:list):
        for i in range(0,len(list)):
            print(list[i])
            
        numCuenta = int(input("Que cuenta desea Eliminar Ingrese el numero"))
        for i in range(0,len(list)):
            num = list[i].NumCuenta #ObjetoEntero
            
            if num == numCuenta:
                print (f" El numero de la cuenta que se va a eliminar es->{list[i].NumCuenta}")
                list.remove(list[i])
                break
    
    def ModificarSaldo(self):
        "Itero sobre la lista cuentas / Me traigo la lista cuentas/Itero parecido a cuando desasocie cuentas"
        "Uso de referencia al num de la lista /modifico el saldo de la cuenta"
        cuentas = self.Cuentas
        print("Se mostraran las cuentas a continuacion")
        self.solo_mostrar_cuentas(cuentas)
        cuentaAModificar = int(input("Cual cuenta desea modificar?"))
        objCuenta = self.obtenerNumCuenta(cuentas,cuentaAModificar)
        # self.solo_mostrar_cuentas(objCuenta)

        
        objCuenta.Saldo= input("Ingrese el nuevo saldo")
        print(f"Cambios efectuados a continuacion\n{objCuenta}")
        
    
    def obtenerNumCuenta(self,cuentas,numcuenta)->Cuenta:
        for i in range(0,len(cuentas)):
    
            if cuentas[i].NumCuenta == numcuenta:
                print(cuentas[i])
                return cuentas[i]
    
        
    def mostrarCuentas (self):
        if self.Cuentas!=0:
            for cuenta in self.Cuentas:
                print(cuenta)
        else:
            print("No hay cuentas para mostrar")
    def pedirNumeroValido(self)->Cuenta:
        NumCuenta = input("Ingrese el numero de la cuenta")
        if NumCuenta.isnumeric():
            for cuenta in self.Cuentas:
                if cuenta.NumCuenta == int(NumCuenta):
                    return cuenta
        else:
            raise ValueError("Ha ingresado un numero o un caracter invalido")

    def EnlazarCuenta(self,instance,NuevaCuenta:Cuenta)->None:#Deberia enlazar la cuenta
        
        usuario = instance.ver_alumnos(input("ingrese el Cuil del usuario al que quiere adosar su cuenta"))
        
        while not usuario:
            if not usuario:
                usuario = instance.ver_alumnos(input("Lo ingreso mal, hagalo nuevamente"))
        
        # usuario = self.EnlazarCuenta(self.instance)
        
        usuario.listaDeCuentas.append(NuevaCuenta)
        print(f"Se enlazo la cuenta con exito{usuario}")

    def validarMoneda(self,moneda:str)->str:
            
            if moneda.lower() in ['brs','ars','usd']:
                
                return moneda
            else:
                raise ValueError("moneda incorrecta o inexistente. Hagalo nuevamente:")
            
    def validarSaldo(self,saldo:str)->bool:
        if saldo.isnumeric()==False or int(saldo)<0:
            raise ValueError("Monto invalido o inexistente")
        else:
            return saldo 

        pass
    def validarCuenta(self,Char)->str:

            if not Char.lower() in ["c",'a',"s"]:
                raise ValueError("""Tipo de cuenta invalida, recorda que debe ser "C" o en su defecto "A","S" """)
            else:
                return  Char    


class GestorDeUsuarios:
    def __init__(self):
        self.usuarios: list[Usuario] = []

    def _es_fecha_nacimiento_valida(self, fecha_str: str) -> bool:
        try:
            Fecha(fecha_str)
            return True
        except ValueError:
            return False

    def _pedir_fecha_nacimiento_valida(self) -> Fecha:
        fecha_nacimiento = 'NO_VALIDA'
        while not self._es_fecha_nacimiento_valida(fecha_nacimiento):
            fecha_nacimiento = input(
                'Ingrese la fecha de nacimiento del alumno (dd/mm/aaaa): ')
            if not self._es_fecha_nacimiento_valida(fecha_nacimiento):
                print('Formato de fecha no válido. Debe ser dd/mm/aaaa')
        return Fecha(fecha_nacimiento)

    def agregar_usuario(self):
        MaxCuentas = 50
        count = 0
        "Usuario = Cuil(OID)/nombre/ Apellido/ Fecha de nacimiento"


        
        if count<=MaxCuentas:
            Nombre = input("Por favor ingrese un nombre valido")
            Apellido = input("Por favor ingrese el apellido")
            cuil= self.VerificarCuil()

            print(f"cuil guardado exitosamente{cuil}")
            fecha = self._pedir_fecha_nacimiento_valida()
            
            listaDeCuentas=[]
            usuarioNuevo = Usuario(listaDeCuentas,cuil,Nombre,Apellido,fecha)
            self.usuarios.append(usuarioNuevo)
            count+=1
        else:
            print(f"Se ha alcanzado el maximo de cuentas permitido---->{MaxCuentas}")
    
    def VerificarCuil(self)->Cuil:
        while True:
            cuil = (input("Ingrese un cuil valido por favor"))
            try:
                Cuil(cuil) #Devuelve true or exception

                return cuil
            except ValueError as e:
                    
                print(e)        
    def ConsultaCuil(self):
        print(f"A continuacion se mostrara el Usuario:{self.ver_alumnos(self.VerificarCuil())}")
    
    def MostrarCliente(self):
        if len(self.usuarios)<=0:
            print("No hay clientes para mostrar")
        else:
            for cliente in self.usuarios:
                print(f"{cliente}\n")



    "Reestructurar para que busque por cuil"
    def buscar_alumno_por_codigo(self, cuil: int) -> Usuario:
        for i in cuil:
            if i.cuil == cuil:
                return Usuario
        return None

    def modificar_alumno(self)->None:
        
        # La función de modificar solo permitirá modificar el telefono.
        
        eleccion = float('inf')
        while eleccion not in['3']:
            UsuarioAModificar = self.ver_alumnos(input("Ingrese el cuil de la persona que quiere modificar"))
            if UsuarioAModificar:
                while True:
                    if eleccion=="1":
                        UsuarioAModificar.Nombre = (input("Ingrese el nuevo nombre"))
                        print(f"Cambios mostrados a continuacion\t{UsuarioAModificar}")
                        eleccion = '3'
                        break    
                    elif eleccion=='2':
                        UsuarioAModificar.Apellido = (input("Ingrese el nuevo apellido"))
                        print(f"Cambios mostrados a continuacion\t{UsuarioAModificar}")
                        eleccion = '3'
                        break                            
                    elif eleccion =='3':
                        break

                    eleccion = input('¿Que desea modificar?\n1_Nombre\n2_Apellido_\nSi desea salir ingrese  3  ')
            else:
                print("No se encontro un cliente asociado a ese cuil")
                eleccion = '3'
            
        



    "Este metodoo no lo voy a usar"
    def eliminar_alumno(self):
        cod_alumno = int(
            input('Ingrese el código del alumno a eliminar: '))
        alumno_a_eliminar = self.buscar_alumno_por_codigo(cod_alumno)
        if alumno_a_eliminar:
            print(f"Se va a eliminar el alumno: {alumno_a_eliminar}")
            confirmacion = input(
                "¿Está seguro que desea eliminar el alumno? (S/N)")
            if confirmacion.lower() in ('s', 'si', 'sí'):
                self.alumnos.remove(alumno_a_eliminar)
                print("Alumno eliminado correctamente")
            else:
                print("Eliminación cancelada.")
        else:
            print('No se encontró el alumno con el código ingresado')
    def ver_alumnos(self,cuil:Cuil)->Usuario:
        # print(type(cuil))
        # print(f"chequeando si se guardan--->{len(self.usuarios)}")
        "probar tipos de parametros q recibe"   
        for usuario in self.usuarios:
            #print(f"""cuil del objeto{usuario.Cuil}\nCuil del input:{cuil}""")
            if usuario.Cuil == cuil:
                
                return usuario

        return None

class Main:


    def __init__(self):
        
                
        self.instanciacuentas = GestordeCuentas()
        self.instanciaUsuarios = GestorDeUsuarios()
        self.opcion = float('inf')
        while self.opcion != '3':
            if self.opcion =='1':
                self.menuCuentas()
            elif self.opcion =='2':
                self.menuCliente()
                print()
            else:
                print("Opcion incorrecta")
            self.opcion = input("Por favor ingrese una opcion\n1_Para ingresar al menu de cuentas\n2_Para ingresar al menu de clientes\n3_Para salir")
            print()


    def menuCuentas(self):
        
        opciones = ['1.Alta de Cuenta', '2. Modificación de Saldo', '3. Consulta de Todas las Cuentas',
                    '4. Consulta por Número de Cuenta', '5. Volver al menú anterior']
        menu = Menu(opciones)

        while True:
            menu.mostrar_menu()
            opcion_seleccionada = menu.pedir_opcion_de_menu_valida()
            if opcion_seleccionada == 1:
                self.instanciacuentas.CrearCuenta(self.instanciaUsuarios)
            elif opcion_seleccionada == 2:
                self.instanciacuentas.ModificarSaldo()
                
            elif opcion_seleccionada == 3:
                 self.instanciacuentas.mostrarCuentas()
            elif opcion_seleccionada == 4:
                 cuenta = self.instanciacuentas.pedirNumeroValido()
                 print(f"La cuenta que buscas es{cuenta}")
            elif opcion_seleccionada == 5:
                print('Saliendo del programa...')
                break
            else:
                print("Opcion Incorrecta")
    def menuCliente(self):
        opciones = ['1. Alta de Cliente', '2. Modificación de Cliente', '3. Consulta de Todos los Clientes',
                    '4. Consulta por Número de CUIL', '5. Asociar Cuenta a Cliente', '6. Desasociar Cuenta de Cliente',
                    '7. Volver al menú anterior']
        menu = Menu(opciones)

        while True:
            menu.mostrar_menu()
            opcion_seleccionada =  menu.pedir_opcion_de_menu_valida()
            if opcion_seleccionada == 1:
                self.instanciaUsuarios.agregar_usuario()
            elif opcion_seleccionada == 2:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                 self.instanciaUsuarios.modificar_alumno()  
            elif opcion_seleccionada == 3:  
                 self.instanciaUsuarios.MostrarCliente()
            elif opcion_seleccionada == 4:  #Muestra la cuenta por codigo
                 self.instanciaUsuarios.ConsultaCuil()
            elif opcion_seleccionada == 5:
                self.instanciacuentas.EnlazarCuentaDirecto(self.instanciaUsuarios)
            elif opcion_seleccionada == 6:
                self.instanciacuentas.desasociarCuenta(self.instanciaUsuarios)
            elif opcion_seleccionada == 7:
                print('Saliendo del programa...')
                break
            else:
                print("Opción inválida")
            print()

ejecutar = Main()

