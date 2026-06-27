const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
} = require("docx");

const FONT = "Times New Roman";
const cb = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: cb, bottom: cb, left: cb, right: cb };
const FIG = "results/figures/";

function p(text, o = {}) {
  return new Paragraph({ spacing: { after: o.after ?? 0, line: 276 }, alignment: o.align,
    children: [new TextRun({ text, font: FONT, size: o.size ?? 24, bold: o.bold, italics: o.italics, color: o.color })] });
}
function img(path, w, h, cap) {
  const arr = [ new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 20 },
    children: [ new ImageRun({ data: fs.readFileSync(path), transformation: { width: w, height: h } }) ] }) ];
  if (cap) arr.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 },
    children: [ new TextRun({ text: cap, italics: true, font: FONT, size: 20, color: "404040" }) ] }));
  return arr;
}
function biPara(vn, en, size = 22) {
  return [ new Paragraph({ spacing: { after: 20 }, children: [new TextRun({ text: vn, font: FONT, size })] }),
    new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: en, font: FONT, size, italics: true, color: "404040" })] }) ];
}
function cell(width, paras, o = {}) {
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 90, right: 90 }, verticalAlign: o.valign ?? VerticalAlign.TOP,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR } : undefined, children: paras });
}
function hc(width, vn, en) {
  return cell(width, [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 10 }, children: [new TextRun({ text: vn, bold: true, font: FONT, size: 22 })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: en, bold: true, italics: true, font: FONT, size: 22, color: "404040" })] }),
  ], { fill: "D9D9D9", valign: VerticalAlign.CENTER });
}

// Tasks table
const W3 = [1900, 5326, 1800];
const tasksTable = new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: W3, rows: [
  new TableRow({ tableHeader: true, children: [hc(W3[0],"Thời gian","Time"), hc(W3[1],"Nội dung công việc theo tuần","Content of the week's work"), hc(W3[2],"Hoàn thành","Completion")] }),
  new TableRow({ children: [
    cell(W3[0], [ new Paragraph({ children: [new TextRun({ text: "Tuần 3 / Week 3", bold: true, font: FONT, size: 22 })] }),
                 new Paragraph({ children: [new TextRun({ text: "(16/06/2026 – 20/06/2026)", bold: true, font: FONT, size: 22 })] }) ]),
    cell(W3[1], [
      ...biPara("- Bổ sung theo góp ý Tuần 2: mô tả chi tiết 6 nguồn, sơ đồ Data Integration Pipeline, thêm biểu đồ trực quan, làm rõ tiêu chí khử trùng lặp và đánh giá chất lượng dữ liệu.",
                "Week-2 supplements per feedback: detailed source descriptions, Data Integration Pipeline diagram, extra visualizations, dedup criteria, and data-quality assessment."),
      ...biPara("- Hoàn thiện tiền xử lý văn bản: chuẩn hóa Unicode (NFKC), làm sạch HTML, thay URL/email/điện thoại bằng token, chuẩn hóa ký tự & khoảng trắng.",
                "Finalize preprocessing: Unicode (NFKC), HTML cleaning, URL/email/phone tokenization, special-char & whitespace normalization."),
      ...biPara("- Trích đặc trưng TF-IDF (1–2 gram); sweep số đặc trưng để chọn max_features=20.000.",
                "TF-IDF extraction (1–2 gram); feature-count sweep selecting max_features=20,000."),
      ...biPara("- Huấn luyện 5 mô hình ML (LR, NB, DT, RF, Linear SVM) và đánh giá Accuracy/Precision/Recall/F1/ROC-AUC/PR-AUC + Confusion Matrix; lưu mô hình & kết quả.",
                "Train 5 ML models (LR, NB, DT, RF, Linear SVM) with Accuracy/Precision/Recall/F1/ROC-AUC/PR-AUC + confusion matrices; save models & results."),
    ]),
    cell(W3[2], [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "100%", bold: true, font: FONT, size: 22 })] })], { valign: VerticalAlign.CENTER }),
  ]}),
]});

