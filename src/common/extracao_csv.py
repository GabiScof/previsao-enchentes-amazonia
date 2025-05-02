from src.helpers.extrai_arquivos import extracaoCSV

if __name__ == "__main__":
    print('Iniciando extração dos dados de clima.')
    classe = extracaoCSV()
    classe.extracao_csv()
    classe.extracao_final()
    print('Extração dos dados finalizada!')