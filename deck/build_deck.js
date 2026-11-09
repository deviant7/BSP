// Presentation deck for the BS project, in the format of the reference decks (consulting style, 4:3).
// Run: node deck/build_deck.js   (needs deck/figs/*.png from analysis/deck_figures.py)
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const SKILL = "/root/.claude/skills/synced/e0a82d13-199d-48ef-a456-82ceb3895c04_a2b91922-6749-493b-b7fd-5638ecdae803/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));

const ROOT = path.resolve(__dirname, "..");
const FIG = path.join(__dirname, "figs");
const OUT = path.join(ROOT, "BSP_Presentation_Nov2026.pptx");

const THEME = {
  name: "BSP Consulting",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "254780", lt2: "E6E6E6",
    accent1: "00A3E8", accent2: "254780", accent3: "6A93B0", accent4: "0B1F33", accent5: "2D6DD8", accent6: "FFF2B3",
    hlink: "2D6DD8", folHlink: "6A93B0",
  },
};
const HEX = { navy: "254780", blue: "00A3E8", mid: "1F6FB4", steel: "6A93B0", black: "0B1F33", grey: "4D4D4D",
  panel: "E6E6E6", light: "DDF0FA", yellow: "FFF2B3", link: "2D6DD8", rule: "254780", rule2: "4F81D6" };

