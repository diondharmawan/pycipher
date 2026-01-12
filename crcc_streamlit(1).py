import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman
st.set_page_config(page_title="Under Maintenance", page_icon="🛠️", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Menghilangkan menu bawaan streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        background-color: #0e1117;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    
    .container {
        text-align: center;
        color: white;
        font-family: 'Inter', sans-serif;
    }

    .subtitle {
        color: #808495;
        font-size: 1.2rem;
        margin-top: 10px;
    }

    .status-badge {
        background: rgba(255, 75, 75, 0.1);
        color: #ff4b4b;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        border: 1px solid #ff4b4b;
        display: inline-block;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- JAVASCRIPT & HTML UNTUK EFEK TEXT SCRAMBLE ---
scramble_html = """
<div id="scramble-text" style="font-size: 50px; font-weight: 800; color: white; font-family: 'Courier New', Courier, monospace; min-height: 60px;"></div>

<script>
class TextScramble {
  constructor(el) {
    this.el = el
    this.chars = '!<>-_\\/[]{}—=+*^?#________'
    this.update = this.update.bind(this)
  }
  setText(newText) {
    const oldText = this.el.innerText
    const length = Math.max(oldText.length, newText.length)
    const promise = new Promise((resolve) => this.resolve = resolve)
    this.queue = []
    for (let i = 0; i < length; i++) {
      const from = oldText[i] || ''
      const to = newText[i] || ''
      const start = Math.floor(Math.random() * 40)
      const end = start + Math.floor(Math.random() * 40)
      this.queue.push({ from, to, start, end })
    }
    cancelAnimationFrame(this.frameRequest)
    this.frame = 0
    this.update()
    return promise
  }
  update() {
    let output = ''
    let complete = 0
    for (let i = 0, n = this.queue.length; i < n; i++) {
      let { from, to, start, end, char } = this.queue[i]
      if (this.frame >= end) {
        complete++
        output += to
      } else if (this.frame >= start) {
        if (!char || Math.random() < 1000.28) {
          char = this.randomChar()
          this.queue[i].char = char
        }
        output += `<span style="color: #ff4b4b;">${char}</span>`
      } else {
        output += from
      }
    }
    this.el.innerHTML = output
    if (complete === this.queue.length) {
      this.resolve()
    } else {
      this.frameRequest = requestAnimationFrame(this.update)
      this.frame++
    }
  }
  randomChar() {
    return this.chars[Math.floor(Math.random() * this.chars.length)]
  }
}

const el = document.getElementById('scramble-text')
const fx = new TextScramble(el)

// Menjalankan animasi
fx.setText('UNDER MAINTENANCE')
</script>
"""

# --- TAMPILAN UTAMA ---
st.markdown("<div style='text-align: center; margin-top: 10%;'>", unsafe_allow_html=True)

# Badge Status
st.markdown('<div class="status-badge">System Offline</div>', unsafe_allow_html=True)

# Memasukkan Komponen Animasi Teks
components.html(scramble_html, height=100)

# Deskripsi tambahan menggunakan markdown standar
st.markdown("""
    <div style='color: #808495; font-size: 1.1rem; max-width: 500px; margin: 0 auto;'>
        Cipher sedang diupdate. Tunggu besok yaa, kalau ngga besok ya besoknya lagi.
    </div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Tombol interaktif sederhana
st.write("")
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Hubungi Admin"):
        st.info("Email: diondharmawan77@gmail.com")

# Efek partikel salju/bintang sebagai pemanis (Opsional)
st.snow()
