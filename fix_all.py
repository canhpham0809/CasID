import base64, re

# Read PDF and encode
with open('2026.06 BB Đối soát CMC CS - CASSO EKYC-merged.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

# Read current HTML (without base64 - 29KB version)
with open('casID-sign-view.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ────────────────────────────────────────────────────────────────
# 1. Add pdf.js to <head> if missing
if 'pdf.min.js' not in html:
    html = html.replace(
        '<script src="https://cdn.tailwindcss.com"></script>',
        '<script src="https://cdn.tailwindcss.com"></script>\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.min.js"></script>'
    )

# ────────────────────────────────────────────────────────────────
# 2. Add pdf-loading spinner inside pdf-scroll-container if missing
if 'pdf-loading' not in html:
    html = html.replace(
        '<div id="pdf-pages-container" class="flex flex-col gap-4 items-center">',
        '<div id="pdf-loading" class="flex items-center justify-center py-12"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div></div>\n                <div id="pdf-pages-container" class="flex flex-col gap-4 items-center">'
    )

# ────────────────────────────────────────────────────────────────
# 3. Completely replace everything from <script> to </script>
script_start = html.find('<script>')
script_end = html.rfind('</script>') + len('</script>')

new_script = f"""<script>
        // ─── PDF DATA ───────────────────────────────────────────────
        const pdfData = "{pdf_b64}";

        // ─── STATE ──────────────────────────────────────────────────
        let pdfDoc = null;
        let currentScale = 1.0;
        let totalPages = 0;

        // ─── TABS ───────────────────────────────────────────────────
        let currentTab = 'draw';
        let uploadedImageSrc = null;

        function switchTab(tabId) {{
            currentTab = tabId;
            ['draw', 'text', 'image'].forEach(id => {{
                const btn = document.getElementById('tab-' + id);
                const section = document.getElementById('section-' + id);
                if (id === tabId) {{
                    btn.className = "flex-1 pb-3 text-[14px] font-bold text-emerald-600 border-b-2 border-emerald-600 transition-colors";
                    section.classList.remove('hidden');
                    section.classList.add('flex');
                    if (id === 'draw' && canvas) {{
                        const rect = canvas.parentElement.getBoundingClientRect();
                        if (rect.width > 0) {{ canvas.width = rect.width; canvas.height = rect.height; }}
                    }}
                }} else {{
                    btn.className = "flex-1 pb-3 text-[14px] font-semibold text-gray-400 border-b-2 border-transparent transition-colors hover:text-emerald-500";
                    section.classList.add('hidden');
                    section.classList.remove('flex');
                }}
            }});
        }}

        // ─── MODAL ──────────────────────────────────────────────────
        function openSignatureModal() {{
            const modal = document.getElementById('signature-modal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            setTimeout(() => {{
                modal.querySelector('.modal-overlay').classList.remove('opacity-0');
                modal.querySelector('.modal-content').classList.remove('translate-y-full');
            }}, 10);
            if (!ctx) initCanvas();
        }}

        function closeSignatureModal() {{
            const modal = document.getElementById('signature-modal');
            modal.querySelector('.modal-overlay').classList.add('opacity-0');
            modal.querySelector('.modal-content').classList.add('translate-y-full');
            setTimeout(() => {{
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }}, 300);
        }}

        // ─── DRAW LOGIC ─────────────────────────────────────────────
        let canvas, ctx;
        let isDrawing = false;
        let hasDrawn = false;

        function initCanvas() {{
            canvas = document.getElementById('sign-canvas');
            const rect = canvas.parentElement.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
            ctx = canvas.getContext('2d');
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.strokeStyle = '#022c22';

            canvas.addEventListener('mousedown', startPos);
            canvas.addEventListener('mouseup', endPos);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('mouseleave', endPos);
            canvas.addEventListener('touchstart', (e) => {{ e.preventDefault(); startPos(e.touches[0]); }}, {{ passive: false }});
            canvas.addEventListener('touchend', (e) => {{ e.preventDefault(); endPos(); }});
            canvas.addEventListener('touchmove', (e) => {{ e.preventDefault(); draw(e.touches[0]); }}, {{ passive: false }});
        }}

        function startPos(e) {{ isDrawing = true; draw(e); }}
        function endPos() {{ isDrawing = false; if(ctx) ctx.beginPath(); }}
        function draw(e) {{
            if (!isDrawing) return;
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            ctx.lineTo(x, y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x, y);
            hasDrawn = true;
        }}
        function clearCanvas() {{
            if (ctx && canvas) {{ ctx.clearRect(0, 0, canvas.width, canvas.height); hasDrawn = false; }}
        }}

        // ─── TEXT LOGIC ─────────────────────────────────────────────
        function updateTextPreview() {{
            document.getElementById('sign-text-preview').textContent = document.getElementById('sign-text-input').value;
        }}
        function textToCanvas() {{
            const val = document.getElementById('sign-text-input').value;
            if (!val.trim()) return null;
            const tc = document.createElement('canvas');
            tc.width = 400; tc.height = 200;
            const tctx = tc.getContext('2d');
            tctx.font = "60px 'Dancing Script', cursive";
            tctx.fillStyle = '#022c22';
            tctx.textAlign = 'center';
            tctx.textBaseline = 'middle';
            tctx.fillText(val, 200, 100);
            return tc.toDataURL('image/png');
        }}

        // ─── IMAGE LOGIC ─────────────────────────────────────────────
        function handleImageUpload(e) {{
            const file = e.target.files[0];
            if (file) {{
                const reader = new FileReader();
                reader.onload = function(event) {{
                    uploadedImageSrc = event.target.result;
                    document.getElementById('sign-image-preview').src = uploadedImageSrc;
                    document.getElementById('upload-placeholder').classList.add('hidden');
                    document.getElementById('upload-preview-container').classList.remove('hidden');
                    document.getElementById('upload-preview-container').classList.add('flex');
                }};
                reader.readAsDataURL(file);
            }}
        }}
        function removeUploadedImage() {{
            uploadedImageSrc = null;
            document.getElementById('sign-image-upload').value = '';
            document.getElementById('upload-preview-container').classList.add('hidden');
            document.getElementById('upload-preview-container').classList.remove('flex');
            document.getElementById('upload-placeholder').classList.remove('hidden');
        }}

        // ─── SAVE SIGNATURE ──────────────────────────────────────────
        function saveSignature() {{
            let finalDataURL = null;
            if (currentTab === 'draw') {{
                if (!hasDrawn) {{ alert('Vui lòng vẽ chữ ký!'); return; }}
                finalDataURL = canvas.toDataURL('image/png');
            }} else if (currentTab === 'text') {{
                finalDataURL = textToCanvas();
                if (!finalDataURL) {{ alert('Vui lòng nhập tên!'); return; }}
            }} else if (currentTab === 'image') {{
                if (!uploadedImageSrc) {{ alert('Vui lòng tải ảnh!'); return; }}
                finalDataURL = uploadedImageSrc;
            }}

            if (finalDataURL) {{
                // Apply signature to all pages
                for (let i = 1; i <= totalPages; i++) {{
                    const img = document.getElementById(`signature-image-${{i}}`);
                    const result = document.getElementById(`signed-result-${{i}}`);
                    const box = document.getElementById(`signature-box-${{i}}`);
                    if (img && result && box) {{
                        img.src = finalDataURL;
                        result.classList.remove('hidden');
                        box.classList.add('hidden');
                    }}
                }}
                document.getElementById('sign-done-btn').innerHTML = '<i class="fa-solid fa-check"></i> Hoàn tất ký';
                closeSignatureModal();
            }}
        }}

        // ─── SIGN DONE ───────────────────────────────────────────────
        function handleSignDone() {{
            const result1 = document.getElementById('signed-result-1');
            if (!result1 || result1.classList.contains('hidden')) {{
                alert("Vui lòng chạm vào khung để ký tài liệu trước!");
                return;
            }}
            window.location.href = 'casso-account-login.html';
        }}

        // ─── PDF RENDERING ───────────────────────────────────────────
        function loadPdfJs() {{
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js';

            const loadingEl = document.getElementById('pdf-loading');
            if (loadingEl) loadingEl.classList.remove('hidden');

            const binary_string = window.atob(pdfData);
            const bytes = new Uint8Array(binary_string.length);
            for (let i = 0; i < binary_string.length; i++) {{
                bytes[i] = binary_string.charCodeAt(i);
            }}

            pdfjsLib.getDocument({{ data: bytes }}).promise.then(function(doc) {{
                pdfDoc = doc;
                totalPages = pdfDoc.numPages;

                const container = document.getElementById('pdf-pages-container');
                container.innerHTML = '';

                const renders = [];
                for (let i = 1; i <= totalPages; i++) {{
                    const wrapper = document.createElement('div');
                    wrapper.id = `page-wrapper-${{i}}`;
                    wrapper.className = 'relative bg-white shadow-lg mx-auto';

                    const cvs = document.createElement('canvas');
                    cvs.id = `pdf-canvas-${{i}}`;
                    wrapper.appendChild(cvs);

                    const sigContainer = document.createElement('div');
                    sigContainer.id = `sig-container-${{i}}`;
                    sigContainer.className = 'absolute left-1/2 -translate-x-1/2 w-4/5 max-w-[300px] border-2 border-dashed border-emerald-500 bg-emerald-50/60 rounded-xl cursor-pointer flex flex-col items-center justify-center p-3 hover:bg-emerald-50 transition-colors z-20';
                    sigContainer.style.bottom = '3%';
                    sigContainer.onclick = function() {{ openSignatureModal(); }};
                    sigContainer.innerHTML = `
                        <div id="signature-box-${{i}}" class="flex flex-col items-center">
                            <i class="fa-solid fa-signature text-2xl text-emerald-600 mb-1"></i>
                            <span class="text-xs font-semibold text-emerald-700">Chạm để ký</span>
                        </div>
                        <div id="signed-result-${{i}}" class="absolute inset-0 bg-white/90 rounded-xl flex items-center justify-center p-2 hidden z-30">
                            <img id="signature-image-${{i}}" src="" class="max-w-full max-h-full object-contain" />
                        </div>
                    `;
                    wrapper.appendChild(sigContainer);
                    container.appendChild(wrapper);
                    renders.push(renderPage(i));
                }}

                Promise.all(renders).then(() => {{
                    if (loadingEl) loadingEl.classList.add('hidden');
                }});

            }}).catch(function(err) {{
                console.error("PDF Error:", err);
                if (loadingEl) loadingEl.innerHTML = '<span class="text-red-500 text-sm p-4">Lỗi tải PDF: ' + err.message + '</span>';
            }});
        }}

        function renderPage(num) {{
            return pdfDoc.getPage(num).then(function(page) {{
                const containerWidth = document.getElementById('pdf-scroll-container').clientWidth - 32;
                const naturalWidth = page.getViewport({{ scale: 1.0 }}).width;
                const fitScale = (containerWidth / naturalWidth) * currentScale;
                const viewport = page.getViewport({{ scale: fitScale }});

                if (num === 1) {{
                    window.baseViewportWidth = viewport.width;
                    window.baseViewportHeight = viewport.height;
                }}

                const wrapper = document.getElementById(`page-wrapper-${{num}}`);
                wrapper.style.width = Math.floor(viewport.width) + 'px';
                wrapper.style.height = Math.floor(viewport.height) + 'px';

                const cvs = document.getElementById(`pdf-canvas-${{num}}`);
                const ctx2 = cvs.getContext('2d');
                const dpr = window.devicePixelRatio || 1;
                cvs.width = Math.floor(viewport.width * dpr);
                cvs.height = Math.floor(viewport.height * dpr);
                cvs.style.width = '100%';
                cvs.style.height = '100%';

                page.render({{
                    canvasContext: ctx2,
                    transform: [dpr, 0, 0, dpr, 0, 0],
                    viewport: viewport
                }});
            }});
        }}

        function zoomPdf(delta) {{
            currentScale = Math.min(3.0, Math.max(0.5, currentScale + delta));
            if (!pdfDoc) return;
            document.getElementById('pdf-pages-container').innerHTML = '';
            const loadingEl = document.getElementById('pdf-loading');
            if (loadingEl) loadingEl.classList.remove('hidden');
            const renders = [];
            for (let i = 1; i <= totalPages; i++) {{
                const wrapper = document.createElement('div');
                wrapper.id = `page-wrapper-${{i}}`;
                wrapper.className = 'relative bg-white shadow-lg mx-auto';

                const cvs = document.createElement('canvas');
                cvs.id = `pdf-canvas-${{i}}`;
                wrapper.appendChild(cvs);
                document.getElementById('pdf-pages-container').appendChild(wrapper);
                renders.push(renderPage(i));
            }}
            Promise.all(renders).then(() => {{ if (loadingEl) loadingEl.classList.add('hidden'); }});
        }}

        window.onload = function() {{
            setTimeout(loadPdfJs, 200);
        }};
    </script>"""

html = html[:script_start] + new_script + "\n</body>\n\n</html>"

with open('casID-sign-view.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done. File size: {len(html):,} bytes")
