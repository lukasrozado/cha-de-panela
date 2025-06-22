from flask import Flask, render_template, request, redirect
import json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configurações de e-mail
EMAIL_REMETENTE = "raphasgiffonis@gmail.com"
SENHA_APP = "bqph buno yfmr gjlb"
EMAIL_DESTINO = "raphasgiffonis@gmail.com"
RESERVAS_PATH = "reservas.json"

def carregar_reservas():
    try:
        with open(RESERVAS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_reservas(dados):
    with open(RESERVAS_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def enviar_email(assunto, corpo):
    mensagem = MIMEMultipart()
    mensagem['From'] = EMAIL_REMETENTE
    mensagem['To'] = EMAIL_DESTINO
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(mensagem)
            print(f"E-mail enviado: {assunto}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

@app.route("/")
def home():
    reservas = carregar_reservas()
    return render_template("index.html", reservas=reservas)

@app.route("/reservar", methods=["POST"])
def reservar():
    item = request.form["item"]
    nome = request.form["nome"]
    celular = request.form["celular"]

    reservas = carregar_reservas()
    if item not in reservas or reservas[item] is None:
        reservas[item] = {"nome": nome, "celular": celular}
        salvar_reservas(reservas)

        corpo = f"""
        🎁 Nova reserva feita:

        Item: {item}
        Nome: {nome}
        Celular: {celular}
        """
        enviar_email(f"Reserva de {item}", corpo)
    else:
        print(f"Item {item} já está reservado.")

    return redirect("/#presentes")

@app.route("/confirmar", methods=["POST"])
def confirmar():
    nome = request.form["nome"]
    celular = request.form["celular"]
    confirmacao = request.form["confirmacao"]

    corpo = f"""
    🥂 Confirmação de Presença recebida:

    Nome: {nome}
    Celular: {celular}
    Presença: {confirmacao}
    """
    enviar_email("Nova Confirmação de Presença", corpo)

    print(f"Confirmação recebida: {nome} | {celular} | {confirmacao}")

    return redirect("/#confirmacao")

if __name__ == "__main__":
    app.run(debug=True)
