const fs=require("fs");
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,ImageRun,AlignmentType,BorderStyle,WidthType,ShadingType,VerticalAlign}=require("docx");
const FONT="Times New Roman", FIG="results/figures/";
const cb={style:BorderStyle.SINGLE,size:4,color:"000000"}; const borders={top:cb,bottom:cb,left:cb,right:cb};
function p(t,o={}){return new Paragraph({spacing:{after:o.after??0,line:276},alignment:o.align,children:[new TextRun({text:t,font:FONT,size:o.size??24,bold:o.bold,italics:o.italics,color:o.color})]});}
function img(path,w,h,cap){const a=[new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:80,after:20},children:[new ImageRun({data:fs.readFileSync(path),transformation:{width:w,height:h}})]})];if(cap)a.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:160},children:[new TextRun({text:cap,italics:true,font:FONT,size:20,color:"404040"})]}));return a;}
function bi(vn,en,s=22){return [new Paragraph({spacing:{after:20},children:[new TextRun({text:vn,font:FONT,size:s})]}),new Paragraph({spacing:{after:60},children:[new TextRun({text:en,font:FONT,size:s,italics:true,color:"404040"})]})];}
function cell(w,paras,o={}){return new TableCell({borders,width:{size:w,type:WidthType.DXA},margins:{top:60,bottom:60,left:90,right:90},verticalAlign:o.valign??VerticalAlign.TOP,shading:o.fill?{fill:o.fill,type:ShadingType.CLEAR}:undefined,children:paras});}
function hc(w,vn,en){return cell(w,[new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:10},children:[new TextRun({text:vn,bold:true,font:FONT,size:21})]}),new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:en,bold:true,italics:true,font:FONT,size:21,color:"404040"})]})],{fill:"D9D9D9",valign:VerticalAlign.CENTER});}

// ---- 3. Tasks table ----
const W3=[1900,5326,1800];
const tasks=new Table({width:{size:9026,type:WidthType.DXA},columnWidths:W3,rows:[
 new TableRow({tableHeader:true,children:[hc(W3[0],"Thời gian","Time"),hc(W3[1],"Nội dung công việc theo tuần","Content of the week's work"),hc(W3[2],"Hoàn thành","Completion")]}),
 new TableRow({children:[
  cell(W3[0],[new Paragraph({children:[new TextRun({text:"Tuần 4 / Week 4",bold:true,font:FONT,size:22})]}),new Paragraph({children:[new TextRun({text:"(23/06/2026 – 27/06/2026)",bold:true,font:FONT,size:22})]})]),
  cell(W3[1],[
   ...bi("- Phân tích nguyên nhân chênh lệch giữa các mô hình (SVM > LR; RF/DT thấp hơn; NB precision cao – recall thấp).","Analyze why models differ (SVM > LR; RF/DT lower; NB high precision, low recall)."),
   ...bi("- Error Analysis (FP/FN, nguồn khó); kiểm định McNemar + Bootstrap CI 95%; Calibration Curve.","Error analysis (FP/FN, hard sources); McNemar + 95% bootstrap CI; calibration curves."),
   ...bi("- Bổ sung timing & retention từng bước pipeline; triển khai SHAP (toàn cục) + LIME (cục bộ) + nhất quán.","Add per-step pipeline timing & retention; SHAP (global) + LIME (local) + consistency."),
   ...bi("- Chuẩn bị script fine-tune transformer (BERT/DistilBERT/RoBERTa) cho GPU.","Prepare transformer fine-tuning script (BERT/DistilBERT/RoBERTa) for GPU."),
  ]),
  cell(W3[2],[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:"90%",bold:true,font:FONT,size:22})]}),new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:"(transformer: chờ GPU)",italics:true,font:FONT,size:18,color:"404040"})]})],{valign:VerticalAlign.CENTER}),
 ]}),
]});

