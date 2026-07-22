import re
with open('/tmp/pdf_base64.txt', 'r') as f:
    b64 = f.read().strip()

with open('/Users/canhphq/CanhPHQ/0207_CassoAccount/Casso ID/casID-sign-view.html', 'r') as f:
    html = f.read()

# Remove the script tag logic
html = re.sub(r'const dataScript = document\.createElement.*?document\.head\.appendChild\(dataScript\);', 'loadPdfJs();', html, flags=re.DOTALL)

# Replace the base64 variable
html = html.replace('const binary_string = window.atob(pdfBase64Data);', f'const binary_string = window.atob("{b64}");')

with open('/Users/canhphq/CanhPHQ/0207_CassoAccount/Casso ID/casID-sign-view.html', 'w') as f:
    f.write(html)
