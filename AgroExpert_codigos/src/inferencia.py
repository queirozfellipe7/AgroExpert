
import sqlite3

def process_inputs(soil, season):
    # Conectar ao banco de dados
    conexao = sqlite3.connect('src\sistema_recomendacao.db')
    cursor = conexao.cursor()

    # Consultar a tabela de culturas com base no tipo de solo e estação
    cursor.execute("""
        SELECT cultura, tempo_plantio_colheita, adubacao_indicada
        FROM culturas
        WHERE solo_indicado = ? AND estacao_ideal LIKE ?
    """, (soil, f"%{season}%"))
    
    # Obter todos os resultados
    resultados = cursor.fetchall()

    # Fechar conexão
    conexao.close()

    if resultados:
        recomendacoes = []
        for resultado in resultados:
            recomendacao = (f"Cultura: {resultado[0]}\n"
                            f"Tempo de plantio à colheita: {resultado[1]} dias\n"
                            f"Adubação indicada: {resultado[2]}")
            recomendacoes.append(recomendacao)
        
        return recomendacoes, None
    
    return None, "Nenhuma cultura recomendada para as condições informadas."
