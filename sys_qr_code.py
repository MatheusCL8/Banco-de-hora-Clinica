import cv2
from PyQt5 import QtCore
from PyQt5.QtCore  import pyqtSlot
from PyQt5.QtGui import QIcon,QImage , QPixmap
from PyQt5.QtWidgets import QMainWindow,QMessageBox
from PyQt5.uic import loadUi
from _imagens import imagens
from datetime import datetime
from util import read_barcodes,sleep,dados_func
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
import sys
from leitor_excel import folha_de_ponto
from criar_qr_code import cria_qr_code
app = QtWidgets.QApplication(sys.argv)

class sis_qr_code(QMainWindow):
    global horario_atual,hd,user
    hd=datetime.now()
    horario_atual=hd.strftime('%H:%M:%S')
    def __init__(self):
        
        super(sis_qr_code,self).__init__()
        self.window=loadUi("leitor_qr.ui",self)
        self.setMaximumSize(1300, 850)
        self.logic = 0
        self.value = 0
        #BOTÃO QUE ABRE A CÂMERA
        self.abrir_camera.clicked.connect(self.onClicked)    
        #BOTÃO QUE FECHA A CÂMERA
        self.fechar_camera.clicked.connect(self.CloseCapture)
        #BOTÃO DE LOGOUT
        self.sair.clicked.connect(self.closeEvent)
        self.qr_code.clicked.connect(self.passar_nome_func)
        self.enviar_nome.clicked.connect(self.criar_qr)
        #CONTROLE DE CAMADAS
        self.window.imgLabel.close()
        self.window.pega_nome.close()
        self.window.info.close()
        self.window.fechar_camera.close()
        self.hora_func.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 75 12pt \"Arial\";")
        self.nome_func.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 75 12pt \"Arial\";")

    @pyqtSlot()
    def onClicked(self):  
        _translate = QtCore.QCoreApplication.translate
        self.window.abrir_camera.close()
        self.window.fechar_camera.show()
        #FUNÇÃO QUE ABRE A CÂMERA
        self.window.imgLabel.show()
        try:
            self.cap =cv2.VideoCapture(0)
            while(self.cap.isOpened()):  
                ret, frame=self.cap.read()
                ok=False
                frame,ok = read_barcodes(frame)
                self.displayImage(frame,1)
                cv2.waitKey(0)
                if ok is True:
                    nome_funcionario=dados_func()
                    sleep(2)
                    validador=folha_de_ponto(nome_funcionario)
                    if validador is True:
                        self.nome_func.setText(f'Funcionário: {nome_funcionario}')
                        self.nome_func.setStyleSheet("background-color: rgb(121, 255, 152);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 75 12pt \"Arial\";")
                        self.hora_func.setText(f'Registrado no horário: {horario_atual}')
                        self.hora_func.setStyleSheet("background-color: rgb(121, 255, 152);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 75 12pt \"Arial\";")
                        sleep(3)
                        self.window.nome_func.setText(_translate("MainWindow", "Nome Funcionário"))
                        self.window.hora_func.setText(_translate("MainWindow", "Horário Registrado"))
                        self.hora_func.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 75 12pt \"Arial\";")
                        self.nome_func.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 75 12pt \"Arial\";")
                        
                    elif validador is False:
                        self.window.info.show()
                        self.info_text.setText('BANCO DE HORA CRIADO\nCOM SUCESSO\nPASSE O QR-CODE NOVAMENTE')
                        self.info_text.setStyleSheet("background-color: rgb(202,0,88);\n"
                                                "color: rgb(0, 0, 0);\n"
                                                "font: 75 10pt \"Arial\";\n"
                                                "font-align:center;"
                                                )
                        sleep(2)
                        self.window.info.close()
                   
                        
                if self.logic==2:
                    continue

                elif self.logic==3:
                    break

                elif (self.logic==4):
                    #FECHA A CAMERA
                    self.cap.release()
                    self.window.imgLabel.close()
                    self.window.fechar_camera.close()
                    self.window.abrir_camera.show()
                    self.logic=0             
        except:
            '''self.window.regi_saida.show()
            self.text_saida.setText("Camera não encontrada\nPor favor, contatar o técnico")
            self.text_saida.setStyleSheet("color: rgb(255, 255, 255);\n"
    "font: 75 16pt \"Arial\";\n"
    "padding-top:5px;\n"
    "padding-left: 5px;\n"
    "align: center;")
            sleep(7)
            self.window.regi_saida.close()'''
            self.window.imgLabel.close()
            self.window.fechar_camera.close()
            self.window.abrir_camera.show()

        self.cap.release()
        cv2.destroyAllWindows()
    
    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("Deseja fechar o programa?")
        close.setStyleSheet("background-color: rgb(255,255,255);\n"
                                "color: rgb(28, 41, 48);\n"
                                "font: 75 10pt \"Arial\";\n")
        
        #close.setStyleSheet("QButton{background-color: rgb(255, 255, 255);}")
        close.setWindowTitle ("CLINICA ESPAÇO SAÚDE")
        close.setWindowIcon(QIcon('./_imagens/clinica.ico'))
        close.setIcon(QMessageBox.Warning)
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()
        if close == QMessageBox.Yes:
            self.logic=3
            self.window.close()
        elif close==QMessageBox.Cancel:
            if not type(event) == bool:
                event.ignore()
                self.logic=2

    def CloseCapture(self):
        self.logic=4
    
    def passar_nome_func(self):
        self.value+=1
        self.window.pega_nome.show()
        if self.value>1:
            self.window.pega_nome.close()
            self.value=0
    
    def criar_qr(self):
        nome=self.window.nome.text()
        nome=nome.upper()
        confirmacao=cria_qr_code(nome)
        if confirmacao is True:
            self.window.pega_nome.close()
            self.window.info.show()
            self.info_text.setText('QR-CODE CRIADO\nCOM SUCESSO')
            self.info_text.setStyleSheet("background-color: rgb(202,0,88);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 75 12pt \"Arial\";"
                                    )
            sleep(2)
            self.window.info.close()
                       
    def displayImage(self,img,window=1):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if(img.shape[2])==4:
                qformat=QImage.Format_RGBA888
            else:
                qformat=QImage.Format_RGB888
        img = QImage(img,img.shape[1],img.shape[0],qformat)
        img=img.scaled(900, 700, QtCore.Qt.KeepAspectRatio)
        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

def main():
    tela_login=sis_qr_code()
    tela_login.show()
    sys.exit(app.exec_())

main() 