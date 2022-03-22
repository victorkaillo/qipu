# qipu
WebSCRAPPING de aisweb

## Desenvolvedor:
### Victor Kaillo
- Entre no diretorio do projeto scrapping_aisweb:
    - ```cd scrapping_aisweb```
- Crie o ambiente usando virtualenv:
    - ```virtualenv venv```
        - Ou crie o ambiente usando venv:
            - ```python3 -m venv ./venv```
- Ative o ambiente:
    - ```source /path/to/venv/bin/activate```
- Intale os pacotes recomendados:
    - ```pip install -r requirements.txt```
- Execute a classe com o comando:
    - ```python3 info_from_aisweb.py -icao_list SBJD```

Sendo SBJD exemplo de Código ICAO que pode ser utilizado na solicitação

- Em caso de desejar informações de mais um Código ICAO:
    - ```python3 info_from_aisweb.py -icao_list SBJD SBMT```

Sendo SBJD e SBMT exemplos de Código ICAO que podem ser utilizados
