import reflex as rx
import ipaddress
from dataclasses import field
from Subnettingpy.Conversor_binario import ConversorBinario as CB
from typing import List, Dict


cbin = CB()

class State(rx.State):
    """The app state."""
    # ENTENDER COMO HACER QUE EL TAB SEA DINAMICO
    selected_tab: str = "tab1"  # Estado para el tab seleccionado



class Sunetting(rx.State):
    """Recibe una red con con su CIDR por defecto identificador de la red y recibe el nuevo CIDR con el que se va a recibir la red."""
    ip: str = ""
    cidr: str = ""
    subredes_data: List[Dict[str, str]] = []
    page: int = 1         # Página actual
    page_size: int = 10   # Registros por página

    @rx.var
    def get_paginated_data(self) -> List[Dict[str, str]]:
        """Devuelve los datos de la página actual."""
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        return self.subredes_data[start:end]

    def calcular_subredes(self):
        """Calcula las subredes y actualiza la lista de datos."""
        try:
            # Crear la red base
            red_base = ipaddress.IPv4Network(self.ip, strict=True)
        except ValueError:
            # Encaso de error devuelve un diccionario vacio con el error de Formato invalido
            self.subredes_data = [{
                "subred": "Error",
                "direccion_red": "Formato inválido",
                "broadcast": "",
                "rango_hosts": "",
                "direcciones": ""
            }]
            return

        try:
            nueva_mascara = int(self.cidr)
        except ValueError:
            #En caso de error devuelve un diccionario vacio con el error de cidr invalido
            self.subredes_data = [{
                "subred": "Error",
                "direccion_red": "CIDR inválido",
                "broadcast": "",
                "rango_hosts": "",
                "direcciones": ""
            }]
            return

        # Obtengo las subredes con el nuevo CIDR
        subredes = list(red_base.subnets(new_prefix=nueva_mascara))
        
        data = [] # Inicializo lista que va a almacenar la información de las subredes en un diccionario
        

        #Para cada indice y subred en la lista de subredes
        for idx, subred in enumerate(subredes):
            direccion_red = subred.network_address #Obtenemos la dirección de la red
            direccion_broadcast = subred.broadcast_address #Obtenemos la direccion de broadcast
            hosts = list(subred.hosts()) #Obtenemos la lista de direcciones ip de los hosts en la subred
            if hosts:
                # Obtenemos el primer y ultimo host
                primer_host = hosts[0]
                ultimo_host = hosts[-1]
            else:
                primer_host = ultimo_host = "N/A"

            # Agregamos la informacion de la subred al diccionario
            data.append({
                "subred": f"Subred {idx}", #Identificador de la subred
                "direccion_red": str(direccion_red), # la dirección de la red
                "broadcast": str(direccion_broadcast), # La de broadcast
                "rango_hosts": f"Desde: {primer_host} hasta: {ultimo_host}", # Un rango de hosts
                "direcciones": str(subred.num_addresses) # Y el total de direcciones assignables por red
            })
        self.subredes_data = data
        self.page = 1  # Reinicia a la primera página

    def next_page(self):
        """Avanza a la siguiente página si es posible."""
        if self.page * self.page_size < len(self.subredes_data):
            self.page += 1

    def prev_page(self):
        """Retrocede a la página anterior si es posible."""
        if self.page > 1:
            self.page -= 1


#### Operación and bit a bit.
class operacion_and(rx.State):
    """Función que identifica a que red pertenece una ip"""
    netmask: str
    ip: str #estados fijos si o si necesitados
    red: str #Este es el estado que puede cambiar.

    def operacion_and(self):

        try:
            # Dividir la IP y la Netmask
            ip_parts = self.ip.split(".")
            netmask_parts = self.netmask.split(".")

            # Validar que haya 4 octetos
            if len(ip_parts) != 4 or len(netmask_parts) != 4:
                self.red = "Error: IP o Netmask incorrecta"
                return

            # Convertir a binario usando la librería externa
            ipBin = cbin.binario(ip_parts)
            ncBin = cbin.binario(netmask_parts)

            # Realizar la operación AND bit a bit
            lred = []
            for byte1, byte2 in zip(ncBin, ipBin):
                octeto = "".join("1" if b1 == "1" and b2 == "1" else "0" for b1, b2 in zip(byte1, byte2))
                lred.append(str(int(octeto, 2)))  # Convertir de binario a decimal

            # Guardar resultado en el estado
            dred = cbin.decimal(lred)
            self.red = f"La IP {self.ip} pertenece a la red {'.'.join(dred)}"

        except Exception as e:
            self.red = f"Error: {str(e)}"




##### Rango de direcciones 
class Rango_direcciones(rx.State):
    """Recibe la red y su notación CIDR y devuelve la cantidad de direcciones que pueden recibir los hosts"""
    red: str # Se debe recibir la red con  /# 0.0.0.0/24
    rango : str


    def rango_direcciones(self):
        
        obj_red = ipaddress.ip_network(self.red) # seria algo como => 0.0.0.0/0

        direccion_red = obj_red.network_address
        direccion_broadcast = obj_red.broadcast_address

        self.rango = f"Rango de direcciones: {direccion_red} - {direccion_broadcast}"












