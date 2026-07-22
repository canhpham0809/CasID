import re

with open('casID-sign-view.html', 'r') as f:
    html = f.read()

# 1. Update Zoom Controls position
old_zoom = '<div class="fixed bottom-[90px] right-4 flex flex-col gap-2 z-10 pointer-events-auto">'
new_zoom = '<div class="fixed bottom-[140px] right-4 flex flex-col gap-2 z-10 pointer-events-auto">'
html = html.replace(old_zoom, new_zoom)

# 2. Revert Header Info (remove prev/next from header)
old_header = """            <!-- Document Info -->
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

old_header_user_edit = """            <!-- Document Info -->
            <div class="bg-white px-4 py-3 border-b border-gray-200 flex justify-between items-center">
                <div class="flex-1 pr-2">
                    <h2 id="doc-title" class="text-[15px] font-bold text-gray-800 leading-snug mb-1">Biên bản đối soát
                        đại lý chữ ký số tháng 06/2026 (1/2)</h2>
                    <p id="doc-sender" class="text-xs text-gray-500">Người gửi: KySoQR.io - Hôm nay lúc 09:30</p>
                </div>
                <div class="flex gap-2 text-gray-400">
                    <button id="prev-doc-btn" onclick="switchDocument(-1)"
                        class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 hover:text-emerald-600 disabled:opacity-30 transition-colors"><i
                            class="fa-solid fa-chevron-left"></i></button>
                    <button id="next-doc-btn" onclick="switchDocument(1)"
                        class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 hover:text-emerald-600 disabled:opacity-30 transition-colors"><i
                            class="fa-solid fa-chevron-right"></i></button>
                </div>
            </div>"""

new_header = """            <!-- Document Info -->
            <div class="bg-white px-4 py-3 border-b border-gray-200">
                <h2 id="doc-title" class="text-[15px] font-bold text-gray-800 leading-snug mb-1">Biên bản đối soát đại lý chữ ký số tháng 06/2026 (1/2)</h2>
                <p id="doc-sender" class="text-xs text-gray-500">Người gửi: KySoQR.io - Hôm nay lúc 09:30</p>
            </div>"""

if old_header in html:
    html = html.replace(old_header, new_header)
else:
    html = html.replace(old_header_user_edit, new_header)

# 3. Update Bottom Action Bar
old_bottom_bar = """        <!-- Bottom Action Bar -->
        <div
            class="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-4 py-4 flex gap-3 pb-8 z-10 shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
            <button
                class="flex-1 py-3.5 rounded-2xl border border-gray-300 text-gray-600 font-bold text-[15px] bg-white hover:bg-gray-50 transition-colors">
                Từ chối
            </button>
            <button id="sign-done-btn" onclick="handleSignDone()"
                class="flex-[1.5] py-3.5 rounded-2xl bg-emerald-600 text-white font-bold text-[15px] shadow-lg shadow-emerald-600/30 hover:bg-emerald-700 flex items-center justify-center gap-2 transition-colors">
                Ký tiếp (1/2)
            </button>
        </div>"""

new_bottom_bar = """        <!-- Bottom Action Bar -->
        <div class="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-3 py-4 flex items-center justify-between gap-2 pb-8 z-10 shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
            <button class="w-[85px] py-3.5 rounded-2xl border border-gray-300 text-gray-600 font-bold text-[14px] bg-white hover:bg-gray-50 transition-colors text-center shrink-0">
                Từ chối
            </button>
            
            <div class="flex items-center justify-center gap-1 bg-gray-100 rounded-full p-1 h-12 shrink-0">
                <button id="prev-doc-btn" onclick="switchDocument(-1)" class="w-10 h-10 flex items-center justify-center rounded-full bg-white shadow-sm hover:text-emerald-600 disabled:opacity-30 disabled:shadow-none transition-colors"><i class="fa-solid fa-chevron-left"></i></button>
                <button id="next-doc-btn" onclick="switchDocument(1)" class="w-10 h-10 flex items-center justify-center rounded-full bg-white shadow-sm hover:text-emerald-600 disabled:opacity-30 disabled:shadow-none transition-colors"><i class="fa-solid fa-chevron-right"></i></button>
            </div>

            <button id="sign-done-btn" onclick="handleSignDone()"
                class="flex-1 py-3.5 px-2 rounded-2xl bg-emerald-600 text-white font-bold text-[14px] shadow-lg shadow-emerald-600/30 hover:bg-emerald-700 flex items-center justify-center gap-1 transition-colors whitespace-nowrap overflow-hidden shrink-0">
                Ký tiếp (1/2)
            </button>
        </div>"""

html = html.replace(old_bottom_bar, new_bottom_bar)

# 4. Update pdf-scroll-container and pdf-page-wrapper for proper zooming
old_scroll_container = """            <!-- PDF.js Viewer Container -->
            <div id="pdf-scroll-container"
                class="w-full h-full bg-gray-400 overflow-auto relative flex justify-center p-2 pb-[120px]">

                <!-- PDF Page Wrapper (Scaling and positioning) -->
                <div id="pdf-page-wrapper"
                    class="relative bg-white shadow-lg transition-transform origin-top origin-left"
                    style="transform: scale(1);">"""

new_scroll_container = """            <!-- PDF.js Viewer Container -->
            <div id="pdf-scroll-container"
                class="w-full h-full bg-gray-400 overflow-auto relative p-4 pb-[120px]">

                <!-- PDF Page Wrapper (Scaling and positioning) -->
                <div id="pdf-page-wrapper"
                    class="relative bg-white shadow-lg mx-auto transition-all duration-200"
                    style="">"""

html = html.replace(old_scroll_container, new_scroll_container)

# 5. Fix zoom in JS
old_zoom_js = """        let currentZoom = 1.0;
        function zoomPdf(delta) {
            currentZoom += delta;
            if (currentZoom < 0.5) currentZoom = 0.5;
            if (currentZoom > 3.0) currentZoom = 3.0;
            document.getElementById('pdf-page-wrapper').style.transform = `scale(${currentZoom})`;
        }"""

new_zoom_js = """        let currentScale = 1.0;
        function zoomPdf(delta) {
            currentScale += delta;
            if (currentScale < 0.5) currentScale = 0.5;
            if (currentScale > 3.0) currentScale = 3.0;
            
            const wrapper = document.getElementById('pdf-page-wrapper');
            wrapper.style.width = Math.floor(window.baseViewportWidth * currentScale) + "px";
            wrapper.style.height = Math.floor(window.baseViewportHeight * currentScale) + "px";
        }"""
if old_zoom_js in html:
    html = html.replace(old_zoom_js, new_zoom_js)
else:
    # Handle if currentZoom was currentScale due to earlier changes? The viewed code had currentZoom.
    pass

# Update switchDocument zoom reset
old_switch_zoom = """                // Reset Zoom
                currentScale = 1.0;
                document.getElementById('pdf-page-wrapper').style.transform = `scale(1)`;"""
new_switch_zoom = """                // Reset Zoom
                currentScale = 1.0;"""
html = html.replace(old_switch_zoom, new_switch_zoom)

# 6. Update renderPage to save base viewport and set wrapper size
old_render = """                canvasPdf.style.width = Math.floor(viewport.width) + "px";
                canvasPdf.style.height = Math.floor(viewport.height) + "px";"""

new_render = """                window.baseViewportWidth = viewport.width;
                window.baseViewportHeight = viewport.height;
                
                const wrapper = document.getElementById('pdf-page-wrapper');
                wrapper.style.width = Math.floor(viewport.width * currentScale) + "px";
                wrapper.style.height = Math.floor(viewport.height * currentScale) + "px";
                
                canvasPdf.style.width = "100%";
                canvasPdf.style.height = "100%";"""

html = html.replace(old_render, new_render)

with open('casID-sign-view.html', 'w') as f:
    f.write(html)

