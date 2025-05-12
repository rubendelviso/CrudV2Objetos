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
                raise ValueError('Formato de fecha no válido. Debe ser dd/mm/aaaa')
            partes = str(fecha_str).split('/')
            self.dia = int(partes[0])
            self.mes = int(partes[1])
            self.anio = int(partes[2])

    def es_fecha_valida(self, fecha: str):
        patron = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
        return re.match(patron, fecha)

    def __str__(self):
        return f"{self.dia}/{self.mes}/{self.anio}"


class Cuenta:
    """Representa una cuenta bancaria con sus datos."""

    def __init__(self, numero_cuenta: int, tipo_cuenta: str, saldo: float, moneda: str):
        """Inicializa una cuenta bancaria."""
        if tipo_cuenta.upper() not in ('C', 'A', 'S'):
            raise ValueError("Tipo de cuenta inválido. Debe ser 'C' (Corriente) o 'A' (Ahorro) o 'S' (Sueldo).")
        if not isinstance(numero_cuenta, int) or numero_cuenta <= 0:
            raise ValueError("El número de cuenta debe ser un entero positivo.")
        if not isinstance(saldo, (int, float)):
            raise ValueError("El saldo debe ser un valor numérico.")
        if moneda.upper() not in ('ARS', 'USD', 'BRL'):
            raise ValueError("Moneda inválido. Debe ser ARS (pesos argentinos), USD (dolares), BRL (real brasileño).")

        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta.upper()  # Almacenar en mayúscula para consistencia
        self.saldo = float(saldo)  # Asegurar que sea flotante
        self.moneda = moneda

    def __str__(self) -> str:
        """Devuelve una representación legible de la cuenta."""
        tipo_str = None
        if self.tipo_cuenta == 'C':
            tipo_str = "Cuenta corriente"
        elif self.tipo_cuenta == 'A':
            tipo_str = "Caja de ahorro"
        else:
            tipo_str = "Cuenta sueldo"
        # Formatear saldo con 2 decimales y separador de miles si es necesario
        return (f"CUENTA N°: {self.numero_cuenta} - Tipo: {tipo_str} ({self.tipo_cuenta}) "
                f"- Saldo: ${self.saldo:,.2f} - Moneda: {self.moneda}")  # Formato de moneda


class Cliente:
    """Representa una cliente del banco con sus datos."""

    def __init__(self, cuil: str, nombre: str, apellido: str, fecha_nac: Fecha, cuentas: [Cuenta] = None):
        """Inicializa un cliente."""
        self.cuil: str = cuil
        self.nombre: str = nombre
        self.apellido: str = apellido
        self.fecha_nacimiento: Fecha = fecha_nac
        self.cuentas: [Cuenta] = []
        if cuentas is not None:
            self.cuentas: [Cuenta] = cuentas

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def asociar_cuenta(self, cuenta: Cuenta):
        self.cuentas.append(cuenta)

    def desasociar_cuenta(self, cuenta: Cuenta):
        self.cuentas.remove(cuenta)

    def __str__(self) -> str:
        """Devuelve una representación legible del cliente"""
        return f"Cliente {self.nombre_completo()} ({self.cuil}) - Nacimiento: {self.fecha_nacimiento}"


class Menu:
    """Gestiona la presentación y selección de opciones de un menú bancario."""

    def __init__(self, opciones: [str]):
        if not isinstance(opciones, list):
            raise ValueError("El parametro opciones debe ser una lista de opciones")
        self.opciones_menu = opciones

    def mostrar_menu(self) -> None:
        """Muestra las opciones del menú en la consola."""
        print("\n--- MENÚ BANCARIO ---")
        for opcion in self.opciones_menu:
            print(opcion)
        print("---------------------")

    def pedir_opcion_de_menu_valida(self) -> int:
        """Solicita al usuario una opción del menú y la valida."""
        opcion_seleccionada = ''
        num_opciones = len(self.opciones_menu)
        while not opcion_seleccionada.isdigit() or \
                int(opcion_seleccionada) not in range(1, num_opciones + 1):
            opcion_seleccionada = input(f'Seleccione una opción (1-{num_opciones}): ')
            if not opcion_seleccionada.isdigit() or \
                    int(opcion_seleccionada) not in range(1, num_opciones + 1):
                print(f'Opción no válida. Debe ser un número entre 1 y {num_opciones}.')
        return int(opcion_seleccionada)


