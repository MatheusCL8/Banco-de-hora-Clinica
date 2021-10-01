import qrcode
from PIL import Image

def cria_qr_code(nome_funcionario):
    face = Image.open('_imagens/clinica.png')

    qr_big = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr_big.add_data(nome_funcionario)
    qr_big.make()
    img_qr_big = qr_big.make_image().convert('RGB')

    pos = ((img_qr_big.size[0] - face.size[0]) // 2, (img_qr_big.size[1] - face.size[1]) // 2)

    img_qr_big.paste(face, pos)
    img_qr_big.save(f'_qr_funcionarios/{nome_funcionario}.png')
    
    return True