// Daily table
const W4 = [1500, 3526, 2000, 2000];
function dayRow(dVN, dEN, tVN, tEN, rVN, rEN) {
  return new TableRow({ children: [
    cell(W4[0], [ new Paragraph({ spacing: { after: 10 }, children: [new TextRun({ text: dVN, bold: true, font: FONT, size: 21 })] }),
                  new Paragraph({ children: [new TextRun({ text: dEN, italics: true, font: FONT, size: 21, color: "404040" })] }) ]),
    cell(W4[1], biPara(tVN, tEN, 21)),
    cell(W4[2], [ new Paragraph({ spacing: { after: 10 }, children: [new TextRun({ text: "[Họ tên SV]", font: FONT, size: 21 })] }),
                  new Paragraph({ children: [new TextRun({ text: "[Student name]", italics: true, font: FONT, size: 21, color: "404040" })] }) ]),
    cell(W4[3], biPara(rVN, rEN, 21)),
  ]});
}
const progressTable = new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: W4, rows: [
  new TableRow({ tableHeader: true, children: [hc(W4[0],"Ngày","Date"), hc(W4[1],"Công việc","Tasks"), hc(W4[2],"Người tham gia","Participants"), hc(W4[3],"Vai trò","Roles")] }),
  dayRow("16/06/2026","Jun 16, 2026","Bổ sung mô tả 6 nguồn dữ liệu và vẽ sơ đồ Data Integration Pipeline.","Add detailed descriptions of the 6 sources and draw the Data Integration Pipeline diagram.","Tài liệu hóa dữ liệu.","Data documentation."),
  dayRow("17/06/2026","Jun 17, 2026","Sinh thêm biểu đồ (đóng góp dataset, phân bố nhãn theo nguồn, độ dài email, số URL, domain người gửi); viết đánh giá chất lượng dữ liệu.","Generate extra charts (dataset contribution, per-source labels, email length, URL count, sender domains); write the data-quality assessment.","Trực quan hóa & đánh giá.","Visualization & assessment."),
  dayRow("18/06/2026","Jun 18, 2026","Hoàn thiện tiền xử lý (NFKC, HTML, token URL/email/điện thoại); chạy sweep TF-IDF chọn 20.000 đặc trưng.","Finalize preprocessing (NFKC, HTML, URL/email/phone tokens); run the TF-IDF sweep selecting 20,000 features.","Tiền xử lý & đặc trưng.","Preprocessing & features."),
  dayRow("19/06/2026","Jun 19, 2026","Huấn luyện 5 mô hình ML và đánh giá đa chỉ số trên tập test (14.824 email).","Train the 5 ML models and run multi-metric evaluation on the test set (14,824 emails).","Huấn luyện & đánh giá.","Training & evaluation."),
  dayRow("20/06/2026","Jun 20, 2026","Lưu mô hình, vectorizer và kết quả (JSON, biểu đồ) phục vụ tái lập; đẩy mã lên GitHub.","Save models, vectorizer, and results (JSON, figures) for reproducibility; push to GitHub.","Lưu trữ & tái lập.","Artifacts & reproducibility."),
]});