// ---- 4. Daily progress table (the missing piece) ----
const W4=[1500,3526,2000,2000];
function dayRow(dVN,dEN,tVN,tEN,rVN,rEN){return new TableRow({children:[
 cell(W4[0],[new Paragraph({spacing:{after:10},children:[new TextRun({text:dVN,bold:true,font:FONT,size:21})]}),new Paragraph({children:[new TextRun({text:dEN,italics:true,font:FONT,size:21,color:"404040"})]})]),
 cell(W4[1],bi(tVN,tEN,21)),
 cell(W4[2],[new Paragraph({spacing:{after:10},children:[new TextRun({text:"[Họ tên SV]",font:FONT,size:21})]}),new Paragraph({children:[new TextRun({text:"[Student name]",italics:true,font:FONT,size:21,color:"404040"})]})]),
 cell(W4[3],bi(rVN,rEN,21)),
]});}
const progress=new Table({width:{size:9026,type:WidthType.DXA},columnWidths:W4,rows:[
 new TableRow({tableHeader:true,children:[hc(W4[0],"Ngày","Date"),hc(W4[1],"Công việc","Tasks"),hc(W4[2],"Người tham gia","Participants"),hc(W4[3],"Vai trò","Roles")]}),
 dayRow("23/06/2026","Jun 23, 2026","Phân tích nguyên nhân chênh lệch giữa 5 mô hình dựa trên confusion matrix và đặc điểm thuật toán.","Analyze the performance gaps among the 5 models from confusion matrices and algorithm characteristics.","Phân tích mô hình.","Model analysis."),
 dayRow("24/06/2026","Jun 24, 2026","Thực hiện Error Analysis (FP/FN, lỗi theo nguồn) và kiểm định thống kê McNemar + Bootstrap CI 95%.","Run error analysis (FP/FN, per-source errors) and statistical tests: McNemar + 95% bootstrap CI.","Kiểm định & phân tích lỗi.","Testing & error analysis."),
 dayRow("25/06/2026","Jun 25, 2026","Vẽ Calibration Curve cho 5 mô hình; bổ sung timing & retention từng bước của Data Integration Pipeline.","Plot calibration curves for the 5 models; add per-step timing & retention for the data integration pipeline.","Hiệu chỉnh & pipeline.","Calibration & pipeline."),
 dayRow("26/06/2026","Jun 26, 2026","Triển khai SHAP (toàn cục) và LIME (cục bộ) trên mô hình tốt nhất; đo nhất quán SHAP–LIME.","Implement SHAP (global) and LIME (local) on the best model; measure SHAP–LIME consistency.","Diễn giải mô hình (XAI).","Explainability (XAI)."),
 dayRow("27/06/2026","Jun 27, 2026","Chuẩn bị & kiểm thử script fine-tune transformer cho GPU; tổng hợp kết quả và viết báo cáo.","Prepare & test the transformer fine-tuning script for GPU; compile results and write the report.","Chuẩn bị transformer & báo cáo.","Transformer prep & reporting."),
]});

