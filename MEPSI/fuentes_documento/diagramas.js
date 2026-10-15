// Genera los diagramas de la propuesta MEPSI como SVG -> PNG
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const OUT = process.argv[2] || 'img';
fs.mkdirSync(OUT, { recursive: true });

const C = {
  azul: '#1F3864', azulClaro: '#D9E2F3', oro: '#C9A227', oroClaro: '#FFF2CC',
  gris: '#595959', grisClaro: '#F2F2F2', verde: '#E2EFDA', verdeOsc: '#375623',
  rojoClaro: '#FBE5D6', rojo: '#843C0C', blanco: '#FFFFFF', negro: '#222222',
};
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function box(x, y, w, h, fill, stroke, lines, opts = {}) {
  const fs_ = opts.fs || 15, bold = opts.bold, rx = opts.rx ?? 6;
  let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${opts.sw || 1.5}"/>`;
  const lh = fs_ * 1.3;
  const total = lines.length * lh;
  let ty = opts.top ? y + fs_ + 8 : y + h / 2 - total / 2 + fs_ * 0.95;
  lines.forEach((l, i) => {
    const isB = bold === true || (bold === 'first' && i === 0);
    s += `<text x="${x + w / 2}" y="${ty + i * lh}" font-size="${i === 0 && opts.fsTitle ? opts.fsTitle : fs_}" text-anchor="middle" font-family="Arial" fill="${opts.color || C.negro}" ${isB ? 'font-weight="bold"' : ''}>${esc(l)}</text>`;
  });
  return s;
}
function arrow(x1, y1, x2, y2, label, opts = {}) {
  const col = opts.color || C.gris;
  let s = `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${opts.sw || 2}" ${opts.dash ? 'stroke-dasharray="7,5"' : ''} marker-end="url(#ah)"/>`;
  if (label) {
    const mx = (x1 + x2) / 2 + (opts.dx || 0), my = (y1 + y2) / 2 + (opts.dy || -6);
    s += `<text x="${mx}" y="${my}" font-size="${opts.fs || 13}" text-anchor="${opts.anchor || 'middle'}" font-family="Arial" fill="${C.negro}" ${opts.italic ? 'font-style="italic"' : ''}>${esc(label)}</text>`;
  }
  return s;
}
const defs = `<defs><marker id="ah" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="${C.gris}"/></marker></defs>`;
const svg = (w, h, body) => `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="100%" height="100%" fill="#fff"/>${defs}${body}</svg>`;

async function render(name, s) {
  fs.writeFileSync(path.join(OUT, name + '.svg'), s);
  await sharp(Buffer.from(s), { density: 192 }).png().toFile(path.join(OUT, name + '.png'));
  console.log('ok', name);
}

