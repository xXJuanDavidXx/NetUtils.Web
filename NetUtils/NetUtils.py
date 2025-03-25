import reflex as rx
from .state import Sunetting as SubnetState


def index() -> rx.Component:
    return rx.vstack(
        rx.input(
            placeholder="Ingresa la red base (ej. 192.168.0.0/24)",
            value=SubnetState.ip,
            on_change=SubnetState.set_ip,
        ),
        rx.input(
            placeholder="Ingresa el nuevo CIDR (ej. 26)",
            value=SubnetState.cidr,
            on_change=SubnetState.set_cidr,
        ),
        rx.button(
            "Calcular subredes",
            on_click=SubnetState.calcular_subredes,
        ),
        # Tabla de resultados
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Subred"),
                    rx.table.column_header_cell("Dirección de red"),
                    rx.table.column_header_cell("Broadcast"),
                    rx.table.column_header_cell("Rango de hosts"),
                    rx.table.column_header_cell("Direcciones"),
                )
            ),
            rx.table.body(
                rx.foreach(SubnetState.get_paginated_data, lambda item:
                    rx.table.row(
                        rx.table.cell(item["subred"]),
                        rx.table.cell(item["direccion_red"]),
                        rx.table.cell(item["broadcast"]),
                        rx.table.cell(item["rango_hosts"]),
                        rx.table.cell(item["direcciones"]),
                    )
                )
            ),
        ),
        # Controles de paginación
        rx.hstack(
            rx.button("Anterior", on_click=SubnetState.prev_page),
            rx.text(lambda: f"Página {SubnetState.page} de {((len(SubnetState.subredes_data)-1)//SubnetState.page_size)+1}"),
            rx.button("Siguiente", on_click=SubnetState.next_page),
            spacing="10",
        ),
        align="center",
        justify="center",
        width="100%",
    )











app = rx.App()
app.add_page(index)








######REVISAR EL CODIGO Y CORREGIR
    #return rx.container(

        #rx.vstack(
        ## Tabs para seleccionar la funcionalidad

            #rx.tabs.root(
                #rx.tabs.list(
                    #rx.tabs.trigger("Subneteo", value="tab1", on_click=lambda: State.set_selected_tab("tab1")),
                    #rx.tabs.trigger("Conversor", value="tab2", on_click=lambda: State.set_selected_tab("tab2")),
                #),
            #),

            ## Contenido dinámico según el tab seleccionado
            #rx.cond(
                #State.selected_tab == "tab1",
                #rx.vstack(
                    #rx.text("Calculadora de Subnetting", font_size="xl"),
                    #rx.input(placeholder="Ingresa una IP"),
                    #rx.button("Calcular", on_click=lambda: print("Función de subneteo aqui")),
                #),
                #rx.vstack(
                    #rx.text("Conversor de Binario a Decimal", font_size="xl"),
                    #rx.input(placeholder="Ingresa un número binario"),
                    #rx.button("Convertir", on_click=lambda: print("Función de conversión aquí")),
                #)
            #)
        #),
        #size="1",
    #)







#        rx.color_mode.button(position="top-right"),
#        rx.vstack(
           # rx.heading("Welcome to Reflex!", size="9"),
            #rx.text(
              #  "Get started by editing ",
             #   rx.code(f"{config.app_name}/{config.app_name}.py"),
            #    size="5",
           # ),
          #  rx.link(
         #       rx.button("Check out our docs!"),
        #        href="https://reflex.dev/docs/getting-started/introduction/",
       #         is_external=True,
      #      ),
     #       spacing="5",
    #        justify="center",
   #         min_height="85vh",
  #      ),
 #       rx.logo(),
#    )


