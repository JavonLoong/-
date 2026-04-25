import sys, os
scripts_dir = os.path.join('d:\\', '\u865a\u62dfc\u76d8', '\u6d41\u4f53\u529b\u5b66', '.agents', 'skills', 'office_automation', 'scripts')
sys.path.insert(0, scripts_dir)
from office_com import Officer
word = Officer.Word
word.Visible = False
word.DisplayAlerts = False
base = os.path.join('d:\\', '\u865a\u62dfc\u76d8', '\u6d41\u4f53\u529b\u5b66', '\u671f\u4e2d\u590d\u4e60', '\u590d\u4e60\u603b\u7ed3')
files = ['\u8003\u8bd5\u8303\u56f4.docx', '\u6d41\u529b\u8003\u70b9\u9884\u6d4b.docx', '\u6c34\u529b\u5b66\u590d\u4e60\u6458\u8981.doc']
for f in files:
    fp = os.path.join(base, f)
    doc = word.Documents.Open(fp)
    text = doc.Content.Text
    doc.Close(False)
    print(f'=== {f} ===')
    print(text[:3000])
    print()
Officer.Quit('Word')
