import streamlit as st
import streamlit.components.v1 as components 
import re
import time
import random
import string

class SecuredCiscoCipher:
    def __init__(self):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        # Database parameter router
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
                
                # ALGORITMA BARU: Mengamankan index h dengan penambahan v1, v2, v3
                h_original = self.alphabet.index(char) + 1
                h_masked = h_original + v1 + v2 + v3
                
                encoded_words.append(f"{self.get_char(v1)}{v1} {v2}{self.get_char(v2)} {self.get_char(v3)}{v3} | {h_masked}")
        return "  ".join(encoded_words)

    def decrypt(self, cipher_text):
        # Membersihkan karakter non-standar dan split blok
        blocks = cipher_text.replace('\xa0', ' ').strip().split("  ")
        
        if len(blocks) > 200:
            return "Error: Pesan terlalu panjang."

        try:
            decoded = ""
            for block in blocks:
                if block.strip() == "/":
                    decoded += " "
                elif "|" in block:
                    parts = block.split("|")
                    h_masked = int(parts[-1].strip())
                    
                    # Ekstrak nilai v1, v2, v3 dari teks sebelum pipa (|)
                    # Contoh blok: "d4 0z z2 | 11"
                    sub_parts = parts[0].strip().split(" ")
                    v1 = int(re.sub(r'[^0-9]', '', sub_parts[0]))
                    v2 = int(re.sub(r'[^0-9]', '', sub_parts[1]))
                    v3 = int(re.sub(r'[^0-9]', '', sub_parts[2]))
                    
                    # Kalkulasi balik index asli
                    h_original = h_masked - v1 - v2 - v3
                    idx = h_original - 1
                    
                    if 0 <= idx < 26:
                        decoded += self.alphabet[idx]
            return decoded
        except Exception:
            return "Format tidak valid."

# --- INITIALIZATION ---
st.set_page_config(page_title="Cisco Series Cipher", page_icon="🛡️")

# Menyembunyikan elemen bawaan Streamlit
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
    st.error("DOS ATTACK DETECTED. SYSTEM LOCKED.")
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
st.sidebar.image("https://s6.imgcdn.dev/YzpPD2.png", width=250)
#
scramble_html = """
<style>
    #scramble-container {
        width: 100%;
        text-align: center;
        padding: 10px 0;
        overflow: hidden;
    }
    
    #scramble-text {
        font-family: 'Courier New', Courier, monospace;
        font-weight: 800;
        color: white;
        min-height: 1.2em;
        line-height: 1.3;
        margin: 0 auto;
        display: inline-block;
        max-width: 100%;
        word-break: break-word;
    }

    /* Responsive font size */
    @media (max-width: 768px) {
        #scramble-text {
            font-size: clamp(28px, 7vw, 42px) !important;
        }
    }
    
    @media (min-width: 769px) {
        #scramble-text {
            font-size: clamp(40px, 6.5vw, 64px) !important;
        }
    }
</style>

<div id="scramble-container">
    <div id="scramble-text"></div>
</div>

<script>
class TextScramble {
  constructor(el) {
    this.el = el;
    this.chars = '!<>-_\\/[]{}—=+*^?#________';
    this.update = this.update.bind(this);
  }

  setText(newText) {
    const oldText = this.el.innerText;
    const length = Math.max(oldText.length, newText.length);
    const promise = new Promise(resolve => this.resolve = resolve);
    
    this.queue = [];
    for (let i = 0; i < length; i++) {
      const from = oldText[i] || '';
      const to = newText[i] || '';
      const start = Math.floor(Math.random() * 80) + 40;   // lebih cepat sedikit di mobile
      const end = start + Math.floor(Math.random() * 100) + 60;
      this.queue.push({ from, to, start, end, char: null });
    }

    cancelAnimationFrame(this.frameRequest);
    this.frame = 0;
    this.update();
    return promise;
  }

  update() {
    let output = '';
    let complete = 0;

    for (let i = 0; i < this.queue.length; i++) {
      let { from, to, start, end, char } = this.queue[i];
      
      if (this.frame >= end) {
        complete++;
        output += to;
      } else if (this.frame >= start) {
        if (!char || Math.random() < 0.12) {
          char = this.chars[Math.floor(Math.random() * this.chars.length)];
          this.queue[i].char = char;
        }
        output += `<span style="color: #ff4b4b;">${char}</span>`;
      } else {
        output += from;
      }
    }

    this.el.innerHTML = output;

    if (complete === this.queue.length) {
      this.resolve();
    } else {
      this.frameRequest = requestAnimationFrame(this.update);
      this.frame++;
    }
  }
}

const el = document.getElementById('scramble-text');
const fx = new TextScramble(el);

const phrases = [
  'CISCO SERIES CIPHER',
  'AUTO DETECT SYSTEM' ,
  'ENCRYPT • DECRYPT',
  'SECURE YOUR DATA',
  'NOT NEXT-GEN CIPHER',
  'HENGKER DILARANG MENYERANG',
  'KAORI CICAK' 

];

let index = 0;

const runLoop = async () => {
  const text = phrases[index];
  await fx.setText(text);
  
  // Durasi tampil lebih pendek di mobile agar tidak terlalu lama scroll
  const displayTime = window.innerWidth < 768 ? 4000 : 6000;
  
  setTimeout(() => {
    el.innerHTML = '';           // bersihkan dulu
    index = (index + 1) % phrases.length;
    runLoop();
  }, displayTime);
};

// Mulai
runLoop();
</script>
"""