class GestorDeCuentas:
    """Gestiona la colección de cuentas bancarias (altas, modificaciones, consultas)."""
    MAX_CUENTAS = 50

    def __init__(self):
        """Inicializa el gestor con una lista vacía de cuentas."""
        self.cuentas: list[Cuenta] = []

    def buscar_cuenta_por_numero(self, numero_cuenta: int) -> Cuenta | None:
        """Busca una cuenta por su número. Devuelve la Cuenta o None si no se encuentra."""
        for cuenta in self.cuentas:
            if cuenta.numero_cuenta == numero_cuenta:
                return cuenta
        return None

    def pedir_numero_cuenta_valido(self, mensaje_prompt: str) -> int:
        """
        Solicita un número de cuenta (entero positivo).
        Devuelve el número como entero.
        """
        while True:
            num_str = input(mensaje_prompt).strip().lower()
            try:
                num_int = int(num_str)
                if num_int > 0:
                    return num_int
                else:
                    print("El número de cuenta debe ser un entero positivo.")
            except ValueError:
                print("Entrada inválida. Por favor ingrese un número entero positivo o 'c' para cancelar.")

    def _pedir_tipo_cuenta_valido(self) -> str:
        """Solicita un tipo de cuenta ('C' o 'A')."""
        while True:
            tipo_str = input(
                "Ingrese el tipo de cuenta (C: Corriente, A: Ahorro, S: Cuenta Sueldo): ").strip().lower()
            if tipo_str.upper() in ('C', 'A', 'S'):
                return tipo_str.upper()
            else:
                print("Tipo de cuenta inválido. Ingrese 'C' o 'A' o 'S.")

    def _pedir_moneda_valida(self) -> str:
        """Solicita una moneda ('ARS' o 'USD' o 'BRL')."""
        while True:
            moneda_str = input(
                "Ingrese la moneda en la que esta la cuenta (ARS: Pesos Argentinos, USD: Dolares, BRL: Reales): ").strip().lower()
            if moneda_str.upper() in ('ARS', 'USD', 'BRL'):
                return moneda_str.upper()
            else:
                print("Tipo de moneda inválido. Ingrese 'ARS' o 'USD' o 'BRL.")

    def _pedir_saldo_valido(self) -> float | None:
        """Solicita un saldo inicial (flotante)."""
        while True:
            saldo_str = input("Ingrese el saldo inicial: ").strip().lower()
            try:
                # Reemplazar coma por punto si se usa como decimal
                saldo_float = float(saldo_str.replace(',', '.'))
                return saldo_float
            except ValueError:
                print("Entrada inválida. Por favor ingrese un valor numérico para el saldo (ej: 1500.50).")

    def agregar_cuenta(self):
        """Solicita datos y agrega una nueva cuenta si hay capacidad y el número es único."""
        print("\n--- Alta de Nueva Cuenta ---")

        if len(self.cuentas) >= self.MAX_CUENTAS:
            print(f"Error: Se ha alcanzado la capacidad máxima de {self.MAX_CUENTAS} cuentas.")
            print("No se puede agregar una nueva cuenta.")
            return

        # Pedir número de cuenta asegurando que sea único
        numero_cuenta = None
        while numero_cuenta is None:
            num_temp = self.pedir_numero_cuenta_valido("Ingrese el número para la nueva cuenta (entero positivo): ")
            if self.buscar_cuenta_por_numero(num_temp):
                print(f"Error: El número de cuenta {num_temp} ya existe. Intente con otro.")
            else:
                numero_cuenta = num_temp  # Número válido y único

        # Pedir tipo de cuenta
        tipo_cuenta = self._pedir_tipo_cuenta_valido()

        # Pedir saldo inicial
        saldo = self._pedir_saldo_valido()

        # Pedir moneda válida
        moneda = self._pedir_moneda_valida()

        # Crear y agregar la cuenta
        try:
            nueva_cuenta = Cuenta(numero_cuenta, tipo_cuenta, saldo, moneda)
            self.cuentas.append(nueva_cuenta)
            print("-" * 28)
            print(f"¡Cuenta N° {numero_cuenta} agregada con éxito!")
            print(nueva_cuenta)
            print("-" * 28)
        except ValueError as e:
            # Esto no debería ocurrir por las validaciones previas, pero es una salvaguarda
            print(f"Error inesperado al crear la cuenta: {e}")
            print("Alta cancelada.")

    def modificar_saldo_cuenta(self):
        """Solicita número de cuenta, la busca y permite modificar su saldo."""
        print("\n--- Modificar Saldo de Cuenta ---")
        if not self.cuentas:
            print("No hay cuentas registradas para modificar.")
            return

        numero_cuenta = self.pedir_numero_cuenta_valido(
            'Ingrese el número de cuenta a modificar: ')

        cuenta_a_modificar = self.buscar_cuenta_por_numero(numero_cuenta)

        if cuenta_a_modificar:
            print(f"Se modificará el saldo de la cuenta: {cuenta_a_modificar}")
            nuevo_saldo = self._pedir_saldo_valido()
            cuenta_a_modificar.saldo = nuevo_saldo  # Actualizar el saldo
            print("-" * 28)
            print(f"¡Saldo de la cuenta {cuenta_a_modificar.numero_cuenta} modificado correctamente!")
            print(f"Nuevo estado: {cuenta_a_modificar}")
            print("-" * 28)
        else:
            print(f'Error: No se encontró ninguna cuenta con el número {numero_cuenta}.')

    def ver_cuentas(self):
        """Muestra un listado de todas las cuentas registradas, ordenadas por número."""
        print("\n--- Listado de Todas las Cuentas ---")
        if not self.cuentas:
            print("No hay cuentas registradas.")
        else:
            for cuenta in self.cuentas:
                print(cuenta)
        print("-" * 35)

    def buscar_y_mostrar_cuenta(self):
        """Pide un número de cuenta, la busca y muestra su información si la encuentra."""
        print("\n--- Buscar Cuenta por Número ---")
        if not self.cuentas:
            print("No hay cuentas registradas para buscar.")
            return

        numero_cuenta = self.pedir_numero_cuenta_valido(
            'Ingrese el número de la cuenta a buscar: ')
        cuenta_buscada = self.buscar_cuenta_por_numero(numero_cuenta)
        if cuenta_buscada:
            print("\n--- Cuenta Encontrada ---")
            print(cuenta_buscada)
            print("------------------------\n")
        else:
            print(f'No se encontró ninguna cuenta con el número {numero_cuenta}.')


