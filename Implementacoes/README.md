# Implementações e relatório executivo

O arquivo [relatorio_pesquisa_trilha_c.pdf](relatorio_pesquisa_trilha_c.pdf) resume a revisão de literatura da Trilha C, as diferenças entre nove modelos e os caminhos para animação por fala. O PDF é gerado por [gerar_relatorio.py](gerar_relatorio.py) com Python e ReportLab.

**Estado:** ainda não há treinamento, inferência, comparação quantitativa ou vídeo experimental produzido neste repositório. Os números do PDF são resultados publicados pelos autores, com as condições indicadas. O protocolo para produzir resultados próprios está em [relatorio_trilha_c.md](../relatorio_trilha_c.md).

Para regenerar o PDF:

```bash
python -m pip install reportlab
python Implementacoes/gerar_relatorio.py
```

O gerador requer Arial nos caminhos `C:\Windows\Fonts\arial.ttf` e `C:\Windows\Fonts\arialbd.ttf`.
