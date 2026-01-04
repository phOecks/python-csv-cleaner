import argparse
import csv
import os
from typing import List

class CSVAligner:
    def __init__(self, delimiter: str = ";"):
        """Inicializa a classe com as configurações básicas e definições de colunas."""
        self.delimiter = delimiter
        self.rows: List[List[str]] = []
        
        # Definição dos índices das colunas de destino (Baseado em 0: F=5, T=19, U=20)
        self.DEST_NUMERIC = 5      # Coluna F: Destino para valores numéricos
        self.DEST_CATEGORIA_A = 19 # Coluna T: Destino para 'TITULAR' ou 'DEPENDENTE'
        self.DEST_TEXT_GERAL = 36  # Coluna AJ: Destino para qualquer outro texto

    def load_file(self, file_path: str):
        """Tenta ler o ficheiro CSV testando diferentes tipos de codificação para evitar erros de acentuação."""
        for enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(file_path, "r", newline="", encoding=enc) as f:
                    # Carrega todo o conteúdo do CSV para uma lista na memória
                    self.rows = list(csv.reader(f, delimiter=self.delimiter))
                return
            except Exception:
                continue
        raise Exception("Erro ao ler o ficheiro CSV. Verifique o formato ou permissões.")

    def _is_numeric(self, value: str) -> bool:
        """Limpa o texto de pontos e vírgulas para verificar se o conteúdo é um número."""
        clean_val = value.replace('.', '').replace(',', '').strip()
        return clean_val.isdigit()

    def get_destination_column(self, value: str) -> int:
        """Determina em qual coluna os dados devem ser colados com base no texto da Coluna B."""
        upper_val = value.upper().strip()
        
        # Regra 1: Se o texto contiver palavras-chave específicas, vai para a coluna 19 (T)
        if "TITULAR" in upper_val or "DEPENDENTE" in upper_val:
            return self.DEST_CATEGORIA_A
        
        # Regra 2: Se for um valor numérico/financeiro, vai para a coluna 5 (F)
        if self._is_numeric(value):
            return self.DEST_NUMERIC
        
        # Regra 3: Se não for nenhuma das anteriores, vai para a coluna 20 (U)
        return self.DEST_TEXT_GERAL

    def process_alignment(self):
        """Lógica principal para identificar linhas fragmentadas, mover dados e excluir a linha órfã."""
        idx = 1 # Começa na segunda linha (índice 1) para preservar o cabeçalho
        
        while idx < len(self.rows):
            row = self.rows[idx]
            
            # GATILHO: Verifica se a Coluna A está vazia e a B tem conteúdo (característica de erro de quebra)
            if len(row) > 1 and not row[0].strip() and row[1].strip():
                conteudo_b = row[1]
                # Decide o destino (5, 19 ou 20) com base no conteúdo de B
                dest_col = self.get_destination_column(conteudo_b)
                
                prev_idx = idx - 1 # Linha de cima (destino da colagem)
                data_block = row[1:44] # Captura o bloco de dados das colunas B até AR
                
                # Verifica se a linha de cima tem colunas suficientes para receber os novos dados
                needed_size = dest_col + len(data_block)
                if len(self.rows[prev_idx]) < (needed_size):
                    # Adiciona colunas vazias se necessário para evitar erro de índice
                    self.rows[prev_idx].extend([""] * (needed_size - len(self.rows[prev_idx])))
                
                # Transfere cada célula do bloco da linha atual para a posição correta na linha superior
                for i, val in enumerate(data_block):
                    self.rows[prev_idx][dest_col + i] = val

                # Remove a linha atual da lista (simula o 'Delete Shift Up' do Excel)
                self.rows.pop(idx)
                
                # Não aumenta o idx aqui, pois a linha de baixo 'subiu' para a posição atual
                continue 
            
            idx += 1

    def save(self, output_path: str):
        """Grava os dados processados num novo ficheiro CSV com codificação UTF-8."""
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerows(self.rows)

def main():
    """Configura os argumentos de linha de comando e inicia a execução do script."""
    parser = argparse.ArgumentParser(description="Alinhador de CSV por lógica de conteúdo.")
    parser.add_argument("input", help="Caminho do ficheiro CSV de entrada")
    args = parser.parse_args()

    aligner = CSVAligner()
    try:
        aligner.load_file(args.input)
        print(f"Lendo e processando: {args.input}")
        
        aligner.process_alignment()
        
        # Define o nome do ficheiro de saída adicionando o sufixo '_LIMPA'
        output = os.path.splitext(args.input)[0] + "_LIMPA.csv"
        aligner.save(output)
        print(f"Sucesso! Ficheiro gerado: {output}")
        
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")

if __name__ == "__main__":
    main()