class GestorDeClientes:
    """Gestiona la colección de clientes (altas, modificaciones, consultas)."""

    def __init__(self, gestor_de_cuentas: GestorDeCuentas):
        """Inicializa el gestor con una lista vacía de cuentas."""
        self.clientes: list[Cliente] = []
        self.gestor_de_cuentas = gestor_de_cuentas

    def _buscar_cliente_por_cuil(self, cuil: str) -> Cliente | None:
        """Busca un cliente por su cuil. Devuelve el Cliente o None si no se encuentra."""
        for cliente in self.clientes:
            if cliente.cuil == cuil:
                return cliente
        return None

    def _pedir_cuil_valido(self) -> str:
        """Solicita un Cuil valido."""
        cuil = None
        while cuil is None:
            cuil_temp = input("Ingrese el CUIL del cliente: ")
            if self._buscar_cliente_por_cuil(cuil_temp):
                print(f"Error: El CUIL {cuil_temp} ya existe. Intente con otro.")
            else:
                cuil = cuil_temp  # CUIL válido y único
        return cuil

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

    def agregar_cliente(self):
        """Solicita datos y agrega un nuevo cliente."""
        print("\n--- Alta de Cliente ---")
        cuil = self._pedir_cuil_valido()
        nombre = input("Ingrese el nombre del cliente: ")
        apellido = input("Ingrese el apellido del cliente: ")
        fecha_nacimiento = self._pedir_fecha_nacimiento_valida()
        cliente = Cliente(cuil, nombre, apellido, fecha_nacimiento)
        self.clientes.append(cliente)
        print("-" * 28)
        print(f"¡Cliente agregada con éxito!")
        print(cliente)
        print("-" * 28)

    def modificar_cliente(self):
        """Modifica los datos del cliente"""
        print("\n--- Modificar Cliente ---")
        if not self.clientes:
            print("No hay clientes registrados para modificar.")
            return

        cuil_a_buscar = self._pedir_cuil_valido()

        cliente_a_modificar = self._buscar_cliente_por_cuil(cuil_a_buscar)

        if cliente_a_modificar is not None:
            print(f"Se modificará el cliente: {cliente_a_modificar}")
            nuevo_nombre = input("Ingrese el nuevo nombre del cliente o Enter si no quiere cambiar.")
            if not nuevo_nombre:
                cliente_a_modificar.nombre = nuevo_nombre
            nuevo_apellido = input("Ingrese el nuevo apellido del cliente o Enter si no quiere cambiar.")
            if not nuevo_apellido:
                cliente_a_modificar.apellido = nuevo_apellido
            print("-" * 28)
            print("¡Cliente modificado correctamente!")
            print(cliente_a_modificar)
            print("-" * 28)
        else:
            print(f'Error: No se encontró ningun cliente con CUIL {cuil_a_buscar}.')

    def ver_clientes(self):
        """Muestra un listado de todas los clientes registrados."""
        print("\n--- Listado de Todos los Clientes ---")
        if not self.clientes:
            print("No hay clientes registrados.")
        else:
            for cliente in self.clientes:
                print(cliente)
        print("-" * 35)

    def buscar_y_mostrar_cliente(self):
        """Pide un número de cuil, lo busca y muestra su información si lo encuentra."""
        print("\n--- Buscar Cliente por CUIL ---")
        if not self.clientes:
            print("No hay clientes registrados para buscar.")
            return
        cuil_a_consultar = input("Ingrese el CUIL del cliente al que quiere buscar: ")
        cliente_encontrado = self._buscar_cliente_por_cuil(cuil_a_consultar)
        if cliente_encontrado:
            print("\n--- Cliente Encontrado ---")
            print(cliente_encontrado)
            if cliente_encontrado.cuentas:
                print("Cuentas asociadas")
                for cuenta_del_cliente in cliente_encontrado.cuentas:
                    print(cuenta_del_cliente)
            print("------------------------\n")
        else:
            print(f'No se encontró ningun cliente con el CUIL {cuil_a_consultar}.')

    def asociar_cuenta_a_cliente(self):
        print("\n--- Asociacion de Cuentas a Clientes")
        cliente: Cliente = self._buscar_cliente_por_cuil(input("Ingrese el CUIL del cliente al que quiere asociar cuentas: "))
        if cliente:
            numero_de_cuenta_a_asociar = self.gestor_de_cuentas.pedir_numero_cuenta_valido(
                f"Ingrese el número de cuenta a asociar al cliente {cliente.cuil}")
            cuenta_a_asociar = self.gestor_de_cuentas.buscar_cuenta_por_numero(numero_de_cuenta_a_asociar)
            if cuenta_a_asociar:
                cliente.asociar_cuenta(cuenta_a_asociar)
                print(f"Cuenta {cuenta_a_asociar} asociada correctamenta a {cliente}")
            else:
                print(f"No se encontró la cuenta con número {numero_de_cuenta_a_asociar}")

    def desasociar_cuenta_a_cliente(self):
        print("\n--- Desasociacion de Cuentas a Clientes")
        cliente: Cliente = self._buscar_cliente_por_cuil(input("Ingrese el CUIL del cliente al que quiere desasociar cuentas: "))
        if cliente:
            numero_de_cuenta_a_asociar = self.gestor_de_cuentas.pedir_numero_cuenta_valido(
                f"Ingrese el número de cuenta a desasociar al cliente {cliente.cuil}")
            cuenta_a_asociar = self.gestor_de_cuentas.buscar_cuenta_por_numero(numero_de_cuenta_a_asociar)
            if cuenta_a_asociar:
                cliente.desasociar_cuenta(cuenta_a_asociar)
                print(f"Cuenta {cuenta_a_asociar} desasociada correctamenta a {cliente}")
            else:
                print(f"No se encontró la cuenta con número {numero_de_cuenta_a_asociar}")


