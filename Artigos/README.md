# Guia crítico dos modelos — Trilha C

**Responsável:** Fernando

**Atualização:** 16 de outubro de 2026

**Natureza:** revisão de artigos e projetos dos autores. Este repositório ainda não reproduziu os métodos nem mediu seus resultados.

## Como ler as fichas

Cada ficha separa **o que os autores descrevem** de **como poderíamos usar o método nesta pesquisa**. “Aplicação na Trilha C” é uma proposta nossa, não uma funcionalidade já testada aqui. “Integração com fala” indica a interface de movimento que teria de receber um módulo áudio→expressão; não significa que o artigo inclua um sistema de fala. Os trabalhos possuem entradas e dados diferentes, portanto seus números publicados não formam um ranking direto.

### Mapa rápido

| Pergunta que domina o trabalho | Métodos | Consequência para a pesquisa |
| --- | --- | --- |
| Como associar gaussianas a geometria deformável? | GaussianAvatars, SplattingAvatar, FlashAvatar, GeoAvatar | Referências principais para o experimento de rigging. |
| Como reconstruir a partir de poucas imagens? | Avat3r, FiCA, OMEGA-Avatar, SpiD | Interessam quando a captura é limitada; dependem de modelos gerais treinados previamente. |
| Como obter cabeça completa e vistas não observadas? | OMEGA-Avatar; parcialmente FiCA | Importa para cabelo, orelhas e parte posterior da cabeça. |
| Como escalar captura com muitas câmeras e identidades? | HeadsUp | Referência para estúdio multivista e animação por blendshapes. |
| Como a fala move a boca? | Nenhum dos nove é, por sua proposta central, um sistema áudio→movimento. | Exige controlador externo ou comparação com trabalhos específicos de cabeça falante. |

## 1. GaussianAvatars