// ---------------------------------------------------------------- 1. Arquitectura
function arquitectura() {
  const W = 1500, H = 900;
  let b = '';
  // Cliente
  b += box(40, 30, 620, 150, C.oroClaro, C.oro, ['Cliente: navegador web del aspirante', 'AngularJS 1.x (SPA) · ngRoute · angular-timer', 'blockUI · ngSanitize · Bootstrap 4.1 · jQuery', 'Vistas JSP parciales + imágenes de reactivos'], { bold: 'first', fs: 16 });
  b += arrow(350, 180, 350, 240, 'HTTPS · JSON (REST) / HTML parcial', { dx: 12, anchor: 'start' });
  // Servidor
  b += `<rect x="20" y="245" width="680" height="560" rx="8" fill="${C.grisClaro}" stroke="${C.azul}" stroke-width="2" stroke-dasharray="8,5"/>`;
  b += `<text x="40" y="272" font-size="17" font-weight="bold" font-family="Arial" fill="${C.azul}">Servidor de aplicaciones GlassFish 4.1 · Java EE 7 (WAR)</text>`;
  const layers = [
    ['Seguridad: Spring Security', 'Login por formulario · BCrypt · ROLE_USUARIO · @PreAuthorize', 'Bloqueo 10 intentos · reCAPTCHA · máx. 2 sesiones'],
    ['Presentación: Spring MVC (DispatcherServlet)', 'AnonymousController · UsuarioController(Data)', 'CuestionarioController · CuestionarioControllerData'],
    ['Negocio: servicios Spring (@Bean)', 'UsuarioExamenService · PreguntasService', 'UsuarioService · PDFConstanciaService (iText + QR)'],
    ['Persistencia: Spring Data JPA + Hibernate', '8 repositorios DAO · 13 entidades JPA', 'Pool de conexiones HikariCP (máx. 30)'],
  ];
  const fills = [C.rojoClaro, C.azulClaro, C.verde, C.oroClaro];
  layers.forEach((l, i) => {
    const y = 290 + i * 128;
    b += box(50, y, 620, 100, fills[i], C.azul, l, { bold: 'first', fs: 15 });
    if (i < 3) b += arrow(360, y + 100, 360, y + 128);
  });
  // BD
  b += arrow(700, 725, 900, 725, 'JDBC (MySQL Connector/J)', { dy: -10 });
  b += `<ellipse cx="1060" cy="660" rx="150" ry="28" fill="${C.azulClaro}" stroke="${C.azul}" stroke-width="2"/>`;
  b += `<path d="M910,660 L910,790 A150,28 0 0 0 1210,790 L1210,660" fill="${C.azulClaro}" stroke="${C.azul}" stroke-width="2"/>`;
  b += `<text x="1060" y="715" font-size="17" font-weight="bold" text-anchor="middle" font-family="Arial">MySQL 5.7</text>`;
  b += `<text x="1060" y="740" font-size="15" text-anchor="middle" font-family="Arial">Esquema mepsi · 13 tablas</text>`;
  b += `<text x="1060" y="762" font-size="15" text-anchor="middle" font-family="Arial">InnoDB · latin1</text>`;
  // Procesos fuera de linea
  b += box(820, 250, 640, 250, C.verde, C.verdeOsc, ['Estación de trabajo DGOAE (procesos fuera de línea, Python 3)', '1. Alta masiva: Excel → pandas → BCrypt → INSERT', '2. Extracción de respuestas (usuario_procesa_datos)', '3. Calificación: claves, escalas, puntuación T y normas', '4. Interpretación por rangos y Excel de resultados', '5. Reporte individual (combinación de correspondencia)', '6. Separación de PDFs por aspirante y carpeta'], { bold: 'first', fs: 15 });
  b += arrow(1060, 500, 1060, 625, 'Túnel SSH (pymysql + sshtunnel)', { dx: 12, anchor: 'start' });
  // Programa posgrado
  b += box(820, 40, 640, 120, C.oroClaro, C.oro, ['Coordinación del programa de posgrado', 'Envía el formato Excel de aspirantes', 'Recibe los reportes individuales en PDF'], { bold: 'first', fs: 15 });
  b += arrow(1060, 160, 1060, 245, 'Correo institucional', { dx: 12, anchor: 'start' });
  b += `<text x="40" y="870" font-size="14" font-family="Arial" fill="${C.gris}">Figura de elaboración propia. Línea continua: flujo en línea; el cuadro verde corre fuera del servidor de aplicaciones.</text>`;
  return svg(W, H, b);
}

