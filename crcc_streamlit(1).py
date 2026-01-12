import streamlit as st
import streamlit.components.v1 as components  # Tambahan untuk redirect
import re
import time
import random
import string

class SecuredCiscoCipher:
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

    def get_char(self, value):
        if value == 0: return 'z'
        return self.alphabet[(value - 1) % 26]

    def encrypt(self, text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        if len(text) > 500: text = text[:500] 
        
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
        cipher_text = re.sub(r'[^a-zA-Z0-9\s/|]', '', cipher_text)
        blocks = cipher_text.replace('\xa0', ' ').split("  ")
        
        if len(blocks) > 200:
            return "Error: Pesan terlalu panjang."

        try:
            decoded = ""
            for block in blocks:
                if block.strip() == "/":
                    decoded += " "
                elif "|" in block:
                    parts = block.split("|")
                    h_val = parts[-1].strip()
                    if h_val.isdigit():
                        idx = int(h_val) - 1
                        if 0 <= idx < 26:
                            decoded += self.alphabet[idx]
            return decoded
        except Exception:
            return "Format tidak valid."

# --- INITIALIZATION ---
st.set_page_config(page_title="CRCC-X v2 Secure", page_icon="🛡️")

# CSS untuk menyembunyikan elemen standar
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

cipher = SecuredCiscoCipher()

# Initialize Session States
if 'last_action_time' not in st.session_state: st.session_state.last_action_time = 0
if 'target_char' not in st.session_state: st.session_state.target_char = random.choice(string.ascii_lowercase)
if 'score' not in