const pres = new pptxgen();
pres.layout = "LAYOUT_4x3";           // 10 x 7.5 in, as the reference decks
pres.author = "Prince Kumar";
pres.title = "Limits to Arbitrage in the Indian Equity Market";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ------------------------------------------------------------------ layouts
const LOGO = path.join(ROOT, "thesis", "Images", "iitb_logo.png");
pres.defineSlideMaster({
  title: "TITLE",
  background: { color: "FFFFFF" },
  objects: [
    { image: { x: 0.55, y: 0.45, w: 0.95, h: 0.93, path: LOGO } },
    { placeholder: { options: { name: "title", type: "title", x: 0.55, y: 2.45, w: 8.6, h: 0.6, fontSize: 30, bold: true, color: "4D4D4D", fontFace: "Arial", align: "left", valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "sub", type: "body", x: 0.55, y: 3.05, w: 8.6, h: 0.55, fontSize: 24, color: "4D4D4D", fontFace: "Arial", valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "date", type: "body", x: 0.55, y: 4.35, w: 6, h: 0.4, fontSize: 16, color: "4D4D4D", fontFace: "Arial", margin: 0 }, text: "" } },
    { rect: { x: 0.08, y: 5.15, w: 9.84, h: 1.55, fill: { color: HEX.navy }, line: { color: HEX.navy } } },
    { placeholder: { options: { name: "band", type: "body", x: 0.4, y: 5.25, w: 9.2, h: 1.35, fontSize: 22, bold: true, color: "FFFFFF", fontFace: "Arial", align: "center", valign: "middle", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "DIVIDER",
  background: { color: "FFFFFF" },
  objects: [
    { text: { text: "Agenda", options: { x: 0.55, y: 0.72, w: 6, h: 0.5, fontSize: 24, bold: true, color: HEX.navy, fontFace: "Arial", margin: 0 } } },
    { line: { x: 0.12, y: 1.25, w: 9.76, h: 0, line: { color: HEX.rule, width: 2.5 } } },
    { line: { x: 0.12, y: 1.29, w: 9.76, h: 0, line: { color: HEX.rule2, width: 0.75 } } },
    { rect: { x: 0.12, y: 3.45, w: 9.76, h: 0.62, fill: { color: HEX.navy }, line: { color: HEX.navy } } },
    { placeholder: { options: { name: "section", type: "body", x: 0.45, y: 3.45, w: 9.0, h: 0.62, fontSize: 20, bold: true, color: "FFFFFF", fontFace: "Arial", valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 9.15, y: 7.0, w: 0.5, h: 0.25, fontSize: 9, color: "000000", fontFace: "Arial", align: "right" },
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "tracker", type: "body", x: 0.55, y: 0.3, w: 7, h: 0.25, fontSize: 12, color: "4D4D4D", fontFace: "Arial", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.55, y: 0.56, w: 9.0, h: 0.45, fontSize: 24, bold: true, color: HEX.navy, fontFace: "Arial", align: "left", valign: "middle", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "sub", type: "body", x: 0.55, y: 1.0, w: 9.0, h: 0.33, fontSize: 15, color: HEX.navy, fontFace: "Arial", align: "left", valign: "middle", margin: 0 }, text: "" } },
    { line: { x: 0.12, y: 1.4, w: 9.76, h: 0, line: { color: HEX.rule, width: 2.5 } } },
    { line: { x: 0.12, y: 1.44, w: 9.76, h: 0, line: { color: HEX.rule2, width: 0.75 } } },
    { placeholder: { options: { name: "source", type: "body", x: 0.55, y: 7.0, w: 8.2, h: 0.25, fontSize: 8, color: "000000", fontFace: "Arial", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 9.15, y: 7.0, w: 0.5, h: 0.25, fontSize: 9, color: "000000", fontFace: "Arial", align: "right" },
});

// ------------------------------------------------------------------ helpers
function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}
function fig(slide, name, x, y, w, h, alt) {
  const f = path.join(FIG, name + ".png");
  const s = pngSize(f);
  const r = Math.min(w / s.w, h / s.h);
  const iw = s.w * r, ih = s.h * r;
  slide.addImage({ path: f, x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih, altText: alt || name });
}
let SECTION = "";
function content(tracker, title, sub, source, notes) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: SECTION });
  if (tracker) s.addText(tracker, { placeholder: "tracker" });
  s.addText(title, { placeholder: "title" });
  if (sub) s.addText(sub, { placeholder: "sub" });
  s.addText(source || "Source: NSE archives; author's analysis", { placeholder: "source" });
  if (notes) s.addNotes(notes);
  return s;
}
function divider(name) {
  SECTION = name;
  pres.addSection({ title: name });
  const s = pres.addSlide({ masterName: "DIVIDER", sectionTitle: SECTION });
  s.addText(name, { placeholder: "section" });
  return s;
}
function callout(s, text, y = 6.18) {
  s.addText(text, { x: 1.4, y, w: 7.2, h: 0.55, fontSize: 13, bold: true, color: "000000", align: "center", valign: "middle",
    fill: { color: HEX.yellow }, line: { color: "000000", width: 0.75 }, margin: 4, isTextBox: true, objectName: "callout" });
}
function panelHeader(s, text, x, y, w, h = 0.5) {
  s.addText(text, { x, y, w, h, fontSize: 12, bold: true, color: "000000", align: "center", valign: "bottom", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: x + 0.05, y: y + h + 0.05, w: w - 0.1, h: 0, line: { color: HEX.navy, width: 1.5 } });
}
function chevron(s, x, y) {
  s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x, y, w: 0.6, h: 0.3, rotate: 90, fill: { color: "BFBFBF" }, line: { color: "BFBFBF" } });
}
function bullets(items, size = 12) {
  return items.map((it, i) => {
    const runs = Array.isArray(it) ? it : [{ text: it }];
    return runs.map((r, j) => ({ text: r.text, options: Object.assign({ fontSize: size, color: "000000",
      bullet: j === 0 ? { indent: 12 } : undefined, paraSpaceAfter: j === runs.length - 1 ? 9 : 0,
      breakLine: j === runs.length - 1 && i < items.length - 1 }, r.b ? { bold: true } : {}, r.blue ? { bold: true, color: HEX.link } : {}) }));
  }).flat();
}
function textPanel(s, header, items, x, y, w, h, size = 12) {
  panelHeader(s, header, x, y, w, 0.3);
  s.addText(bullets(items, size), { x, y: y + 0.48, w, h: h - 0.48, valign: "top", margin: [2, 2, 2, 4], isTextBox: true });
}
function defRows(s, rows, x, y, w, rowH, gap = 0.1, labelW = 1.3, size = 11) {
  rows.forEach((r, i) => {
    const yy = y + i * (rowH + gap);
    s.addText(r[0], { x, y: yy, w: labelW, h: rowH, fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle",
      fill: { color: HEX.navy }, line: { color: HEX.navy }, margin: 3, isTextBox: true });
    s.addText(bullets(r[1], size), { x: x + labelW, y: yy, w: w - labelW, h: rowH, valign: "middle", fill: { color: HEX.panel },
      line: { color: HEX.panel }, margin: [3, 6, 3, 8], isTextBox: true });
  });
}
function twoPanels(s, lh, lfig, rh, rfig, top = 1.62) {
  panelHeader(s, lh, 0.45, top, 4.4);
  panelHeader(s, rh, 5.15, top, 4.4);
  fig(s, lfig, 0.45, top + 0.65, 4.4, 5.95 - top - 0.65);
  fig(s, rfig, 5.15, top + 0.65, 4.4, 5.95 - top - 0.65);
}
function chartAndPanel(s, figName, header, items, figW = 5.6) {
  fig(s, figName, 0.4, 1.65, figW, 4.3);
  chevron(s, 0.4 + figW + 0.02, 3.6);
  textPanel(s, header, items, 0.4 + figW + 0.55, 1.75, 9.6 - (0.4 + figW + 0.55), 4.2, 11.5);
}
const TBL_H = { bold: true, color: "FFFFFF", fill: { color: HEX.mid }, fontSize: 11, align: "center", valign: "middle" };
function tbl(s, header, rows, x, y, w, colW, opt = {}) {
  const data = [header.map((h) => ({ text: h, options: TBL_H }))];
  rows.forEach((r, i) => data.push(r.map((c, j) => {
    const o = { fontSize: opt.size || 10.5, color: "000000", valign: "middle", fill: { color: i % 2 ? "FFFFFF" : HEX.light } };
    if (j === 0) { o.bold = true; o.color = HEX.navy; }
    if (typeof c === "object") return { text: c.text, options: Object.assign(o, c.o || {}) };
    return { text: c, options: o };
  })));
  s.addTable(data, { x, y, w, colW, border: { type: "solid", pt: 0.5, color: "8EA9C1" }, margin: [3, 5, 3, 5], rowH: opt.rowH || 0.32 });
}

// ------------------------------------------------------------------ 1. title and agenda
SECTION = "Opening";
pres.addSection({ title: "Opening" });
let s = pres.addSlide({ masterName: "TITLE", sectionTitle: SECTION });
s.addText("Limits to arbitrage in Indian equities", { placeholder: "title" });
s.addText("BS project presentation (EC 495)", { placeholder: "sub" });
s.addText("November 2026", { placeholder: "date" });
s.addText([{ text: "Prince Kumar (23B3032)", options: { breakLine: true } },
  { text: "Guide: Prof. Aditi Chaubal, Department of Economics, IIT Bombay", options: { fontSize: 13, bold: false } }], { placeholder: "band" });
