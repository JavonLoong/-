import fitz, os
pdf_path = os.path.join('d:\\', '\u865a\u62dfc\u76d8', '\u6d41\u4f53\u529b\u5b66', '\u671f\u4e2d\u590d\u4e60', '\u671f\u4e2d\u901f\u67e5\u8868.pdf')
out_dir = os.path.join('d:\\', '\u865a\u62dfc\u76d8', '\u6d41\u4f53\u529b\u5b66', '\u671f\u4e2d\u590d\u4e60')
doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    out = os.path.join(out_dir, f'_p{i+1}.png')
    pix.save(out)
    print(f'Page {i+1}: {pix.width}x{pix.height}')
doc.close()
