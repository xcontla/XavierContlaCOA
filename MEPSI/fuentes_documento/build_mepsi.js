const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, ImageRun, TableOfContents, Footer, Header, PageNumber,
  LevelFormat, PageBreak, VerticalAlign,
} = require('docx');

const contenido = require('./contenido_mepsi');
const IMG = path.join(__dirname, 'figuras');
const OUT = process.argv[2];

const FONT = 'Arial';
const AZUL = '1F3864';
const LINE = 360; // interlineado 1.5

// --- texto enriquecido: **negrita**, `código`, {{verificar}}
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`|\{\{[^}]+\}\})/g;
  let last = 0, m;
  const push = (t, o = {}) => {
    // {{...}} puede contener `código`
    if (o.highlight && /`/.test(t)) {
      t.split(/(`[^`]+`)/).filter(Boolean).forEach(part => {
        if (part.startsWith('`')) out.push(new TextRun({ text: part.slice(1, -1), font: 'Consolas', size: base.size ? base.size - 2 : 22, highlight: 'yellow' }));
        else out.push(new TextRun({ text: part, font: FONT, size: base.size || 24, highlight: 'yellow', bold: base.bold }));
      });
      return;
    }
    out.push(new TextRun({ text: t, font: o.font || FONT, size: o.size || base.size || 24, bold: o.bold || base.bold, italics: base.italics, highlight: o.highlight, color: base.color }));
  };
  while ((m = re.exec(text))) {
    if (m.index > last) push(text.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith('**')) {
      // negrita que puede contener {{}}: simple
      push(tok.slice(2, -2), { bold: true });
    } else if (tok.startsWith('`')) push(tok.slice(1, -1), { font: 'Consolas', size: (base.size || 24) - 2 });
    else push(tok.slice(2, -2), { highlight: 'yellow' });
    last = m.index + tok.length;
  }
  if (last < text.length) push(text.slice(last));
  return out;
}

const P = (text, opts = {}) => new Paragraph({
  children: runs(text, opts.run || {}),
  alignment: opts.align || AlignmentType.JUSTIFIED,
  spacing: { line: opts.line || LINE, after: opts.after ?? 120, before: opts.before || 0 },
  ...(opts.extra || {}),
});

function tabla(t) {
  const total = t.widths.reduce((a, b) => a + b, 0);
  const sz = t.small ? 18 : 20;
  const border = { style: BorderStyle.SINGLE, size: 4, color: '8EA9DB' };
  const borders = { top: border, bottom: border, left: border, right: border };
  const cell = (txt, i, head) => new TableCell({
    width: { size: t.widths[i], type: WidthType.DXA },
    borders,
    verticalAlign: VerticalAlign.CENTER,
    shading: head ? { type: ShadingType.CLEAR, color: 'auto', fill: AZUL } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({
      alignment: i === 0 || t.widths[i] > 2500 ? AlignmentType.LEFT : AlignmentType.CENTER,
      spacing: { line: 240, after: 0 },
      children: runs(txt, { size: sz, bold: head, color: head ? 'FFFFFF' : undefined }),
    })],
  });
  const rows = [new TableRow({ tableHeader: true, children: t.head.map((h, i) => cell(h, i, true)) })];
  t.rows.forEach((r, ri) => rows.push(new TableRow({
    children: r.map((c, i) => {
      const tc = cell(c, i, false);
      return tc;
    }),
  })));
  const els = [];
  if (t.caption) els.push(P(t.caption, { align: AlignmentType.LEFT, run: { bold: true, size: 20 }, after: 60, before: 120, line: 240, extra: { keepNext: true } }));
  els.push(new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: t.widths, rows }));
  els.push(P(t.note || '', { align: AlignmentType.LEFT, run: { size: 18, italics: true }, after: 160, line: 240 }));
  return els;
}

function figura(f) {
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, keepNext: true,
      children: [new ImageRun({ type: 'png', data: fs.readFileSync(path.join(IMG, f.file)), transformation: { width: f.w, height: f.h } })],
    }),
    P(f.caption, { align: AlignmentType.CENTER, run: { bold: true, size: 20 }, after: 200, line: 240 }),
  ];
}

let olRef = 0;
const children = [];

