# Pesquisa Trilha C — Cabeças 3DGS animáveis

**Responsável:** Fernando  
**Questão central:** como vincular gaussianas 3D a um modelo de cabeça controlável, preservando identidade e detalhes visuais durante mudanças de pose e expressão?  
**Estado:** revisão inicial e protocolo experimental; resultados de implementação ainda não medidos.

## 1. Resumo executivo

Uma cabeça reconstruída com 3D Gaussian Splatting (3DGS) pode parecer convincente em uma pose e falhar ao sorrir, falar ou virar para o perfil. A dificuldade principal é definir **a correspondência entre cada gaussiana e a geometria deformável**. Uma solução prática é usar uma malha paramétrica, como FLAME, como estrutura de controle. Cada gaussiana recebe uma posição canônica ligada a um triângulo, ponto UV ou região da malha. Quando os parâmetros de pose e expressão mudam, a malha se deforma e as gaussianas acompanham a transformação. Região da boca, cabelo e áreas não observadas exigem tratamento adicional.

**Hipótese de trabalho:** começar com gaussianas presas a triângulos de FLAME, reproduzir animações controladas e adicionar liberdade residual apenas onde o vínculo rígido produz artefatos. Essa escolha é uma proposta experimental inspirada principalmente em [GaussianAvatars](https://arxiv.org/abs/2312.02069), [SplattingAvatar](https://arxiv.org/abs/2403.05087) e [GeoAvatar](https://arxiv.org/abs/2507.18155); não é uma conclusão já demonstrada neste repositório.

## 2. O que significa “prender” uma gaussiana

Uma gaussiana 3D possui, entre outros parâmetros, centro, orientação, escala, opacidade e cor. Para torná-la animável, é preciso guardar sua posição em uma **cabeça canônica** e uma regra que a transporte para a cabeça deformada.

1. Ajustar uma malha de cabeça aos quadros de entrada e estimar parâmetros de identidade, expressão, mandíbula e pose.
2. Associar cada gaussiana a uma face da malha, coordenadas baricêntricas ou coordenadas UV, incluindo deslocamento local quando necessário.
3. Em cada quadro, atualizar o centro e a orientação da gaussiana a partir da deformação da malha. Escala, opacidade e aparência podem receber correções condicionadas à expressão.
4. Renderizar a nova vista e comparar com imagem real, máscaras e marcos faciais, regularizando a distância entre gaussiana e superfície.

O vínculo puramente rígido tende a ser insuficiente para lábios, bochechas e cabelo. O experimento deve distinguir **erro de rastreamento da malha**, **erro de associação gaussiana–malha** e **erro de aparência/renderização** antes de adicionar complexidade.

## 3. Mapa dos trabalhos

| Trabalho | Entrada e ideia relevante | Papel nesta pesquisa |
| --- | --- | --- |
| [GaussianAvatars](https://arxiv.org/abs/2312.02069) | Gaussianas em referenciais locais de triângulos de um modelo facial deformável, com deslocamentos otimizáveis. | Base principal para rigging explícito e transferência de expressão. |
| [SplattingAvatar](https://arxiv.org/abs/2403.05087) | Associação treinável de gaussianas a uma malha; abrange avatares de corpo e cabeça. | Comparar vínculo aprendido com ancoragem simples. |
| [FlashAvatar](https://arxiv.org/abs/2312.02214) | Incorporação eficiente de gaussianas em um modelo paramétrico facial. | Referência para custo de treino e renderização. |
| [Avat3r](https://arxiv.org/abs/2502.20220) | Reconstrução animável a partir de poucas imagens, com modelo treinado para inferência direta. | Examinar cenário de poucas vistas e generalização; requer pesos e dados adequados para reprodução. |
| [GeoAvatar](https://arxiv.org/abs/2507.18155) | Regularização geométrica adaptativa, atenção à anatomia da boca e ao rigging com 3DMM. | Testar onde ancoragem rígida degrada a animação. |
| [SpiD](https://arxiv.org/abs/2607.28032) | Uma imagem; separa regiões gaussianas e inclui o custo do controle por quadro na inferência. | Referência para decomposição regional e medição honesta de latência. |
| [OMEGA-Avatar](https://arxiv.org/abs/2602.11693) | Uma imagem; cabeça completa 360° com malha deformada e representação UV. | Avaliar completude do cabelo e da parte posterior da cabeça. |
| [FiCA](https://arxiv.org/abs/2606.24232) | Uma imagem; malha gerada/refinada e gaussianas decodificadas para expressões novas. | Analisar o caminho de captura rápida sem otimização por pessoa. |
| [HeadsUp](https://arxiv.org/abs/2605.04035) | Captura multivista; gaussianas parametrizadas em UV e ancoradas a uma cabeça neutra; animação por blendshapes. | Referência para qualidade com múltiplas câmeras e controle por blendshapes. |

**Comparabilidade:** esses trabalhos usam entradas, dados de treino e, por vezes, objetivos distintos. Uma métrica publicada em um artigo não deve ser copiada como se fosse resultado de um teste local. Avat3r, FiCA, OMEGA-Avatar, SpiD e HeadsUp dependem de modelos previamente treinados; só entram em comparação quantitativa direta se houver acesso legítimo aos pesos, dados e pipeline completo.

## 4. Quatro gargalos a investigar

1. **Deslizamento e “flutuação” das gaussianas:** detalhes da pele se afastam da superfície em expressões extremas. Verificar distância à malha e consistência de pontos faciais entre quadros.
2. **Boca e mandíbula:** lábios, dentes e interior da boca têm movimento e oclusão próprios. Separar essas regiões e testar expressão e abertura de mandíbula independentemente.
3. **Cabelo, orelhas e nuca:** a malha facial pode não cobrir toda a cabeça; uma captura frontal tampouco observa a parte posterior. Registrar cobertura por ângulo e tratar regiões sem observação como limitação, não como reconstrução comprovada.
4. **Troca entre fidelidade e custo:** mais gaussianas e correções residuais podem melhorar um quadro, mas aumentar memória, tempo de treino e latência. Medir todo o pipeline, inclusive rastreamento facial quando utilizado.

## 5. Experimento mestre proposto

**Objetivo:** demonstrar quais decisões de ancoragem melhoram a mesma cabeça sob a mesma sequência de controle. O primeiro comparativo deve usar implementações executáveis sob condições equivalentes; os demais artigos permanecem na revisão conceitual até que seus códigos e pesos sejam validados.

### Dados e controles

- Captura de uma pessoa com consentimento e autorização de uso, ou conjunto de dados cuja licença permita o experimento.
- Separação fixa entre quadros de treino e teste, incluindo expressões e ângulos de câmera não vistos no ajuste.
- Mesma resolução, câmeras, parâmetros de pose/expressão e hardware em todas as variantes locais.
- Sequência mínima: neutro → sorriso → abertura/fechamento de boca → sobrancelhas → rotação frontal/perfil → retorno ao neutro.

### Variantes locais

| Variante | O que muda | Pergunta |
| --- | --- | --- |
| A — malha apenas | Renderização do modelo paramétrico ajustado. | Qual é o limite visual da geometria de controle? |
| B — gaussianas fixas no espaço | 3DGS sem deformação vinculada. | Quanto a animação exige rigging explícito? |
| C — gaussianas ancoradas à malha | Transporte pelo triângulo/UV correspondente. | O vínculo básico mantém a identidade e acompanha a expressão? |
| D — C com deslocamentos locais | Ajuste residual regularizado, sobretudo na boca. | O detalhe melhora sem criar flutuação temporal? |

### Métricas e evidências

- **Imagem:** PSNR, SSIM e LPIPS somente em pares com câmera e quadro de referência alinhados; incluir recortes de olhos, boca e perfil.
- **Controle:** erro dos marcos faciais e amplitude da expressão solicitada; registrar falhas de oclusão e distorções em sorriso/abertura de boca.
- **Tempo:** oscilação dos marcos, da posição das gaussianas e do vídeo renderizado; inspecionar lado a lado uma sequência, não só quadros escolhidos.
- **Custo:** tempo de preparação, treino, inferência completa por quadro, FPS, pico de VRAM e número de gaussianas, com GPU e resolução declaradas.
- **Reprodutibilidade:** versão de código, pesos, licenças, comando executado e parâmetros registrados por variante.

Tabela de resultados a preencher **após executar** o protocolo:

| Variante | PSNR ↑ | SSIM ↑ | LPIPS ↓ | Erro de marcos ↓ | FPS total ↑ | VRAM | Observação visual |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| A | — | — | — | — | — | — | Não medido |
| B | — | — | — | — | — | — | Não medido |
| C | — | — | — | — | — | — | Não medido |
| D | — | — | — | — | — | — | Não medido |

## 6. Plano de execução no GitHub

1. **Revisão e viabilidade:** registrar paper, código oficial, pesos, dados, licença, hardware e dependências de cada método. Selecionar um baseline reproduzível, preferencialmente GaussianAvatars, após verificar requisitos de FLAME e do conjunto de dados.
2. **Captura e pré-processamento:** preparar vídeo/imagens, calibração e ajuste facial; salvar divisão treino/teste e parâmetros de câmera. Não versionar mídia pessoal sem permissão.
3. **Baseline:** treinar ou executar uma implementação oficial sem alterações e documentar comando, commit, configuração e resultado.
4. **Ablações de ancoragem:** comparar as variantes A–D. Manter o mesmo sujeito e a mesma sequência de controle.
5. **Relato:** publicar vídeo lado a lado, quadros de erro, tabela preenchida e limitações. Separar explicitamente resultados próprios de afirmações dos artigos.

Estrutura sugerida:

```text
README.md                         visão geral e instruções rápidas
relatorio_trilha_c.md             síntese para reunião e protocolo
artigos/                         fichas e links; PDFs só se a licença permitir
implementacoes/                   código próprio e configurações
resultados/                       tabelas, figuras e vídeos autorizados
``` 

## 7. Critério para recomendação final

Recomendar uma abordagem somente depois de medir, no mesmo cenário, fidelidade da expressão, estabilidade temporal e custo. Se a captura for monocular, a prioridade é robustez em vistas não observadas; se houver múltiplas câmeras, a prioridade pode passar a ser fidelidade e latência. Qualquer número de FPS precisa dizer se inclui rastreamento, deformação e renderização.

## Fontes primárias

- [GaussianAvatars — artigo e código oficial](https://arxiv.org/abs/2312.02069) · [GitHub](https://github.com/ShenhanQian/GaussianAvatars)
- [SplattingAvatar — artigo](https://arxiv.org/abs/2403.05087)
- [FlashAvatar — artigo](https://arxiv.org/abs/2312.02214)
- [Avat3r — artigo e página do projeto](https://arxiv.org/abs/2502.20220) · [Projeto](https://tobias-kirschstein.github.io/avat3r/)
- [GeoAvatar — artigo e página do projeto](https://arxiv.org/abs/2507.18155) · [Projeto](https://hahminlew.github.io/geoavatar/)
- [SpiD — artigo](https://arxiv.org/abs/2607.28032)
- [OMEGA-Avatar — artigo e página do projeto](https://arxiv.org/abs/2602.11693) · [Projeto](https://omega-avatar.github.io/OMEGA-Avatar/)
- [FiCA — artigo e página do projeto](https://arxiv.org/abs/2606.24232) · [Projeto](https://youwangk.github.io/FiCA)
- [HeadsUp — artigo e página do projeto](https://arxiv.org/abs/2605.04035) · [Projeto](https://apple.github.io/ml-headsup/)

