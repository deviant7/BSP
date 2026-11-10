// Stage I (EC 495) presentation, consulting format of the reference decks (4:3). Same masters and helpers as deck/build_deck.js.
// Run: NODE_PATH=<scratch>/node_modules node BSP1/deck/build_deck_bsp1.js   (figures in BSP1/deck/figs)
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const SKILL = "/root/.claude/skills/synced/e0a82d13-199d-48ef-a456-82ceb3895c04_a2b91922-6749-493b-b7fd-5638ecdae803/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));

const ROOT = path.resolve(__dirname, "..", "..");
const FIG = path.join(__dirname, "figs");
const OUT = path.join(ROOT, "BSP1", "BSP1_Presentation_Nov2026.pptx");

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
pres.title = "Limits to Arbitrage in the Indian Equity Market: Stage I";
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

// ------------------------------------------------------------------ title and agenda
SECTION = "Opening";
pres.addSection({ title: "Opening" });
let s = pres.addSlide({ masterName: "TITLE", sectionTitle: SECTION });
s.addText("Limits to arbitrage in Indian equities", { placeholder: "title" });
s.addText("Stage I: theory, data and the futures-cash band", { placeholder: "sub" });
s.addText("BS project, Stage I (EC 495)  |  November 2026", { placeholder: "date" });
s.addText([{ text: "Prince Kumar (23B3032)", options: { breakLine: true } },
  { text: "Guide: Prof. Aditi Chaubal, Department of Economics, IIT Bombay", options: { fontSize: 13, bold: false } }], { placeholder: "band" });
s.addNotes("Stage I of the project: the model, the test plan, the data, the band within which futures and cash prices move, and whether the F&O ban binds on trading. What the limits do to prices is Stage II.");

s = pres.addSlide({ masterName: "CONTENT", sectionTitle: SECTION });
s.addText("Agenda", { placeholder: "title" });
const agenda = [
  ["Executive summary", ""],
  ["The question and the approach", "Why India, the F&O ban, the model and the frozen test plan"],
  ["The data", "Bans and the futures-cash basis, 2015 to 2026"],
  ["The no-arbitrage band", "How wide it is, and what sets it: costs and frictions"],
  ["Does the ban bind on trading?", "Trading in a ban, the 95% trigger and the 2025 rules"],
  ["Conclusion and Stage II", ""],
];
agenda.forEach((a, i) => {
  const y = 1.72 + i * 0.8;
  s.addText(a[0], { x: 0.55, y, w: 8.8, h: 0.33, fontSize: 18, bold: true, color: HEX.navy, margin: 0, isTextBox: true });
  if (a[1]) s.addText([{ text: a[1], options: { bullet: { indent: 14 } } }], { x: 0.55, y: y + 0.33, w: 8.8, h: 0.3, fontSize: 14, color: HEX.navy, margin: 0, isTextBox: true });
});
s.addText(" ", { placeholder: "source" });

// ------------------------------------------------------------------ executive summary
divider("Executive summary");
s = content("Executive summary", "Executive summary", null, "Source: NSE archives, 2010 to 2026; author's analysis",
  "Four messages for Stage I: the band, its relation to costs, trading in a ban, and the 2025 rules.");
s.addText("Futures and cash prices of Indian stocks move in a wide band that costs shape only loosely; the F&O ban binds hard on trading.",
  { x: 0.55, y: 1.65, w: 8.9, h: 0.6, fontSize: 13, bold: true, color: "000000", margin: 0, isTextBox: true });
const exec = [
  [{ text: "A wide, asymmetric band. ", b: true }, { text: "The basis moves between about -35 and +24 bp around each stock's median. Inside, it drifts; outside, it is pushed back. The lower side reaches further because the correcting trade needs a short sale." }],
  [{ text: "Costs shape it loosely. ", b: true }, { text: "A new cash-and-carry round trip costs 27 to 31 bp, in the outer tail. The upper tail rose after the 2024 and 2026 tax increases, as predicted, but by more than the cost changes and not unusually against placebo dates." }],
  [{ text: "The ban binds hard on trading. ", b: true }, { text: "Futures volume falls by about 87% in a ban. Once violations were checked on intraday positions (from March 2020), every futures trade in a ban closed positions." }],
  [{ text: "The 2025 rules cut bans. ", b: true }, { text: "Against the old rule applied to the same stocks, ban days fell by about three quarters in the first year." }],
];
s.addText(bullets(exec, 13), { x: 0.6, y: 2.45, w: 8.85, h: 4.3, valign: "top", margin: 0, isTextBox: true });

