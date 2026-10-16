# Experimentos Avatar — Trilha C

Pesquisa de Fernando sobre **cabeças 3D Gaussian Splatting (3DGS) animáveis**. Investigamos como associar gaussianas a um modelo facial controlável e se a fala pode mover boca e mandíbula com sincronia verossímil.

## Relatório

Leia o [relatório da Trilha C](relatorio_trilha_c.md). Ele apresenta os nove trabalhos de referência, os gargalos técnicos, um protocolo de comparação e uma seção sobre integração com áudio. Compara um caminho modular (áudio → expressão facial → malha → gaussianas) com modelos 3DGS já dirigidos por fala.

**Estado atual:** revisão bibliográfica e plano experimental. Ainda não há resultados de implementação medidos neste repositório.

## Próximos passos

1. Verificar código, pesos, dados, licenças e requisitos de hardware do baseline GaussianAvatars.
2. Preparar captura autorizada ou conjunto de dados com licença compatível e separar treino/teste.
3. Reproduzir o baseline e comparar gaussianas fixas, gaussianas ancoradas à malha e deslocamentos locais.
4. Publicar vídeos, métricas, configurações e limitações de cada experimento.
5. Testar o mesmo áudio em português brasileiro com um avatar controlável e um baseline de cabeça falante, registrando sincronia, naturalidade e latência total.

Relatório inspirado na estrutura de [Experimentos Avatar 01 — Humans](https://github.com/CleiverJr/Experimentos-Avatar-01-Humans), de Cleiver Junior.

