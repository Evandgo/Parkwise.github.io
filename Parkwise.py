import flet as ft

# Dados dos aeroportos
aeroportos = {
    "BSB": (44.74, 9.42, 0),
    "CNF": (61.24, 12.98, 106.39),
    "GIG": (37.28, 7.85, 320.75),
    "IGU": (65.04, 13.66, 189.38),
}

def calcular_custos(aeroporto, horas):
    custo_manobra, custo_estacionamento, custo_reboque = aeroportos[aeroporto]
    
    # Custo de manobra
    if horas <= 3:
        custo_manobra_total = 0
    else:
        custo_manobra_total = custo_manobra * horas

    # Custo de estacionamento
    custo_estacionamento_total = (custo_estacionamento * horas) + (custo_reboque * 2)

    # Cálculo da economia
    saving = custo_manobra_total - custo_estacionamento_total

    # Decisão
    resposta = "PERMANECER EM POSIÇÃO DE MANOBRAS" if saving <= 0 else "MOVIMENTAR PARA POSIÇÃO DE ESTACIONAMENTO"

    return custo_manobra_total, custo_estacionamento_total, saving, resposta

def main(page: ft.Page):
    page.bgcolor = ft.colors.BLACK

    # Imagem do produto
    product_images = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(
                    src='https://drive.google.com/uc?export=view&id=1Q8U7ac6WbhI_bNGmdK0D6DL12tzoTimz',
                )
            ]
        )
    )

    # Criação do dropdown e entrada de horas
    aeroporto_dropdown = ft.Dropdown(
        label="Selecione o Aeroporto",
        options=[ft.dropdown.Option(aeroporto) for aeroporto in aeroportos.keys()],
        width=300,
        bgcolor=ft.colors.WHITE,  # Cor de fundo do dropdown
        color=ft.colors.BLACK,    # Cor da fonte do dropdown
    )
    
    horas_input = ft.TextField(
        label="Horas em Solo (INT)",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        bgcolor=ft.colors.WHITE,  # Cor de fundo do input
        color=ft.colors.BLACK,    # Cor da fonte do input
    )
    
    resultado = ft.Column()  # Para exibir os resultados
    

    def calcular(aeroporto, horas):
        try:
            horas = int(horas)  # Converte para inteiro
            if horas < 0:
                raise ValueError("As horas não podem ser negativas.")
            
            # Limpa resultados anteriores
            resultado.controls.clear() 

            custo_manobra_total, custo_estacionamento_total, saving, resposta = calcular_custos(aeroporto, horas)

            resultado.controls.append(
                ft.Text(f"Custo de Manobra: R${custo_manobra_total:.2f}", color=ft.colors.WHITE),
            )
            resultado.controls.append(
                ft.Text(f"Custo de Estacionamento: R${custo_estacionamento_total:.2f}", color=ft.colors.WHITE),
            )
            resultado.controls.append(
                ft.Text(f"Economia: R${saving:.2f}", color=ft.colors.WHITE),
            )

            # Mensagem de decisão com formatação
            if resposta == "PERMANECER EM POSIÇÃO DE MANOBRAS":
                resultado.controls.append(
                    ft.Text(resposta, color=ft.colors.RED, weight=ft.FontWeight.BOLD)
                )
            else:
                resultado.controls.append(
                    ft.Text(resposta, color=ft.colors.GREEN, weight=ft.FontWeight.BOLD)
                )
                
            page.update()  # Atualiza a página para mostrar os resultados
        except ValueError as ve:
            resultado.controls.clear()  # Limpa resultados anteriores antes de mostrar erro
            resultado.controls.append(
                ft.Text(f"Erro: {str(ve)}", color=ft.colors.RED),
            )
            page.update()  # Atualiza a página para mostrar o erro

    # Botão de calcular
    calcular_button = ft.ElevatedButton(
        text="Calcular", 
        on_click=lambda e: calcular(aeroporto_dropdown.value, horas_input.value)
    )

    # Layout principal
    layout = ft.Container(
        width=900,
        height=400,
        margin=ft.margin.all(30),
        shadow=ft.BoxShadow(blur_radius=30, color='#00058c'),
        content=ft.Column(  # Mudei para Column para melhor organização
            controls=[
                product_images,
                aeroporto_dropdown,
                horas_input,
                calcular_button,
                ft.Divider(color=ft.colors.WHITE),
                resultado
            ]
        )
    )

    page.add(layout)

if __name__ == '__main__':
    ft.app(target=main)