s = content("Executive summary", "Both primary tests of this stage hold as specified",
  "Pre-specified tests of Stage I; primary tests Holm-corrected with the two of Stage II", null,
  "H3 and H8 are primary; H1 and the density test are secondary. H6 and H7, the other two primary hypotheses, are in Stage II.");
tbl(s, ["Test", "Prediction", "Result", "Verdict"], [
  ["H8 Trading in a ban (primary)", "Futures volume falls; trades only close positions", "-2.00 log points (s.e. 0.11)", { text: "Supported", o: { bold: true, color: HEX.mid } }],
  ["H3 Costs and the band (primary)", "Upper edge rises with each tax increase", "+6.96 bp (s.e. 0.61); weak against placebo dates", { text: "Supported, weakly", o: { bold: true, color: HEX.mid } }],
  ["H1 Frictions and the band", "Wider bands where frictions are higher", "+3.5 bp per s.d. (p = 0.002), across stocks", { text: "Supported", o: { bold: true, color: HEX.mid } }],
  ["Density at the 95% trigger", "Not signed by the model", "No bunching (p = 0.86)", { text: "Descriptive", o: { bold: true, color: HEX.grey } }],
], 0.45, 1.7, 9.1, [2.4, 2.55, 2.75, 1.4], { rowH: 0.55, size: 11 });
s.addText(bullets([
  [{ text: "Every detail the plan left open ", b: true }, { text: "was fixed in a dated log before the test that needed it." }],
  [{ text: "Analyses added after a result ", b: true }, { text: "(for example, the split by enforcement period) are labelled as such." }],
], 12), { x: 0.6, y: 5.05, w: 8.8, h: 0.9, valign: "top", margin: 0, isTextBox: true });
callout(s, "Both primary tests of Stage I hold; the cost result is weak once common shocks are allowed for");

// ------------------------------------------------------------------ the question and approach
divider("The question and the approach");
s = content("The question and the approach", "India changes almost every limit on a known date",
  "Futures STT, ban enforcement, the position-limit rule and arbitrage capital, 2015 to 2026",
  "Source: SEBI circulars and press releases; NSE circulars; AMFI", "Dated rule changes are what make each limit measurable.");
fig(s, "fig_timeline", 0.45, 1.7, 9.1, 4.2);
callout(s, "Dated rule changes let me measure each limit instead of assuming it");

s = content("The question and the approach", "The F&O ban lets every trader only reduce positions",
  "Utilisation of the position limit for SAIL, the most-banned stock, January to June 2024", null,
  "The ban binds everyone, not only arbitrageurs. That is what makes it different from a cap on one trader.");
chartAndPanel(s, "fig_util_example", "How the rule works", [
  [{ text: "Enter ", b: true }, { text: "the day after open interest exceeds 95% of the market-wide position limit" }],
  [{ text: "Leave ", b: true }, { text: "after it falls to 80%" }],
  [{ text: "In between, everyone ", b: true }, { text: "may only reduce positions, in all expiries" }],
  [{ text: "1,788 spells ", blue: true }, { text: "in 141 stocks, 2015 to October 2026" }],
]);
callout(s, "To my knowledge, no study had examined this rule");

s = content("The question and the approach", "Stage I builds the foundation; Stage II asks about prices",
  "How strongly do limits to arbitrage bind, and how much mispricing do they explain?", null,
  "The project is split into two stages. This presentation covers Stage I.");
textPanel(s, "Stage I (this presentation)", [
  [{ text: "A model ", b: true }, { text: "with every Indian limit as a parameter" }],
  [{ text: "A frozen test plan ", b: true }, { text: "and a data set from public NSE files" }],
  [{ text: "How wide is the band ", b: true }, { text: "within which the futures-cash basis moves?" }],
  [{ text: "Do costs and frictions ", b: true }, { text: "set its edges?" }],
  [{ text: "Does the ban bind ", b: true }, { text: "on trading, as the rule intends?" }],
], 0.45, 1.65, 4.35, 4.3, 12);
textPanel(s, "Stage II", [
  [{ text: "What a ban does to prices: ", b: true }, { text: "one-sided correction, the level of the basis at ban start" }],
  [{ text: "Position limits before a ban: ", b: true }, { text: "anticipation; the 2025 formula; the 2020 halving" }],
  [{ text: "Arbitrage capital: ", b: true }, { text: "do fund inflows narrow the band?" }],
  [{ text: "Short-sale constraints: ", b: true }, { text: "F&O entry, anomalies, a constraint index for all stocks" }],
  [{ text: "Policy ", b: true }, { text: "on position limits and their enforcement" }],
], 5.2, 1.65, 4.35, 4.3, 12);
callout(s, "Stage I answers three questions: where the band lies, what sets it, and whether bans bind");

