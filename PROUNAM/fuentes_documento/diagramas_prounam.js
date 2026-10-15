// Diagramas de la propuesta PROUNAM (Prueba 1) como SVG -> PNG
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const OUT = process.argv[2] || 'img_prounam';
fs.mkdirSync(OUT, { recursive: true });

const C = {
  azul: '#1F3864', azulClaro: '#D9E2F3', oro: '#C9A227', oroClaro: '#FFF2CC',
  gris: '#595959', grisClaro: '#F2F2F2', verde: '#E2EFDA', verdeOsc: '#375623',
  rojoClaro: '#FBE5D6', rojo: '#843C0C', negro: '#222222', cafe: '#7F6000', morado: '#E4DFEC', moradoOsc: '#5B3F86',
};
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function box(x, y, w, h, fill, stroke, lines, opts = {}) {
  const fs_ = opts.fs || 15, bold = opts.bold, rx = opts.rx ?? 6;
  let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="${opts.sw || 1.5}" ${opts.dash ? 'stroke-dasharray="8,5"' : ''}/>`;
  const lh = fs_ * 1.3, total = lines.length * lh;
  const ty = opts.top ? y + fs_ + 10 : y + h / 2 - total / 2 + fs_ * 0.95;
  lines.forEach((l, i) => {
    const isB = bold === true || (bold === 'first' && i === 0);
    s += `<text x="${opts.left ? x + 12 : x + w / 2}" y="${ty + i * lh}" font-size="${fs_}" text-anchor="${opts.left ? 'start' : 'middle'}" font-family="Arial" fill="${opts.color || C.negro}" ${isB ? 'font-weight="bold"' : ''}>${esc(l)}</text>`;
  });
  return s;
}
function arrow(x1, y1, x2, y2, label, opts = {}) {
  let s = `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${C.gris}" stroke-width="${opts.sw || 2}" ${opts.dash ? 'stroke-dasharray="7,5"' : ''} marker-end="url(#ah)"/>`;
  if (label) {
    const mx = (x1 + x2) / 2 + (opts.dx || 0), my = (y1 + y2) / 2 + (opts.dy ?? -8);
    s += `<text x="${mx}" y="${my}" font-size="${opts.fs || 13}" text-anchor="${opts.anchor || 'middle'}" font-family="Arial" fill="${C.negro}">${esc(label)}</text>`;
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

// ------------------------------------------------ 1. Arquitectura
function arquitectura() {
  const W = 1500, H = 980;
  let b = '';
  const cl = [['Alumno', 'navegador (casa o plantel)'], ['Orientador', 'DGOAE y planteles'], ['Administrador', 'DGOAE'], ['Público', 'registro, estadísticas']];
  cl.forEach((c, i) => {
    b += box(40 + i * 235, 20, 215, 70, C.oroClaro, C.oro, c, { bold: 'first', fs: 14 });
    b += arrow(147 + i * 235, 90, 147 + i * 235, 150);
  });
  b += `<text x="40" y="128" font-size="13" font-family="Arial" fill="${C.gris}">AngularJS 1.x (SPA por módulo) · HTTPS · JSON</text>`;
  b += `<rect x="20" y="152" width="960" height="760" rx="8" fill="${C.grisClaro}" stroke="${C.azul}" stroke-width="2" stroke-dasharray="8,5"/>`;
  b += `<text x="40" y="180" font-size="17" font-weight="bold" font-family="Arial" fill="${C.azul}">GlassFish 4.1 · Java EE 7 (servidor compartido con MEPSI)</text>`;
  b += box(40, 195, 920, 80, C.rojoClaro, C.azul, ['Spring Security: roles ALUMNO · ORIENTADOR · ADMIN_ALUMNO · ADMIN_ORIENTADOR · ADMIN · TESTER', 'BCrypt · bloqueo a 10 intentos · reCAPTCHA (4 intentos / 4 h) · 1 sesión por usuario · HSTS'], { bold: 'first', fs: 14 });
  const mods = [
    ['Público', 'AnonymousController', 'DataEntityController', '(registro, contraseña,', 'estadísticas)'],
    ['Alumno', 'AlumnoController(Data)', 'ProunamController(Data)', 'RecuperaController(Data)', 'UsuarioController(Data)'],
    ['Orientador', 'OrientadorController', 'OrientadorDataController', '(alumnos del plantel,', 'calificar, PDF)'],
    ['Administración', 'AdminController', 'AdminDataController', '(usuarios, cargas,', 'calificación por plantel)'],
  ];
  mods.forEach((m, i) => { b += box(40 + i * 232, 295, 220, 135, C.azulClaro, C.azul, m, { bold: 'first', fs: 13 }); });
  b += `<text x="40" y="452" font-size="14" font-weight="bold" font-family="Arial" fill="${C.azul}">Spring MVC (controladores JSON)</text>`;
  b += arrow(500, 432, 500, 470);
  b += box(40, 472, 920, 150, C.verde, C.verdeOsc, ['Servicios (44): CalificaPruebas · ProunamExamenGuardar · ProunamMasivo · PDFService', 'Carrera/CarreraAptitud/CarreraInteres · NormaProunam/NormaInvoca · Statics · Sociodemografico · CSV', 'Eventos de Spring (registro, envío de información) → TaskExecutor asíncrono (2 a 30 hilos, cola 60)', 'iText: reporte de resultados y comprobante en PDF'], { bold: 'first', fs: 14 });
  b += arrow(500, 622, 500, 660);
  b += box(40, 662, 920, 110, C.oroClaro, C.azul, ['Persistencia: Spring Data JPA + Hibernate', '66 repositorios DAO · 70 entidades (52 + 18 catálogos) · consultas derivadas y @Query', 'Pool HikariCP (máx. 30 conexiones)'], { bold: 'first', fs: 14 });
  b += box(40, 800, 920, 90, '#fff', C.gris, ['Recursos estáticos: imágenes de reactivos (figuras, ensamble, mecánica), CSS, JS', 'Vistas JSP parciales por subprueba (instrucciones y reactivos)'], { fs: 13 });
  // BD
  b += arrow(960, 717, 1110, 717, 'JDBC', { dy: -8 });
  b += `<ellipse cx="1270" cy="650" rx="150" ry="28" fill="${C.azulClaro}" stroke="${C.azul}" stroke-width="2"/>`;
  b += `<path d="M1120,650 L1120,790 A150,28 0 0 0 1420,790 L1420,650" fill="${C.azulClaro}" stroke="${C.azul}" stroke-width="2"/>`;
  b += `<text x="1270" y="705" font-size="17" font-weight="bold" text-anchor="middle" font-family="Arial">MySQL 5.7</text>`;
  b += `<text x="1270" y="730" font-size="15" text-anchor="middle" font-family="Arial">Esquema portaloae</text>`;
  b += `<text x="1270" y="752" font-size="15" text-anchor="middle" font-family="Arial">~75 tablas · ~1.8 GB · UTF-8</text>`;
  // correo
  b += box(1080, 420, 380, 90, C.morado, C.moradoOsc, ['Servidor de correo (SMTP)', 'confirmación de registro, contraseña,', 'envío del reporte en PDF'], { bold: 'first', fs: 14 });
  b += arrow(960, 560, 1075, 480, 'asíncrono', { dy: 18 });
  // JMeter
  b += box(1080, 200, 380, 120, C.grisClaro, C.gris, ['Pruebas de carga (Apache JMeter)', 'plan POEMeter.jmx parametrizado', '(servidor, usuarios, rampa)', '700 usuarios concurrentes'], { bold: 'first', fs: 14, dash: true });
  b += arrow(1080, 260, 985, 260, '', {});
  b += `<text x="40" y="945" font-size="13" font-family="Arial" fill="${C.gris}">Figura de elaboración propia a partir del código fuente del Portal de Orientación (poe_2022).</text>`;
  return svg(W, H, b);
}

// ------------------------------------------------ 2. Modelo de datos por grupos
function datos() {
  const W = 1500, H = 900;
  let b = '';
  const grp = (x, y, w, h, titulo, color, filas, plain) => {
    let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#fff" stroke="${color}" stroke-width="2"/>`;
    s += `<rect x="${x}" y="${y}" width="${w}" height="34" rx="6" fill="${color}"/>`;
    s += `<text x="${x + w / 2}" y="${y + 23}" font-size="16" font-weight="bold" text-anchor="middle" font-family="Arial" fill="#fff">${esc(titulo)}</text>`;
    filas.forEach((f, i) => { s += `<text x="${x + 12}" y="${y + 58 + i * 22}" font-size="14" font-family="Arial" ${(f.startsWith('•') || f.startsWith(' ') || plain) ? '' : 'font-weight="bold"'}>${esc(f)}</text>`; });
    return s;
  };
  b += grp(30, 30, 440, 330, '1. Usuarios y perfil', C.azul, ['usuario (credenciales BCrypt, estado)', 'usuario_rol → cat_rol', '• usuario_datos_personales', '• usuario_datos_academicos → carrera_facultad', '• usuario_datos_domiciliares', '• usuario_no_institucion_unam', '• usuario_aviso_privacidad', '• usuario_sociodemografico(_renglon)', '• datos_orientador · usuario_orientador_facultad', '• admin_bitacora · orientador_bitacora', '• alumno_bitacora_resultados']);
  b += grp(530, 30, 440, 250, '2. Banco de reactivos', C.cafe, ['cat_examen (PROUNAM, INVOCA, …)', 'cat_parte · cat_seccion (9 subpruebas)', 'examen_pregunta (c_indice)', '• pregunta (+ pregunta_imagen)', '• opcion (n_valor) (+ opcion_imagen)', '• cat_tipo_dato', '• prounam_eps (total de reactivos)']);
  b += grp(1030, 30, 440, 250, '3. Acceso y aplicación', C.verdeOsc, ['cat_codigo (código del mes)', 'usuario_examen_permisos', 'usuario_examen (subprueba presentada)', 'usuario_respuesta_renglon', '  (cadena de respuestas, b_calificado)']);
  b += grp(530, 400, 440, 300, '4. Resultados', C.rojo, ['usuario_resultado_prounam (aciertos)', 'usuario_resultado_invoca (puntaje)', 'usuario_tt_prounam (estandarizado)', 'usuario_tt_invoca (estandarizado)', '• norma_prounam · norma_invoca(_b)', '• cat_resultado_prounam (11 escalas)', '• cat_resultado_invoca (14 escalas)', '• *_historico (aplicaciones previas)']);
  b += grp(1030, 400, 440, 300, '5. Orientación profesional', C.moradoOsc, ['cat_carrera (517 activas)', 'cat_escuela_facultad · carrera_facultad', 'cat_area · area_carrera', 'carrera_aptitudes (133 carreras)', 'carrera_intereses (133 carreras)', 'carrera_url (información, alta demanda)']);
  b += grp(30, 400, 440, 300, 'Volumen (oct-2026)', C.gris, ['• 255 mil cuentas de alumno', '• 1.7 millones de subpruebas', '  guardadas (usuario_examen)', '• 1.9 millones de resultados PROUNAM', '• 2.4 millones de resultados INVOCA', '• 195 mil cuestionarios', '  sociodemográficos', '• ≈ 1.8 GB en total'], true);
  b += `<polyline points="470,330 1180,330 1180,288" fill="none" stroke="${C.gris}" stroke-width="2" marker-end="url(#ah)"/>`;
  b += `<text x="520" y="322" font-size="13" font-family="Arial">el alumno presenta</text>`;
  b += arrow(970, 160, 1025, 160);
  b += arrow(1360, 280, 975, 470, 'calificación', { dy: -12 });
  b += arrow(970, 560, 1025, 560, '', {});
  b += `<text x="998" y="600" font-size="13" text-anchor="middle" font-family="Arial">aptitudes</text><text x="998" y="616" font-size="13" text-anchor="middle" font-family="Arial">× intereses</text>`;
  b += arrow(750, 280, 750, 395, 'claves y valores', { dx: 10, dy: 40, anchor: 'start' });
  b += `<text x="30" y="760" font-size="14" font-family="Arial" fill="${C.gris}">Negritas: tablas principales de cada grupo; • tablas de apoyo. Flechas: dependencias funcionales entre grupos.</text>`;
  return svg(W, 790, b);
}

// ------------------------------------------------ 3. Secuencia: aplicación y calificación
function secuencia() {
  const W = 1500;
  const parts = ['Alumno', 'AngularJS', 'ProunamDataController', 'ProunamExamenGuardar', 'CalificaPruebas', 'MySQL'];
  const xs = parts.map((_, i) => 120 + i * 252);
  let b = '', y = 110;
  parts.forEach((p, i) => {
    b += box(xs[i] - 115, 20, 230, 52, i === 0 ? C.oroClaro : (i === 5 ? C.azulClaro : C.verde), C.azul, [p], { bold: true, fs: 14 });
  });
  const msg = (a, c, t, ret) => { const toLeft0 = c === 0; const s = arrow(xs[a], y, xs[c] + (c > a ? -4 : 4), y, t, { dash: ret, fs: 13, dy: -9, anchor: toLeft0 ? 'start' : 'middle', dx: toLeft0 ? (xs[0] + 10 - (xs[a] + xs[c]) / 2) : 0 }); y += 44; return s; };
  const note = t => { const s = `<rect x="20" y="${y - 24}" width="1460" height="30" fill="${C.grisClaro}"/><text x="30" y="${y - 4}" font-size="14" font-weight="bold" font-family="Arial" fill="${C.azul}">${esc(t)}</text>`; y += 34; return s; };
  b += note('(a) Presentación de una subprueba (se repite para las 9 subpruebas y el INVOCA)');
  b += msg(1, 2, 'GET /getExamenByIds/ide/1/idp/1/ids/{n}');
  b += msg(2, 5, '¿existe usuario_examen para esta subprueba?');
  b += msg(2, 1, 'si existe: {next: true} → pasa a la siguiente; si no: reactivos e imágenes', true);
  b += msg(1, 0, 'cronómetro de la subprueba (p. ej. 3, 7, 20 o 25 min)', true);
  b += msg(1, 2, 'POST /saveProunamAnswersByExamenIdInRow {acrónimo, cadena}');
  b += msg(2, 3, 'guardar renglón');
  b += msg(3, 5, 'INSERT usuario_examen + usuario_respuesta_renglon (b_calificado = 0)');
  y += 8;
  b += note('(b) Calificación (por alumno desde el orientador, o por plantel desde administración)');
  b += msg(2, 4, 'calificarUnAlumno(u)');
  b += msg(4, 5, 'sumaAciertos: compara cada carácter con opcion.n_valor → usuario_resultado_*');
  b += msg(4, 5, 'sumaPAyVP: potencial académico y velocidad perceptual');
  b += msg(4, 5, 'calificaPROUNAM / calificaINVOCA: (x − media) / DE × 15 + 50 → usuario_tt_*');
  b += msg(4, 5, 'marca b_calificado = 1 (no se recalifica dos veces)');
  y += 8;
  b += note('(c) Consulta de resultados por el alumno');
  b += msg(1, 2, 'POST /alumnoResultados · POST /getPreCarrers');
  b += msg(2, 5, '3 aptitudes y 3 intereses más altos × carrera_aptitudes / carrera_intereses');
  b += msg(2, 1, 'perfil + hasta 20 carreras sugeridas (área, información, alta demanda)', true);
  b += msg(1, 0, 'pantalla de resultados · PDF (iText) · envío por correo', true);
  parts.forEach((p, i) => { b = `<line x1="${xs[i]}" y1="72" x2="${xs[i]}" y2="${y}" stroke="#999" stroke-dasharray="5,5"/>` + b; });
  return svg(W, y + 10, b);
}

// ------------------------------------------------ 4. Ciclo de operación
function ciclo() {
  const W = 1500, H = 760;
  const lanes = ['Orientador (DGOAE / plantel)', 'Alumno', 'Portal (en línea)', 'DGOAE (administración)'];
  const cols = [C.oroClaro, C.rojoClaro, C.azulClaro, C.verde];
  let b = '';
  lanes.forEach((l, i) => {
    const y = 60 + i * 170;
    b += `<rect x="20" y="${y}" width="1460" height="160" fill="${cols[i]}" opacity="0.45" stroke="${C.azul}"/>`;
    b += `<rect x="20" y="${y}" width="150" height="160" fill="${C.azul}"/>`;
    const [a, c] = l.split(' (');
    b += `<text x="95" y="${y + 80}" font-size="15" font-weight="bold" text-anchor="middle" font-family="Arial" fill="#fff">${esc(a)}</text>`;
    if (c) b += `<text x="95" y="${y + 100}" font-size="12" text-anchor="middle" font-family="Arial" fill="#fff">(${esc(c)}</text>`;
  });
  b += `<text x="190" y="35" font-size="15" font-family="Arial" fill="${C.azul}" font-weight="bold">Modalidad masiva: CCH (enero y febrero, 5 planteles) y ENP (octubre y noviembre, 9 planteles) · Modalidad bajo demanda: todo el año</text>`;
  const bw = 180, bh = 96;
  const st = (n, lane, x, lines) => box(x, 60 + lane * 170 + 32, bw, bh, '#fff', C.azul, [`${n}. ${lines[0]}`, ...lines.slice(1)], { bold: 'first', fs: 13 });
  const cy = l => 60 + l * 170 + 32 + bh / 2;
  b += st(1, 0, 190, ['Convoca o asesora', 'jornada por plantel', 'o cita individual']);
  b += st(2, 1, 390, ['Autorregistro', 'confirmación por', 'correo y datos']);
  b += st(3, 1, 590, ['Código de acceso', 'del mes (cuando', 'está activo)']);
  b += st(4, 2, 790, ['9 subpruebas', '+ INVOCA', 'con cronómetro']);
  b += st(5, 3, 790, ['Calificación', 'por plantel', '(lote)']);
  b += st(6, 0, 990, ['Calificación', 'individual y', 'consulta']);
  b += st(7, 2, 1100, ['Normas y', 'sugerencia de', 'carreras']);
  b += st(8, 1, 1290, ['Resultados', 'pantalla · PDF', '· correo']);
  b += st(9, 0, 1290, ['Entrevista de', 'orientación con', 'los resultados']);
  b += arrow(370, cy(0) + 20, 395, cy(1) - 30);
  b += arrow(570, cy(1), 590, cy(1));
  b += arrow(770, cy(1) + 20, 800, cy(2) - 40);
  b += arrow(880, cy(2) + bh / 2, 880, cy(3) - bh / 2 - 4);
  b += arrow(970, cy(2) - 30, 1000, cy(0) + 40);
  b += arrow(970, cy(3) - 20, 1105, cy(2) + 30);
  b += arrow(1170, cy(0) + 30, 1180, cy(2) - bh / 2 - 4);
  b += arrow(1280, cy(2) - 20, 1300, cy(1) + 30);
  b += arrow(1380, cy(1) - bh / 2, 1380, cy(0) + bh / 2 + 4);
  return svg(W, H, b);
}

// ------------------------------------------------ 5. Aplicaciones por año (gráfica)
function grafica() {
  const W = 1500, H = 640;
  const d = [['2019', 24790, 'papel*'], ['2020', 26606], ['2021', 26045], ['2022', 10811], ['2023', 33155], ['2024', 30898], ['2025', 31598], ['2026', 18966, 'parcial']];
  const x0 = 120, y0 = 540, h = 440, max = 35000, bw = 120;
  let b = '';
  [0, 10000, 20000, 30000].forEach(v => {
    const y = y0 - v / max * h;
    b += `<line x1="${x0}" y1="${y}" x2="1440" y2="${y}" stroke="#ddd"/>`;
    b += `<text x="${x0 - 12}" y="${y + 5}" font-size="16" text-anchor="end" font-family="Arial" fill="${C.gris}">${v.toLocaleString('en-US')}</text>`;
  });
  d.forEach((r, i) => {
    const x = x0 + 40 + i * (bw + 40), bh = r[1] / max * h;
    const col = r[2] === 'papel*' ? '#A6A6A6' : (r[2] === 'parcial' ? '#8EA9DB' : C.azul);
    b += `<rect x="${x}" y="${y0 - bh}" width="${bw}" height="${bh}" fill="${col}"/>`;
    b += `<text x="${x + bw / 2}" y="${y0 - bh - 10}" font-size="17" font-weight="bold" text-anchor="middle" font-family="Arial">${r[1].toLocaleString('en-US')}</text>`;
    b += `<text x="${x + bw / 2}" y="${y0 + 26}" font-size="17" text-anchor="middle" font-family="Arial">${r[0]}</text>`;
    if (r[2]) b += `<text x="${x + bw / 2}" y="${y0 + 48}" font-size="14" text-anchor="middle" font-family="Arial" fill="${C.gris}">${r[2]}</text>`;
  });
  b += `<line x1="${x0}" y1="${y0}" x2="1440" y2="${y0}" stroke="${C.gris}" stroke-width="1.5"/>`;
  b += `<text x="${x0}" y="40" font-size="18" font-weight="bold" font-family="Arial" fill="${C.azul}">Alumnos con PROUNAM II calificado por año (total 2019-2026: 202,869)</text>`;
  b += `<text x="${x0}" y="615" font-size="14" font-family="Arial" fill="${C.gris}">* 2019: última aplicación en papel, integrada al portal por carga de lectura óptica. 2026: datos a octubre (falta el periodo de la ENP).</text>`;
  return svg(W, H, b);
}

(async () => {
  await render('fig1_arquitectura', arquitectura());
  await render('fig2_datos', datos());
  await render('fig3_secuencia', secuencia());
  await render('fig4_ciclo', ciclo());
  await render('fig5_aplicaciones', grafica());
})();
