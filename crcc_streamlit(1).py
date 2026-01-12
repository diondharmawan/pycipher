import streamlit as st
import re
import time
import random
import string
import streamlit.components.v1 as components

# --- KONFIGURASI KEAMANAN ---
MAX_VIOLATIONS = 3  # Berapa kali boleh melanggar rate limit sebelum diblokir
THRESHOLD_SECONDS = 1.5

class SecuredCiscoCipher:
    # ... (Method init, get_char, encrypt, decrypt sama seperti sebelumnya) ...
    def __init__(self):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.router_data = {
            'a': [1, 4, 0, 1, 2], 'b': [1, 4, 0, 1, 2], 'c': [1, 8, 0, 1, 2],
            'd': [1, 4, 0, 1, 2], 'e': [1, 6, 0, 1, 2], 'f': [1, 3, 0, 1, 2],
            'g': [1, 4, 0, 1, 2], 'h': [1, 4, 0, 1, 2], 'i': [1, 4, 0, 1, 2],
            'j': [1, 4, 0, 1, 2], 'k': [2, 8, 10, 1, 2], 'l': [2, 12, 20, 1, 2],
            'm': [2, 12, 40, 1, 2], 'n': [3, 6, 14, 1, 2], 'o': [3, 6, 40, 1, 2],
            'p': [3, 6, 100, 1, 2], 'q': [3, 6, 160, 1, 2], 'r': [3, 6, 10, 1, 3],
            's': [3, 6, 5, 1, 3], 't': [4, 4, 1, 1, 2], 'u': [4, 4, 1, 1, 2],
            'v': [4, 2, 0, 1, 1], 'w': [5, 2, 0, 0, 1], 'x': [5, 2, 0, 0, 1],
            'y': [5, 4, 0, 1, 2], 'z': [5, 4, 0, 1, 2]
        }

    def encrypt(self, text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)[:500]
        encoded_words = []
        for char in text.lower():
            if char == " ": encoded_words.append("/"); continue
            if char in self.router_data:
                d = self.router_data[char]
                v1, v2, v3 = d[0]*d[1], d[2], d[-2]*d[-1]
                h = self.alphabet.index(char) + 1
                encoded_words.append(f"{self.get_char(v1)}{v1} {v2}{self.get_char(v2)} {self.get_char(v3)}{v3} | {h}")
        return "  ".join(encoded_words)

    def decrypt(self, cipher_text):
        cipher_text = re.sub(r'[^a-zA-Z0-9\s/|]', '', cipher_text)
        blocks = cipher_text.split("  ")[:100]
        try:
            decoded = ""
            for block in blocks:
                if block.strip() == "/": decoded += " "
                elif "|" in block:
                    h_val = block.split("|")[-1].strip()
                    if h_val.isdigit():
                        idx = int(h_val) - 1
                        if 0 <= idx < 26: decoded += self.alphabet[idx]
            return decoded
        except: return "Invalid Format"

    def get_char(self, value):
        if value == 0: return 'z'
        return self.alphabet[(value - 1) % 26]

# --- SESSION STATE & DETEKSI ---
if 'violations' not in st.session_state: st.session_state.violations = 0
if 'is_blocked' not in st.session_state: st.session_state.is_blocked = False
if 'last_time' not in st.session_state: st.session_state.last_time = 0

def trigger_tarpit():
    """Menyuntikkan JS yang akan memakan CPU client jika terdeteksi serangan."""
    components.html("""
        <script>
        console.log("Security Triggered: Resource Tarpit Active.");
        // Membuat loop berat di sisi client tanpa membebani server
        let data = [];
        for (let i = 0; i < 1000000; i++) {
            data.push(Math.random() * Math.random());
            if (i % 100 == 0) console.log("System Overload: " + i);
        }
        // Redirect ke situs tak berguna untuk membersihkan session
        alert("Aktivitas mencurigakan terdeteksi. Browser Anda melambat untuk verifikasi keamanan.");
        window.location.href = "https://www.google.com";
        </script>
    """, height=0)

# --- UI LOGIC ---
st.set_page_config(page_title="CRCC-X v2 Ultra Secure")

# Jika user sudah diblokir
if st.session_state.is_blocked:
    st.error("🚫 AKSES DIBLOKIR: Terdeteksi aktivitas automasi berbahaya.")
    trigger_tarpit()
    st.stop()

cipher = SecuredCiscoCipher()

st.title("🛡️ CRCC-X v2: Ultra Secure Engine")

user_input = st.text_area("Input:", max_chars=1000)

if st.button("🚀 PROSES"):
    now = time.time()
    
    # Cek Rate Limit
    if now - st.session_state.last_time < THRESHOLD_SECONDS:
        st.session_state.violations += 1
        st.warning(f"⚠️ Peringatan: Jangan spam! (Pelanggaran {st.session_state.violations}/{MAX_VIOLATIONS})")
        
        if st.session_state.violations >= MAX_VIOLATIONS:
            st.session_state.is_blocked = True
            st.rerun()
    else:
        # Reset perlahan jika user mulai normal
        if st.session_state.violations > 0:
            st.session_state.violations -= 0.5
            
        st.session_state.last_time = now
        
        # Eksekusi normal
        if "|" in user_input:
            st.success(f"Hasil: {cipher.decrypt(user_input)}")
        else:
            st.code(cipher.encrypt(user_input))

# Sidebar Info
st.sidebar.subheader("Security Monitoring")
st.sidebar.write(f"Violations Score: {st.session_state.violations}")
if st.session_state.violations > 1:
    st.sidebar.warning("Status: Suspicious Activity")