s = content("The question and the approach", "Model: costs set the band; a ban blocks two things",
  "Equilibrium basis against the demand pressure of outside traders, with illustrative costs",
  "Source: author's model; illustrative parameters, not estimates",
  "Inside the band the basis follows demand one for one. The ban removes new arbitrage and also blocks new futures demand.");
fig(s, "model_band", 0.4, 1.7, 4.6, 4.2);
defRows(s, [
  ["Band", [[{ text: "Arbitrage pays only outside " }, { text: "[-c-, c+]", b: true }], "Costs set the edges; capital and risk set how far the basis travels beyond them"]],
  ["Ban: arbitrage", ["Arbitrageurs may only reduce positions", [{ text: "Rich futures are no longer corrected", b: true }]]],
  ["Ban: demand", ["New futures demand is blocked; part moves to the stock", [{ text: "This lowers the basis", b: true }]]],
], 5.15, 1.85, 4.45, 1.2, 0.17, 1.25, 11);
callout(s, "Stage I tests the band and trading in a ban; the price predictions come in Stage II");

s = content("The question and the approach", "I fixed the tests before looking at outcomes",
  "Five safeguards against fitting theory and data to each other", null, "Order of work: model, frozen plan, data, estimator tests, full reporting.");
s.addText("What I did", { x: 2.75, y: 1.62, w: 4.0, h: 0.3, fontSize: 12, bold: true, align: "center", margin: 0, isTextBox: true });
s.addText("Why", { x: 6.95, y: 1.62, w: 2.6, h: 0.3, fontSize: 12, bold: true, align: "center", margin: 0, isTextBox: true });
s.addShape(pres.shapes.LINE, { x: 2.8, y: 1.95, w: 3.9, h: 0, line: { color: HEX.navy, width: 1.5 } });
s.addShape(pres.shapes.LINE, { x: 7.0, y: 1.95, w: 2.5, h: 0, line: { color: HEX.navy, width: 1.5 } });
const steps = [
  ["Model", [{ text: "One model; " }, { text: "every limit a parameter", blue: true }, { text: "; each prediction with what would contradict it" }], "Hypotheses are derived, not fitted"],
  ["Frozen plan", [{ text: "Tests and signs " }, { text: "fixed with a time stamp", blue: true }, { text: " on 5 November 2026" }], "No choosing specifications after seeing results"],
  ["Data", [{ text: "Built from " }, { text: "public NSE files", blue: true }, { text: " and checked against the exchange's rules" }], "Errors caught before testing"],
  ["Estimator tests", [{ text: "Each estimator " }, { text: "recovers known effects", blue: true }, { text: " on simulated data" }], "Methods checked before real data"],
  ["Full reporting", [{ text: "Primary tests " }, { text: "Holm-corrected", blue: true }, { text: "; weak and failed results kept" }], "Nothing is left out"],
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

s = content("The question and the approach", "Each prediction states what would contradict it",
  "Predictions of the model and where they are tested", "Source: pre-analysis plan, frozen 5 November 2026",
  "Primary hypotheses of the plan: H3, H6, H7, H8. H3 and H8 are in Stage I.");
const T1 = (t) => ({ text: t, o: { bold: true, color: HEX.mid } });
const T2 = (t) => ({ text: t, o: { color: HEX.grey } });
tbl(s, ["Prediction", "Contradicted if", "Plan label", "Tested in"], [
  ["The basis moves in an asymmetric band, wider below zero", "No band; a symmetric band", "Band", T1("Stage I")],
  ["Tax increases raise the upper edge, more for larger ones", "Edges unrelated to costs", "H3 (primary)", T1("Stage I")],
  ["Bands are wider where frictions are higher", "No relation", "H1", T1("Stage I")],
  ["In a ban futures volume falls and trades only close positions", "Futures activity unchanged", "H8 (primary)", T1("Stage I")],
  ["In a ban rich futures revert more slowly", "No asymmetry, or the opposite", "H7 (primary)", T2("Stage II")],
  ["The level effect follows the composition of trading", "Sign unrelated to composition", "Level effect", T2("Stage II")],
  ["Short-sale access speeds price adjustment", "No change, or the opposite", "H6 (primary)", T2("Stage II")],
], 0.45, 1.7, 9.1, [3.9, 2.4, 1.45, 1.35], { rowH: 0.5, size: 10.5 });

// ------------------------------------------------------------------ data
divider("The data");
s = content("The data", "The data come entirely from public NSE files",
  "Sources, coverage and the main checks", "Source: NSE archives; OECD via FRED; author's analysis",
  "Everything is rebuilt by scripts; a full rerun reproduces every number.");
defRows(s, [
  ["Bans and limits", ["Daily open interest, position limits and ban lists, February 2010 to October 2026", "Next-day flags match the official ban list for 11,753 of 11,764 flags"]],
  ["Prices and basis", ["Futures and cash bhavcopies 2015 to 2026; basis from volume-weighted prices", "Settlement prices avoided: they are set at cost of carry on thin days"]],
  ["Corporate events", ["Dividends subtracted at present value", "Contracts with a dividend or other event in their life excluded"]],
  ["Lending, rates", ["Daily stock-lending trades, 2015 to 2026", "Three-month interbank rate for the cost of carry"]],
], 0.45, 1.75, 6.2, 0.95, 0.12, 1.45, 10.5);
const kpi = [["1,788", "ban spells"], ["9,416", "ban stock-days"], ["486,040", "stock-days of basis"], ["371", "stocks with futures"]];
kpi.forEach((k, i) => {
  const y = 1.8 + i * 1.04;
  s.addText(k[0], { x: 6.95, y, w: 2.7, h: 0.5, fontSize: 26, bold: true, color: HEX.navy, margin: 0, isTextBox: true });
  s.addText(k[1], { x: 6.95, y: y + 0.48, w: 2.7, h: 0.3, fontSize: 12, color: HEX.navy, margin: 0, isTextBox: true });
});

s = content("The data", "Bans come in waves and fell under the new rule",
  "Stock-days in the ban per month, February 2010 to October 2026", "Source: NSE securities-in-ban lists; author's analysis",
  "Bans are concentrated in a few stocks; SAIL had 76 spells.");
chartAndPanel(s, "fig_ban_month", "What the chart shows", [
  [{ text: "1,788 spells ", b: true }, { text: "in 141 stocks, 2015 to October 2026" }],
  [{ text: "Typical spell: ", b: true }, { text: "4 trading days before the reform, 9 after it" }],
  [{ text: "1 October 2025: ", b: true }, { text: "every stock's limit cut, to a median of 73% of the old value" }],
]);
callout(s, "Bans are frequent enough to study, and concentrated in a few stocks");

s = content("The data", "The basis is centred near zero with a long lower tail",
  "Futures-cash basis of the analysis sample, 2015 to 2026", null,
  "Median +1.1 bp; 10th percentile -39.1; 90th +26.8. The basis narrows toward expiry as carrying costs shrink.");
twoPanels(s, "Median +1.1 bp; cheap futures go further from zero", "fig_basis_dist",
  "The basis narrows as expiry approaches", "fig_basis_expiry");
callout(s, "Cheap futures are further from zero, as expected when the correcting trade needs a short sale");

// ------------------------------------------------------------------ band
divider("The no-arbitrage band");
s = content("The no-arbitrage band", "The basis moves in a wide, asymmetric band",
  "Pooled threshold model, non-ban days, 2015 to 2026, 360 stocks", null,
  "Linearity rejected (sup-F 7,471 against a critical value of 31). The band is stable across years except 2020.");
twoPanels(s, "Pull back grows with the deviation; band -34.5 to +23.9 bp", "fig_band_scatter",
  "Stable across years, apart from March 2020", "fig_band_years");
callout(s, "The band is about 58 bp wide, far wider than intraday bands found in earlier Indian studies");

s = content("The no-arbitrage band", "The band's location is robust; its speed is not",
  "Reversion slopes by regime, before and after a correction for noise", null,
  "Instrumenting yesterday's deviation with the deviation two days earlier removes the bias from measurement noise.");
tbl(s, ["", "Lower regime", "Middle", "Upper regime"], [
  ["Threshold (bp)", "below -34.5", "", "above +23.9"],
  ["Share of days", "12%", "76%", "12%"],
  ["Slope, threshold model", "-0.08", "-0.47", "-0.81"],
  ["Slope, noise-corrected", "-0.12", "-0.19", "-0.14"],
], 0.45, 1.75, 5.4, [1.95, 1.2, 0.95, 1.3], { rowH: 0.5, size: 11 });
textPanel(s, "What this means", [
  [{ text: "Daily volume-weighted prices ", b: true }, { text: "contain noise that looks like fast reversion" }],
  [{ text: "Corrected, ", b: true }, { text: "the three slopes are small and similar" }],
  [{ text: "Smooth-transition models ", b: true }, { text: "fit almost as well; a symmetric one fits worse" }],
], 6.15, 1.75, 3.4, 3.8, 11.5);
callout(s, "Read the thresholds, not the speeds, as the main evidence on the band");

// ------------------------------------------------------------------ what sets the band
divider("What sets the band");
s = content("What sets the band", "Tax rises lifted the upper tail, but not unusually",
  "Change in stocks' 80th percentile at the STT dates and at 30 placebo dates (bp)", null,
  "Pre-specified H3: +6.96 bp pooled over 2024 and 2026 (s.e. 0.61). Placebo s.d. 7.4 bp; 10% and 7% of placebo dates show a rise as large.");
chartAndPanel(s, "fig_h3_placebo", "What the test shows", [
  [{ text: "Predicted: ", b: true }, { text: "the upper edge rises with each tax increase, more for larger ones" }],
  [{ text: "Found: ", b: true }, { text: "+6.4 bp (2024) and +7.4 bp (2026); ordered as the cost changes" }],
  [{ text: "But: ", b: true }, { text: "larger than the cost changes, the median moved too, and placebo dates move as much" }],
]);
callout(s, "Costs push the band the predicted way but do not set its edges tightly");

s = content("What sets the band", "A new position costs more than the estimated edge",
  "Round trip of an overnight cash-and-carry position, by STT period (bp)",
  "Source: NSE circulars on STT and transaction charges; author's analysis",
  "Brokerage 0.01% per leg; 25 to 38 bp for brokerage between 0.005% and 0.03%.");
chartAndPanel(s, "fig_cost_band", "What the chart shows", [
  [{ text: "New position: ", b: true }, { text: "27 to 31 bp, between the 90th and 95th percentiles of the basis" }],
  [{ text: "Estimated upper edge: ", b: true }, { text: "+22 to +28 bp" }],
  [{ text: "Rolling an existing position: ", b: true }, { text: "only 4 to 8 bp" }],
]);
callout(s, "New capital enters only at large gaps; funds that roll lean against small ones");

s = content("What sets the band", "Bands are wider in stocks that are harder to trade",
  "Band width and mean absolute basis by decile of a friction index (previous quarter)", null,
  "Index: spread, illiquidity, idiosyncratic volatility, utilisation, lack of stock lending. +3.5 bp per s.d. (s.e. 1.1, p = 0.002).");
fig(s, "fig_h1_bins", 0.45, 1.7, 9.1, 4.25);
callout(s, "The link holds across stocks, not within a stock over time");

// ------------------------------------------------------------------ ban and trading
divider("Does the ban bind on trading?");
s = content("Does the ban bind on trading?", "In a ban, futures trading collapses",
  "Effect on log futures contracts, and median R on ban days, by enforcement regime", null,
  "Pre-specified H8: -2.00 log points on futures volume, cash +7.5%, delivery share +4.1 points, against the same stock at 80 to 95% utilisation.");
fig(s, "fig_h8_era", 0.45, 1.7, 9.1, 4.25);
callout(s, "Futures volume falls by about 87% in a ban; cash trading rises and turns toward delivery");

s = content("Does the ban bind on trading?", "Intraday checks made the rule bind trade by trade",
  "Monthly median on ban days of R = (change in open interest + volume) / volume", null,
  "R = 0 when every trade closes a long and a short. The break in March 2020 matches SEBI press release 18/2020. The split by period was added after the pooled result.");
chartAndPanel(s, "fig_ban_R", "What the chart shows", [
  [{ text: "To 22 March 2020 ", b: true }, { text: "violations were judged on end-of-day positions: median R 0.87" }],
  [{ text: "From 23 March 2020 ", b: true }, { text: "on peak intraday positions: median R 0.011" }],
  [{ text: "From October 2025 ", b: true }, { text: "the delta rule allows offsetting trades: 0.19 to 0.36" }],
]);
callout(s, "The rule changes trading as designed only when positions are checked during the day");

s = content("Does the ban bind on trading?", "Traders do not hold back below the 95% trigger",
  "End-of-day utilisation of stocks that were below 95% the day before, 2015 to September 2025", null,
  "Density test (Cattaneo, Jansson and Ma) T = -0.18, p = 0.86. The population is stocks below 95% the day before, because above 95% a stock enters the ban.");
chartAndPanel(s, "fig_density", "What the chart shows", [
  [{ text: "No bunching ", b: true }, { text: "just below 95% (p = 0.86)" }],
  [{ text: "Utilisation speeds up ", b: true }, { text: "near the trigger rather than stalling" }],
  [{ text: "Chance of crossing next day: ", b: true }, { text: "7% at 85% utilisation, about half at 93 to 95%" }],
]);
callout(s, "There is no sign that traders hold back to avoid a ban");

s = content("Does the ban bind on trading?", "Trading breaks sharply at the 95% trigger",
  "Binned means by utilisation at the end of the previous day, stocks not in a ban the day before", null,
  "Regression discontinuity: futures -1.53 log points, R -0.66, delivery share +5.1 points; cash volume does not jump.");
fig(s, "fig_rd_trading", 0.45, 1.7, 9.1, 4.25);
callout(s, "Crossing 95% puts a stock in the ban the next day in 99.7% of cases");

s = content("Does the ban bind on trading?", "The 2025 rules cut ban days by about three quarters",
  "Ban stock-days, 1 October 2025 to 27 October 2026, actual and counterfactual rules", null,
  "The simulated ban rule reproduces the official lists exactly. The old-formula limit is an approximation.");
chartAndPanel(s, "fig_spurious", "What the reform did", [
  [{ text: "Aim: ", b: true }, { text: "SEBI set out to reduce 'spurious' bans" }],
  [{ text: "Before 2025 ", b: true }, { text: "bans came from rising open interest; only 0.4% from a falling limit" }],
  [{ text: "Delta-adjusted open interest ", b: true }, { text: "removes almost all bans; the lower limit alone would have quadrupled them" }],
  [{ text: "Net: ", b: true }, { text: "412 ban days against 1,505 under the old rule" }],
]);
callout(s, "The reform met its stated aim on the number of bans");

// ------------------------------------------------------------------ conclusion
divider("Conclusion and Stage II");
s = content("Conclusion", "What Stage I shows", "The three questions of this stage and their answers", null,
  "Position limits bind hard on trading; costs shape the band loosely.");
tbl(s, ["Question", "Answer", "Main evidence"], [
  ["How wide is the band?", "Wide and asymmetric", "-35 to +24 bp around each stock's median; linearity rejected; stable over time"],
  ["Do costs set its edges?", "Loosely", "Upper tail up after 2024 and 2026 tax rises, but not unusually; new position costs 27 to 31 bp"],
  ["Do frictions widen it?", "Across stocks", "+3.5 bp per s.d. of a friction index; no effect within a stock"],
  ["Does the ban bind on trading?", "Yes, strongly", "Futures volume -87%; every trade closes positions under intraday checks; 2025 rules cut bans by three quarters"],
], 0.45, 1.75, 9.1, [2.3, 1.6, 5.2], { rowH: 0.78, size: 11 });
callout(s, "Limits bind hard on trading; what they do to prices is the question of Stage II");

s = content("Conclusion", "Four limitations of this stage", null, null,
  "These shape the design of Stage II.");
const risks = [
  ["Daily data", "Intraday arbitrage is out of scope, and noise inflates measured reversion", "Noise-corrected estimates reported alongside"],
  ["Positions unobserved", "The arbitrage book in the model is not seen in public data", "Edges tested through changes, not levels"],
  ["Few cost events", "Three tax increases, one on the same day as a fund tax change", "Placebo dates calibrate the test"],
  ["Short post-reform period", "Only 44 ban spells since October 2025", "Reform effect on prices left to Stage II"],
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
callout(s, "Intraday data and a longer post-reform sample would sharpen the tests");

s = content("Conclusion", "Stage II asks what the limits do to prices", "The plan for the second stage", null,
  "Two primary hypotheses (H6, H7) and the remaining secondary tests of the frozen plan, plus new work.");
const plan2 = [
  ["The ban and prices", "One-sided correction in a ban (H7); the basis when a ban starts; placebo bans"],
  ["Limits before a ban", "Is the basis richer as utilisation nears 95%? The 2025 formula; the 2020 halving"],
  ["Arbitrage capital", "Do inflows into arbitrage funds narrow the band?"],
  ["Short-sale access", "F&O entry and exit (H6); anomalies; a constraint index for all stocks"],
  ["Policy", "Design and enforcement of position limits"],
];
plan2.forEach((r, i) => {
  const y = 1.75 + i * 0.82;
  s.addShape(pres.shapes.OVAL, { x: 0.45, y: y + 0.13, w: 0.36, h: 0.36, fill: { color: HEX.navy }, line: { color: "FFFFFF", width: 1 } });
  s.addText(String(i + 1), { x: 0.45, y: y + 0.13, w: 0.36, h: 0.36, fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText(r[0], { x: 0.95, y, w: 2.4, h: 0.62, fontSize: 13, bold: true, align: "center", valign: "middle", fill: { color: HEX.panel }, line: { color: HEX.panel }, margin: 2, isTextBox: true });
  s.addText(r[1], { x: 3.5, y, w: 6.05, h: 0.62, fontSize: 12, valign: "middle", margin: 2, isTextBox: true });
});
callout(s, "Stage I's model, plan and data carry over unchanged");

s = pres.addSlide({ masterName: "TITLE", sectionTitle: SECTION });
s.addText("Limits to arbitrage in Indian equities", { placeholder: "title" });
s.addText("Thank you", { placeholder: "sub" });
s.addText("BS project, Stage I (EC 495)  |  November 2026", { placeholder: "date" });
s.addText([{ text: "Prince Kumar (23B3032)", options: { breakLine: true } },
  { text: "Guide: Prof. Aditi Chaubal, Department of Economics, IIT Bombay", options: { fontSize: 13, bold: false } }], { placeholder: "band" });

// ------------------------------------------------------------------ appendix
divider("Appendix");
s = content("Appendix", "The model's propositions behind each test", null, "Source: author's model; proofs in the Stage I report",
  "The propositions are theoretical derivations; the tests ask whether the data agree with them.");
tbl(s, ["Proposition", "Statement", "Tested by"], [
  ["1 Band", "Arbitrage pays only outside [-c-, c+]; inside, the basis follows demand", "Band estimation"],
  ["2 What moves it", "Costs set the edges; capital and risk set how far the basis goes beyond", "H3 (Stage I); H4 (Stage II)"],
  ["3 Existing book", "The no-trade region moves with the existing position", "Design of the cost test"],
  ["4 One-sided", "In a ban rich futures are not corrected; cheap ones are while positions last", "H7 (Stage II)"],
  ["5 Level effect", "The ban's effect on the level has no fixed sign", "Stage II"],
  ["6 Trading", "If the rule binds on every trade, each trade closes positions", "H8 (Stage I)"],
], 0.45, 1.65, 9.1, [1.9, 4.9, 2.3], { rowH: 0.6, size: 10.5 });

s = content("Appendix", "How the data were built and checked", null, "Source: author's analysis; Stage I report, Section 5 and Appendix B",
  "Every data set is rebuilt from raw files by scripts with a report of counts and checks.");
defRows(s, [
  ["Bans", ["Next-day flags agree with the official list for 11,753 of 11,764 flags", "95% entry and 80% exit rules hold for 99.4% and 99.7% of spells"]],
  ["Basis", ["Volume-weighted futures and cash prices, net of dividends and carry", "Futures price inside the day's range for 99.8% of contracts"]],
  ["Sample", ["Near contract, next one in the last three trading days; at least five contracts", "First 20 days after F&O entry excluded; winsorised at 1% and 99% within each year"]],
  ["Reproduction", ["One script sequence produces every estimate; a full rerun reproduced every number", "Each estimator first recovered known effects on simulated data"]],
], 0.45, 1.75, 9.1, 0.95, 0.12, 1.6, 11);

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
