from data_reader import ler_dados
from data_cleaner import limpar_dados
from sheet_generator import gerar_relatorio
 
 
CAMINHO_ENTRADA = "vendas_bagunçado.xlsx"
CAMINHO_SAIDA = "relatorio_final.xlsx"
 
 
def main() -> None:
    print(f"Lendo dados de: {CAMINHO_ENTRADA}")
    df_bruto = ler_dados(CAMINHO_ENTRADA)
    print(f"{len(df_bruto)} linhas lidas.")
 
    print("Limpando e tratando os dados...")
    df_limpo = limpar_dados(df_bruto)
    print(f"{len(df_limpo)} linhas válidas após a limpeza "
          f"({len(df_bruto) - len(df_limpo)} linhas descartadas).")
 
    print("Gerando relatório...")
    gerar_relatorio(df_limpo, CAMINHO_SAIDA)
 
 
if __name__ == "__main__":
    main()