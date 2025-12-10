import io
import ctypes
import os
import sys
from ctypes import c_uint8, c_int, c_float, c_size_t, POINTER, Structure
from ctypes.util import find_library
from PIL import Image
import numpy as np

# Store diagnostic information
_libwebp_load_errors = []

def _try_load_libwebp(path):
    """Try to load libwebp from a specific path."""
    try:
        lib = ctypes.CDLL(path)
        _libwebp_load_errors.append(f"✅ Successfully loaded: {path}")
        return lib
    except OSError as e:
        _libwebp_load_errors.append(f"❌ Failed to load {path}: {e}")
        return None
    except Exception as e:
        _libwebp_load_errors.append(f"❌ Error loading {path}: {e}")
        return None

# Try to load libwebp library
libwebp = None

try:
    # First, try using find_library (works on most systems)
    found_lib = find_library('webp')
    if found_lib:
        libwebp = _try_load_libwebp(found_lib)
    
    # Also try 'libwebp' name
    if not libwebp:
        found_lib = find_library('libwebp')
        if found_lib:
            libwebp = _try_load_libwebp(found_lib)
    
    # If find_library didn't work, try manual paths
    if not libwebp:
        if hasattr(ctypes, 'windll'):
            # Windows - try multiple locations
            search_paths = [
                'libwebp.dll',  # System PATH
                'webp.dll',     # Alternative name
                os.path.join(os.path.dirname(__file__), 'libwebp.dll'),  # Same directory as script
                os.path.join(os.path.dirname(__file__), 'webp.dll'),
                os.path.join(sys.exec_prefix, 'libwebp.dll'),  # Python installation directory
                'C:\\Windows\\System32\\libwebp.dll',  # System32
                'C:\\Program Files\\libwebp\\bin\\libwebp.dll',  # Common installation path
            ]
            
            for path in search_paths:
                libwebp = _try_load_libwebp(path)
                if libwebp:
                    break
        else:
            # Linux/Mac
            search_paths = [
                'libwebp.so',      # System PATH
                'libwebp.so.7',    # Versioned
                'libwebp.so.8',
                'libwebp.dylib',   # macOS
                os.path.join(os.path.dirname(__file__), 'libwebp.so'),
                '/usr/lib/libwebp.so',
                '/usr/local/lib/libwebp.so',
                '/opt/homebrew/lib/libwebp.dylib',  # Homebrew on Apple Silicon
            ]
            
            for path in search_paths:
                libwebp = _try_load_libwebp(path)
                if libwebp:
                    break
except Exception as e:
    _libwebp_load_errors.append(f"❌ Unexpected error: {e}")
    libwebp = None

# Define WebP function signatures if libwebp is available
if libwebp:
    # WebPEncodeRGBA signature
    libwebp.WebPEncodeRGBA.argtypes = [
        POINTER(c_uint8),  # rgba
        c_int,             # width
        c_int,             # height
        c_int,             # stride
        c_float,           # quality_factor
        POINTER(POINTER(c_uint8))  # output
    ]
    libwebp.WebPEncodeRGBA.restype = c_size_t
    
    # WebPEncodeRGB signature
    libwebp.WebPEncodeRGB.argtypes = [
        POINTER(c_uint8),  # rgb
        c_int,             # width
        c_int,             # height
        c_int,             # stride
        c_float,           # quality_factor
        POINTER(POINTER(c_uint8))  # output
    ]
    libwebp.WebPEncodeRGB.restype = c_size_t
    
    # WebPEncodeLosslessRGBA signature
    libwebp.WebPEncodeLosslessRGBA.argtypes = [
        POINTER(c_uint8),  # rgba
        c_int,             # width
        c_int,             # height
        c_int,             # stride
        POINTER(POINTER(c_uint8))  # output
    ]
    libwebp.WebPEncodeLosslessRGBA.restype = c_size_t
    
    # WebPDecodeRGBA signature
    libwebp.WebPDecodeRGBA.argtypes = [
        POINTER(c_uint8),  # data
        c_size_t,          # data_size
        POINTER(c_int),    # width
        POINTER(c_int)     # height
    ]
    libwebp.WebPDecodeRGBA.restype = POINTER(c_uint8)
    
    # WebPDecodeRGB signature
    libwebp.WebPDecodeRGB.argtypes = [
        POINTER(c_uint8),  # data
        c_size_t,          # data_size
        POINTER(c_int),    # width
        POINTER(c_int)     # height
    ]
    libwebp.WebPDecodeRGB.restype = POINTER(c_uint8)
    
    # WebPFree signature for freeing memory
    libwebp.WebPFree.argtypes = [ctypes.c_void_p]
    libwebp.WebPFree.restype = None
    
    # WebPGetInfo signature
    libwebp.WebPGetInfo.argtypes = [
        POINTER(c_uint8),  # data
        c_size_t,          # data_size
        POINTER(c_int),    # width
        POINTER(c_int)     # height
    ]
    libwebp.WebPGetInfo.restype = c_int


