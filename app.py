"""
Multi-Modal Steganography System — Streamlit Application
Hide text, images, or audio inside image/audio/video carriers.
"""

import streamlit as st
import io
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image
from ui.styles import get_custom_css
from core.engine import encode, decode, check_capacity
from core.utils import image_to_bytes

# ── Page Config ──
st.set_page_config(
    page_title="StegaVault — Multi-Modal Steganography",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔐 StegaVault")
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Navigation")
    page = st.radio("", ["🏠 Home", "📥 Encode", "📤 Decode"], label_visibility="collapsed")

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Supported Modes")
    st.markdown("""
    | Data | Carrier |
    |------|---------|
    | Text | Image 🖼️ |
    | Image | Audio 🎵 |
    | Audio | Video 🎬 |
    | Text | Audio 🎵 |
    | Text | Video 🎬 |
    """)
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.caption("Built with 💜 using Python & Streamlit")


# ══════════════════════════════════════════════
#  HOME PAGE
# ══════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown("""
    <div class="hero-banner">
        <h1>🔐 StegaVault</h1>
        <p>Multi-Modal Steganography System with AES Encryption</p>
        <p style="color:#888; font-size:0.85rem; margin-top:0.5rem;">
            Hide any data inside any media — securely and invisibly
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>🖼️ Image Carrier</h3>
            <p>LSB steganography on PNG images. Modify the least significant bits of pixel
            channels to embed data with zero visual distortion.</p>
            <span class="status-badge badge-success">High Capacity</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🎵 Audio Carrier</h3>
            <p>Embed data in WAV audio samples using LSB modification. Imperceptible changes
            to the audio signal preserve quality.</p>
            <span class="status-badge badge-info">WAV Format</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3>🎬 Video Carrier</h3>
            <p>Frame-wise LSB steganography across video frames. Massive capacity with
            lossless FFV1 codec preservation.</p>
            <span class="status-badge badge-warn">AVI Output</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Workflow
    st.markdown("### 🔄 How It Works")
    col_enc, col_dec = st.columns(2)
    with col_enc:
        st.markdown("""
        <div class="glass-card">
            <h3>📥 Encoding</h3>
            <div class="workflow-step"><span class="step-num">1</span><span class="step-text">Select your secret data type</span></div>
            <div class="workflow-step"><span class="step-num">2</span><span class="step-text">Upload or type your secret data</span></div>
            <div class="workflow-step"><span class="step-num">3</span><span class="step-text">Choose & upload a carrier file</span></div>
            <div class="workflow-step"><span class="step-num">4</span><span class="step-text">Set optional AES password</span></div>
            <div class="workflow-step"><span class="step-num">5</span><span class="step-text">Download your stego file</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col_dec:
        st.markdown("""
        <div class="glass-card">
            <h3>📤 Decoding</h3>
            <div class="workflow-step"><span class="step-num">1</span><span class="step-text">Upload the stego file</span></div>
            <div class="workflow-step"><span class="step-num">2</span><span class="step-text">Select the carrier type</span></div>
            <div class="workflow-step"><span class="step-num">3</span><span class="step-text">Enter AES password (if used)</span></div>
            <div class="workflow-step"><span class="step-num">4</span><span class="step-text">Extract original data</span></div>
            <div class="workflow-step"><span class="step-num">5</span><span class="step-text">View & download recovered data</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Metrics
    st.markdown("""
    <div class="metric-row">
        <div class="metric-card"><div class="value">3</div><div class="label">Carrier Types</div></div>
        <div class="metric-card"><div class="value">3</div><div class="label">Data Formats</div></div>
        <div class="metric-card"><div class="value">AES-256</div><div class="label">Encryption</div></div>
        <div class="metric-card"><div class="value">LSB</div><div class="label">Algorithm</div></div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  ENCODE PAGE
# ══════════════════════════════════════════════
elif page == "📥 Encode":
    st.markdown("""
    <div class="hero-banner" style="padding:1.5rem;">
        <h1 style="font-size:1.8rem;">📥 Encode — Hide Your Data</h1>
        <p>Select data → Choose carrier → Embed securely</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    # ── Left: Data Input ──
    with col_left:
        st.markdown('<div class="glass-card"><h3>🔑 Secret Data</h3></div>', unsafe_allow_html=True)

        data_type = st.selectbox("Data Type to Hide", ["Text", "Image", "Audio"], key="enc_dtype")
        secret_data = None
        data_type_key = data_type.lower()

        if data_type == "Text":
            text_input = st.text_area("Enter your secret message", height=150,
                                      placeholder="Type your secret message here...")
            if text_input:
                secret_data = text_input.encode('utf-8')

        elif data_type == "Image":
            img_file = st.file_uploader("Upload secret image", type=['png', 'jpg', 'jpeg', 'bmp'],
                                        key="enc_img")
            if img_file:
                secret_img = Image.open(img_file)
                st.image(secret_img, caption="Secret Image Preview", width=250)
                secret_data = image_to_bytes(secret_img)

        elif data_type == "Audio":
            audio_file = st.file_uploader("Upload secret audio", type=['wav'], key="enc_audio")
            if audio_file:
                secret_data = audio_file.read()
                st.audio(secret_data, format='audio/wav')

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        # Security
        st.markdown('<div class="glass-card"><h3>🔐 Security (Optional)</h3></div>',
                    unsafe_allow_html=True)
        use_encryption = st.checkbox("Enable AES-256 Encryption", value=False)
        password = None
        if use_encryption:
            password = st.text_input("Encryption Password", type="password", key="enc_pass")
            if password:
                st.markdown('<span class="status-badge badge-success">🔒 Encrypted</span>',
                            unsafe_allow_html=True)

    # ── Right: Carrier ──
    with col_right:
        st.markdown('<div class="glass-card"><h3>📦 Carrier Medium</h3></div>',
                    unsafe_allow_html=True)

        carrier_type = st.selectbox("Carrier Type", ["Image", "Audio", "Video"], key="enc_carrier")
        carrier_type_key = carrier_type.lower()

        carrier_data = None
        if carrier_type == "Image":
            carrier_file = st.file_uploader("Upload carrier image",
                                            type=['png', 'jpg', 'jpeg', 'bmp'],
                                            key="carrier_img")
            if carrier_file:
                carrier_data = carrier_file.read()
                st.image(carrier_data, caption="Carrier Image", width=300)

        elif carrier_type == "Audio":
            carrier_file = st.file_uploader("Upload carrier audio (WAV)",
                                            type=['wav'], key="carrier_audio")
            if carrier_file:
                carrier_data = carrier_file.read()
                st.audio(carrier_data, format='audio/wav')

        elif carrier_type == "Video":
            carrier_file = st.file_uploader("Upload carrier video",
                                            type=['avi', 'mp4', 'mkv'], key="carrier_video")
            if carrier_file:
                carrier_data = carrier_file.read()
                st.video(carrier_data)

        # Capacity info
        if carrier_data:
            try:
                cap = check_capacity(carrier_data, carrier_type_key)
                data_size = len(secret_data) if secret_data else 0
                cap_kb = cap / 1024
                data_kb = data_size / 1024

                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-card">
                        <div class="value">{cap_kb:.1f} KB</div>
                        <div class="label">Carrier Capacity</div>
                    </div>
                    <div class="metric-card">
                        <div class="value">{data_kb:.1f} KB</div>
                        <div class="label">Data Size</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if secret_data and data_size > cap:
                    st.error("⚠️ Data exceeds carrier capacity! Use a larger carrier.")
                elif secret_data:
                    pct = (data_size / cap) * 100
                    st.progress(min(pct / 100, 1.0), text=f"Usage: {pct:.1f}%")
            except Exception as e:
                st.warning(f"Could not calculate capacity: {e}")

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        # Encode button
        if st.button("🚀 Encode & Generate Stego File", use_container_width=True, key="btn_encode"):
            if not secret_data:
                st.error("Please provide secret data to hide.")
            elif not carrier_data:
                st.error("Please upload a carrier file.")
            elif use_encryption and not password:
                st.error("Please enter an encryption password.")
            else:
                with st.spinner("🔄 Embedding data..."):
                    try:
                        video_ext = '.' + carrier_file.name.split('.')[-1] if carrier_type == "Video" else '.avi'
                        stego = encode(
                            data=secret_data,
                            data_type=data_type_key,
                            carrier_bytes=carrier_data,
                            carrier_type=carrier_type_key,
                            password=password if use_encryption else None,
                            video_ext=video_ext,
                        )

                        st.success("✅ Data embedded successfully!")
                        st.balloons()

                        # Determine file extension and mime
                        ext_map = {'image': ('.png', 'image/png'),
                                   'audio': ('.wav', 'audio/wav'),
                                   'video': ('.avi', 'video/x-msvideo')}
                        ext, mime = ext_map[carrier_type_key]

                        st.download_button(
                            label=f"⬇️ Download Stego File ({ext})",
                            data=stego,
                            file_name=f"stego_output{ext}",
                            mime=mime,
                            use_container_width=True,
                        )

                        if carrier_type_key == 'image':
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.image(carrier_data, caption="Original", width=250)
                            with col_b:
                                st.image(stego, caption="Stego (with hidden data)", width=250)

                    except Exception as e:
                        st.error(f"❌ Encoding failed: {e}")


# ══════════════════════════════════════════════
#  DECODE PAGE
# ══════════════════════════════════════════════
elif page == "📤 Decode":
    st.markdown("""
    <div class="hero-banner" style="padding:1.5rem;">
        <h1 style="font-size:1.8rem;">📤 Decode — Extract Hidden Data</h1>
        <p>Upload a stego file and recover the original secret</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="glass-card"><h3>📂 Stego File Input</h3></div>',
                    unsafe_allow_html=True)

        stego_type = st.selectbox("Stego Carrier Type",
                                  ["Image", "Audio", "Video"], key="dec_type")
        stego_type_key = stego_type.lower()

        stego_data = None
        if stego_type == "Image":
            stego_file = st.file_uploader("Upload stego image",
                                          type=['png', 'bmp'], key="dec_img")
            if stego_file:
                stego_data = stego_file.read()
                st.image(stego_data, caption="Stego Image", width=300)

        elif stego_type == "Audio":
            stego_file = st.file_uploader("Upload stego audio",
                                          type=['wav'], key="dec_audio")
            if stego_file:
                stego_data = stego_file.read()
                st.audio(stego_data, format='audio/wav')

        elif stego_type == "Video":
            stego_file = st.file_uploader("Upload stego video",
                                          type=['avi'], key="dec_video")
            if stego_file:
                stego_data = stego_file.read()

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card"><h3>🔐 Decryption</h3></div>',
                    unsafe_allow_html=True)
        was_encrypted = st.checkbox("Data was encrypted", value=False, key="dec_enc")
        dec_password = None
        if was_encrypted:
            dec_password = st.text_input("Decryption Password", type="password", key="dec_pass")

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        if st.button("🔍 Extract Hidden Data", use_container_width=True, key="btn_decode"):
            if not stego_data:
                st.error("Please upload a stego file.")
            elif was_encrypted and not dec_password:
                st.error("Please enter the decryption password.")
            else:
                with st.spinner("🔄 Extracting hidden data..."):
                    try:
                        data_type, extracted = decode(
                            stego_bytes=stego_data,
                            carrier_type=stego_type_key,
                            password=dec_password if was_encrypted else None,
                        )
                        st.session_state['decoded_type'] = data_type
                        st.session_state['decoded_data'] = extracted
                        st.success(f"✅ Extracted {data_type} data successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Decoding failed: {e}")

    with col_right:
        st.markdown('<div class="glass-card"><h3>🎯 Extracted Output</h3></div>',
                    unsafe_allow_html=True)

        if 'decoded_data' in st.session_state and st.session_state['decoded_data']:
            data_type = st.session_state['decoded_type']
            data = st.session_state['decoded_data']

            st.markdown(f'<span class="status-badge badge-success">Type: {data_type}</span>',
                        unsafe_allow_html=True)
            st.markdown("")

            if data_type == 'text':
                decoded_text = data.decode('utf-8', errors='replace')
                st.markdown(f"""
                <div class="glass-card">
                    <h3>💬 Recovered Message</h3>
                    <p style="color:#e0e0e0; font-size:1.05rem; line-height:1.6;">{decoded_text}</p>
                </div>
                """, unsafe_allow_html=True)
                st.download_button("⬇️ Download as Text", decoded_text,
                                   file_name="recovered_message.txt",
                                   use_container_width=True)

            elif data_type == 'image':
                recovered_img = Image.open(io.BytesIO(data))
                st.image(recovered_img, caption="Recovered Image", use_container_width=True)
                st.download_button("⬇️ Download Image", data,
                                   file_name="recovered_image.png",
                                   mime="image/png", use_container_width=True)

            elif data_type == 'audio':
                st.audio(data, format='audio/wav')
                st.download_button("⬇️ Download Audio", data,
                                   file_name="recovered_audio.wav",
                                   mime="audio/wav", use_container_width=True)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:3rem;">
                <p style="font-size:3rem; margin-bottom:0.5rem;">🔍</p>
                <p style="color:#888;">Upload a stego file and click Extract to see results here</p>
            </div>
            """, unsafe_allow_html=True)
