import streamlit.components.v1 as components

def copy_button(text, label="Copiar"):
    
    components.html(f"""
        <div style="display: flex; align-items: center; gap: 8px;">
            <button onclick="copyText()" 
                style="
                    padding: 6px 12px;
                    border-radius: 6px;
                    border: none;
                    background-color: #4CAF50;
                    color: white;
                    cursor: pointer;
                ">
                {label}
            </button>
            <span id="status" style="font-size: 12px; color:#4CAF50"></span>
        </div>

        <script>
        function copyText() {{
            navigator.clipboard.writeText(`{text}`);
            document.getElementById("status").innerText = "Copiado!";
            setTimeout(() => {{
                document.getElementById("status").innerText = "";
            }}, 1500);
        }}
        </script>
    """, height=40)