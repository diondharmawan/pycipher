import streamlit as st
import streamlit.components.v1 as components 
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
st.set_page_config(page_title="CRCC-X v2", page_icon="🛡️")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

cipher = SecuredCiscoCipher()

if 'last_action_time' not in st.session_state: st.session_state.last_action_time = 0
if 'target_char' not in st.session_state: st.session_state.target_char = random.choice(string.ascii_lowercase)
if 'score' not in st.session_state: st.session_state.score = 0
if 'violation_count' not in st.session_state: st.session_state.violation_count = 0

def trigger_dos_protection():
    youtube_html = """
    <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: black; z-index: 9999999;">
        <iframe width="100%" height="100%" 
        src="https://www.youtube.com/embed/c5EevDyeQUE?si=xrWqd3qlJ0uxzaNJ&amp;controls=0&autoplay=1&mute=1" 
        title="YouTube video player" frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
        </iframe>
    </div>
    <style>
        body { overflow: hidden; } 
    </style>
    """
    components.html(youtube_html, height=1000, width=1500)
    st.error("🚨 DOS ATTACK DETECTED. SYSTEM LOCKED.")
    st.stop()

def check_rate_limit():
    current_time = time.time()
    if current_time - st.session_state.last_action_time < 1.5:
        st.session_state.violation_count += 1
        if st.session_state.violation_count >= 4:
            trigger_dos_protection()
        return False
    st.session_state.last_action_time = current_time
    st.session_state.violation_count = 0
    return True

# --- UI UTAMA ---
st.title("🛡️ CRCC-X v2: Secure Engine")

user_input = st.text_area("Input Teks atau Kode Cipher", 
                          placeholder="Ketik pesan atau tempel kode cipher di sini...", 
                          height=120, 
                          max_chars=1000)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    run_button = st.button("🚀 JALANKAN PROSES", use_container_width=True)

if run_button:
    if not check_rate_limit():
        st.warning(f"⚠️ Terlalu cepat! Pelanggaran: {st.session_state.violation_count}/4")
    elif user_input.strip():
        # --- BOX VISUALISASI PROSES ---
        if "|" in user_input:
            # PROSES DEKRIPSI
            with st.status("🔍 Menganalisis & Mendekripsi Sinyal...", expanded=True) as status:
                st.write("Mengidentifikasi blok data...")
                progress_bar = st.progress(0)
                log_box = st.empty()
                
                blocks = user_input.replace('\xa0', ' ').split("  ")
                decoded_result = ""
                
                for i, block in enumerate(blocks):
                    # Simulasi efek loading per karakter
                    time.sleep(0.1) 
                    char_decoded = cipher.decrypt(block)
                    decoded_result += char_decoded
                    log_box.code(f"Processing Block {i+1}: {block} \nResult: '{char_decoded}'")
                    progress_bar.progress((i + 1) / len(blocks))
                
                status.update(label="✅ Dekripsi Selesai!", state="complete", expanded=False)
                st.success(f"Hasil Akhir: **{decoded_result}**")
        else:
            # PROSES ENKRIPSI
            with st.status("🔐 Mengamankan & Enkripsi Data...", expanded=True) as status:
                st.write("Menjalankan algoritma router cisco...")
                progress_bar = st.progress(0)
                log_box = st.empty()
                
                clean_text = re.sub(r'[^a-zA-Z\s]', '', user_input.lower())
                encrypted_blocks = []
                
                for i, char in enumerate(clean_text):
                    time.sleep(0.1)
                    single_encrypt = cipher.encrypt(char)
                    encrypted_blocks.append(single_encrypt)
                    log_box.code(f"Char: '{char}' -> Encrypted: {single_encrypt}")
                    progress_bar.progress((i + 1) / len(clean_text))
                
                final_cipher = "  ".join(encrypted_blocks)
                status.update(label="✅ Enkripsi Berhasil!", state="complete", expanded=False)
                st.code(final_cipher)
    else:
        st.warning("Input tidak boleh kosong.")

st.markdown("---")
# ... (Sisanya tetap sama seperti kode awal kamu)
st.write("### 🎮 Tebak Cipher")
st.subheader(f"Enkripsi Huruf: :red[{st.session_state.target_char}]")
player_guess = st.text_input("Jawabanmu:", placeholder="v1 v2 v3 | h", max_chars=50)

g_col1, g_col2 = st.columns(2)
with g_col1:
    if st.button("🎯 Cek Jawaban", use_container_width=True):
        if not check_rate_limit():
            st.warning("Rate limit aktif.")
        else:
            correct_answer = cipher.encrypt(st.session_state.target_char).strip()
            if player_guess.strip() == correct_answer:
                st.balloons()
                st.success("Tepat! +10 XP")
                st.session_state.score += 10
                st.session_state.target_char = random.choice(string.ascii_lowercase)
                time.sleep(1)
                st.rerun()
            else:
                st.error("Jawaban tidak sesuai dengan algoritma router.")

with g_col2:
    if st.button("🔄 Ganti Huruf", use_container_width=True):
        st.session_state.target_char = random.choice(string.ascii_lowercase)
        st.rerun()

st.sidebar.metric("Security Status", "PROTECTED" if st.session_state.violation_count < 2 else "WARNING")
st.sidebar.metric("User Score", f"{st.session_state.score} XP")
st.sidebar.divider()
st.sidebar.info(f"Rate limit: 1.5s\nPelanggaran: {st.session_state.violation_count}/4")