class Aplicacion:

    def __init__(self):
        self.menu_principal = Menu(['1- Gestionar Cuentas', '2- Gestionar Clientes', '3- Salir'])
        self.gestor_de_cuentas = GestorDeCuentas()
        
    def _submenu_cuentas(self):
        while True:
            menu_cuentas = Menu(
                ['1. Alta de Cuenta', '2. Modificación de Saldo', '3. Consulta de Todas las Cuentas',
                 '4. Consulta por Número de Cuenta', '5. Volver al menú anterior'])
            menu_cuentas.mostrar_menu()
            opcion_menu_cuentas_seleccionada = menu_cuentas.pedir_opcion_de_menu_valida()
            if opcion_menu_cuentas_seleccionada == 1:
                self.gestor_de_cuentas.agregar_cuenta()
            elif opcion_menu_cuentas_seleccionada == 2:
                self.gestor_de_cuentas.modificar_saldo_cuenta()
            elif opcion_menu_cuentas_seleccionada == 3:
                self.gestor_de_cuentas.ver_cuentas()
            elif opcion_menu_cuentas_seleccionada == 4:
                self.gestor_de_cuentas.buscar_y_mostrar_cuenta()
            elif opcion_menu_cuentas_seleccionada == 5:
                break


    def _submenu_clientes(self):
        while True:
            menu_clientes = Menu(
                ['1. Alta de Cliente', '2. Modificación de Cliente', '3. Consulta de Todos los Clientes',
                 '4. Consulta por Número de CUIL', '5. Asociar Cuenta a Cliente', '6. Desasociar Cuenta de Cliente',
                 '7. Volver al menú anterior'])
            menu_clientes.mostrar_menu()
            opcion_menu_clientes_seleccionada = menu_clientes.pedir_opcion_de_menu_valida()
            if opcion_menu_clientes_seleccionada == 1:
                self.gestor_de_clientes.agregar_cliente()
            elif opcion_menu_clientes_seleccionada == 2:
                self.gestor_de_clientes.modificar_cliente()
            elif opcion_menu_clientes_seleccionada == 3:
                self.gestor_de_clientes.ver_clientes()
            elif opcion_menu_clientes_seleccionada == 4:
                self.gestor_de_clientes.buscar_y_mostrar_cliente()
            elif opcion_menu_clientes_seleccionada == 5:
                self.gestor_de_clientes.asociar_cuenta_a_cliente()
            elif opcion_menu_clientes_seleccionada == 6:
                self.gestor_de_clientes.desasociar_cuenta_a_cliente()
            elif opcion_menu_clientes_seleccionada == 7:
                break

    def ejecutar(self):
        while True:
            self.menu_principal.mostrar_menu()
            opcion_seleccionada = self.menu_principal.pedir_opcion_de_menu_valida()

            if opcion_seleccionada == 1:
                self._submenu_cuentas()
            if opcion_seleccionada == 2:
                self._submenu_clientes()
            elif opcion_seleccionada == 3:
                print('\nSaliendo del programa... ¡Gracias por usar nuestros servicios!')
                break

            # Pausa para que el usuario vea el resultado antes de volver al menú
            input("\nPresione Enter para continuar...")


app = Aplicacion()
app.ejecutar()