def is_libwebp_available():
    """Check if libwebp library is available."""
    return libwebp is not None


def get_libwebp_diagnostics():
    """Get diagnostic information about libwebp loading attempts."""
    return _libwebp_load_errors.copy()


def encode_to_webp(rgba_data, width, height, quality_factor=80.0, lossless=False):
    """
    Encode RGBA image data to WebP using libwebp API.
    
    Args:
        rgba_data: bytes or numpy array of RGBA data
        width: image width
        height: image height
        quality_factor: quality factor (0-100) for lossy encoding
        lossless: if True, use lossless encoding
    
    Returns:
        bytes: WebP encoded data
    """
    if not libwebp:
        raise RuntimeError("libwebp library not found. Please install libwebp.")
    
    # Convert to bytes if numpy array
    if isinstance(rgba_data, np.ndarray):
        rgba_data = rgba_data.tobytes()
    
    # Create ctypes array
    rgba_array = (c_uint8 * len(rgba_data)).from_buffer_copy(rgba_data)
    stride = width * 4  # RGBA = 4 bytes per pixel
    
    # Create output pointer
    output_ptr = POINTER(c_uint8)()
    
    if lossless:
        # Use lossless encoding
        size = libwebp.WebPEncodeLosslessRGBA(
            rgba_array, width, height, stride, ctypes.byref(output_ptr)
        )
    else:
        # Use lossy encoding
        size = libwebp.WebPEncodeRGBA(
            rgba_array, width, height, stride, quality_factor, ctypes.byref(output_ptr)
        )
    
    if size == 0 or output_ptr is None:
        raise RuntimeError("WebP encoding failed")
    
    # Copy the encoded data
    webp_data = bytes(ctypes.string_at(output_ptr, size))
    
    # Free the memory allocated by libwebp
    libwebp.WebPFree(output_ptr)
    
    return webp_data


def decode_from_webp(webp_data):
    """
    Decode WebP image data to RGBA using libwebp API.
    
    Args:
        webp_data: bytes of WebP encoded data
    
    Returns:
        tuple: (rgba_data, width, height) where rgba_data is bytes
    """
    if not libwebp:
        raise RuntimeError("libwebp library not found. Please install libwebp.")
    
    # Create ctypes array from WebP data
    webp_array = (c_uint8 * len(webp_data)).from_buffer_copy(webp_data)
    
    # Get image info first
    width = c_int()
    height = c_int()
    if libwebp.WebPGetInfo(webp_array, len(webp_data), ctypes.byref(width), ctypes.byref(height)) == 0:
        raise RuntimeError("Invalid WebP data")
    
    width_val = width.value
    height_val = height.value
    
    # Decode RGBA
    rgba_ptr = libwebp.WebPDecodeRGBA(webp_array, len(webp_data), ctypes.byref(width), ctypes.byref(height))
    
    if rgba_ptr is None:
        raise RuntimeError("WebP decoding failed")
    
    # Calculate size and copy data
    rgba_size = width_val * height_val * 4
    rgba_data = bytes(ctypes.string_at(rgba_ptr, rgba_size))
    
    # Free the memory allocated by libwebp
    libwebp.WebPFree(rgba_ptr)
    
    return rgba_data, width_val, height_val