# --- penggunaan di Streamlit ---
import streamlit.components.v1 as components

components.html(scramble_html, height=120)   # naikkan height sedikit agar aman di mobile
#components.html(scramble_html, height=50)

#st.title("🛡️ Cisco Series Cipher: Secure Engine")
#st.image("https://s6.imgcdn.dev/YzpPD2.png", use_container_width=True)
st.caption("Algoritma terbaru dengan masking nilai indeks (h = idx + v1 + v2 + v3)")

user_input = st.text_area("Input Teks atau Kode Cipher", 
                          placeholder="Ketik pesan atau tempel kode cipher di sini...", 
                          height=120, 
                          max_chars=10000)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    run_button = st.button("JALANKAN PROSES", use_container_width=True)

if run_button:
    if not check_rate_limit():
        st.warning(f"Terlalu cepat! Pelanggaran: {st.session_state.violation_count}/4")
    elif user_input.strip():
        if "|" in user_input:
            # PROSES DEKRIPSI
            with st.status("Menganalisis & Mendekripsi Sinyal...", expanded=True) as status:
                st.write("Mengidentifikasi blok data & kalkulasi balik...")
                progress_bar = st.progress(0)
                log_box = st.empty()
                
                blocks = user_input.replace('\xa0', ' ').strip().split("  ")
                decoded_result = ""
                
                for i, block in enumerate(blocks):
                    time.sleep(0.1) 
                    char_decoded = cipher.decrypt(block)
                    decoded_result += char_decoded
                    log_box.code(f"Processing Block {i+1}: {block} \nResult: '{char_decoded}'")
                    progress_bar.progress((i + 1) / len(blocks))
                
                status.update(label="Dekripsi Selesai. Lihat hasilnya disini!", state="complete", expanded=False)
                st.success(f"Hasil Akhir: **{decoded_result}**")
        else:
            # PROSES ENKRIPSI
            with st.status("Mengamankan & Enkripsi Data...", expanded=True) as status:
                st.write("Menjalankan algoritma router masking...")
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
                status.update(label="Enkripsi Berhasil. Lihat hasilnya disini!", state="complete", expanded=False)
                st.code(final_cipher)
                st.info("💡 Angka di belakang '|' sekarang disamarkan dengan parameter v1, v2, v3.")
    else:
        st.warning("Input tidak boleh kosong.")

st.markdown("---")

# --- GAME TEBAK CIPHER ---
st.write("### 🎮 Tebak Cipher")
st.subheader(f"Enkripsi Huruf: :red[{st.session_state.target_char}]")
player_guess = st.text_input("Jawabanmu:", placeholder="v1 v2 v3 | h_masked", max_chars=50)

g_col1, g_col2 = st.columns(2)
with g_col1:
    if st.button("Cek Jawaban", use_container_width=True):
        if not check_rate_limit():
            st.warning("Rate limit aktif.")
        else:
            correct_answer = cipher.encrypt(st.session_state.target_char).strip()
            if player_guess.strip() == correct_answer:
                st.balloons()
                st.success("Tepat! Algoritma masking terpecahkan. +10 XP")
                st.session_state.score += 10
                st.session_state.target_char = random.choice(string.ascii_lowercase)
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Salah! Jawaban yang benar adalah: {correct_answer}")

with g_col2:
    if st.button("Ganti Huruf", use_container_width=True):
        st.session_state.target_char = random.choice(string.ascii_lowercase)
        st.rerun()

# --- SIDEBAR ---
st.sidebar.metric("Security Status", "PROTECTED" if st.session_state.violation_count < 2 else "WARNING")
st.sidebar.metric("User Score", f"{st.session_state.score} XP")
st.sidebar.divider()
st.sidebar.info(f"Rate limit: 1.5s\nPelanggaran: {st.session_state.violation_count}/4")
st.sidebar.write("### 🛡️ Keamanan Baru")
st.sidebar.write("Indeks karakter sekarang dijumlahkan dengan parameter v1, v2, dan v3 untuk mencegah teknik guessing sederhana.")