// ---------------------------------------------------------------- 2. Entidad-relación
function er() {
  const W = 1500, H = 1010;
  let b = '';
  const T = {};
  function tabla(id, x, y, w, titulo, cols, color) {
    const h = 34 + cols.length * 22 + 8;
    T[id] = { x, y, w, h };
    let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="${C.azul}" stroke-width="1.6"/>`;
    s += `<rect x="${x}" y="${y}" width="${w}" height="32" fill="${color || C.azul}"/>`;
    s += `<text x="${x + w / 2}" y="${y + 22}" font-size="16" font-weight="bold" text-anchor="middle" font-family="Arial" fill="#fff">${esc(titulo)}</text>`;
    cols.forEach((c, i) => {
      const pk = c.startsWith('PK '), fk = c.startsWith('FK ');
      s += `<text x="${x + 10}" y="${y + 54 + i * 22}" font-size="14" font-family="Arial" ${pk ? 'font-weight="bold"' : ''} fill="${fk ? C.rojo : C.negro}">${esc(c)}</text>`;
    });
    return s;
  }
  const azulOsc = C.azul, cat = '#7F6000', res = C.verdeOsc;
  b += tabla('usuario', 40, 40, 300, 'usuario', ['PK id_usuario', 'c_username', 'c_email', 'c_password (BCrypt)', 'b_status'], azulOsc);
  b += tabla('usuariorol', 40, 250, 300, 'usuariorol', ['PK id_usuario_rol', 'FK id_usuario', 'FK id_rol', 'd_creacion'], azulOsc);
  b += tabla('rol', 40, 440, 300, 'rol', ['PK id_rol', 'c_nombreRol', 'b_status'], azulOsc);
  b += tabla('uda', 400, 40, 340, 'usuario_datos_alumno', ['PK/FK id_usuario', 'c_apPaterno, c_apMaterno, c_nombres', 'c_sexo, d_fechaNacimiento', 'c_nacionalidad, c_correo', 'c_num_cuenta', 'c_posgrado_ingresar, c_nivel', 'c_licenciatura, c_posgrado', 'd_creacion, d_modificacion'], azulOsc);
  b += tabla('upd', 400, 300, 340, 'usuario_procesa_datos', ['PK/FK id_usuario', 'datos de identificación', 'c_posgrado_ingresar, c_nivel', 'c_respuestas (8 secciones)', 'b_completo', 'd_creacion, d_modificacion'], res);
  b += tabla('ue', 800, 40, 300, 'usuario_examen', ['PK id_usuario_examen', 'FK id_usuario', 'FK id_examen', 'd_creacion (inicio)', 'd_modificacion'], res);
  b += tabla('ur', 1160, 40, 300, 'usuario_respuesta', ['PK id_respuesta', 'FK id_usuario_examen', 'c_respuesta (cadena)', 'd_creacion (envío)', 'd_modificacion'], res);
  b += tabla('ce', 800, 300, 300, 'cat_examen', ['PK id_examen (1..8)', 'c_nombreExamen', 'b_status'], cat);
  b += tabla('ep', 800, 480, 300, 'examen_pregunta', ['PK id_examen_pregunta', 'FK id_examen', 'c_indice'], cat);
  b += tabla('preg', 600, 700, 300, 'pregunta', ['PK id_pregunta', 'FK id_examen_pregunta', 'FK id_tipo_dato', 'c_pregunta', 'b_status'], cat);
  b += tabla('op', 1000, 700, 300, 'opcion', ['PK id_opcion', 'FK id_examen_pregunta', 'FK id_tipo_dato', 'c_pos_indice, c_opcion', 'n_valor, b_status'], cat);
  b += tabla('pi', 600, 900, 300, 'pregunta_imagen', ['PK/FK id_pregunta, c_nombre_archivo'], cat);
  b += tabla('oi', 1000, 900, 300, 'opcion_imagen', ['PK/FK id_opcion, c_nombre_archivo'], cat);
  b += tabla('td', 1160, 480, 300, 'cat_tipo_dato', ['PK id_tipo_dato', 'c_nombre_dato'], cat);
  // relaciones
  const L = (x1, y1, x2, y2, lab) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${C.gris}" stroke-width="1.8"/>` + (lab ? `<text x="${(x1 + x2) / 2 + 6}" y="${(y1 + y2) / 2 - 5}" font-size="13" font-family="Arial" fill="${C.gris}">${lab}</text>` : '');
  b += L(190, T.usuario.y + T.usuario.h, 190, 250, '1 : N');
  b += L(190, 440, 190, T.usuariorol.y + T.usuariorol.h, 'N : 1');
  b += L(340, 90, 400, 90, '1:1');
  b += L(340, 150, 370, 150) + L(370, 150, 370, 330) + L(370, 330, 400, 330, '');
  b += `<text x="300" y="300" font-size="13" font-family="Arial" fill="${C.gris}"></text>`;
  b += L(340, 70, 360, 70) + L(360, 70, 360, 20) + L(360, 20, 950, 20) + L(950, 20, 950, 40);
  b += `<text x="620" y="15" font-size="13" font-family="Arial" fill="${C.gris}">1 : N (una fila por sección iniciada)</text>`;
  b += L(1100, 90, 1160, 90, '1:1');
  b += L(950, 300, 950, T.ue.y + T.ue.h, 'N : 1');
  b += L(950, T.ce.y + T.ce.h, 950, 480, '1 : N');
  b += L(900, T.ep.y + T.ep.h, 750, 700, '1 : N');
  b += L(1000, T.ep.y + T.ep.h, 1150, 700, '1 : N');
  b += L(750, T.preg.y + T.preg.h, 750, 900, '1:1');
  b += L(1150, T.op.y + T.op.h, 1150, 900, '1:1');
  b += L(1310, T.td.y + T.td.h, 1280, 700, '');
  b += L(1160, 540, 900, 760);
  // leyenda
  const lg = (x, col, t) => `<rect x="${x}" y="975" width="18" height="18" fill="${col}"/><text x="${x + 26}" y="990" font-size="14" font-family="Arial">${t}</text>`;
  b += lg(40, C.azul, 'Usuarios y seguridad') + lg(260, C.verdeOsc, 'Aplicación y respuestas') + lg(520, '#7F6000', 'Banco de reactivos (catálogos)');
  b += `<text x="40" y="960" font-size="13" font-family="Arial" fill="${C.rojo}">FK = llave foránea</text>`;
  return svg(W, H, b);
}

// ---------------------------------------------------------------- 3. Secuencia
function secuencia() {
  const W = 1500, H = 1000;
  const parts = ['Aspirante', 'AngularJS (cuestionario.js)', 'CuestionarioControllerData', 'UsuarioExamenService', 'PreguntasService', 'MySQL (JPA/Hibernate)'];
  const xs = parts.map((_, i) => 120 + i * 252);
  let b = '';
  parts.forEach((p, i) => {
    b += box(xs[i] - 115, 20, 230, 52, i === 0 ? C.oroClaro : (i === 5 ? C.azulClaro : C.verde), C.azul, [p], { bold: true, fs: 14 });
    b += `<line x1="${xs[i]}" y1="72" x2="${xs[i]}" y2="${H - 30}" stroke="#999" stroke-dasharray="5,5"/>`;
  });
  let y = 110;
  const msg = (a, c, t, ret) => { const toLeft0 = c === 0; const s = arrow(xs[a], y, xs[c] + (c > a ? -4 : 4), y, t, { dash: ret, fs: 13, dy: -9, anchor: toLeft0 ? 'start' : 'middle', dx: toLeft0 ? (xs[0]+10-(xs[a]+xs[c])/2) : 0 }); y += 46; return s; };
  const note = (t) => { const s = `<rect x="20" y="${y - 24}" width="1460" height="30" fill="${C.grisClaro}"/><text x="30" y="${y - 4}" font-size="14" font-weight="bold" font-family="Arial" fill="${C.azul}">${esc(t)}</text>`; y += 34; return s; };
  b += note('(a) Apertura de la sección n (1..8)');
  b += msg(0, 1, 'Lee instrucciones y pulsa "Comenzar"');
  b += msg(1, 2, 'GET /cuestionario.dgoae/data/getpreguntas_id_n');
  b += msg(2, 3, 'createUsuarioExamen(n, usuario)');
  b += msg(3, 5, 'SELECT usuario_examen (usuario, sección); si no existe: INSERT');
  b += msg(5, 3, 'id_usuario_examen', true);
  b += msg(2, 3, 'hasRespuestas(id_usuario_examen)');
  b += msg(2, 4, 'listPreguntas(n)  [secciones 3 a 8]');
  b += msg(4, 5, 'SELECT examen_pregunta, pregunta, opcion');
  b += msg(4, 2, 'reactivos con opciones barajadas (Collections.shuffle)', true);
  b += msg(2, 1, 'JSON {hastest, hasanswers, preguntas}', true);
  b += msg(1, 0, 'Si hasanswers: avanza a la siguiente sección; si no: muestra reactivos e inicia timer', true);
  y += 10;
  b += note('(b) Envío de respuestas (al terminar o al agotarse el tiempo)');
  b += msg(1, 2, 'POST /data/saveQuestions {idUsuarioExamen, answers}');
  b += msg(2, 3, 'saveRespuestas(id, usuario, cadena)');
  b += msg(3, 5, 'Si ya hay respuesta: no se inserta (idempotente); si no: INSERT usuario_respuesta');
  b += msg(3, 2, 'true / false', true);
  b += msg(2, 1, '{msj: "Todo bien"}', true);
  b += msg(1, 0, 'Instrucciones de la siguiente sección; al final, comprobante PDF con QR', true);
  return svg(W, Math.max(H, y + 20), b);
}

// ---------------------------------------------------------------- 4. Ciclo de operacion
function ciclo() {
  const W = 1500, H = 720;
  const lanes = ['Programa (de posgrado)', 'DGOAE (scripts Python)', 'MEPSI en línea', 'Aspirante'];
  const cols = [C.oroClaro, C.verde, C.azulClaro, C.rojoClaro];
  let b = '';
  lanes.forEach((l, i) => {
    const y = 20 + i * 170;
    b += `<rect x="20" y="${y}" width="1460" height="160" fill="${cols[i]}" opacity="0.45" stroke="${C.azul}"/>`;
    b += `<rect x="20" y="${y}" width="150" height="160" fill="${C.azul}"/>`;
    b += `<text x="95" y="${y + 85}" font-size="15" font-weight="bold" text-anchor="middle" font-family="Arial" fill="#fff">${esc(l.split(' (')[0])}</text>`;
    if (l.includes('(')) b += `<text x="95" y="${y + 105}" font-size="13" text-anchor="middle" font-family="Arial" fill="#fff">(${esc(l.split(' (')[1])}</text>`;
  });
  const bw = 190, bh = 92;
  const st = (n, lane, x, lines) => box(x, 20 + lane * 170 + 34, bw, bh, '#fff', C.azul, [`${n}. ${lines[0]}`, ...lines.slice(1)], { bold: 'first', fs: 13 });
  b += st(1, 0, 190, ['Formato Excel', 'lista de aspirantes', 'y fecha de aplicación']);
  b += st(2, 1, 420, ['Alta masiva', 'valida, cifra con', 'BCrypt e inserta']);
  b += st(3, 3, 420, ['Recibe usuario', '(correo) y contraseña', '']);
  b += st(4, 2, 650, ['Aplicación', '8 secciones con', 'tiempo controlado']);
  b += st(5, 1, 880, ['Extracción y', 'calificación', 'puntuación T y normas']);
  b += st(6, 1, 1100, ['Reportes', 'combinación de', 'correspondencia + PDF']);
  b += st(7, 0, 1270, ['Recibe resultados', 'PDF por aspirante', 'para su comité']);
  b += st(8, 3, 880, ['Comprobante', 'PDF con QR', '']);
  const y0 = l => 20 + l * 170 + 34 + bh / 2;
  b += arrow(190 + bw, y0(0), 420, y0(1) - 30);
  b += arrow(420 + bw / 2, y0(1) + bh / 2, 420 + bw / 2, y0(3) - bh / 2 - 4);
  b += arrow(420 + bw, y0(3), 650, y0(2) + 20);
  b += arrow(650 + bw, y0(2) - 20, 880, y0(1) + 20);
  b += arrow(650 + bw, y0(2) + 30, 880, y0(3) - 20);
  b += arrow(880 + bw, y0(1), 1100, y0(1));
  b += arrow(1100 + bw / 2, y0(1) - bh / 2, 1270 + 20, y0(0) + bh / 2 - 4);
  return svg(W, H, b);
}

(async () => {
  await render('fig1_arquitectura', arquitectura());
  await render('fig2_er', er());
  await render('fig3_secuencia', secuencia());
  await render('fig4_ciclo', ciclo());
})();
