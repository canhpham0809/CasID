import re

with open('casID-sign-view.html', 'r') as f:
    html = f.read()

# 1. Update Document Info HTML
doc_info_old = """            <!-- Document Info -->
            <div class="bg-white px-4 py-3 border-b border-gray-200">
                <h2 id="doc-title" class="text-[15px] font-bold text-gray-800 leading-snug mb-1">Biên bản đối soát đại lý chữ ký số
                    tháng 06/2026 (1/2)</h2>
                <p id="doc-sender" class="text-xs text-gray-500">Người gửi: KySoQR.io - Hôm nay lúc 09:30</p>
            </div>"""

doc_info_new = """            <!-- Document Info -->
            <div class="bg-white px-4 py-3 border-b border-gray-200 flex justify-between items-center">
                <div class="flex-1 pr-2">
                    <h2 id="doc-title" class="text-[15px] font-bold text-gray-800 leading-snug mb-1">Biên bản đối soát đại lý chữ ký số tháng 06/2026 (1/2)</h2>
                    <p id="doc-sender" class="text-xs text-gray-500">Người gửi: KySoQR.io - Hôm nay lúc 09:30</p>
                </div>
                <div class="flex gap-2 text-gray-400">
                    <button id="prev-doc-btn" onclick="switchDocument(-1)" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 hover:text-emerald-600 disabled:opacity-30 transition-colors"><i class="fa-solid fa-chevron-left"></i></button>
                    <button id="next-doc-btn" onclick="switchDocument(1)" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 hover:text-emerald-600 disabled:opacity-30 transition-colors"><i class="fa-solid fa-chevron-right"></i></button>
                </div>
            </div>"""

html = html.replace(doc_info_old, doc_info_new)

# 2. Update JavaScript currentDoc assignment
current_doc_old = """                const currentDoc = documents[currentDocumentIndex || 0];
                const binary_string = window.atob(currentDoc.data);"""

current_doc_new = """                documents[0].bottomPos = '3.5%';
                documents[1].bottomPos = '1%';
                const currentDoc = documents[currentDocumentIndex || 0];
                const binary_string = window.atob(currentDoc.data);
                
                // Adjust signature box position
                const sigContainer = document.getElementById('signature-container');
                if (sigContainer) sigContainer.style.bottom = currentDoc.bottomPos;
                
                updateNavButtons();"""

html = html.replace(current_doc_old, current_doc_new)

# 3. Add switchDocument and updateNavButtons functions, and change handleSignDone
js_funcs_old = """        function handleSignDone() {
            const signedResult = document.getElementById('signed-result');
            if(signedResult.classList.contains('hidden')) {
                alert("Vui lòng chạm vào khung để ký tài liệu trước!");
                return;
            }
            
            if (currentDocumentIndex === 0) {
                currentDocumentIndex = 1;
                
                document.getElementById('signature-box').classList.remove('hidden');
                signedResult.classList.add('hidden');
                document.getElementById('signature-image').src = "";
                
                document.getElementById('pdf-loading').classList.remove('hidden');
                ctxPdf.clearRect(0, 0, canvasPdf.width, canvasPdf.height);
                
                loadPdfJs();
                
                // Reset Zoom
                currentScale = 1.0;
                document.getElementById('pdf-page-wrapper').style.transform = `scale(1)`;
                document.getElementById('pdf-scroll-container').scrollTop = 0;
                
                const btn = document.getElementById('sign-done-btn');
                btn.innerHTML = 'Chưa ký tài liệu (2/2)';
            } else {
                window.location.href = 'casso-account-login.html';
            }
        }"""

js_funcs_new = """        function switchDocument(dir) {
            const newIndex = currentDocumentIndex + dir;
            // Prevent out of bounds
            if (newIndex >= 0 && newIndex < 2) {
                currentDocumentIndex = newIndex;
                
                document.getElementById('signature-box').classList.remove('hidden');
                document.getElementById('signed-result').classList.add('hidden');
                document.getElementById('signature-image').src = "";
                
                document.getElementById('pdf-loading').classList.remove('hidden');
                ctxPdf.clearRect(0, 0, canvasPdf.width, canvasPdf.height);
                
                loadPdfJs();
                
                // Reset Zoom
                currentScale = 1.0;
                document.getElementById('pdf-page-wrapper').style.transform = `scale(1)`;
                document.getElementById('pdf-scroll-container').scrollTop = 0;
                
                const btn = document.getElementById('sign-done-btn');
                if (currentDocumentIndex === 0) {
                    btn.innerHTML = 'Ký tiếp (1/2) <i class="fa-solid fa-arrow-right"></i>';
                } else {
                    btn.innerHTML = 'Chưa ký tài liệu (2/2)';
                }
            }
        }

        function updateNavButtons() {
            const prevBtn = document.getElementById('prev-doc-btn');
            const nextBtn = document.getElementById('next-doc-btn');
            if(prevBtn) prevBtn.disabled = currentDocumentIndex === 0;
            if(nextBtn) nextBtn.disabled = currentDocumentIndex === 1;
        }

        function handleSignDone() {
            const signedResult = document.getElementById('signed-result');
            if(signedResult.classList.contains('hidden')) {
                alert("Vui lòng chạm vào khung để ký tài liệu trước!");
                return;
            }
            
            if (currentDocumentIndex === 0) {
                switchDocument(1);
            } else {
                window.location.href = 'casso-account-login.html';
            }
        }"""

html = html.replace(js_funcs_old, js_funcs_new)

with open('casID-sign-view.html', 'w') as f:
    f.write(html)

