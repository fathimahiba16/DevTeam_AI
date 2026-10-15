
from pathlib import Path
from xml.sax.saxutils import escape

import markdown

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    Preformatted,
)

from reportlab.platypus.tableofcontents import TableOfContents

from xml.etree import ElementTree as ET


class PDFGenerator:
    def __init__(self):
        self.styles = {
            "title": ParagraphStyle(
                name="CollegeTitle",
                fontName="Times-Bold",
                fontSize=20,
                leading=28,
                alignment=TA_CENTER,
                spaceAfter=20,
            ),
            "subtitle": ParagraphStyle(
                name="CollegeSubtitle",
                fontName="Times-Bold",
                fontSize=15,
                leading=22,
                alignment=TA_CENTER,
            ),
            "heading1": ParagraphStyle(
                name="CollegeHeading1",
                fontName="Times-Bold",
                fontSize=15,
                leading=21,
                spaceBefore=18,
                spaceAfter=10,
                keepWithNext=True,
            ),
            "heading2": ParagraphStyle(
                name="CollegeHeading2",
                fontName="Times-Bold",
                fontSize=12,
                leading=18,
                spaceBefore=12,
                spaceAfter=7,
                keepWithNext=True,
            ),
            "body": ParagraphStyle(
                name="CollegeBody",
                fontName="Times-Roman",
                fontSize=11,
                leading=17,
                alignment=TA_JUSTIFY,
                spaceAfter=10,
            ),
            "bullet": ParagraphStyle(
                name="CollegeBullet",
                fontName="Times-Roman",
                fontSize=11,
                leading=17,
                leftIndent=12,
                spaceAfter=5,
            ),
            "code": ParagraphStyle(
                name="CollegeCode",
                fontName="Courier",
                fontSize=8,
                leading=11,
                leftIndent=10,
                spaceAfter=10,
            ),
        }

    def _inline_text(self, element):
        """
        Convert supported Markdown inline formatting
        into ReportLab paragraph markup.
        """
        parts = []

        if element.text:
            parts.append(escape(element.text))

        for child in element:
            content = self._inline_text(child)

            if child.tag in ("strong", "b"):
                parts.append(f"<b>{content}</b>")
            elif child.tag in ("em", "i"):
                parts.append(f"<i>{content}</i>")
            elif child.tag == "code":
                parts.append(
                    f'<font name="Courier">{content}</font>'
                )
            elif child.tag == "a":
                # Show link text without embedding untrusted URLs.
                parts.append(content)
            else:
                parts.append(content)

            if child.tail:
                parts.append(escape(child.tail))

        return "".join(parts)

    def _add_element(self, element, story):
        tag = element.tag

        if tag in ("h1", "h2", "h3", "h4"):
            level = 1 if tag == "h1" else 2
            style = self.styles[
                "heading1" if level == 1 else "heading2"
            ]

            paragraph = Paragraph(
                self._inline_text(element),
                style,
            )

            # Used to identify TOC entries.
            paragraph.toc_level = level - 1
            story.append(paragraph)

        elif tag == "p":
            content = self._inline_text(element).strip()

            if content:
                story.append(
                    Paragraph(content, self.styles["body"])
                )

        elif tag in ("ul", "ol"):
            items = []

            for item in element.findall("li"):
                content = self._inline_text(item).strip()

                if content:
                    items.append(
                        ListItem(
                            Paragraph(
                                content,
                                self.styles["bullet"],
                            )
                        )
                    )

            if items:
                story.append(
                    ListFlowable(
                        items,
                        bulletType=(
                            "1" if tag == "ol" else "bullet"
                        ),
                        leftIndent=20,
                    )
                )

                story.append(Spacer(1, 0.2 * cm))

        elif tag == "pre":
            code = "".join(element.itertext())

            story.append(
                Preformatted(
                    code,
                    self.styles["code"],
                    maxLineLength=75,
                    splitChars=" ",
                )
            )

        elif tag == "blockquote":
            for child in element:
                self._add_element(child, story)

        elif tag == "hr":
            story.append(Spacer(1, 0.3 * cm))

        else:
            # Handle other container elements recursively.
            for child in element:
                self._add_element(child, story)

    def generate_pdf(
        self,
        report_content,
        output_path,
        project_title="Software Project",
    ):
        output_path = Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        styles = self.styles

        class CollegeDocument(BaseDocTemplate):
            def __init__(self, filename):
                super().__init__(
                    str(filename),
                    pagesize=A4,
                    leftMargin=2.5 * cm,
                    rightMargin=2.5 * cm,
                    topMargin=2.5 * cm,
                    bottomMargin=2.5 * cm,
                )

                frame = Frame(
                    self.leftMargin,
                    self.bottomMargin,
                    self.width,
                    self.height,
                    id="normal",
                )

                self.addPageTemplates(
                    PageTemplate(
                        id="college",
                        frames=frame,
                        onPage=self.draw_page_number,
                    )
                )

            def draw_page_number(self, canvas, doc):
                canvas.saveState()

                canvas.setFont("Times-Roman", 9)

                canvas.drawCentredString(
                    A4[0] / 2,
                    1.5 * cm,
                    f"Page {doc.page}",
                )

                canvas.restoreState()

            def afterFlowable(self, flowable):
                if (
                    isinstance(flowable, Paragraph)
                    and hasattr(flowable, "toc_level")
                ):
                    self.notify(
                        "TOCEntry",
                        (
                            flowable.toc_level,
                            flowable.getPlainText(),
                            self.page,
                        ),
                    )

        doc = CollegeDocument(output_path)
        story = []

        # COVER PAGE
        story.append(Spacer(1, 5 * cm))

        story.append(
            Paragraph(
                escape(project_title),
                styles["title"],
            )
        )

        story.append(Spacer(1, 1 * cm))

        story.append(
            Paragraph(
                "MINI PROJECT REPORT",
                styles["title"],
            )
        )

        story.append(Spacer(1, 2 * cm))

        story.append(
            Paragraph(
                "Generated by DevTeam AI",
                styles["subtitle"],
            )
        )

        story.append(PageBreak())

        # TABLE OF CONTENTS
        story.append(
            Paragraph(
                "TABLE OF CONTENTS",
                styles["title"],
            )
        )

        toc = TableOfContents()

        toc.levelStyles = [
            ParagraphStyle(
                name="TOCLevel1",
                fontName="Times-Roman",
                fontSize=11,
                leading=18,
                leftIndent=12,
                firstLineIndent=-12,
            ),
            ParagraphStyle(
                name="TOCLevel2",
                fontName="Times-Roman",
                fontSize=10,
                leading=16,
                leftIndent=28,
                firstLineIndent=-12,
            ),
        ]

        story.append(toc)
        story.append(PageBreak())

        # CONVERT MARKDOWN TO HTML
        html = markdown.markdown(
            report_content,
            extensions=["extra", "sane_lists"],
        )

        # Parse the generated HTML as XML.
        # Standard Markdown output for the supported
        # headings, paragraphs, lists, and code blocks
        # is compatible with this approach.
        try:
            root = ET.fromstring(
                f"<document>{html}</document>"
            )
        except ET.ParseError as error:
            raise ValueError(
                f"Could not parse report Markdown: {error}"
            ) from error

        for element in root:
            self._add_element(element, story)

        # Build twice so TOC page numbers are populated.
        doc.multiBuild(story)

        return str(output_path)
