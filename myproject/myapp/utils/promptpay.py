# utils/promptpay.py
import libscrc
import qrcode
from io import BytesIO
from PIL import Image

def _format_tlv(tag: str, value: str) -> str:
    length_str = f"{len(value):02d}"
    return f"{tag}{length_str}{value}"

def calculate_crc(payload: str) -> str:
    crc = libscrc.ccitt_false(payload.encode('ascii'))
    return f"{crc:04X}"

def generate_promptpay_payload(mobile: str, amount: float) -> str:
    if not (len(mobile) == 10 and mobile.isdigit()):
        raise ValueError("Mobile must be 10 digits")

    mobile_value = f"00TH{mobile[1:]}"
    payload = (
        _format_tlv("00", "01") +
        _format_tlv("01", "12") +
        _format_tlv("29", _format_tlv("00", "A000000677010111") + _format_tlv("01", mobile_value)) +
        _format_tlv("53", "764") +
        _format_tlv("54", f"{float(amount):.2f}") +
        _format_tlv("58", "TH")
    )
    full_payload = payload + "6304"
    crc = calculate_crc(full_payload)
    return full_payload + crc

def generate_qr_image(payload: str) -> BytesIO:
    qr = qrcode.QRCode(box_size=8, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer
