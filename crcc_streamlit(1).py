import streamlit as st
import re
import time
import random
import string

class SecuredCiscoCipher:
    def __init__(self):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        # Data Router Lengkap
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

    def get_char(self, value):
        if value == 0: return 'z'
        return self.alphabet[(value - 1) % 26]

    def encrypt(self, text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        encoded_words = []
        for char in text.lower():
            if char == " ":
                encoded_words.append("/")
                continue
            if char in self.router_data:
                d = self.router_data[char]
                v1, v2, v3 = d[0]*d[1], d[2], d[-2]*d[-1]
                h = self.alphabet.index(char) + 1
                encoded_words.append(f"{self.get_char(v1)}{v1} {v2}{self.get_char(v2)} {self.get_char(v3)}{v3} | {h}")
        return "  ".join(encoded_words)

    def decrypt(self, cipher_text):
        try:
            decoded = ""
            blocks = cipher_text.replace('\xa0', ' ').split("  ")
            for block in blocks:
                if block.strip() == "/":
                    decoded += " "
                elif "|" in block:
                    h_val = block.split("|")[-1].strip()
                    if h_val.isdigit():
                        idx = int(h_val) - 1
                        decoded += self.alphabet[idx]
            return decoded
        except:
            return "Format tidak valid."

# --- INITIALIZATION & STYLING ---
st.set_page_config(page_title="CRCC-X v2 Pro", page_icon="🛡️")

# CSS untuk menyembunyikan header Streamlit default agar tampilan clean
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

cipher = SecuredCiscoCipher()

if 'target_char' not in st.session_state:
    st.session_state.target_char = random.choice(string.ascii_lowercase)
if 'score' not in st.session_state:
    st.session_state.score = 0

# --- UI UTAMA ---
st.title("🛡️ CRCC-X v2: Secure Auto-Detect")

user_input = st.text_area("Input Teks atau Kode Cipher:", placeholder="Ketik pesan atau tempel kode...", height=120)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    run_button = st.button("🚀 JALANKAN PROSES", use_container_width=True)

if run_button:
    if user_input.strip():
        if "|" in user_input:
            st.info("🔎 **Mode:** Dekripsi")
            st.success(f"Hasil: **{cipher.decrypt(user_input)}**")
        else:
            st.info("🔎 **Mode:** Enkripsi")
            st.code(cipher.encrypt(user_input))
    else:
        st.warning("Input kosong.")

st.markdown("---")

# --- BAGIAN GAME (Header sudah dihapus) ---
st.write("### 🎮 Tebak Cipher")
st.write("Uji pemahamanmu! Enkripsi huruf di bawah ini dengan format: `v1 v2 v3 | h` (Contoh: `d4 0z b2 | 1`)")

# Box Tantangan
st.subheader(f"Enkripsi Huruf: :red[{st.session_state.target_char}]")

player_guess = st.text_input("Jawabanmu:", placeholder="v1 v2 v3 | h")

g_col1, g_col2 = st.columns(2)

with g_col1:
    if st.button("🎯 Cek Jawaban", use_container_width=True):
        correct_answer = cipher.encrypt(st.session_state.target_char).strip()
        if player_guess.strip() == correct_answer:
            st.balloons()
            st.success(f"LUAR BIASA! Jawaban benar. +10 Poin!")
            st.session_state.score += 10
            st.session_state.target_char = random.choice(string.ascii_lowercase)
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"Salah! Petunjuk: Gunakan tabel router untuk huruf '{st.session_state.target_char}'")

with g_col2:
    if st.button("🔄 Ganti Huruf", use_container_width=True):
        st.session_state.target_char = random.choice(string.ascii_lowercase)
        st.rerun()

st.sidebar.metric("Skor Pemain", f"{st.session_state.score} XP")
st.sidebar.divider()
st.sidebar.write("**Tabel Bantuan Singkat:**")
st.sidebar.json({
    "a, b, d": "1, 4, 0, 1, 2",
    "e": "1, 6, 0, 1, 2",
    "n": "3, 6, 14, 1, 2"
})
