import streamlit as st
from PIL import Image
from imgconvrtr import convert_img_format

# Maximum file size limit: 200MB
MAX_FILE_SIZE_MB = 200
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # 200MB in bytes

# App Title
st.title("Image Converter")
st.markdown("**Powered by libwebp API, AVIF, and advanced optimizers**")

# Check library and tool availability
from imgconvrtr import (is_libwebp_available, get_libwebp_diagnostics,
                        is_libavif_available, get_libavif_diagnostics,
                        get_compression_tools)

libwebp_available = is_libwebp_available()
libavif_available = is_libavif_available()
compression_tools = get_compression_tools()

libwebp_status = "✅ Available" if libwebp_available else "⚠️ Not found (using Pillow fallback)"
libavif_status = "✅ Available" if libavif_available else "⚠️ Not found"

st.caption(f"libwebp status: {libwebp_status} | libavif status: {libavif_status}")

# Show compression tools status
tools_status = []
if compression_tools.get('mozjpeg'):
    tools_status.append("MozJPEG ✅")
if compression_tools.get('oxipng'):
    tools_status.append("OxiPNG ✅")
if compression_tools.get('optipng'):
    tools_status.append("OptiPNG ✅")

if tools_status:
    st.caption(f"Compression tools: {', '.join(tools_status)}")