s.addNotes("Title. The project asks how strongly limits to arbitrage bind in Indian equities, using India's F&O ban as the sharpest lens.");

s = pres.addSlide({ masterName: "CONTENT", sectionTitle: SECTION });
s.addText("Agenda", { placeholder: "title" });
s.addText("Executive summary", { x: 0.55, y: 1.72, w: 8.8, h: 0.35, fontSize: 18, bold: true, color: HEX.navy, margin: 0, isTextBox: true });
const agenda = [
  ["The question and our approach", "Why India, how the F&O ban works, the model and the frozen test plan"],
  ["The F&O ban", "Trading, correction and the level of the basis when a ban starts"],
  ["The band: costs, capital and position limits", "How wide the band is and what moves it"],
  ["Short-sale constraints", "F&O entry and a constraint index for every listed stock"],
  ["Conclusion and policy", ""],
];
agenda.forEach((a, i) => {
  const y = 2.32 + i * 0.78;
  s.addText(a[0], { x: 0.55, y, w: 8.8, h: 0.33, fontSize: 18, bold: true, color: HEX.navy, margin: 0, isTextBox: true });
  if (a[1]) s.addText([{ text: a[1], options: { bullet: { indent: 14 } } }], { x: 0.55, y: y + 0.33, w: 8.8, h: 0.3, fontSize: 14, color: HEX.navy, margin: 0, isTextBox: true });
});
s.addText(" ", { placeholder: "source" });

// ------------------------------------------------------------------ 2. executive summary
divider("Executive summary");
s = content("Executive summary", "Executive summary", null, "Source: NSE archives, 2010 to 2026; author's analysis",
  "Five messages. Trading effects are large and clean; price effects are real but not the textbook one-sided channel.");
s.addText("Limits to arbitrage bind hard on trading in Indian equities. On prices they bind less, and differently, than the textbook channel predicts.",
  { x: 0.55, y: 1.65, w: 8.9, h: 0.6, fontSize: 13, bold: true, color: "000000", margin: 0, isTextBox: true });
const exec = [
  [{ text: "Bans bind on trading. ", b: true }, { text: "In a ban, futures volume falls by about two log points. Once violations were judged on intraday positions (from March 2020), every futures trade in a ban closed positions." }],
  [{ text: "Correction is not one-sided as predicted. ", b: true }, { text: "Rich futures revert faster in a ban, mostly in its first days, and the basis falls about 6 bp when a ban starts before recovering within a week. Neither appears at false ban dates." }],
  [{ text: "Costs shape a wide band; capital leaves weak traces. ", b: true }, { text: "The basis moves in a band of about -35 to +24 bp; a new cash-and-carry round trip (27 to 31 bp) lies in its outer tail. Inflows to arbitrage funds go with a lower upper tail, weakly." }],
  [{ text: "Short-sale access speeds price adjustment. ", b: true }, { text: "After a stock enters the F&O segment its price delay falls by 0.11. A constraint index built from frictions predicts slower adjustment across all stocks, also after a size control." }],
  [{ text: "The 2025 reform met its aim. ", b: true }, { text: "Against the old rule applied to the same stocks, the October 2025 rules cut ban days by about three quarters." }],
];
s.addText(bullets(exec, 13), { x: 0.6, y: 2.45, w: 8.85, h: 4.3, valign: "top", margin: 0, isTextBox: true });

s = content("Executive summary", "Three of four primary tests hold as specified",
  "The four pre-specified primary hypotheses, corrected jointly (Holm, 5%)", null,
  "The primary family was fixed in advance. H7 failed with the opposite sign and is reported in full.");
tbl(s, ["Hypothesis", "Prediction", "Result", "Holm p", "Verdict"], [
  ["H8 Trading in a ban", "Futures volume falls; trades only close positions", "-2.00 log points (s.e. 0.11)", "7e-41", { text: "Supported", o: { bold: true, color: HEX.mid } }],
  ["H3 Costs and the band", "Upper edge rises with each tax increase", "+6.96 bp (s.e. 0.61); weak against placebos", "6e-24", { text: "Supported", o: { bold: true, color: HEX.mid } }],
  ["H6 Short-sale access", "F&O entry lowers delay and bad-news drift", "Delay -0.109 (s.e. 0.023); drift the other way", "1e-5", { text: "Supported (delay)", o: { bold: true, color: HEX.mid } }],
  ["H7 One-sided correction", "Rich futures revert more slowly in a ban", "-0.089 (s.e. 0.037): faster, not slower", "1", { text: "Rejected", o: { bold: true, color: "C0504D" } }],
], 0.45, 1.75, 9.1, [2.0, 2.45, 2.55, 0.8, 1.3], { rowH: 0.62, size: 11 });
s.addText(bullets([
  [{ text: "Ten secondary tests ", b: true }, { text: "were reported without adjustment and read as a pattern; three are below 0.05." }],
  [{ text: "Every detail the plan left open ", b: true }, { text: "was fixed in a dated log before the test that needed it." }],
], 12), { x: 0.6, y: 4.95, w: 8.8, h: 0.9, valign: "top", margin: 0, isTextBox: true });
callout(s, "The failed prediction is reported in full: rich futures revert faster in a ban");

// ------------------------------------------------------------------ 3. question and approach
divider("The question and our approach");
s = content("The question and our approach", "India changes almost every limit on a known date",
  "Futures STT, ban enforcement, the position-limit rule and arbitrage capital, 2015 to 2026",
  "Source: SEBI circulars and press releases; NSE circulars; AMFI", "Dated rule changes are what make each limit measurable.");