// ---- 5. stats table ----
const W5=[2600,2200,2100,2100];
function r5(c,o={}){return new TableRow({children:c.map((t,i)=>cell(W5[i],[new Paragraph({alignment:i===0?AlignmentType.LEFT:AlignmentType.CENTER,children:[new TextRun({text:t,font:FONT,size:20,bold:o.bold})]})],o.fill?{fill:o.fill}:{}))});}
const stats=new Table({width:{size:9000,type:WidthType.DXA},columnWidths:W5,rows:[
 new TableRow({tableHeader:true,children:[hc(W5[0],"Mô hình","Model"),hc(W5[1],"F1 [CI 95%]","F1 [95% CI]"),hc(W5[2],"McNemar vs SVM (p)","McNemar p"),hc(W5[3],"Ý nghĩa","Significant?")]}),
 r5(["Linear SVM","0.9826 [.9806–.9845]","—","(mốc tốt nhất)"],{bold:true,fill:"EAF2EA"}),
 r5(["Logistic Regression","0.9792 [.9769–.9814]","3.9e-06","Có"]),
 r5(["Random Forest","0.9764 [.9740–.9787]","4.6e-09","Có"]),
 r5(["Naive Bayes","0.9633 [.9603–.9660]","1.9e-30","Có"]),
 r5(["Decision Tree","0.9557 [.9524–.9589]","1.1e-51","Có"]),
]});
// error table
const W6=[3000,3000,3000];
function r6(c,o={}){return new TableRow({children:c.map((t,i)=>cell(W6[i],[new Paragraph({alignment:i===0?AlignmentType.LEFT:AlignmentType.CENTER,children:[new TextRun({text:t,font:FONT,size:20,bold:o.bold})]})],o.fill?{fill:o.fill}:{}))});}
const errtab=new Table({width:{size:9000,type:WidthType.DXA},columnWidths:W6,rows:[
 new TableRow({tableHeader:true,children:[hc(W6[0],"Chỉ tiêu lỗi (SVM)","Error metric (SVM)"),hc(W6[1],"Giá trị","Value"),hc(W6[2],"Nguồn khó nhất","Hardest source")]}),
 r6(["False Positive","227 (3.43%)","SpamAssassin 4.52%"]),
 r6(["False Negative","62 (0.76%)","Nazario 3.79%"]),
]});

