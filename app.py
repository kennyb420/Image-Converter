import streamlit as st
from PIL import Image
from imgconvrtr import convert_img_format

# App Title
st.title("Image Converter")
st.markdown("**Powered by libwebp API**")

# Check libwebp availability
from imgconvrtr import is_libwebp_available, get_libwebp_diagnostics

libwebp_available = is_libwebp_available()
libwebp_status = "✅ Available" if libwebp_available else "⚠️ Not found (using Pillow fallback)"
st.caption(f"libwebp status: {libwebp_status}")

# Show diagnostics if libwebp is not available
if not libwebp_available:
    with st.expander("🔍 libwebp Diagnostic Information"):
        st.write("**Why libwebp is not found:**")
        diagnostics = get_libwebp_diagnostics()
        if diagnostics:
            for msg in diagnostics:
                st.text(msg)
        else:
            st.text("No diagnostic information available.")
        
        st.markdown("---")
        st.write("**How to fix:**")
        
        st.markdown("""
        **Option 1: Automatic Setup (Easiest)**
        
        Run one of these scripts in your project folder:
        - **PowerShell:** `.\setup_libwebp.ps1`
        - **Command Prompt:** `setup_libwebp.bat`
        
        These scripts will automatically download and set up libwebp.dll for you!
        """)
        
        st.markdown("""
        **Option 2: Manual Setup**
        
        1. **Download libwebp for Windows:**
           - Visit: https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.2.1-windows-x64.zip
           - Extract the ZIP file
           - Copy `libwebp.dll` from the `bin` folder to the same folder as `app.py`
        
        2. **Restart the Streamlit app** after copying the DLL file
        """)
        
        st.markdown("""
        **Option 3: Use Pillow's built-in WebP support**
        
        - The app will automatically use Pillow's WebP support as a fallback
        - Pillow includes libwebp internally, so WebP conversion will still work
        - You just won't get the direct libwebp API integration
        """)
        
        st.info("💡 **Tip:** Use Option 1 (automatic setup) for the easiest installation!")

# File Uploader - Support more formats including WebP
uploaded_file = st.file_uploader(
    "Upload an Image", 
    type=["png", "jpg", "jpeg", "jfif", "bmp", "webp"]
)

if uploaded_file is not None:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)
    st.write(f"**Original format:** {img.format}")
    st.write(f"**Image dimensions:** {img.size[0]} x {img.size[1]} pixels")
    
    # Format selection dropdown - Include WebP
    output_format = st.selectbox(
        "Choose the output format", 
        ["WebP", "PNG", "JPEG", "JFIF", "BMP"]
    )
    
    # Quality and lossless options (especially for WebP)
    col1, col2 = st.columns(2)
    
    with col1:
        quality = st.slider(
            "Quality (for lossy formats)", 
            min_value=0, 
            max_value=100, 
            value=80,
            help="Higher values mean better quality but larger file size"
        )
    
    with col2:
        lossless = False
        if output_format.lower() == "webp":
            lossless = st.checkbox(
                "Lossless encoding", 
                value=False,
                help="Lossless WebP encoding (no quality loss, larger file size)"
            )
    
    # Convert and download the image
    if st.button("Convert 📸"):
        with st.spinner("Converting image..."):
            try:
                converted_img = convert_img_format(
                    uploaded_file, 
                    output_format.lower(), 
                    quality=quality,
                    lossless=lossless
                )
                
                # Determine MIME type
                mime_types = {
                    "webp": "image/webp",
                    "png": "image/png",
                    "jpeg": "image/jpeg",
                    "jpg": "image/jpeg",
                    "jfif": "image/jpeg",
                    "bmp": "image/bmp"
                }
                
                mime_type = mime_types.get(output_format.lower(), "image/webp")
                
                st.success("✅ Conversion successful!")
                st.download_button(
                    label=f"Download as {output_format}",
                    data=converted_img,
                    file_name=f"image.{output_format.lower()}",
                    mime=mime_type
                )
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")
                st.exception(e)

# Footer with information
st.markdown("---")
st.markdown("""
### Supported Formats
- **Input:** PNG, JPEG, JFIF, BMP, WebP
- **Output:** WebP (via libwebp API), PNG, JPEG, JFIF, BMP

### Features
- Direct integration with libwebp C API for WebP encoding/decoding
- Lossless and lossy WebP encoding options
- Quality control for lossy formats
- Automatic format detection and conversion
""")