fig(s, "fig_timeline", 0.45, 1.7, 9.1, 4.2);
callout(s, "Dated rule changes let us measure each limit instead of assuming it");

s = content("The question and our approach", "The F&O ban lets every trader only reduce positions",
  "Utilisation of the position limit for SAIL, the most-banned stock, January to June 2024", null,
  "The ban binds everyone, not only arbitrageurs. That is what makes it different from a cap on one trader.");
chartAndPanel(s, "fig_util_example", "How the rule works", [
  [{ text: "Enter ", b: true }, { text: "the day after open interest exceeds 95% of the market-wide position limit" }],
  [{ text: "Leave ", b: true }, { text: "after it falls to 80%" }],
  [{ text: "In between, everyone ", b: true }, { text: "may only reduce positions, in all expiries" }],
  [{ text: "1,788 spells ", blue: true }, { text: "in 141 stocks, 2015 to October 2026" }],
]);
callout(s, "To my knowledge, no study had estimated what this rule does to prices");

s = content("The question and our approach", "We fixed the tests before looking at outcomes",
  "The five safeguards of the project", null, "Order of work: model, frozen plan, blind data, estimator tests, full reporting.");
s.addText("What we did", { x: 2.75, y: 1.62, w: 4.0, h: 0.3, fontSize: 12, bold: true, align: "center", margin: 0, isTextBox: true });
s.addText("Why", { x: 6.95, y: 1.62, w: 2.6, h: 0.3, fontSize: 12, bold: true, align: "center", margin: 0, isTextBox: true });
s.addShape(pres.shapes.LINE, { x: 2.8, y: 1.95, w: 3.9, h: 0, line: { color: HEX.navy, width: 1.5 } });
s.addShape(pres.shapes.LINE, { x: 7.0, y: 1.95, w: 2.5, h: 0, line: { color: HEX.navy, width: 1.5 } });
const steps = [
  ["Model", [{ text: "One model; " }, { text: "every limit a parameter", blue: true }, { text: "; each prediction with what would contradict it" }], "Hypotheses are derived, not fitted"],
  ["Frozen plan", [{ text: "Tests and signs " }, { text: "fixed with a git time stamp", blue: true }, { text: " on 5 November 2026" }], "No choosing specifications after seeing results"],
  ["Blind data", [{ text: "Built from " }, { text: "public NSE files", blue: true }, { text: "; treatment and outcome code kept apart" }], "No peeking while the data are built"],
  ["Estimator tests", [{ text: "Each estimator " }, { text: "recovers known effects", blue: true }, { text: " on simulated data" }], "Methods checked before real data"],
  ["Full reporting", [{ text: "Primary family " }, { text: "Holm-corrected", blue: true }, { text: "; nulls and contradictions kept" }], "The failed prediction stays in"],
];
steps.forEach((r, i) => {
  const y = 2.1 + i * 0.78;
  s.addShape(pres.shapes.OVAL, { x: 0.3, y: y - 0.08, w: 0.3, h: 0.3, fill: { color: HEX.navy }, line: { color: "FFFFFF", width: 1 } });
  s.addText(String(i + 1), { x: 0.3, y: y - 0.08, w: 0.3, h: 0.3, fontSize: 11, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText(r[0], { x: 0.7, y, w: 1.85, h: 0.62, fontSize: 13, bold: true, align: "center", valign: "middle", fill: { color: HEX.panel }, line: { color: HEX.panel }, margin: 2, isTextBox: true });
  s.addText(r[1].map((t) => ({ text: t.text, options: Object.assign({ fontSize: 12, color: "000000" }, t.blue ? { bold: true, color: HEX.link } : {}) })),
    { x: 2.75, y, w: 4.0, h: 0.62, valign: "middle", margin: 2, isTextBox: true });
  s.addText(r[2], { x: 6.95, y, w: 2.6, h: 0.62, fontSize: 12, valign: "middle", margin: 2, isTextBox: true });
  if (i < steps.length - 1) s.addShape(pres.shapes.LINE, { x: 2.75, y: y + 0.7, w: 6.8, h: 0, line: { color: "BFBFBF", width: 0.75, dashType: "dash" } });
});

s = content("The question and our approach", "Costs set the band; a ban blocks two things",
  "Equilibrium basis against the demand pressure of outside traders, with illustrative costs",
  "Source: author's model (thesis, Chapter 4 and Appendix C); illustrative parameters, not estimates",
  "Inside the band the basis follows demand one for one. The ban removes new arbitrage and also blocks new futures demand.");
fig(s, "model_band", 0.4, 1.7, 4.6, 4.2);
defRows(s, [
  ["Band", [[{ text: "Arbitrage starts only outside " }, { text: "[-c-, c+]", b: true }], "Costs set the edges; capital and risk set how far the basis travels beyond them"]],
  ["Ban: arbitrage", ["Arbitrageurs may only reduce positions", [{ text: "Rich futures are no longer corrected", b: true }]]],
  ["Ban: demand", ["New futures demand is blocked; part moves to the stock", [{ text: "This lowers the basis", b: true }]]],
], 5.15, 1.85, 4.45, 1.2, 0.17, 1.25, 11);
callout(s, "So the ban's effect on the level has no fixed sign: it depends on what is blocked");

s = content("The question and our approach", "Each hypothesis states what would contradict it",
  "Predictions derived from the model; the first four form the primary family", "Source: frozen pre-analysis plan (git tag pap-v1, 5 November 2026)",
  "Primary family: H8, H7, H3, H6. Secondary tests are reported without adjustment.");
tbl(s, ["", "Prediction", "Contradicted if"], [
  ["H8", "In a ban futures volume falls and every trade closes positions", "Futures activity unchanged"],
  ["H7", "In a ban rich futures revert more slowly, cheap ones as fast or faster", "No asymmetry, or the opposite"],
  ["H3", "Band edges move with the STT, more for larger increases", "Edges unrelated to cost changes"],
  ["H6", "F&O entry lowers price delay and bad-news drift; exit raises them", "No change or the opposite"],
  ["Level", "The basis level at ban start follows the composition of open interest", "Sign unrelated to composition"],
  ["H9", "The upper tail grows smoothly as utilisation nears 95%", "Jump only at 95%"],
  ["H1, H4, H5", "Wider bands with frictions; scarcer capital widens; overpricing anomalies stronger where shorting is hard", "No relation; symmetric effects"],
], 0.45, 1.7, 9.1, [1.2, 5.0, 2.9], { rowH: 0.52, size: 11 });

s = content("The question and our approach", "The data come entirely from public NSE files",
  "Sources, coverage and the main checks", "Source: NSE archives; AMFI; OECD via FRED; author's analysis",
  "Everything is rebuilt by scripts; a full rerun reproduces every number.");
defRows(s, [
  ["Bans and limits", ["Daily open interest, position limits and ban lists, February 2010 to October 2026", "Next-day flags match the official ban list for 99.9% of stock-days"]],
  ["Prices and basis", ["Futures and cash bhavcopies 2015 to 2026; basis from volume-weighted prices", "Settlement prices avoided: they are set at cost of carry on thin days"]],
  ["Events", ["Results dated from the exchange's first dissemination time", "239 entries into and 171 exits from the F&O segment"]],
  ["Capital, lending", ["AMFI arbitrage-fund flows and assets, April 2018 to September 2026", "Daily securities-lending trades, 2015 to 2026"]],
], 0.45, 1.75, 6.2, 0.95, 0.12, 1.45, 10.5);
const kpi = [["1,788", "ban spells"], ["486,040", "stock-days of basis"], ["80,042", "stock-quarters in the index"], ["3,310", "stocks in the cash market"]];
kpi.forEach((k, i) => {
  const y = 1.8 + i * 1.04;
  s.addText(k[0], { x: 6.95, y, w: 2.7, h: 0.5, fontSize: 26, bold: true, color: HEX.navy, margin: 0, isTextBox: true });
  s.addText(k[1], { x: 6.95, y: y + 0.48, w: 2.7, h: 0.3, fontSize: 12, color: HEX.navy, margin: 0, isTextBox: true });
});

// ------------------------------------------------------------------ 4. the ban
divider("The F&O ban");
s = content("The F&O ban", "In a ban, futures trading collapses",
  "Effect of a ban on log futures contracts, and the median R on ban days, by enforcement regime", null,
  "Pre-specified H8: -2.00 log points on futures volume, cash +7.5%, delivery share +4.1 points.");
fig(s, "fig_h8_era", 0.45, 1.7, 9.1, 4.25);
callout(s, "Futures volume falls by about 87% in a ban; cash trading rises and turns toward delivery");

s = content("The F&O ban", "Intraday checks made the rule bind trade by trade",
  "Monthly median on ban days of R = (change in open interest + volume) / volume", null,
  "R = 0 when every trade closes a long and a short. The break in March 2020 matches SEBI press release 18/2020.");
chartAndPanel(s, "fig_ban_R", "What the chart shows", [
  [{ text: "To 22 March 2020 ", b: true }, { text: "violations were judged on end-of-day positions: median R 0.87" }],
  [{ text: "From 23 March 2020 ", b: true }, { text: "on peak intraday positions: median R 0.011" }],
  [{ text: "From October 2025 ", b: true }, { text: "the delta rule allows offsetting trades: 0.19 to 0.36" }],
]);
callout(s, "The rule changes trading as designed only when positions are checked during the day");

s = content("The F&O ban", "Correction is not one-sided: rich futures revert faster",
  "Change in the reversion slope on ban days, by regime, with 95% intervals", null,
  "The prediction came from the reduce-only arbitrage channel alone. The opposite sign survives a noise correction.");
chartAndPanel(s, "fig_h7_dots", "Why it matters", [
  [{ text: "Predicted: ", b: true }, { text: "slower reversion of rich futures (above 0)" }],
  [{ text: "Found: ", b: true }, { text: "-0.089 (s.e. 0.037); cheap futures revert more slowly" }],
  [{ text: "Robust: ", b: true }, { text: "-0.190 when instrumented; +0.037 at false ban dates" }],
  [{ text: "Timing: ", b: true }, { text: "concentrated in the first five days of a spell" }],
]);
callout(s, "The pre-specified prediction failed, with the opposite sign");

s = content("The F&O ban", "The basis falls when a ban starts, then recovers",
  "Change in the basis around ban entry, treated minus matched controls (bp)", null,
  "889 matched entries, 2015 to September 2025. Controls: same week, 85 to 95% utilisation, matched on path and basis.");
twoPanels(s, "About -6 bp in the first days, more after fast build-ups", "fig_level_profile",
  "Both long and short build-ups; nothing at false entries", "fig_level_groups");
callout(s, "Blocked new futures demand fits both facts, a reading formed after the results");

s = content("The F&O ban", "Traders do not hold back below the 95% trigger",
  "Utilisation around the trigger, and outcomes on either side of it", null,
  "Density test p = 0.86. Regression discontinuity: futures -1.53 log points; basis -12.9 bp, but already -11.3 on the crossing day.");
twoPanels(s, "No bunching below 95% (density test p = 0.86)", "fig_density",
  "Futures trading drops at 95%; the basis is lower above it", "fig_rd");
callout(s, "The trigger works mechanically; the basis gap is already there the day it is crossed");

// ------------------------------------------------------------------ 5. band
divider("The band: costs, capital and position limits");
s = content("The band", "The basis moves in a wide, asymmetric band",
  "Pooled threshold model, non-ban days, 2015 to 2026 (473,110 observations, 360 stocks)", null,
  "Linearity rejected (sup-F 7,471). Instrumenting with the deviation two days earlier shrinks all slopes: daily reversion is mostly noise.");
twoPanels(s, "Reversion grows with the deviation; band -34.5 to +23.9 bp", "fig_band_scatter",
  "Stable across years, apart from March 2020", "fig_band_years");
callout(s, "Much daily reversion is price noise; where the band lies is the robust part");

s = content("The band", "Tax rises lifted the whole distribution",
  "Change in stocks' 80th percentile at STT dates, and the bottom-up cost of a new position", null,
  "Pre-specified H3: +6.96 bp pooled. Placebo standard deviation 7.4 bp; true changes rank at the 10th and 7th percentiles.");
twoPanels(s, "Large changes, but within the range of placebo dates", "fig_h3_placebo",
  "A new round trip costs 27 to 31 bp, above the upper edge", "fig_cost_band");
callout(s, "New capital enters only at large gaps; funds that roll lean against small ones (4 to 8 bp)");

s = content("The band", "Arbitrage capital leaves weak traces",
  "Arbitrage-fund flows, assets and the upper tail of the basis, monthly", "Source: AMFI monthly reports; NSE archives; author's analysis",
  "Pre-specified H4: -17.5 bp per unit of flow, p = 0.11. First differences -20.6 (s.e. 6.8).");
twoPanels(s, "Inflows go with a lower upper tail next month (p = 0.11)", "fig_h4_flows",
  "Fund assets quadrupled after debt funds lost their tax edge", "fig_arb_aum");
callout(s, "The link is clearer month on month and before 2023, and invisible after");

s = content("The band", "Rich futures become more common near the trigger",
  "Upper-tail share by utilisation, and the 2020 restoration of halved limits", null,
  "H9 slope +0.079 (p = 0.019). Restoration on 27 November 2020: utilisation -0.21, ban days -4.6 points, upper tail -6.8 points.");
twoPanels(s, "The upper-tail share rises from 0.20 to 0.27 (p = 0.019)", "fig_h9_tails",
  "Restoring halved limits cut utilisation at once", "fig_covid");
callout(s, "The level of the limit matters for prices even before a ban starts");

s = content("The band", "The 2025 rules cut ban days by about three quarters",
  "Ban stock-days, 1 October 2025 to 27 October 2026, actual and counterfactual rules", null,
  "The simulated ban rule reproduces the official lists exactly. The old-formula limit is an approximation.");
chartAndPanel(s, "fig_spurious", "What the reform did", [
  [{ text: "Aim: ", b: true }, { text: "SEBI set out to reduce 'spurious' bans" }],
  [{ text: "Before 2025 ", b: true }, { text: "bans came from rising open interest; only 0.4% from a falling limit" }],
  [{ text: "Delta-adjusted open interest ", b: true }, { text: "removes almost all bans; the lower limit alone would have quadrupled them" }],
  [{ text: "Net: ", b: true }, { text: "412 ban days against 1,505 under the old rule" }],
]);
callout(s, "The reform met its stated aim");

// ------------------------------------------------------------------ 6. short-sale constraints
divider("Short-sale constraints");
s = content("Short-sale constraints", "F&O entry speeds up how prices respond to news",
  "Change in price delay by year relative to the first full year after entry or exit", null,
  "Callaway and Sant'Anna estimator; Sun and Abraham gives -0.063. Drift after bad news becomes stronger after entry, not weaker.");
fig(s, "fig_h6_es", 0.4, 1.7, 5.6, 4.2);
tbl(s, ["Component", "Estimate", "p"], [
  ["Entry: price delay", "-0.109", "1e-6"],
  ["Entry: bad-news drift", "-0.040", "0.99"],
  ["Exit: price delay", "+0.053", "0.09"],
  ["Exit: bad-news drift", "+0.014", "0.77"],
], 6.2, 2.1, 3.35, [1.75, 0.85, 0.75], { rowH: 0.45, size: 10.5 });
s.addText("Prediction: entry lowers delay and drift; exit raises them", { x: 6.2, y: 4.55, w: 3.35, h: 0.6, fontSize: 10.5, italic: true, color: HEX.grey, margin: 0, isTextBox: true });
callout(s, "Delay falls by 0.11 after entry (median 0.24 before); drift after bad news does not weaken");

s = content("Short-sale constraints", "Constrained stocks adjust more slowly, market-wide",
  "A quarterly index from five frictions for all NSE stocks: loadings and validation", "Source: NSE bhavcopies and SLB files; AMFI market capitalisation; author's analysis",
  "80,042 stock-quarters, 3,310 stocks. Associations, not causal effects.");
fig(s, "fig_index", 0.45, 1.7, 9.1, 4.25);
callout(s, "The link with price delay survives a size control; the bad-news link is a size effect");

s = content("Short-sale constraints", "Anomalies are not one-sided where shorting is hard",
  "Cash-only stocks without lending minus F&O stocks, % a month", null,
  "Pre-specified H5: short-leg difference +0.04% (s.e. 0.20), p = 0.57.");
chartAndPanel(s, "fig_h5_legs", "What the chart shows", [
  [{ text: "Value-weighted, ", b: true }, { text: "the overpriced side does no worse where shorting is hardest" }],
  [{ text: "Equal-weighted, ", b: true }, { text: "anomalies are stronger among small cash-only stocks, on both sides" }],
  [{ text: "Momentum ", b: true }, { text: "alone fits the prediction (-0.51%)" }],
]);
callout(s, "Groups differ greatly in size, which limits what this comparison can show");

// ------------------------------------------------------------------ 7. conclusion
divider("Conclusion and policy");
s = content("Conclusion", "Limits bind hard on trading, less cleanly on prices",
  "What each limit does, and how strong the evidence is", null,
  "Position limits matter most; costs set the band; capital is a weak force; short-sale access matters for speed.");
const G = (t) => ({ text: t, o: { fill: { color: "00A3E8" }, color: "FFFFFF", bold: true, align: "center" } });
const L = (t) => ({ text: t, o: { fill: { color: "BFE6F8" }, color: "000000", align: "center" } });
const N = (t) => ({ text: t, o: { fill: { color: "E6E6E6" }, color: "4D4D4D", align: "center" } });
tbl(s, ["Limit", "On trading", "On prices", "Main evidence"], [
  ["Position limits", G("Strong"), L("Real, not one-sided"), { text: "Volume -2 log points; basis -6 bp at ban start; 2025 rules cut bans by three quarters" }],
  ["Short-sale constraints", N("Not tested"), G("Speed of adjustment"), { text: "Delay -0.11 after F&O entry; no effect on bad-news drift or overpricing" }],
  ["Trading costs", N("Not tested"), L("Set the band"), { text: "Band -35 to +24 bp; new round trip in the outer tail; edges not one-for-one with the tax" }],
  ["Arbitrage capital", N("Not tested"), L("Weak"), { text: "Inflows go with a lower upper tail (p = 0.11); clearer in differences" }],
], 0.45, 1.75, 9.1, [1.9, 1.45, 1.9, 3.85], { rowH: 0.75, size: 11 });
callout(s, "Position limits matter most; costs shape the band; capital is a weak force");

s = content("Conclusion", "Bans restrain demand at the cost of arbitrage",
  "What the evidence shows, and what it implies for the rules",
  "Source: author's analysis; SEBI press release 22/2024; SEBI circulars 2024/132 and 2025/79",
  "SEBI's study: 93% of over one crore individual F&O traders lost money in FY22 to FY24, more than Rs 1.8 lakh crore in total.");
textPanel(s, "What the evidence shows", [
  "A ban cuts futures volume by almost 90%",
  "Its price effect appears at the start of a ban and fades within a week",
  "The rule bites as designed only under intraday checks",
  "The 2025 rules cut ban days by about three quarters",
], 0.45, 1.65, 4.35, 2.6, 12);
textPanel(s, "What it implies", [
  "A ban blocks the speculative demand it targets, and the arbitrage that keeps prices together",
  "Enforcement matters as much as the threshold",
  "Measuring open interest in delta terms removes avoidable bans",
  "F&O access has a measurable benefit: faster price adjustment",
], 5.2, 1.65, 4.35, 2.7, 12);
[["-87%", "futures volume in a ban"], ["~1 week", "for the price effect to fade"], ["-73%", "ban days, 2025 rules against old"], ["93%", "of individual F&O traders lost money, FY22 to FY24"]].forEach((k, i) => {
  const x = 0.55 + i * 2.28;
  s.addShape(pres.shapes.LINE, { x, y: 4.45, w: 2.0, h: 0, line: { color: HEX.navy, width: 1.5 } });
  s.addText(k[0], { x, y: 4.55, w: 2.1, h: 0.55, fontSize: 28, bold: true, color: i === 3 ? HEX.blue : HEX.navy, margin: 0, isTextBox: true });
  s.addText(k[1], { x, y: 5.1, w: 2.1, h: 0.6, fontSize: 11.5, color: HEX.navy, valign: "top", margin: 0, isTextBox: true });
});
callout(s, "Limits restrain a large speculative demand, and arbitrage pays part of the price");

s = content("Conclusion", "Four limitations we know about", null, null,
  "Next steps: intraday data, a longer post-reform sample, and the three papers that could not be read in full.");
const risks = [
  ["Daily data", "Intraday arbitrage is out of scope, and noise inflates measured reversion", "Noise-corrected estimates reported alongside"],
  ["Inventory unobserved", "The model's arbitrage book is not seen in public data", "Composition of open interest used as a proxy"],
  ["Short post-reform sample", "Only 44 ban spells since October 2025", "Post-reform results labelled low-powered"],
  ["Size confounds", "Constrained stocks are much smaller", "Size controls; F&O entry as a within-stock design"],
];
s.addText("Limitation", { x: 0.45, y: 1.6, w: 2.1, h: 0.3, fontSize: 12, bold: true, align: "center", margin: 0, isTextBox: true });
s.addText("What could go wrong", { x: 2.7, y: 1.6, w: 3.6, h: 0.3, fontSize: 12, bold: true, align: "center", margin: 0, isTextBox: true });
s.addText("...and what I did", { x: 6.45, y: 1.6, w: 3.1, h: 0.3, fontSize: 12, bold: true, align: "center", margin: 0, isTextBox: true });
[[0.5, 2.0], [2.75, 3.5], [6.5, 3.0]].forEach((p) => s.addShape(pres.shapes.LINE, { x: p[0], y: 1.95, w: p[1], h: 0, line: { color: HEX.navy, width: 1.5 } }));
risks.forEach((r, i) => {
  const y = 2.08 + i * 0.95;
  if (i % 2 === 0) s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y, w: 9.1, h: 0.85, fill: { color: HEX.panel }, line: { color: HEX.panel } });
  s.addText(r[0], { x: 0.5, y, w: 2.0, h: 0.85, fontSize: 12, bold: true, color: HEX.navy, valign: "middle", margin: 4, isTextBox: true });
  s.addText(r[1], { x: 2.7, y, w: 3.6, h: 0.85, fontSize: 11.5, valign: "middle", margin: 4, isTextBox: true });
  s.addText(r[2], { x: 6.45, y, w: 3.1, h: 0.85, fontSize: 11.5, valign: "middle", margin: 4, isTextBox: true });
});
callout(s, "Intraday data and a longer post-reform sample would sharpen the ban tests");

