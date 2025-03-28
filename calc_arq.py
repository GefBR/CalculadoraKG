from colorama import init, Fore, Style
import time
import os
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import keyboard
from datetime import datetime, timedelta


# Inicializa o colorama para cores no terminal
init()

# Função para exibir o título estilizado
def exibir_titulo():
    print(f"{Fore.GREEN}{Style.BRIGHT}╔════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}║     Calculadora de Projetos  KG     ║{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}╚════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}Precificação para projetos arquitetônicos{Style.RESET_ALL}\n")

# Função para entrada de texto (nome do projeto)
def obter_nome_projeto():
    print(f"{Fore.LIGHTCYAN_EX}Digite o nome do projeto{Style.RESET_ALL}", end="")
    nome = input(": ").strip()
    while not nome:
        print(f"{Fore.RED}Erro: O nome do projeto não pode ser vazio!{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}Digite o nome do projeto{Style.RESET_ALL}", end="")
        nome = input(": ").strip()
    return nome

# Função para entrada de valores numéricos com validação
def obter_valor(texto, cor):
    while True:
        try:
            print(f"{cor}{texto}{Style.RESET_ALL}", end="")
            valor = float(input(": "))
            if valor <= 0:
                print(f"{Fore.RED}Erro: O valor deve ser maior que zero!{Style.RESET_ALL}")
                continue
            return valor
        except ValueError:
            print(f"{Fore.RED}Erro: Digite um número válido!{Style.RESET_ALL}")

# Função para capturar opção com suporte a Esc
def obter_opcao(texto):
    print(f"{Fore.LIGHTCYAN_EX}{texto}{Style.RESET_ALL}", end="")
    entrada = ""
    while True:
        if keyboard.is_pressed("esc"):
            print("\nEsc pressionado")
            return "3"
        entrada = input(": ")
        if entrada in ["1", "2", "3"]:
            return entrada
        else:
            print(f"{Fore.RED}Opção inválida! Escolha entre 1, 2 ou 3 .{Style.RESET_ALL}")
            print(f"{Fore.LIGHTCYAN_EX}{texto}{Style.RESET_ALL}", end="")

# Função para salvar o log com diálogo
def salvar_log(dados):
    root = Tk()
    root.withdraw()
    arquivo_padrao = f"{dados['nome_projeto']}.txt"
    caminho = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de texto", "*.txt")],
        initialfile=arquivo_padrao,
        title="Salvar log do projeto"
    )
    if not caminho:
        print(f"{Fore.YELLOW}Salvamento cancelado.{Style.RESET_ALL}")
        return
    with open(caminho, "a", encoding="utf-8") as arquivo:
        timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
        arquivo.write(f"[{timestamp}] Projeto: {dados['nome_projeto']}\n")
        for chave, valor in dados.items():
            if chave != "nome_projeto":
                arquivo.write(f"{chave}: {valor}\n")
        arquivo.write("-" * 40 + "\n")
    print(f"{Fore.GREEN}Log salvo com sucesso em '{caminho}'!{Style.RESET_ALL}")

# Função para calcular dias úteis
def calcular_dias_uteis(data_inicio, dias_corridos):
    dias_uteis = 0
    data_atual = data_inicio
    for _ in range(int(dias_corridos) + 1):  # +1 para incluir o dia final
        if data_atual.weekday() < 5:  # 0-4 são segunda a sexta
            dias_uteis += 1
        data_atual += timedelta(days=1)
    return dias_uteis

# Calculadora por metro quadrado
def calculadora_metro_quadrado():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_titulo()
        print(Fore.GREEN + "Calculando precificação do projeto com base no valor do metro quadrado trabalhado" + Style.RESET_ALL)
        nome_projeto = obter_nome_projeto()
        valor_m2 = obter_valor("Digite o valor do metro quadrado (R$)", Fore.LIGHTCYAN_EX)
        tamanho_m2 = obter_valor("Digite o tamanho do projeto (m²)", Fore.LIGHTCYAN_EX)
        resultado = valor_m2 * tamanho_m2

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            exibir_titulo()
            print(f"{Fore.YELLOW}Calculando...{Style.RESET_ALL}")
            time.sleep(1)
            print(f"{Fore.GREEN}{Style.BRIGHT}═" * 40 + Style.RESET_ALL)
            print(f"{Fore.LIGHTGREEN_EX}Projeto: {nome_projeto}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}R$ {resultado:,.2f}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}═" * 40 + Style.RESET_ALL)

            print(f"\n{Fore.LIGHTBLUE_EX}O que deseja fazer?{Style.RESET_ALL}")
            print(f"{Fore.CYAN}1. Novo cálculo{Style.RESET_ALL}")
            print(f"{Fore.CYAN}2. Salvar em log{Style.RESET_ALL}")
            print(f"{Fore.CYAN}3. Voltar ao menu principal{Style.RESET_ALL}")
            
            opcao = obter_opcao("Escolha uma opção (1-3)")
            if opcao == "1":
                break
            elif opcao == "2":
                dados = {"nome_projeto": nome_projeto, "Valor por m²": f"R$ {valor_m2:,.2f}", 
                         "Tamanho": f"{tamanho_m2} m²", "Total": f"R$ {resultado:,.2f}"}
                salvar_log(dados)
                time.sleep(1)
                continue
            elif opcao == "3":
                return