const doc=new Document({styles:{default:{document:{run:{font:FONT,size:24}}}},sections:[{
 properties:{page:{size:{width:11906,height:16838},margin:{top:1440,right:1440,bottom:1440,left:1440}}},
 children:[
  p("BÁO CÁO KHÓA LUẬN TUẦN 4",{bold:true,size:28,align:AlignmentType.CENTER,after:20}),
  p("THESIS WEEK 4 REPORT",{bold:true,italics:true,size:24,align:AlignmentType.CENTER,after:240,color:"404040"}),
  new Paragraph({spacing:{after:20},children:[new TextRun({text:"1. Thông tin sinh viên: ",bold:true,font:FONT,size:24}),new TextRun({text:"[Điền họ và tên của bạn]",font:FONT,size:24})]}),
  new Paragraph({spacing:{after:160},children:[new TextRun({text:"    Student's Name: ",bold:true,italics:true,font:FONT,size:24,color:"404040"}),new TextRun({text:"[Your full name]",italics:true,font:FONT,size:24,color:"404040"})]}),
  new Paragraph({spacing:{after:20},children:[new TextRun({text:"2. Tên đề tài: ",bold:true,font:FONT,size:24}),new TextRun({text:"Khung Trí tuệ Nhân tạo Khả diễn giải cho Phát hiện Email Lừa đảo Đáng tin cậy: Xây dựng Bộ dữ liệu Đa nguồn, Diễn giải bằng SHAP–LIME và Phân tích Tính bền vững trước Tấn công Đối kháng.",font:FONT,size:24})]}),
  new Paragraph({spacing:{after:200},children:[new TextRun({text:"    Thesis's title: ",bold:true,italics:true,font:FONT,size:24,color:"404040"}),new TextRun({text:"An Explainable AI Framework for Trustworthy Phishing Email Detection: Multi-Source Dataset Construction, SHAP–LIME Interpretability, and Adversarial Robustness.",italics:true,font:FONT,size:24,color:"404040"})]}),

  p("3. Công việc / Tasks:",{bold:true,size:24,after:100}), tasks, p("",{after:240}),
  p("4. Báo cáo tiến độ / Progress report:",{bold:true,size:24,after:100}), progress, p("",{after:240}),

  p("5. Phân tích nguyên nhân & kiểm định thống kê / Why-analysis & statistical tests",{bold:true,size:24,after:80}),
  p("McNemar khẳng định Linear SVM vượt trội có ý nghĩa thống kê so với cả 4 mô hình (p < 0.001). SVM tối đa hóa biên nên tổng quát hóa tốt hơn LR trên TF-IDF thưa 20k chiều; cây (RF/DT) kém hơn do chia trục từng đặc trưng; Naive Bayes precision cao nhưng recall thấp do lỗi tập trung ở Nazario (phishing thật, 21.6%).",{size:22,after:100}),
  stats, p("",{after:200}),

  p("6. Error Analysis / Error analysis",{bold:true,size:24,after:80}),
  p("SVM thiên về false positive (over-flag email hợp pháp) hơn là bỏ sót phishing — kiểu lỗi an toàn hơn cho bộ lọc bảo mật.",{size:22,after:80}),
  errtab, p("",{after:200}),

  p("7. Pipeline timing & retention",{bold:true,size:24,after:60}),
  p("Load+merge 2.38s (82,486) → loại body rỗng 0.39s (−5) → dedup 0.36s (−0) → split 0.17s. Retention = 99.99% (train 67,657 / test 14,824).",{italics:true,size:22,color:"404040",after:200}),

  p("8. Explainable AI: SHAP vs LIME / Explainability",{bold:true,size:24,after:60}),
  p("SHAP (toàn cục) cho thấy bias đã DỊCH từ CEAS (python/opensuse) sang Enron (enron, vince, wrote, pm) — đa nguồn giảm phụ thuộc một corpus nhưng chưa loại bỏ artifact. LIME (cục bộ) nêu được dấu hiệu phishing thật (click, account, alert, lose). Hai phương pháp BỔ SUNG nhau: Jaccard 8.1%, Pearson 0.787.",{size:22,after:80}),
  ...img(FIG+"shap_vs_lime.png",540,250,"Hình 1. So sánh SHAP (toàn cục) và LIME (cục bộ) / Global SHAP vs. local LIME."),
  ...img(FIG+"calibration_curves.png",380,350,"Hình 2. Calibration curves của 5 mô hình / Calibration curves."),

  p("9. Đề xuất công việc tiếp theo / Proposed next tasks:",{bold:true,size:24,after:80}),
  new Paragraph({bullet:{level:0},spacing:{after:20},children:[new TextRun({text:"Chạy fine-tune BERT/DistilBERT/RoBERTa trên GPU; so sánh toàn diện ML cổ điển vs transformer + McNemar.",font:FONT,size:24})]}),
  new Paragraph({bullet:{level:0},spacing:{after:120},children:[new TextRun({text:"Run BERT/DistilBERT/RoBERTa fine-tuning on GPU; full classical-vs-transformer comparison + McNemar.",italics:true,font:FONT,size:24,color:"404040"})]}),
  new Paragraph({bullet:{level:0},spacing:{after:20},children:[new TextRun({text:"Mở rộng SHAP/LIME và tiến tới đánh giá tính bền vững đối kháng (adversarial robustness).",font:FONT,size:24})]}),
  new Paragraph({bullet:{level:0},spacing:{after:120},children:[new TextRun({text:"Expand SHAP/LIME and proceed to adversarial robustness evaluation.",italics:true,font:FONT,size:24,color:"404040"})]}),

  p("TP. HCM, ngày 27 tháng 06 năm 2026",{italics:true,size:24,align:AlignmentType.CENTER,after:0}),
  p("Ho Chi Minh City, June 27, 2026",{italics:true,size:22,align:AlignmentType.CENTER,after:200,color:"404040"}),
  p("Giảng Viên Hướng Dẫn",{bold:true,size:24,align:AlignmentType.CENTER,after:0}),
  p("Supervisor",{bold:true,italics:true,size:22,align:AlignmentType.CENTER,after:600,color:"404040"}),
  p("TS. Nguyễn Quốc Hưng",{bold:true,size:24,align:AlignmentType.CENTER}),
 ],
}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("/home/claude/BaoCao_KhoaLuan_Tuan4.docx",b);console.log("written");});