# Show diagnostics if libraries are not available
if not libwebp_available or not libavif_available:
    with st.expander("🔍 Library Diagnostic Information"):
        if not libwebp_available:
            st.write("**Why libwebp is not found:**")
            diagnostics = get_libwebp_diagnostics()
            if diagnostics:
                for msg in diagnostics:
                    st.text(msg)
            else:
                st.text("No diagnostic information available.")
        
        if not libavif_available:
            st.write("**Why libavif is not found:**")
            diagnostics = get_libavif_diagnostics()
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
        
        2. **Install AVIF support:**
           - Run: `pip install pillow-avif-plugin`
        
        3. **Restart the Streamlit app** after copying the DLL file
        """)
        
        st.markdown("""
        **Option 3: Use Pillow's built-in WebP support**
        
        - The app will automatically use Pillow's WebP support as a fallback
        - Pillow includes libwebp internally, so WebP conversion will still work
        - You just won't get the direct libwebp API integration
        """)
        
        st.info("💡 **Tip:** Use Option 1 (automatic setup) for the easiest installation!")

# File Uploader - Support more formats including WebP, AVIF, and SVG
uploaded_file = st.file_uploader(
    "Upload an Image", 
    type=["png", "jpg", "jpeg", "jfif", "bmp", "webp", "avif", "svg"],
    help=f"Maximum file size: {MAX_FILE_SIZE_MB}MB"
)

if uploaded_file is not None:
    # Check file size limit (200MB)
    file_size = uploaded_file.size
    if file_size > MAX_FILE_SIZE_BYTES:
        def _format_size(num_bytes: int) -> str:
            """Format bytes into a human-readable string."""
            for unit in ["B", "KB", "MB", "GB"]:
                if num_bytes < 1024.0 or unit == "GB":
                    return f"{num_bytes:.1f} {unit}"
                num_bytes /= 1024.0
            return f"{num_bytes:.1f} GB"
        
        st.error(
            f"❌ File size exceeds the maximum limit of {MAX_FILE_SIZE_MB}MB. "
            f"Your file is {_format_size(file_size)}. "
            f"Please upload a smaller file."
        )
        st.stop()
    # Display the uploaded image
    # Handle SVG separately since it's a vector format
    file_extension = uploaded_file.name.lower().split('.')[-1] if uploaded_file.name else ''
    is_svg = file_extension == 'svg'
    
    # Store the original image for later comparison
    original_img_for_comparison = None
    
    if is_svg:
        # For SVG, we'll rasterize it for display
        from imgconvrtr import rasterize_svg
        try:
            svg_data = uploaded_file.read()
            uploaded_file.seek(0)  # Reset for conversion
            img = rasterize_svg(svg_data)
            original_img_for_comparison = img  # Store for comparison
            st.image(img, caption="Uploaded SVG Image (rasterized for preview)", width="stretch")
            st.write(f"**Original format:** SVG")
            st.write(f"**Image dimensions:** {img.size[0]} x {img.size[1]} pixels")
            st.info("ℹ️ SVG files will be rasterized before conversion to the selected format.")
        except Exception as e:
            st.error(f"❌ Could not load SVG: {str(e)}")
            st.stop()
    else:
        img = Image.open(uploaded_file)
        original_img_for_comparison = img.copy()  # Store for comparison
        st.image(img, caption="Uploaded Image", width="stretch")
        st.write(f"**Original format:** {img.format}")
        st.write(f"**Image dimensions:** {img.size[0]} x {img.size[1]} pixels")
    
    # Format selection dropdown - Include WebP and AVIF
    output_format = st.selectbox(
        "Choose the output format", 
        ["AVIF", "WebP", "PNG", "JPEG", "JFIF", "BMP"]
    )
    
    # Quality, lossless, and optimization options
    col1, col2, col3 = st.columns(3)
    
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
        if output_format.lower() in ["webp", "avif"]:
            lossless = st.checkbox(
                "Lossless encoding", 
                value=False,
                help=f"Lossless {output_format} encoding (no quality loss, larger file size)"
            )
    
    with col3:
        optimize = False
        if output_format.lower() in ["png", "jpeg", "jpg", "jfif"]:
            optimize = st.checkbox(
                "Advanced optimization",
                value=False,
                help="Use MozJPEG for JPEG or OxiPNG/OptiPNG for PNG (if available)"
            )
    
    # Convert and download the image
    if st.button("Convert 📸"):
        with st.spinner("Converting image..."):
            try:
                # Calculate original file size
                original_bytes = uploaded_file.getvalue()
                original_size = len(original_bytes) if original_bytes else 0

                converted_img = convert_img_format(
                    uploaded_file,
                    output_format.lower(),
                    quality=quality,
                    lossless=lossless,
                    optimize=optimize,
                )
                
                # Calculate converted file size
                converted_bytes = converted_img.getvalue()
                converted_size = len(converted_bytes)

                # Compute size change and percentage
                size_diff = converted_size - original_size
                if original_size > 0:
                    percent_change = (size_diff / original_size) * 100
                else:
                    percent_change = 0.0

                def _format_size(num_bytes: int) -> str:
                    """Format bytes into a human-readable string."""
                    for unit in ["B", "KB", "MB", "GB"]:
                        if num_bytes < 1024.0 or unit == "GB":
                            return f"{num_bytes:.1f} {unit}"
                        num_bytes /= 1024.0
                    return f"{num_bytes:.1f} GB"

                # Determine MIME type
                mime_types = {
                    "webp": "image/webp",
                    "png": "image/png",
                    "jpeg": "image/jpeg",
                    "jpg": "image/jpeg",
                    "jfif": "image/jpeg",
                    "bmp": "image/bmp",
                    "avif": "image/avif",
                }
                
                mime_type = mime_types.get(output_format.lower(), "image/webp")
                
                st.success("✅ Conversion successful!")
                
                # Before/After Image Comparison
                st.markdown("### 📊 Before/After Comparison")
                col_before, col_after = st.columns(2)
                
                # Load images for display
                # Reuse the original image that was already loaded and displayed
                if original_img_for_comparison is not None:
                    original_img = original_img_for_comparison
                else:
                    # Fallback: load it fresh if somehow not stored
                    uploaded_file.seek(0)  # Reset file pointer
                    if is_svg:
                        from imgconvrtr import rasterize_svg
                        svg_data = uploaded_file.read()
                        uploaded_file.seek(0)  # Reset for download
                        original_img = rasterize_svg(svg_data)
                    else:
                        original_img = Image.open(uploaded_file)
                
                # Load converted image for display
                converted_img.seek(0)  # Reset BytesIO pointer
                converted_img_display = Image.open(converted_img)
                converted_img.seek(0)  # Reset again for download button
                
                with col_before:
                    st.markdown("**📷 Original Image**")
                    st.image(original_img, use_container_width=True)
                    original_format_display = "SVG" if is_svg else (original_img.format or 'Unknown')
                    st.caption(f"**Format:** {original_format_display}")
                    st.caption(f"**Size:** {_format_size(float(original_size))}")
                    st.caption(f"**Dimensions:** {original_img.size[0]} × {original_img.size[1]} px")
                
                with col_after:
                    st.markdown("**✨ Converted Image**")
                    st.image(converted_img_display, use_container_width=True)
                    st.caption(f"**Format:** {output_format.upper()}")
                    st.caption(f"**Size:** {_format_size(float(converted_size))}")
                    st.caption(f"**Dimensions:** {converted_img_display.size[0]} × {converted_img_display.size[1]} px")
                
                # Size comparison statistics
                st.markdown("---")
                st.markdown("### 📈 Size Comparison")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric(
                        label="Original Size",
                        value=_format_size(float(original_size))
                    )
                
                with col_stat2:
                    st.metric(
                        label="Converted Size",
                        value=_format_size(float(converted_size)),
                        delta=f"{percent_change:+.2f}%"
                    )
                
                with col_stat3:
                    size_saved = abs(size_diff) if size_diff < 0 else 0
                    size_increased = size_diff if size_diff > 0 else 0
                    if size_diff < 0:
                        st.metric(
                            label="Space Saved",
                            value=_format_size(float(size_saved))
                        )
                    else:
                        st.metric(
                            label="Size Change",
                            value=_format_size(float(size_increased))
                        )
                
                st.download_button(
                    label=f"📥 Download as {output_format}",
                    data=converted_img,
                    file_name=f"image.{output_format.lower()}",
                    mime=mime_type,
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")
                st.exception(e)

# Footer with information
st.markdown("---")
st.markdown("""
### Supported Formats
- **Input:** PNG, JPEG, JFIF, BMP, WebP, AVIF, SVG
- **Output:** AVIF, WebP (via libwebp API), PNG, JPEG, JFIF, BMP

### Features
- Direct integration with libwebp C API for WebP encoding/decoding
- AVIF output support via Pillow/pillow-avif-plugin
- Lossless and lossy WebP/AVIF encoding options
- Advanced optimization using MozJPEG, OxiPNG, and OptiPNG when available
- Quality control for lossy formats
- Automatic format detection and conversion
""")
