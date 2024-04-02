'''
create a QR code for a site(domain)
'''

import qrcode

url = "https://blue-stone-w.top/"

# Generate a QR code for the URL
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img_path = "./qr_code_example.png"
img.save(img_path)

img_path

