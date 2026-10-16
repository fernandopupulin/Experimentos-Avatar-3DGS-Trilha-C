"""Gera o relatório executivo documental da Trilha C.

O PDF contém somente síntese de fontes citadas e propostas de experimento.
Não importa métricas locais nem simula resultados.

Uso:
    python Implementacoes/gerar_relatorio.py
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Implementacoes" / "relatorio_pesquisa_trilha_c.pdf"
BLUE = colors.HexColor("#183b63")
TEAL = colors.HexColor("#107c83")
LIGHT = colors.HexColor("#eaf1f7")
PALE = colors.HexColor("#f5f8fb")
TEXT = colors.HexColor("#233043")
MUTED = colors.HexColor("#526278")


def register_fonts() -> None:
    fonts = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("Arial", str(fonts / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(fonts / "arialbd.ttf")))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle", parent=base["Title"], fontName="Arial-Bold",
            fontSize=21, leading=27, alignment=TA_LEFT, textColor=BLUE,
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle", parent=base["Normal"], fontName="Arial",
            fontSize=10.5, leading=15, textColor=MUTED, spaceAfter=13,
        ),
        "h1": ParagraphStyle(
            "ReportH1", parent=base["Heading1"], fontName="Arial-Bold",
            fontSize=13, leading=17, textColor=BLUE, spaceBefore=13,
            spaceAfter=7, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "ReportH2", parent=base["Heading2"], fontName="Arial-Bold",
            fontSize=10.2, leading=14, textColor=TEAL, spaceBefore=9,
            spaceAfter=4, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "ReportBody", parent=base["Normal"], fontName="Arial",
            fontSize=9.1, leading=13.5, textColor=TEXT, spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "ReportSmall", parent=base["Normal"], fontName="Arial",
            fontSize=7.8, leading=11.1, textColor=TEXT, spaceAfter=3,
        ),
        "table": ParagraphStyle(
            "ReportTable", parent=base["Normal"], fontName="Arial",
            fontSize=7.8, leading=10.8, textColor=TEXT,
        ),
        "tablehead": ParagraphStyle(
            "ReportTableHead", parent=base["Normal"], fontName="Arial-Bold",
            fontSize=7.8, leading=10.8, textColor=colors.white,
        ),
        "status": ParagraphStyle(
            "ReportStatus", parent=base["Normal"], fontName="Arial-Bold",
            fontSize=8.2, leading=12, textColor=BLUE, alignment=TA_CENTER,
        ),
    }


def para(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def link(label: str, url: str) -> str:
    return f'<link href="{escape(url)}" color="#107c83">{escape(label)}</link>'


def bullet(text: str, style: ParagraphStyle) -> Paragraph:
    return para(f"<font color='#107c83'><b>•</b></font>  {text}", style)


def table(rows: list[list[str]], widths: list[float], styles: dict[str, ParagraphStyle]) -> Table:
    cells = [[para(value, styles["tablehead"] if row_index == 0 else styles["table"])
              for value in row] for row_index, row in enumerate(rows)]
    out = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    out.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, TEAL),
        ("LINEBELOW", (0, 1), (-1, -1), 0.2, colors.HexColor("#d5e0ea")),
    ]))
    return out


def page_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d3deea"))
    canvas.line(19 * mm, 17 * mm, A4[0] - 19 * mm, 17 * mm)
    canvas.setFont("Arial", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(19 * mm, 12 * mm, "Trilha C · Pesquisa documental · Fernando")
    canvas.drawRightString(A4[0] - 19 * mm, 12 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build() -> None:
    register_fonts()
    s = make_styles()
    content_width = A4[0] - 38 * mm
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm,
        topMargin=19 * mm, bottomMargin=23 * mm,
        title="Trilha C — Cabeças 3DGS animáveis e fala",
        author="Fernando",
        subject="Revisão documental de modelos 3DGS e integração com fala",
    )
    story = []

    # Página 1: questão de pesquisa e mapa conceitual.
    story += [
        para("Trilha C: cabeças 3DGS animáveis", s["title"]),
        para("Rigging de gaussianas, aplicações e possibilidade de animação por fala", s["subtitle"]),
        HRFlowable(width="100%", thickness=1.3, color=TEAL),
        Spacer(1, 8),
    ]
    status = Table([[para("REVISÃO DE LITERATURA · SEM RESULTADOS EXPERIMENTAIS LOCAIS", s["status"])]],
                   colWidths=[content_width])
    status.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbd2e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [status, Spacer(1, 9)]
    story += [
        para("1. Perguntas centrais", s["h1"]),
        bullet("Como vincular gaussianas a uma cabeça deformável sem perder detalhes ao mudar pose e expressão?", s["body"]),
        bullet("Uma fala gravada ou ao vivo pode dirigir lábios e mandíbula desse avatar com sincronia verossímil?", s["body"]),
        para("O problema técnico", s["h1"]),
        para("Gaussianas renderizam aparência. Para acompanharem um rosto em movimento, precisam ser ligadas a uma malha, a coordenadas UV, a regiões faciais ou a um campo de deformação. O controle por áudio exige uma etapa adicional que produza movimento facial a partir da fala.", s["body"]),
        para("Famílias de solução", s["h1"]),
        table([
            ["Família", "Trabalhos", "Uso nesta pesquisa"],
            ["Ancoragem em malha", "GaussianAvatars, SplattingAvatar, FlashAvatar, GeoAvatar", "Investigar transporte das gaussianas, deslocamentos e boca."],
            ["Poucas imagens", "Avat3r, SpiD, OMEGA-Avatar, FiCA", "Examinar captura simples, regiões ocultas e expressão."],
            ["Escala multivista", "HeadsUp", "Examinar reconstrução de novas identidades e blendshapes."],
            ["Fala", "Audio2Face-3D, GaussianTalker, TalkingGaussian", "Converter áudio em controle facial ou usar cabeça falante treinada."],
        ], [35 * mm, 68 * mm, content_width - 103 * mm], s),
        Spacer(1, 9),
        para("Regra de evidência", s["h2"]),
        para("Os números deste documento são atribuídos aos autores e acompanhados de suas condições. Aplicações para a Trilha C são hipóteses de trabalho. Nenhum método foi treinado ou comparado neste repositório; portanto não há ranking experimental local.", s["body"]),
    ]

    # Página 2: os nove artigos da trilha.
    story += [PageBreak(), para("2. Modelos: mecanismo e aplicação", s["h1"])]
    model_rows = [
        ["Modelo", "Diferença descrita pelos autores", "Aplicação proposta na Trilha C"],
        ["GaussianAvatars", "Splat em referencial local de triângulo facial, com deslocamento otimizado.", "Baseline de vínculo explícito e transferência de expressão."],
        ["SplattingAvatar", "Coordenadas baricêntricas e deslocamento treinável na malha; serve também para corpo.", "Comparar associação aprendida com ancoragem fixa."],
        ["FlashAvatar", "Campo uniforme na malha paramétrica e deslocamentos para detalhe; foco em eficiência.", "Medir custo e qualidade com o pipeline completo."],
        ["Avat3r", "Reconstrução com quatro imagens e animação condicionada a código de expressão.", "Estudar captura limitada por fotos."],
        ["GeoAvatar", "Regularização distinta para regiões rígidas/flexíveis e estrutura dedicada à boca.", "Examinar anatomia labial e estabilidade ao falar."],
        ["SpiD", "Uma imagem, três ramos gaussianos regionais e driver incluído na inferência.", "Avaliar decomposição regional e latência completa."],
        ["OMEGA-Avatar", "Retrato para cabeça completa em 360°, com malha/cabelo e fusão UV multivista.", "Testar perfil, cabelo e regiões não observadas."],
        ["FiCA", "Retrato para malha gerada/refinada e Gaussian Codec Avatar controlado por expressão.", "Avaliar criação rápida a partir de selfie."],
        ["HeadsUp", "Captura multivista, gaussianas em UV e controle por blendshapes.", "Estudar cenário de estúdio e interface de animação."],
    ]
    story += [table(model_rows, [31 * mm, 78 * mm, content_width - 109 * mm], s)]
    story += [
        Spacer(1, 9),
        para("Diferença que determina a escolha", s["h2"]),
        para("Para a pergunta sobre rigging, GaussianAvatars, SplattingAvatar, FlashAvatar e GeoAvatar são os mais diretamente relacionados. Avat3r, FiCA, SpiD e OMEGA-Avatar enfatizam a obtenção do avatar com entrada escassa; HeadsUp pressupõe captura multivista e treinamento amplo. A ordem de estudo proposta não é uma classificação de qualidade.", s["body"]),
    ]

    # Página 3: fala, interfaces e experimento.
    story += [PageBreak(), para("3. Aplicação conjunta com fala", s["h1"])]
    story += [
        para("A possibilidade está demonstrada em trabalhos específicos de cabeça falante com 3DGS, como GaussianTalker e TalkingGaussian. Nos nove modelos da Trilha C, a entrada central é imagem/vídeo e o controle descrito usa malha, expressão, pose ou blendshapes. Assim, uma integração por áudio precisa ser implementada e testada; não está implícita no termo “animável”.", s["body"]),
        para("Caminho A: controlador facial separado", s["h2"]),
        para("Fala ou TTS → áudio → gerador de movimento facial → parâmetros FLAME/blendshapes → malha animada → gaussianas ancoradas → vídeo. Audio2Face-3D é um candidato ao gerador de movimento; o mapeamento de seus controles para o rig escolhido requer calibração. GaussianAvatars é o primeiro receptor a testar por ter controle explícito de pose e expressão.", s["body"]),
        para("Caminho B: modelo 3DGS condicionado por áudio", s["h2"]),
        para("Fala ou TTS → características acústicas → GaussianTalker ou TalkingGaussian → deformação/renderização → vídeo. GaussianTalker publica inferência com áudio personalizado; TalkingGaussian publica alternativas de extrator, incluindo HuBERT recomendado pelos autores para áudio não inglês. Ambos exigem preparação e treinamento adequados ao falante.", s["body"]),
        para("O que observar", s["h2"]),
        bullet("Formato dos lábios e coarticulação; contato em /p/, /b/ e /m/; repouso durante pausas.", s["body"]),
        bullet("Mandíbula, dentes, interior da boca, identidade, tremor entre quadros e expressão além da boca.", s["body"]),
        bullet("Atraso áudio-vídeo e latência de ponta a ponta, incluindo extração de áudio e controle facial.", s["body"]),
        para("Protocolo mínimo com dados reais", s["h2"]),
        para("Usar a mesma identidade e o mesmo WAV autorizado em português brasileiro. Guardar entrada, controles por quadro, configuração, vídeo renderizado e hardware. Se houver vídeo de referência alinhado, medir erro dos marcos da boca e sincronia; complementar com avaliação humana cega. Começar com arquivo completo. Fala ao vivo requer prova separada de operação em fluxo e atraso interativo.", s["body"]),
        para("Estado de implementação", s["h2"]),
        para("Nenhum dos caminhos foi executado neste repositório. A escolha preliminar é GaussianAvatars + controlador externo para estudar rigging, e GaussianTalker como primeiro piloto de fala 3DGS. Essa escolha é de viabilidade metodológica, não de superioridade visual comprovada.", s["body"]),
    ]

    # Página 4: dados publicados, próximos passos, fontes.
    story += [PageBreak(), para("4. Dados publicados e próximos passos", s["h1"])]
    story += [
        para("Números dos autores, com contexto", s["h2"]),
        table([
            ["Trabalho", "Dado relatado", "Condição / leitura correta"],
            ["SplattingAvatar", ">300 FPS em GPU moderna; 30 FPS em móvel.", "Renderização da representação proposta; não é latência áudio-vídeo."],
            ["FlashAvatar", ">300 FPS.", "Renderização 512 × 512 em RTX 3090, conforme projeto."],
            ["Avat3r", "4 imagens; ~8 FPS de animação.", "Modelo de quatro vistas em RTX 3090, com ativações em cache."],
            ["FiCA", "Criação em até 5 segundos.", "A partir de uma foto, conforme página do projeto."],
            ["HeadsUp", ">10 mil identidades no treino.", "Conjunto interno relatado; não disponível aqui por pressuposto."],
            ["GaussianTalker", "Até 120 FPS.", "Renderização relatada no artigo; pipeline completo não medido aqui."],
        ], [34 * mm, 54 * mm, content_width - 88 * mm], s),
        para("O que falta para resultados próprios", s["h2"]),
        bullet("Escolher dados com direito de uso e documentar câmera, resolução, divisão treino/teste e áudio.", s["body"]),
        bullet("Executar um baseline oficial e registrar commit, dependências, GPU, comandos e saídas.", s["body"]),
        bullet("Aplicar a mesma sequência facial e o mesmo áudio a variantes comparáveis; publicar erros e vídeos completos.", s["body"]),
        para("Fontes primárias", s["h2"]),
    ]
    refs = [
        ("GaussianAvatars", "https://arxiv.org/abs/2312.02069"),
        ("SplattingAvatar", "https://arxiv.org/abs/2403.05087"),
        ("FlashAvatar", "https://arxiv.org/abs/2312.02214"),
        ("Avat3r", "https://arxiv.org/abs/2502.20220"),
        ("GeoAvatar", "https://arxiv.org/abs/2507.18155"),
        ("SpiD", "https://arxiv.org/abs/2607.28032"),
        ("OMEGA-Avatar", "https://arxiv.org/abs/2602.11693"),
        ("FiCA", "https://arxiv.org/abs/2606.24232"),
        ("HeadsUp", "https://arxiv.org/abs/2605.04035"),
        ("GaussianTalker", "https://arxiv.org/abs/2404.16012"),
        ("TalkingGaussian", "https://arxiv.org/abs/2404.15264"),
        ("Audio2Face-3D", "https://github.com/NVIDIA/Audio2Face-3D-SDK"),
    ]
    ref_cells = []
    for start in range(0, len(refs), 3):
        row = []
        for name, url in refs[start:start + 3]:
            row.append(para(link(name, url), s["small"]))
        ref_cells.append(row)
    ref_table = Table(ref_cells, colWidths=[content_width / 3] * 3, hAlign="LEFT")
    ref_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story += [ref_table, Spacer(1, 5), para(
        "Fichas completas, condições dos dados e plano experimental: "
        + link("repositório da Trilha C", "https://github.com/fernandopupulin/Experimentos-Avatar-3DGS-Trilha-C"),
        s["small"],
    )]

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