def convert_img_format(image_file, output_format, quality=80, lossless=False):
    """
    Convert image format using libwebp API for WebP operations.
    
    Args:
        image_file: file-like object or bytes
        output_format: target format (webp, png, jpeg, jpg, jfif, bmp)
        quality: quality factor for lossy formats (0-100)
        lossless: if True, use lossless WebP encoding
    
    Returns:
        BytesIO: converted image data
    """
    output_format_lower = output_format.lower()
    
    # Handle different input types - always read bytes first for reliability
    image_data = None
    
    # Read image data first
    if hasattr(image_file, 'read'):
        # File-like object (e.g., Streamlit UploadedFile)
        try:
            image_file.seek(0)  # Reset to beginning
            image_data = image_file.read()
            if not image_data:
                raise ValueError("Empty file or could not read file data")
        except Exception as e:
            raise ValueError(f"Could not read image file: {e}")
    else:
        # Assume it's bytes
        image_data = image_file
        if not image_data:
            raise ValueError("Empty image data provided")
    
    # Now open with PIL using the bytes data
    try:
        img = Image.open(io.BytesIO(image_data))
    except Exception as e:
        raise ValueError(f"Could not identify image format. The file may be corrupted or in an unsupported format: {e}")
    
    # Convert to RGBA for consistent handling
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    width, height = img.size
    rgba_data = img.tobytes()
    
    # Handle WebP output using libwebp API
    if output_format_lower == 'webp':
        if libwebp:
            try:
                webp_data = encode_to_webp(rgba_data, width, height, quality, lossless)
                output_img = io.BytesIO(webp_data)
                output_img.seek(0)
                return output_img
            except Exception as e:
                # Fallback to PIL if libwebp fails
                print(f"libwebp encoding failed, using PIL fallback: {e}")
                output_img = io.BytesIO()
                img.save(output_img, format='WEBP', quality=quality, lossless=lossless)
                output_img.seek(0)
                return output_img
        else:
            # Fallback to PIL if libwebp not available
            output_img = io.BytesIO()
            img.save(output_img, format='WEBP', quality=quality, lossless=lossless)
            output_img.seek(0)
            return output_img
    
    # Handle WebP input using libwebp API
    elif img.format == 'WEBP' and libwebp:
        try:
            # Decode using libwebp (image_data is always available at this point)
            rgba_data, width, height = decode_from_webp(image_data)
            # Create PIL image from decoded data
            img = Image.frombytes('RGBA', (width, height), rgba_data)
        except Exception as e:
            # Fallback to PIL if libwebp fails
            print(f"libwebp decoding failed, using PIL fallback: {e}")
            # Reopen image using the bytes we already have
            img = Image.open(io.BytesIO(image_data))
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
    
    # Convert to target format using PIL
    output_img = io.BytesIO()
    
    # Handle format-specific options
    save_kwargs = {}
    if output_format_lower in ['jpeg', 'jpg', 'jfif']:
        # Convert RGBA to RGB for JPEG
        if img.mode == 'RGBA':
            # Create white background
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = rgb_img
        save_kwargs['quality'] = quality
        save_kwargs['format'] = 'JPEG'
    elif output_format_lower == 'png':
        save_kwargs['format'] = 'PNG'
    elif output_format_lower == 'bmp':
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        save_kwargs['format'] = 'BMP'
    
    img.save(output_img, **save_kwargs)
    output_img.seek(0)
    return output_img
