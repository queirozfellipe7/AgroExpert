# tkinter_app.py

import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
from src.inferencia import process_inputs  # Importa a função de inferência do arquivo inferencia.py
import sqlite3

def handle_process_inputs():
    # Pega os valores selecionados na interface
    soil = soil_var.get().split(" - ")[0]  # Extrai o número do tipo de solo
    season = season_var.get().split(" - ")[0]  # Extrai o número da estação

    # Processa as entradas
    resultados, error = process_inputs(soil, season)

    if error:
        messagebox.showwarning("Entrada inválida", error)
        return

    # Exibe os resultados na área de texto
    output_text.delete(1.0, tk.END)
    if resultados:
        output_text.insert(tk.END, "\n\n".join(resultados))

# Função para abrir a janela de gerenciamento de culturas
def abrir_gerenciamento_culturas():
    # Criar uma nova janela
    gerenciamento_window = Toplevel(root)
    gerenciamento_window.title("Gerenciamento de Culturas")
    gerenciamento_window.iconbitmap ("src\img\logo.ico")  
    

    # Função para adicionar uma nova cultura no banco de dados
    def adicionar_cultura():
        cultura = cultura_entry.get()
        solo = soil_var.get().split(" - ")[0]  # Pega apenas o número do solo
        estacao = season_var.get().split(" - ")[0]  # Pega apenas o número da estação
        tempo = tempo_entry.get()
        adubacao = adubacao_entry.get()

        if not cultura or not solo or not estacao or not tempo or not adubacao:
            messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
            return
        
        # Conectar ao banco de dados
        conexao = sqlite3.connect('src\sistema_recomendacao.db')
        cursor = conexao.cursor()

        # Inserir nova cultura no banco
        cursor.execute(''' 
            INSERT INTO culturas (cultura, solo_indicado, estacao_ideal, tempo_plantio_colheita, adubacao_indicada) 
            VALUES (?, ?, ?, ?, ?)
        ''', (cultura, solo, estacao, tempo, adubacao))

        # Commit das mudanças e fechar a conexão
        conexao.commit()
        conexao.close()

        # Limpar campos após inserção
        cultura_entry.delete(0, tk.END)
        tempo_entry.delete(0, tk.END)
        adubacao_entry.delete(0, tk.END)

        # Mensagem de sucesso
        messagebox.showinfo("Sucesso", "Cultura adicionada com sucesso!")

    # Função para remover uma cultura do banco de dados
    def remover_cultura():
        cultura = cultura_entry.get()

        if not cultura:
            messagebox.showwarning("Campo vazio", "Por favor, informe o nome da cultura para remover.")
            return

        # Conectar ao banco de dados
        conexao = sqlite3.connect('src\sistema_recomendacao.db')
        cursor = conexao.cursor()

        # Remover cultura do banco
        cursor.execute(''' 
            DELETE FROM culturas WHERE cultura = ?
        ''', (cultura,))

        # Commit das mudanças e fechar a conexão
        conexao.commit()
        conexao.close()

        # Limpar campo após remoção
        cultura_entry.delete(0, tk.END)

        # Mensagem de sucesso
        messagebox.showinfo("Sucesso", "Cultura removida com sucesso!")

    # Widgets de entrada para a nova janela
    cultura_label = tk.Label(gerenciamento_window, text="Nome da Cultura:")
    cultura_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    cultura_entry = tk.Entry(gerenciamento_window, width=40)
    cultura_entry.grid(row=0, column=1, padx=10, pady=5)

    solo_label = tk.Label(gerenciamento_window, text="Tipo de Solo:")
    solo_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    soil_var = tk.StringVar(value="1 - Humífero")  # Valor padrão
    solo_menu = tk.OptionMenu(gerenciamento_window, soil_var, *soil_options)
    solo_menu.grid(row=1, column=1, padx=10, pady=5)

    estacao_label = tk.Label(gerenciamento_window, text="Estação Ideal:")
    estacao_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    season_var = tk.StringVar(value="1 - Primavera")  # Valor padrão
    season_menu = tk.OptionMenu(gerenciamento_window, season_var, *season_options)
    season_menu.grid(row=2, column=1, padx=10, pady=5)

    tempo_label = tk.Label(gerenciamento_window, text="Tempo de Plantio à Colheita:")
    tempo_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tempo_entry = tk.Entry(gerenciamento_window, width=40)
    tempo_entry.grid(row=3, column=1, padx=10, pady=5)

    adubacao_label = tk.Label(gerenciamento_window, text="Adubação Indicada:")
    adubacao_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    adubacao_entry = tk.Entry(gerenciamento_window, width=40)
    adubacao_entry.grid(row=4, column=1, padx=10, pady=5)

    # Botões de adicionar e remover
    adicionar_button = tk.Button(gerenciamento_window, text="Adicionar Cultura", command=adicionar_cultura)
    adicionar_button.grid(row=5, column=0, padx=10, pady=10)

    remover_button = tk.Button(gerenciamento_window, text="Remover Cultura", command=remover_cultura)
    remover_button.grid(row=5, column=1, padx=10, pady=10)

# Configuração da interface principal
root = tk.Tk()
root.title("AgroExpert: Sistema Especialista para Agricultura")

# Adicionando um ícone
root.iconbitmap ("src\img\logo.ico")  

# Opções
soil_options = ["1 - Humífero", "2 - Silte", "3 - Arenoso"]
season_options = ["1 - Primavera", "2 - Verão", "3 - Outono", "4 - Inverno"]

# Widgets para entrada de solo
soil_label = tk.Label(root, text="Tipo de Solo:")
soil_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
soil_var = tk.StringVar(value=soil_options[0])
soil_menu = tk.OptionMenu(root, soil_var, *soil_options)
soil_menu.grid(row=0, column=1, padx=10, pady=5)

# Widgets para entrada de estação
season_label = tk.Label(root, text="Estação Atual:")
season_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
season_var = tk.StringVar(value=season_options[0])
season_menu = tk.OptionMenu(root, season_var, *season_options)
season_menu.grid(row=1, column=1, padx=10, pady=5)

# Botão para processar entradas
process_button = tk.Button(root, text="Processar", command=handle_process_inputs)
process_button.grid(row=2, column=0, columnspan=2, pady=10)

# Área de saída
output_label = tk.Label(root, text="Resultados:")
output_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
output_text = tk.Text(root, width=50, height=15, wrap="word")
output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Botão para abrir o gerenciamento de culturas
gerenciar_culturas_button = tk.Button(root, text="Gerenciar Culturas", command=abrir_gerenciamento_culturas)
gerenciar_culturas_button.grid(row=5, column=0, columnspan=2, pady=10)

# Inicializa a interface
root.mainloop()