// Results table (REAL values)
const W6 = [2600, 1180, 1180, 1180, 1180, 1180, 1180];
function mrow(cells, opts={}) {
  return new TableRow({ children: cells.map((t,i)=> cell(W6[i],[new Paragraph({alignment: i===0?AlignmentType.LEFT:AlignmentType.CENTER, children:[new TextRun({text:t,font:FONT,size:20,bold:opts.bold})]})], opts.fill?{fill:opts.fill}:{})) });
}
const resTable = new Table({ width:{size:9700,type:WidthType.DXA}, columnWidths:W6, rows:[
  new TableRow({ tableHeader:true, children:[hc(W6[0],"Mô hình","Model"),hc(W6[1],"Acc","Acc"),hc(W6[2],"Prec","Prec"),hc(W6[3],"Recall","Recall"),hc(W6[4],"F1","F1"),hc(W6[5],"ROC-AUC","ROC"),hc(W6[6],"PR-AUC","PR")] }),
  mrow(["Linear SVM","0.9805","0.9729","0.9924","0.9826","0.9983","0.9985"],{bold:true,fill:"EAF2EA"}),
  mrow(["Logistic Regression","0.9767","0.9684","0.9901","0.9792","0.9973","0.9978"]),
  mrow(["Random Forest","0.9737","0.9726","0.9801","0.9763","0.9968","0.9971"]),
  mrow(["Naive Bayes","0.9603","0.9897","0.9381","0.9632","0.9965","0.9972"]),
  mrow(["Decision Tree","0.9510","0.9571","0.9543","0.9557","0.9516","0.9402"]),
]});

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 24 } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      p("BÁO CÁO KHÓA LUẬN TUẦN 3", { bold: true, size: 28, align: AlignmentType.CENTER, after: 20 }),
      p("THESIS WEEK 3 REPORT", { bold: true, italics: true, size: 24, align: AlignmentType.CENTER, after: 240, color: "404040" }),

      new Paragraph({ spacing: { after: 20 }, children: [ new TextRun({ text: "1. Thông tin sinh viên: ", bold: true, font: FONT, size: 24 }), new TextRun({ text: "[Điền họ và tên của bạn]", font: FONT, size: 24 }) ] }),
      new Paragraph({ spacing: { after: 160 }, children: [ new TextRun({ text: "    Student's Name: ", bold: true, italics: true, font: FONT, size: 24, color: "404040" }), new TextRun({ text: "[Your full name]", italics: true, font: FONT, size: 24, color: "404040" }) ] }),
      new Paragraph({ spacing: { after: 20 }, children: [ new TextRun({ text: "2. Tên đề tài: ", bold: true, font: FONT, size: 24 }), new TextRun({ text: "Khung Trí tuệ Nhân tạo Khả diễn giải cho Phát hiện Email Lừa đảo Đáng tin cậy: Xây dựng Bộ dữ liệu Đa nguồn, Diễn giải bằng SHAP–LIME và Phân tích Tính bền vững trước Tấn công Đối kháng.", font: FONT, size: 24 }) ] }),
      new Paragraph({ spacing: { after: 200 }, children: [ new TextRun({ text: "    Thesis's title: ", bold: true, italics: true, font: FONT, size: 24, color: "404040" }), new TextRun({ text: "An Explainable AI Framework for Trustworthy Phishing Email Detection: Multi-Source Dataset Construction, SHAP–LIME Interpretability, and Adversarial Robustness.", italics: true, font: FONT, size: 24, color: "404040" }) ] }),

      p("3. Công việc / Tasks:", { bold: true, size: 24, after: 100 }),
      tasksTable,
      p("", { after: 240 }),

      p("4. Báo cáo tiến độ / Progress report:", { bold: true, size: 24, after: 100 }),
      progressTable,
      p("", { after: 240 }),

      p("5. Bổ sung theo góp ý Tuần 2 / Week-2 supplements", { bold: true, size: 24, after: 80 }),
      ...img(FIG+"data_integration_pipeline.png", 470, 292, "Hình 1. Sơ đồ Data Integration Pipeline / Data integration pipeline."),
      ...img(FIG+"phishing_rate_per_source.png", 500, 270, "Hình 2. Phân bố phishing/legitimate theo từng nguồn / Phishing vs. legitimate per source."),

      p("6. Kết quả Tuần 3: so sánh 5 mô hình (tập test, N = 14.824) / Week-3 results: 5-model comparison", { bold: true, size: 24, after: 100 }),
      resTable,
      p("", { after: 60 }),
      p("Linear SVM đạt kết quả tốt nhất (F1 = 0.9826). Sweep TF-IDF cho thấy F1 bão hòa sau 20.000 đặc trưng (50.000 chỉ tăng +0.0003).", { italics: true, size: 22, color: "404040", after: 120 }),
      ...img(FIG+"model_comparison.png", 540, 245, "Hình 3. So sánh đa chỉ số 5 mô hình / Multi-metric comparison of 5 models."),

      p("7. Đề xuất công việc tiếp theo / Proposed next tasks:", { bold: true, size: 24, after: 80 }),
      new Paragraph({ bullet: { level: 0 }, spacing: { after: 20 }, children: [new TextRun({ text: "Fine-tune các mô hình transformer (BERT, DistilBERT, RoBERTa) trên môi trường GPU (Colab/Kaggle) và so sánh với nhóm ML cổ điển bằng McNemar's Test.", font: FONT, size: 24 })] }),
      new Paragraph({ bullet: { level: 0 }, spacing: { after: 120 }, children: [new TextRun({ text: "Fine-tune transformer models (BERT, DistilBERT, RoBERTa) on a GPU environment and compare against the classical ML group via McNemar's test.", italics: true, font: FONT, size: 24, color: "404040" })] }),
      new Paragraph({ bullet: { level: 0 }, spacing: { after: 20 }, children: [new TextRun({ text: "Bổ sung khoảng tin cậy bootstrap 95% cho các chỉ số chính của 5 mô hình hiện tại.", font: FONT, size: 24 })] }),
      new Paragraph({ bullet: { level: 0 }, spacing: { after: 120 }, children: [new TextRun({ text: "Add 95% bootstrap confidence intervals for the main metrics of the current 5 models.", italics: true, font: FONT, size: 24, color: "404040" })] }),

      p("TP. HCM, ngày 20 tháng 06 năm 2026", { italics: true, size: 24, align: AlignmentType.CENTER, after: 0 }),
      p("Ho Chi Minh City, June 20, 2026", { italics: true, size: 22, align: AlignmentType.CENTER, after: 200, color: "404040" }),
      p("Giảng Viên Hướng Dẫn", { bold: true, size: 24, align: AlignmentType.CENTER, after: 0 }),
      p("Supervisor", { bold: true, italics: true, size: 22, align: AlignmentType.CENTER, after: 600, color: "404040" }),
      p("TS. Nguyễn Quốc Hưng", { bold: true, size: 24, align: AlignmentType.CENTER }),
    ],
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync("/home/claude/BaoCao_KhoaLuan_Tuan3.docx", b); console.log("written"); });