# Calculadora por hora trabalhada
def calculadora_hora_trabalhada():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_titulo()
        print(Fore.GREEN + "Calculando precificação do projeto com base no valor da hora trabalhada." + Style.RESET_ALL)
        nome_projeto = obter_nome_projeto()
        valor_hora = obter_valor("Digite o valor da hora trabalhada (R$)", Fore.LIGHTCYAN_EX)
        horas_por_dia = obter_valor("Digite as horas trabalhadas por dia", Fore.LIGHTCYAN_EX)
        tamanho_m2 = obter_valor("Digite o tamanho do projeto (m²)", Fore.LIGHTCYAN_EX)

        # Cálculo do preço
        resultado = valor_hora * tamanho_m2

        # Cálculo do tempo
        horas_totais = tamanho_m2  # 1 m² = 1 hora
        dias_corridos = horas_totais / horas_por_dia
        semanas_corridas = dias_corridos / 7

        # Data atual
        data_inicio = datetime.now()
        dias_uteis = calcular_dias_uteis(data_inicio, dias_corridos)
        semanas_uteis = dias_uteis / 5  # 5 dias úteis por semana

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            exibir_titulo()
            print(f"{Fore.YELLOW}Calculando...{Style.RESET_ALL}")
            time.sleep(1)
            print(f"{Fore.GREEN}{Style.BRIGHT}═" * 40 + Style.RESET_ALL)
            print(f"{Fore.LIGHTGREEN_EX}Projeto: {nome_projeto}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}R$ {resultado:,.2f}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTGREEN_EX}Tempo estimado para entrega do projeto é (início: {data_inicio.strftime('%d/%m/%Y')}):{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}Corridos:{Style.RESET_ALL}")
            print(f"    {Fore.CYAN}{semanas_corridas:.1f} semanas{Style.RESET_ALL}")
            print(f"    {Fore.CYAN}{dias_corridos:.1f} dias{Style.RESET_ALL}")
            print(f"    {Fore.CYAN}{horas_totais:.1f} horas{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}Úteis:{Style.RESET_ALL}")
            print(f"    {Fore.CYAN}{semanas_uteis:.1f} semanas{Style.RESET_ALL}")
            print(f"    {Fore.CYAN}{dias_uteis:.1f} dias{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}═" * 40 + Style.RESET_ALL)

            print(f"\n{Fore.LIGHTBLUE_EX}O que deseja fazer?{Style.RESET_ALL}")
            print(f"{Fore.CYAN}1. Novo cálculo{Style.RESET_ALL}")
            print(f"{Fore.CYAN}2. Salvar em log{Style.RESET_ALL}")
            print(f"{Fore.CYAN}3. Voltar ao menu principal{Style.RESET_ALL}")
            
            opcao = obter_opcao("Escolha uma opção (1-3)")
            if opcao == "1":
                break
            elif opcao == "2":
                dados = {"nome_projeto": nome_projeto, "Valor por hora": f"R$ {valor_hora:,.2f}", 
                         "Horas por dia": f"{horas_por_dia}", "Tamanho": f"{tamanho_m2} m²", 
                         "Total": f"R$ {resultado:,.2f}", 
                         "Tempo Corrido": f"{semanas_corridas:.1f} semanas / {dias_corridos:.1f} dias / {horas_totais:.1f} horas",
                         "Tempo Útil": f"{semanas_uteis:.1f} semanas / {dias_uteis:.1f} dias"}
                salvar_log(dados)
                time.sleep(1)
                continue
            elif opcao == "3":
                return

# Menu principal
def menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_titulo()
        print(f"{Fore.LIGHTBLUE_EX}Escolha uma opção:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1. Calcular por hora trabalhada{Style.RESET_ALL}")
        print(f"{Fore.CYAN}2. Calcular por metro quadrado{Style.RESET_ALL}")
        print(f"{Fore.CYAN}3. Sair{Style.RESET_ALL}")
        
        opcao = obter_opcao("Digite sua escolha (1-3)")
        if opcao == "2":
            calculadora_metro_quadrado()
        elif opcao == "1":
            calculadora_hora_trabalhada()
        elif opcao == "3":
            print(f"{Fore.GREEN}Saindo... Até a próxima!{Style.RESET_ALL}")
            time.sleep(1)
            break

# Executa o programa
if __name__ == "__main__":
    menu_principal()