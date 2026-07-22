import re
import base64

with open('2026.06 BB Đối soát CMC CS - CASSO EKYC.pdf', 'rb') as f:
    pdf1 = base64.b64encode(f.read()).decode('utf-8')
    
with open('2026.06 BB Đối soát CMC CS - CASSO.pdf', 'rb') as f:
    pdf2 = base64.b64encode(f.read()).decode('utf-8')

with open('casID-sign-view.html', 'r') as f:
    html = f.read()

# Replace the single base64 string injection with a multi-document JS variable array
# We need to find the window.atob("...") part.
pattern = re.compile(r'const binary_string = window\.atob\("(.*?)"\);', re.DOTALL)

replacement = f"""
                const documents = [
                    {{
                        title: "Biên bản đối soát đại lý chữ ký số tháng 06/2026 (1/2)",
                        sender: "Người gửi: KySoQR.io - Hôm nay lúc 09:30",
                        data: "{pdf1}"
                    }},
                    {{
                        title: "Biên bản đối soát CMC CS - CASSO (2/2)",
                        sender: "Người gửi: KySoQR.io - Hôm nay lúc 09:35",
                        data: "{pdf2}"
                    }}
                ];
                
                const currentDoc = documents[currentDocumentIndex || 0];
                const binary_string = window.atob(currentDoc.data);
                
                // Update title
                const titleEl = document.getElementById('doc-title');
                const senderEl = document.getElementById('doc-sender');
                if(titleEl) titleEl.innerText = currentDoc.title;
                if(senderEl) senderEl.innerText = currentDoc.sender;
"""

new_html = pattern.sub(replacement, html)

with open('casID-sign-view.html', 'w') as f:
    f.write(new_html)