s = pres.addSlide({ masterName: "TITLE", sectionTitle: SECTION });
s.addText("Limits to arbitrage in Indian equities", { placeholder: "title" });
s.addText("Thank you", { placeholder: "sub" });
s.addText("November 2026", { placeholder: "date" });
s.addText([{ text: "Prince Kumar (23B3032)", options: { breakLine: true } },
  { text: "Guide: Prof. Aditi Chaubal, Department of Economics, IIT Bombay", options: { fontSize: 13, bold: false } }], { placeholder: "band" });

// ------------------------------------------------------------------ 8. appendix
divider("Appendix");
s = content("Appendix", "All pre-specified tests", "Primary family (Holm) and secondary tests (unadjusted)",
  "Source: author's analysis; thesis, Table 9.1", "Secondary tests read as a pattern; one or two values below 0.05 would be expected by chance.");
tbl(s, ["Test", "Result", "Comment"], [
  ["H8 trading", "Supported (p < 1e-10)", "Identity holds under intraday enforcement"],
  ["H3 costs", "Supported (p < 1e-10)", "Weak against placebos; mostly a common shift"],
  ["H6 short-sale access", "Supported (p = 5e-6)", "Through price delay; drift goes the other way"],
  ["H7 one-sided correction", "Rejected, opposite sign", "Survives a noise correction"],
  ["Level effect", "p = 0.083", "Signs as predicted; median split p = 0.025"],
  ["Density, RD at 95%", "p = 0.86; -12.9 bp", "No bunching; gap present before the ban"],
  ["Hysteresis", "+0.4 bp, p = 0.64", "No extra level shift"],
  ["H9 anticipation, reform", "p = 0.019; p = 0.11", "Upper tail grows toward 95%; reform right sign"],
  ["H2, H1, H4, H5", "p = 0.59, 0.002, 0.11, 0.57", "No power; across stocks only; weak; not supported"],
], 0.45, 1.65, 9.1, [2.5, 2.6, 4.0], { rowH: 0.44, size: 10.5 });

