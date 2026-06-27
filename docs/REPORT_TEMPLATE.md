# Weekly Report Template (supervisor-mandated)

This file captures the **exact format** Dr. Nguyen Quoc Hung requires for the weekly thesis
report, so any session can reproduce it. Sample filled reports are in `reports/`.

## Format rules
- **Bilingual:** Vietnamese line (normal) + English line (italic, grey) for every item.
- Font **Times New Roman**, A4, headings bold.
- Built with `docx` (Node). See `build_baocao_tuan3.js` for a working generator to copy.

## Structure (in order)
1. **Title** — `BÁO CÁO KHÓA LUẬN TUẦN N` / `THESIS WEEK N REPORT` (centered).
2. **1. Thông tin sinh viên / Student's Name** — `[Điền họ và tên]` (still unresolved).
3. **2. Tên đề tài / Thesis's title** — VN + EN (see PROGRESS_LOG for the exact title).
4. **3. Công việc / Tasks** — table, 3 columns:
   `Thời gian / Time` | `Nội dung công việc theo tuần / Content of the week's work` | `Hoàn thành / Completion (%)`
   One row for the week, with the week's date range and a 100% (or actual) completion.
5. **4. Báo cáo tiến độ / Progress report** — table, 4 columns, one row per working day:
   `Ngày / Date` | `Công việc / Tasks` | `Người tham gia / Participants` | `Vai trò / Roles`
   (Participants = the student; 5 daily rows Mon–Fri.)
6. **(optional) Kết quả chính / Key results** — tables and embedded figures when the week
   produced results (e.g., Week 3 embedded the pipeline diagram + model-comparison chart and a
   real metrics table).
7. **N. Đề xuất công việc tiếp theo / Proposed next tasks** — bilingual bullet list.
8. **Footer** — `TP. HCM, ngày DD tháng MM năm 2026` / `Ho Chi Minh City, ...` then
   `Giảng Viên Hướng Dẫn / Supervisor` and `TS. Nguyễn Quốc Hưng` (centered).

## Per-student fill-ins (always)
- Student full name + Student ID (placeholder `[Điền họ và tên]` / `[MSSV]`).
- Adjust the week's date range to the real faculty calendar.

## Supervisor feedback incorporated (running list)
- Week 2 → 3: add detailed source descriptions, a Data Integration Pipeline diagram, more
  visualizations (label/length/URL/domain), explicit dedup criteria, and a data-quality
  assessment. Emphasis on **method description, scientific justification, and reproducibility**.