**Fonte:** [artigo](https://arxiv.org/abs/2312.02069) · [código oficial](https://github.com/ShenhanQian/GaussianAvatars)

- **O que faz:** representa a cabeça com gaussianas vinculadas a um modelo facial paramétrico. Cada splat é parametrizado no referencial local de um triângulo e pode ter deslocamento otimizado. O modelo subjacente fornece pose e expressão; a implementação oficial oferece a opção `--bind_to_mesh`.
- **Diferença técnica:** o vínculo explícito ao triângulo torna rastreável como cada gaussiana acompanha a malha. É a referência mais direta para perguntar onde a associação funciona e onde falha.
- **Aplicação na Trilha C (proposta):** baseline de rigging; comparar vinculação à malha, deslocamentos locais e artefatos na boca sob a mesma animação.
- **Fala:** o artigo demonstra controle por parâmetros faciais e sequência motora, não entrada WAV direta. Um gerador áudio→parâmetros FLAME teria de fornecer os controles. O retargeting, sobretudo mandíbula e lábios, precisa ser validado.
- **Limite prático:** usar dados, modelo FLAME e dependências nos termos exigidos pela implementação. O repositório oficial declara licença não comercial para sua distribuição; consultar os termos antes de reutilizar código ou pesos.

## 2. SplattingAvatar

**Fonte:** [artigo](https://arxiv.org/abs/2403.05087) · [código oficial](https://github.com/initialneil/SplattingAvatar)

- **O que faz:** embute gaussianas em uma malha triangular por coordenadas baricêntricas e deslocamento. A associação pode caminhar sobre a malha durante a otimização. A malha descreve movimento e deformação de menor frequência; as gaussianas carregam detalhe visual. O artigo inclui corpo inteiro e cabeça a partir de vídeo monocular.
- **Diferença técnica:** a associação gaussiana–malha é treinável e pode funcionar com animação esquelética, blendshapes ou edição da malha, em vez de ficar limitada a um único rig facial.
- **Aplicação na Trilha C (proposta):** testar se o vínculo aprendido reduz deslizamento em relação à ancoragem simples em triângulos.
- **Fala:** requer uma malha animada pela fala. Se essa malha possuir blendshapes/controle de mandíbula, um gerador de movimento facial poderá dirigi-la; não há entrada de áudio afirmada como função central do artigo.
- **Limite prático:** por cobrir também corpo inteiro, comparações com métodos só de cabeça devem usar a mesma região, câmera e sequência.

## 3. FlashAvatar

**Fonte:** [artigo](https://arxiv.org/abs/2312.02214) · [página do projeto](https://ustc3dv.github.io/FlashAvatar/)

- **O que faz:** parte de um vídeo monocular curto e dispõe um campo uniforme de gaussianas sobre um modelo facial paramétrico. Deslocamentos espaciais representam detalhes e regiões fora da superfície.
- **Diferença técnica:** enfatiza representação compacta, inicialização e eficiência de reconstrução/renderização, mantendo controle pelo modelo facial.
- **Aplicação na Trilha C (proposta):** alternativa quando custo de treino, memória e latência forem decisivos. Os valores de velocidade publicados pertencem ao ambiente do artigo; ainda não foram medidos aqui.
- **Fala:** a malha paramétrica oferece uma possível interface para controles gerados por áudio. Seria necessário converter as saídas do controlador para os parâmetros usados pela implementação e verificar fechamento labial e detalhes da boca.
- **Limite prático:** velocidade de renderização isolada não mede extração de áudio, controle facial e retargeting.

## 4. Avat3r

**Fonte:** [artigo](https://arxiv.org/abs/2502.20220) · [página do projeto](https://tobias-kirschstein.github.io/avat3r/)

- **O que faz:** infere um avatar gaussiano animável a partir de poucas imagens. Usa pistas visuais de DUSt3R e Sapiens e condiciona a animação em um código de expressão por atenção cruzada.
- **Diferença técnica:** desloca o custo de otimização por pessoa para o treinamento de um modelo geral. Seu foco é reconstrução com poucas vistas, inclusive imagens de expressões inconsistentes.
- **Aplicação na Trilha C (proposta):** estudar uma captura por celular ou poucas fotos quando não existe vídeo longo para otimização por pessoa.
- **Fala:** a interface descrita é um código de expressão, não o áudio. Segundo a página do projeto, esse código pode ser, por exemplo, uma descrição de expressão FLAME. Integrar fala ainda exigiria um preditor áudio→código de expressão e avaliação da dinâmica temporal.
- **Limite prático:** comparar a qualidade com métodos treinados por pessoa requer declarar a diferença de dados e tempo de preparação. Em 16 de outubro de 2026, a [página oficial](https://tobias-kirschstein.github.io/avat3r/) ainda apresenta o código como “coming soon”; uma reprodução independente depende de sua liberação.

## 5. GeoAvatar

**Fonte:** [artigo](https://arxiv.org/abs/2507.18155) · [página do projeto](https://hahminlew.github.io/geoavatar/)

- **O que faz:** separa gaussianas em conjuntos rígidos e flexíveis com regularização de deslocamento adaptativa. Introduz estrutura de boca e deformação por partes, além de perda para alinhar gaussianas ao rosto 3DMM. Os autores disponibilizam o conjunto DynamicFace.
- **Diferença técnica:** aborda explicitamente o conflito entre fidelidade de reconstrução e liberdade de expressão, com atenção especial à anatomia da boca.
- **Aplicação na Trilha C (proposta):** referência para a variante com deslocamentos locais e para análise de falhas na mandíbula/lábios.
- **Fala:** um controlador áudio→parâmetros faciais pode ser avaliado sobre o avatar, mas o artigo não demonstra que qualquer fala se converte diretamente em movimento. Sua modelagem da boca é particularmente relevante para testar bilabiais e abertura/fechamento.
- **Limite prático:** benefícios observados pelos autores em seus dados não garantem a mesma qualidade em português brasileiro ou em outra captura.

## 6. SpiD (Split and Drive)

**Fonte:** [artigo](https://arxiv.org/abs/2607.28032)

- **O que faz:** reconstrói uma cabeça gaussiana a partir de uma imagem, separando a representação em três ramos para regiões faciais geometricamente distintas. O trabalho também integra o controle por quadro ao pipeline para contabilizar o custo completo de inferência.
- **Diferença técnica:** prioriza decomposição regional e medição de latência incluindo o driver, problema que benchmarks só de renderização deixam de fora.
- **Aplicação na Trilha C (proposta):** referência para medir o pipeline completo e investigar se a boca precisa de representação especializada.
- **Fala:** “drive” no título não estabelece entrada de áudio. É necessário verificar a interface de controle e conectar um módulo áudio→driver adequado antes de alegar integração.
- **Limite prático:** como método de uma imagem, regiões ocultas precisam ser inferidas; isso deve ser observado em perfil e vistas posteriores.

## 7. OMEGA-Avatar

**Fonte:** [artigo](https://arxiv.org/abs/2602.11693) · [página do projeto](https://omega-avatar.github.io/OMEGA-Avatar/)

- **O que faz:** gera, a partir de um retrato, uma cabeça gaussiana animável e completa em 360°. Usa deformação de malha FLAME com informação semântica e normais multivista para incorporar cabelo, além de agregar características em UV de múltiplas vistas sintetizadas.
- **Diferença técnica:** privilegia completude da cabeça e coerência em ângulos não vistos durante a captura, incluindo cabelo e nuca.
- **Aplicação na Trilha C (proposta):** referência para avaliar perfil, costas da cabeça e consistência de identidade em 360° quando a entrada for uma foto.
- **Fala:** o projeto injeta pose e expressão derivadas de imagem-alvo na malha. Um fluxo por áudio exigiria gerar controles equivalentes e confirmar que o cabelo e a face permanecem coerentes em movimento; isso não é uma capacidade comprovada neste repositório.
- **Limite prático:** partes não observadas são geradas por priors; não devem ser apresentadas como reconstrução medida da anatomia real da pessoa.

## 8. FiCA

**Fonte:** [artigo](https://arxiv.org/abs/2606.24232) · [página do projeto](https://youwangk.github.io/FiCA)

- **O que faz:** cria um Gaussian Codec Avatar a partir de um retrato. Combina priors visuais, difusão para recuperar malha completa, refinamento de malha e decodificação de gaussianas. O artigo afirma animação por expressões novas sem otimização específica por pessoa na inferência.
- **Diferença técnica:** privilegia obtenção rápida de um avatar dirigível a partir de uma única imagem, transferindo o esforço para modelos gerais pré-treinados.
- **Aplicação na Trilha C (proposta):** avaliar captura rápida quando não há vídeo ou estúdio multivista.
- **Fala:** “dirigível por expressões” fornece um ponto potencial de integração, mas não especifica áudio como entrada. É necessário mapear fala para a representação de controle do codec e testar sincronização.
- **Limite prático:** qualidade de uma única foto depende fortemente dos priors para superfícies ocultas e boca interior.

## 9. HeadsUp

**Fonte:** [artigo](https://arxiv.org/abs/2605.04035) · [página do projeto](https://apple.github.io/ml-headsup/)

- **O que faz:** recebe capturas multivista e infere gaussianas parametrizadas em UV, ancoradas a uma cabeça neutra. O artigo relata treinamento em um conjunto interno de mais de 10 mil pessoas e demonstra animação por blendshapes de expressão.
- **Diferença técnica:** prioriza escala de treinamento e reconstrução de novas identidades sem otimização no teste, usando uma representação UV que separa a quantidade de gaussianas da quantidade de vistas de entrada.
- **Aplicação na Trilha C (proposta):** referência para cenário com múltiplas câmeras e para uma interface explícita de blendshapes.
- **Fala:** um sistema áudio→blendshapes é conceitualmente compatível com a demonstração de controle do projeto. Seria preciso conhecer nomes, ordem, amplitude e taxa temporal dos blendshapes e testar retargeting. O artigo não relata um pipeline áudio→HeadsUp.
- **Limite prático:** o grande conjunto de treino descrito é interno; não é um pressuposto de reprodução local.

## Síntese para decisão

### Números verificáveis publicados pelos autores

Estes dados descrevem **experimentos e condições dos respectivos autores**. Não foram medidos neste repositório e não devem ser postos na mesma coluna de um benchmark local.

| Trabalho | Dado publicado | Condição ou interpretação | Fonte |
| --- | --- | --- | --- |
| SplattingAvatar | Mais de 300 FPS em GPU moderna; 30 FPS em dispositivo móvel. | A página apresenta ambas as velocidades para a representação proposta, que inclui avatares de corpo e cabeça; não equivale à latência de áudio→vídeo. | [Artigo/projeto](https://initialneil.github.io/SplattingAvatar) |
| FlashAvatar | Mais de 300 FPS. | Renderização a 512 × 512 em NVIDIA RTX 3090, segundo a página do projeto; o custo de um controlador por áudio fica fora dessa medida. | [Projeto](https://ustc3dv.github.io/FlashAvatar/) |
| Avat3r | Quatro imagens de entrada; aproximadamente 8 FPS para animação do modelo de quatro vistas com ativação em cache. | Página do projeto: GPU RTX 3090. A geração inicial e a animação são etapas distintas. | [Projeto](https://tobias-kirschstein.github.io/avat3r/) |
| FiCA | Criação de avatar em até 5 segundos, conforme os autores. | Uma foto como entrada; a página afirma animação em tempo real sob expressões-alvo, sem especificar aqui um benchmark de áudio. | [Projeto](https://youwangk.github.io/FiCA) |
| HeadsUp | Treinamento em conjunto interno de mais de 10 mil pessoas. | É escala do conjunto de treinamento relatado, não quantidade de pessoas testadas por nós nem garantia de acesso aos dados. | [Artigo](https://arxiv.org/abs/2605.04035) |
| GaussianTalker (referência de fala) | Até 120 FPS de renderização, segundo os autores. | Número do artigo sobre cabeça falante; requer comparar também extração de áudio, driver e codificação do vídeo para latência total. | [Artigo](https://arxiv.org/abs/2404.16012) |

### Recomendações provisórias

- **Para estudar ancoragem:** começar pela interface explícita de [GaussianAvatars](https://github.com/ShenhanQian/GaussianAvatars), depois comparar a associação treinável de [SplattingAvatar](https://github.com/initialneil/SplattingAvatar) e o tratamento de boca de [GeoAvatar](https://arxiv.org/abs/2507.18155). É uma **ordem proposta de trabalho**, não um ranking de desempenho.
- **Para captura limitada:** Avat3r, FiCA, OMEGA-Avatar e SpiD abordam aspectos diferentes da reconstrução com uma ou poucas imagens; escolher depende de expressão, cabeça completa, custo e disponibilidade de implementação.
- **Para integração com fala:** testar primeiro a viabilidade de um controlador áudio→expressão em um rig conhecido e comparar com um sistema áudio→3DGS nativo. O [relatório principal](../relatorio_trilha_c.md#6-pergunta-fundamental-fala-pode-animar-a-cabeça-3dgs) detalha candidatos e critérios.
- **Para afirmar “melhor”:** usar os mesmos dados, áudio, identidade, câmera e hardware. Sem esse ensaio, conclusões numéricas só podem ser atribuídas aos respectivos autores e às condições de seus artigos.