// ---------------- Portada
const C = (t, size, opts = {}) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: opts.after ?? 120, before: opts.before || 0, line: 276 }, children: [new TextRun({ text: t, font: FONT, size, bold: opts.bold, color: opts.color })] });
children.push(
  C('UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO', 28, { bold: true, color: AZUL, before: 600 }),
  C('Dirección General de Orientación y Atención Educativa', 26, { after: 600 }),
  C('Concurso de Oposición Abierto', 24, { bold: true }),
  C('Técnico Académico Titular "A", tiempo completo, interino', 22),
  C('Área: Cómputo · Registro 33709-35', 22),
  C('Convocatoria publicada en Gaceta UNAM el 19 de marzo de 2026', 20, { after: 900 }),
  C('PRUEBA 2', 24, { bold: true, color: AZUL }),
  C('Propuesta de diseño e implementación de un sistema automatizado', 30, { bold: true }),
  C('para la aplicación masiva de pruebas diagnósticas de selección', 30, { bold: true }),
  C('de aspirantes a nivel posgrado', 30, { bold: true, after: 300 }),
  C('Caso: Manual de Evaluación Psicológica (MEPSI)', 26, { color: AZUL, after: 300 }),
  C('Tecnologías: Java J2EE · AngularJS · MySQL · Hibernate · Spring MVC', 22, { after: 1200 }),
  C('Presenta:', 22),
  C('Pedro Xavier Contla Romero', 26, { bold: true, after: 600 }),
  C('Ciudad Universitaria, Cd. Mx., octubre de 2026', 22),
  new Paragraph({ children: [new PageBreak()] }),
);
// ---------------- Índice
children.push(
  new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: 'Índice', font: FONT, size: 28, bold: true, color: AZUL })] }),
  new TableOfContents('Índice', { hyperlink: true, headingStyleRange: '1-2' }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---------------- Cuerpo
for (const b of contenido) {
  if (b.h1) children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: b.h1 })], keepNext: true }));
  else if (b.h2) children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: b.h2 })], keepNext: true }));
  else if (b.p) children.push(P(b.p));
  else if (b.ul) b.ul.forEach(t => children.push(P(t, { after: 60, align: b.left ? AlignmentType.LEFT : undefined, extra: { numbering: { reference: 'vinetas', level: 0 } } })));
  else if (b.code) {
    b.code.forEach((ln, i) => children.push(new Paragraph({
      shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'F2F2F2' },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: '8EA9DB', space: 6 } },
      indent: { left: 200 },
      spacing: { line: 240, after: 0, before: i === 0 ? 80 : 0 }, keepNext: true, keepLines: true,
      children: [new TextRun({ text: ln === '' ? ' ' : ln, font: 'Consolas', size: 17 })],
    })));
    children.push(P(b.caption, { align: AlignmentType.LEFT, run: { size: 18, italics: true }, after: 160, before: 40, line: 240 }));
  }
  else if (b.ol) { olRef++; b.ol.forEach(t => children.push(P(t.replace(/^RF\d+\.\s*/, m => m), { after: 60, extra: { numbering: { reference: 'num', level: 0, instance: olRef } } }))); }
  else if (b.table) children.push(...tabla(b.table));
  else if (b.fig) children.push(...figura(b.fig));
  else if (b.pb) children.push(new Paragraph({ children: [new PageBreak()] }));
}

const doc = new Document({
  creator: 'Pedro Xavier Contla Romero',
  title: 'Prueba 2 - MEPSI - COA 33709-35',
  styles: {
    default: { document: { run: { font: FONT, size: 24 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28, bold: true, font: FONT, color: AZUL }, paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 25, bold: true, font: FONT, color: AZUL }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: 'vinetas', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
      { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] },
    ],
  },
  features: { updateFields: true },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1418, bottom: 1418, left: 1418, right: 1418, header: 708, footer: 708 } },
      titlePage: true,
    },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'COA 33709-35 · Prueba 2 · MEPSI', font: FONT, size: 16, color: '808080' })] })] }),
      first: new Header({ children: [new Paragraph('')] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] }),
      first: new Footer({ children: [new Paragraph('')] }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log('Escrito', OUT); });
