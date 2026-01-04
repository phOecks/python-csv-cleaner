Python CSV Aligner & Cleaner
Este projeto foi desenvolvido para resolver um problema crítico de integridade de dados em arquivos CSV. Ele automatiza o realinhamento de registros que foram "quebrados" em múltiplas linhas, identificando o tipo de conteúdo de cada célula e consolidando as informações na linha correta.
O Problema
Muitas vezes, sistemas legados exportam dados onde um único registro (ex: um Titular e seus dependentes) acaba se espalhando por várias linhas de forma desalinhada. Corrigir isso manualmente no Excel é:
Lento: Pode levar horas em bases grandes.
Arriscado: O erro humano ao "subir células" (Delete Shift Up) é altíssimo.

A Solução
O script tratamentoBase_v1.py utiliza lógica de detecção de tipo de dado para:
Identificar Padrões: Diferencia automaticamente valores numéricos de categorias (Titular/Dependente) e descrições.
Realinhamento Dinâmico: Move informações de linhas "órfãs" para as colunas de destino na linha mestre.
Limpeza Automática: Remove as linhas residuais após a consolidação, entregando uma base limpa e pronta para análise.

Como Usar
Pré-requisitos
Python 3.x instalado.
Passo a Passo
Coloque o arquivo CSV que deseja tratar na mesma pasta do script.
Execute o arquivo inicializador.bat.
Digite o nome do arquivo (ex: base_vendas.csv) quando solicitado.
O arquivo processado será gerado instantaneamente com o sufixo _LIMPA.csv.

Estrutura do Projeto
tratamentoBase_v1.py: O "motor" da automação contendo a lógica de tratamento.
inicializador.bat: Script de lote para facilitar a execução por usuários não técnicos (CLI amigável).

Destaques Técnicos
Resiliência de Encoding: O script testa automaticamente múltiplos encodings (UTF-8, Latin-1, CP1252) para evitar erros de leitura.
Escalabilidade: Processa milhares de linhas em milissegundos.
Baixa Dependência: Desenvolvido utilizando apenas bibliotecas nativas do Python (csv, os, argparse), facilitando a portabilidade.

Desenvolvido por Airton Tadeu Credito Junior conecte-se comigo no LinkedIn: https://www.linkedin.com/in/airton-crédito/
