from pyzbar import pyzbar
import cv2
from PyQt5.QtCore import QEventLoop, QTimer

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    barcode_info=''
    ok=''
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        # 1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 2
        '''font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)'''
        with open("barcode_result.txt", mode='w') as file:
                file.write(barcode_info)
        ok=True
    return frame,ok

def dados_func():
    with open("barcode_result.txt", mode='r') as file:
        dado=file.readlines()
    nome_func=dado[0]
    return nome_func
    
    

def sleep(segundos):
    mili=segundos*1000
    loop = QEventLoop()
    QTimer.singleShot(mili, loop.quit)
    loop.exec_()
