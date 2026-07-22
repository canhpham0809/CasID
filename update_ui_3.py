import re
import base64

with open('2026.06 BB Đối soát CMC CS - CASSO EKYC-merged.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

with open('casID-sign-view.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Zoom Controls (move higher)
html = re.sub(
    r'<div class="fixed bottom-\[\d+px\] right-4 flex flex-col gap-2 z-10 pointer-events-auto">',
    '<div class="fixed bottom-[200px] right-4 flex flex-col gap-2 z-10 pointer-events-auto">',
    html
)

# 2. Update Document Info Header
header_pattern = r'<!-- Document Info -->.*?</div>\s*<!-- PDF\.js Viewer Container -->'
new_header = """<!-- Document Info -->
            <div class="bg-white px-4 py-3 border-b border-gray-200">
                <h2 id="doc-title" class="text-[15px] font-bold text-gray-800 leading-snug mb-1">Biên bản đối soát CMC CS - CASSO EKYC</h2>
                <p id="doc-sender" class="text-xs text-gray-500">Người gửi: KySoQR.io - Hôm nay lúc 09:30</p>
            </div>

            <!-- PDF.js Viewer Container -->"""
html = re.sub(header_pattern, new_header, html, flags=re.DOTALL)

# 3. Update Bottom Action Bar
bottom_bar_pattern = r'<!-- Bottom Action Bar -->.*?</div>\s*<!-- Signature Modal \(Hidden\) -->'
new_bottom_bar = """<!-- Bottom Action Bar -->
        <div class="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-4 py-4 flex gap-3 pb-8 z-10 shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
            <button class="flex-1 py-3.5 rounded-2xl border border-gray-300 text-gray-600 font-bold text-[15px] bg-white hover:bg-gray-50 transition-colors">
                Từ chối
            </button>
            <button id="sign-done-btn" onclick="handleSignDone()"
                class="flex-[1.5] py-3.5 rounded-2xl bg-emerald-600 text-white font-bold text-[15px] shadow-lg shadow-emerald-600/30 hover:bg-emerald-700 flex items-center justify-center gap-2 transition-colors">
                Hoàn thành
            </button>
        </div>

        <!-- Signature Modal (Hidden) -->"""
html = re.sub(bottom_bar_pattern, new_bottom_bar, html, flags=re.DOTALL)

# 4. Update PDF Container
pdf_container_pattern = r'<!-- PDF Page Wrapper \(Scaling and positioning\) -->.*?<!-- Zoom Controls -->'
new_pdf_container = """<div id="pdf-pages-container" class="flex flex-col gap-4 items-center">
                    <!-- Pages will be injected here -->
                </div>
            </div>

            <!-- Zoom Controls -->"""
html = re.sub(pdf_container_pattern, new_pdf_container, html, flags=re.DOTALL)

# 5. Update Javascript Variables and documents array
# Find the start of script and replace documents
script_pattern = r'pdfjsLib\.GlobalWorkerOptions\.workerSrc = .*?;'
script_start = re.search(script_pattern, html).end()
load_pdf_start = html.find('function loadPdfJs()')

js_vars = f"""
                const pdfData = "{pdf_b64}";
                let pdfDoc = null;
                let currentScale = 1.0;
                let totalPages = 0;
                """
html = html[:script_start] + js_vars + html[load_pdf_start:]

# 6. Replace loadPdfJs, renderPage, zoomPdf, saveSignature, handleSignDone, switchDocument(delete)
# Just replace everything from loadPdfJs to the end of the script
funcs_start = html.find('function loadPdfJs()')
funcs_end = html.rfind('</script>')

new_funcs = """function loadPdfJs() {
            document.getElementById('pdf-loading').classList.remove('hidden');
            const binary_string = window.atob(pdfData);
            const len = binary_string.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }

            pdfjsLib.getDocument({ data: bytes }).promise.then(function (pdfDoc_) {
                pdfDoc = pdfDoc_;
                totalPages = pdfDoc.numPages;
                
                const container = document.getElementById('pdf-pages-container');
                container.innerHTML = '';

                for (let i = 1; i <= totalPages; i++) {
                    const wrapper = document.createElement('div');
                    wrapper.id = `page-wrapper-${i}`;
                    wrapper.className = 'relative bg-white shadow-lg mx-auto transition-all duration-200';
                    
                    const canvas = document.createElement('canvas');
                    canvas.id = `pdf-canvas-${i}`;
                    canvas.className = 'block w-full h-full';
                    wrapper.appendChild(canvas);
                    
                    const sigContainer = document.createElement('div');
                    sigContainer.id = `signature-container-${i}`;
                    sigContainer.className = 'absolute left-1/2 -translate-x-1/2 w-4/5 max-w-[300px] border-2 border-dashed border-emerald-500 bg-emerald-50/50 rounded-xl cursor-pointer flex flex-col items-center justify-center p-4 hover:bg-emerald-50 transition-colors z-20';
                    sigContainer.style.bottom = '3.5%';
                    sigContainer.onclick = function() { openSignatureModal(); };
                    
                    sigContainer.innerHTML = `
                        <div id="signature-box-${i}">
                            <i class="fa-solid fa-signature text-2xl text-emerald-600 mb-2"></i>
                            <span class="text-sm font-semibold text-emerald-700">Chạm để ký</span>
                        </div>
                        <div id="signed-result-${i}" class="absolute inset-0 bg-white rounded-xl flex items-center justify-center p-2 hidden z-30">
                            <img id="signature-image-${i}" src="" class="max-w-full max-h-full object-contain" />
                        </div>
                    `;
                    
                    wrapper.appendChild(sigContainer);
                    container.appendChild(wrapper);
                    
                    renderPage(i);
                }
                
                document.getElementById('pdf-loading').classList.add('hidden');
            }).catch(function (error) {
                console.error("Lỗi khi tải PDF:", error);
                document.getElementById('pdf-loading').innerHTML = '<span class="text-red-500">Lỗi khi tải PDF</span>';
            });
        }

        function renderPage(num) {
            pdfDoc.getPage(num).then(function(page) {
                const fitScale = window.innerWidth / page.getViewport({ scale: 1.0 }).width * 0.95;
                const viewport = page.getViewport({ scale: fitScale });
                
                if (num === 1) {
                    window.baseViewportWidth = viewport.width;
                    window.baseViewportHeight = viewport.height;
                }
                
                const wrapper = document.getElementById(`page-wrapper-${num}`);
                wrapper.style.width = Math.floor(viewport.width * currentScale) + "px";
                wrapper.style.height = Math.floor(viewport.height * currentScale) + "px";
                
                const canvas = document.getElementById(`pdf-canvas-${num}`);
                const ctx = canvas.getContext('2d');
                
                const outputScale = window.devicePixelRatio || 1;
                canvas.width = Math.floor(viewport.width * outputScale);
                canvas.height = Math.floor(viewport.height * outputScale);
                
                const renderContext = {
                    canvasContext: ctx,
                    transform: [outputScale, 0, 0, outputScale, 0, 0],
                    viewport: viewport
                };
                page.render(renderContext);
            });
        }

        function zoomPdf(delta) {
            currentScale += delta;
            if (currentScale < 0.5) currentScale = 0.5;
            if (currentScale > 3.0) currentScale = 3.0;
            
            for (let i = 1; i <= totalPages; i++) {
                const wrapper = document.getElementById(`page-wrapper-${i}`);
                if (wrapper) {
                    wrapper.style.width = Math.floor(window.baseViewportWidth * currentScale) + "px";
                    wrapper.style.height = Math.floor(window.baseViewportHeight * currentScale) + "px";
                }
            }
        }

        function handleSignDone() {
            const firstResult = document.getElementById('signed-result-1');
            if(firstResult && firstResult.classList.contains('hidden')) {
                alert("Vui lòng chạm vào khung để ký tài liệu trước!");
                return;
            }
            window.location.href = 'casso-account-login.html';
        }

        function openSignatureModal() {
            const modal = document.getElementById('signature-modal');
            const overlay = modal.querySelector('.modal-overlay');
            const content = modal.querySelector('.modal-content');
            
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            
            setTimeout(() => {
                overlay.classList.remove('opacity-0');
                content.classList.remove('translate-y-full');
            }, 10);
            
            resizeCanvas();
        }

        function closeSignatureModal() {
            const modal = document.getElementById('signature-modal');
            const overlay = modal.querySelector('.modal-overlay');
            const content = modal.querySelector('.modal-content');
            
            overlay.classList.add('opacity-0');
            content.classList.add('translate-y-full');
            
            setTimeout(() => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }, 300);
        }

        function saveSignature() {
            if (signaturePad.isEmpty()) {
                alert("Vui lòng ký trước khi lưu!");
                return;
            }
            
            const dataUrl = signaturePad.toDataURL('image/png');
            
            for (let i = 1; i <= totalPages; i++) {
                const img = document.getElementById(`signature-image-${i}`);
                const result = document.getElementById(`signed-result-${i}`);
                const box = document.getElementById(`signature-box-${i}`);
                if (img && result && box) {
                    img.src = dataUrl;
                    result.classList.remove('hidden');
                    box.classList.add('hidden');
                }
            }
            
            closeSignatureModal();
        }
        
        // Wait for fonts/icons to load then init
        window.onload = function() {
            setTimeout(loadPdfJs, 300);
        };
        """

html = html[:funcs_start] + new_funcs + "\n    " + html[funcs_end:]

with open('casID-sign-view.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Update completed.")