s = content("Appendix", "How the data were built and checked", null, "Source: author's analysis; thesis, Chapter 5 and Appendix B",
  "Every data set is rebuilt from raw files by scripts with a report of counts and checks.");
defRows(s, [
  ["Bans", ["Next-day flags agree with the official list for 11,753 of 11,764 flags", "95% entry and 80% exit rules hold for 99.4% and 99.7% of spells"]],
  ["Basis", ["Volume-weighted futures and cash prices, net of dividends and carry", "Contracts with dividends or corporate events in their life excluded"]],
  ["Results dates", ["Earliest of the exchange's announcement and the filing; board meetings fill gaps", "Covers 98% to 100% of F&O stock-quarters"]],
  ["Reproduction", ["One script sequence produces every estimate; a full rerun reproduced every number", "Each estimator first recovered known effects on simulated data"]],
], 0.45, 1.75, 9.1, 0.95, 0.12, 1.6, 11);

s = content("Appendix", "The model's eleven results map onto the tests", null, "Source: author's model (thesis, Appendix C)",
  "All closed forms were checked numerically against a brute-force solver.");
tbl(s, ["Result", "Statement", "Tested by"], [
  ["1-2 Band", "Arbitrage only outside [-c-, c+]; costs set the edges, capital the passthrough", "H3, H4, band chapter"],
  ["3 Inventory", "The no-trade region moves with the existing book", "Estimator tests"],
  ["4 One-sided", "In a ban rich futures are not corrected; cheap ones are while inventory lasts", "H7"],
  ["5-6 Demand, level", "Blocked new demand reverses its effect; the level effect has no fixed sign", "Level effect"],
  ["7 Trading", "Contract-by-contract enforcement makes every trade close positions", "H8"],
  ["8-9 Anticipation", "The upper edge rises toward 95%; the limit is not an instrument for bans", "H9, density, RD"],
  ["10-11 Short sales", "Bad news slower without a short channel; Miller overpricing", "H2, H5, H6"],
], 0.45, 1.65, 9.1, [1.9, 5.0, 2.2], { rowH: 0.55, size: 10.5 });

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
