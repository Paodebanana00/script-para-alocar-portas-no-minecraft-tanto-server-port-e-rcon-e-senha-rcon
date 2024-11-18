from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import logging
import os
from dotenv import load_dotenv

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Languages dictionary
LANGUAGES = {
    'pt': {
        'start': 'Start',
        'pro': 'Pro',
        'ultra': 'Ultra',
        'hire_now': 'Contratar Agora',
        'features': {
            'anti_ddos': 'Anti-DDoS',
            'panel': 'Painel Pterodactyl',
            'support': 'Suporte 24/7',
            'backup': 'Backup Diário',
            'instant': 'Instalação Instantânea',
            'ip': 'IP Dedicado',
            'priority': 'Prioridade no Suporte'
        }
    },
    'en': {
        'start': 'Start',
        'pro': 'Pro',
        'ultra': 'Ultra',
        'hire_now': 'Hire Now',
        'features': {
            'anti_ddos': 'Anti-DDoS',
            'panel': 'Pterodactyl Panel',
            'support': '24/7 Support',
            'backup': 'Daily Backup',
            'instant': 'Instant Setup',
            'ip': 'Dedicated IP',
            'priority': 'Priority Support'
        }
    }
}

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'super_secret_key')

# Plans definition
plans = [
    {
        "id": 1,
        "name": "Start",
        "cores": 2,
        "ram": 2,
        "disk": "20GB SSD NVMe",
        "bandwidth": "Ilimitado",
        "price": 19.99,
        "features": [
            "Anti-DDoS",
            "Painel Pterodactyl",
            "Suporte 24/7",
            "Backup Diário",
            "Instalação Instantânea"
        ]
    },
    {
        "id": 2,
        "name": "Pro",
        "cores": 4,
        "ram": 4,
        "disk": "40GB SSD NVMe",
        "bandwidth": "Ilimitado",
        "price": 39.99,
        "features": [
            "Anti-DDoS",
            "Painel Pterodactyl",
            "Suporte 24/7",
            "Backup Diário",
            "Instalação Instantânea",
            "IP Dedicado"
        ]
    },
    {
        "id": 3,
        "name": "Ultra",
        "cores": 6,
        "ram": 8,
        "disk": "80GB SSD NVMe",
        "bandwidth": "Ilimitado",
        "price": 59.99,
        "features": [
            "Anti-DDoS",
            "Painel Pterodactyl",
            "Suporte 24/7",
            "Backup Diário",
            "Instalação Instantânea",
            "IP Dedicado",
            "Prioridade no Suporte"
        ]
    }
]

# Coupons definition
coupons = {
    "WELCOME10": {"discount": 0.10, "valid": True},
    "SUPER20": {"discount": 0.20, "valid": True}
}

# Users definition
users = {}

# Routes
@app.route("/")
def index():
    logger.info("Página inicial acessada")
    current_language = session.get('language', 'pt')
    return render_template("index.html", plans=plans, LANGUAGES=LANGUAGES, current_language=current_language)

@app.route('/change_language/<lang>')
def change_language(lang):
    if lang in LANGUAGES:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    plan_id = int(request.form.get("plan_id"))
    plan = next((p for p in plans if p["id"] == plan_id), None)
    
    if not plan:
        logger.error(f"Plano não encontrado: {plan_id}")
        return jsonify({"error": "Plano não encontrado!"}), 404
    
    if "cart" not in session:
        session["cart"] = []
    
    session["cart"].append(plan)
    session.modified = True
    logger.info(f"Plano adicionado ao carrinho: {plan['name']}")
    return jsonify({"message": f"Plano '{plan['name']}' adicionado ao carrinho!"})

@app.route("/cart")
def cart():
    logger.info("Carrinho visualizado")
    cart_items = session.get("cart", [])
    total_price = sum(item["price"] for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total_price=total_price)

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    plan_id = int(request.form.get("plan_id"))
    if "cart" in session:
        session["cart"] = [item for item in session["cart"] if item["id"] != plan_id]
        session.modified = True
        logger.info(f"Plano removido do carrinho: {plan_id}")
        return jsonify({"message": "Plano removido com sucesso!"})
    logger.warning("Tentativa de remover item de carrinho vazio")
    return jsonify({"error": "Carrinho vazio!"}), 404

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        if not session.get("cart"):
            logger.warning("Tentativa de checkout com carrinho vazio")
            return jsonify({"error": "Carrinho vazio!"}), 400
        session.pop("cart", None)
        logger.info("Checkout realizado com sucesso")
        return redirect(url_for("index"))
    
    cart_items = session.get("cart", [])
    total_price = sum(item["price"] for item in cart_items)
    return render_template("checkout.html", cart_items=cart_items, total_price=total_price)

@app.route("/apply_coupon", methods=["POST"])
def apply_coupon():
    code = request.form.get("coupon_code").upper()
    coupon = coupons.get(code)

    if not coupon or not coupon["valid"]:
        return jsonify({"error": "Cupom inválido"}), 400

    session["coupon"] = code
    return jsonify({"message": f"Cupom {code} aplicado com sucesso!"})

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    user_data = users[session["user"]]
    return render_template(
        "dashboard.html",
        orders=user_data["orders"],
        points=user_data["points"]
    )

@app.errorhandler(404)
def not_found_error(error):
    logger.error(f"Página não encontrada: {request.url}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro interno do servidor: {error}")
    return render_template('500.html'), 500

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    # ... (código original)

    # Exibir notificação visual e atualizar página
    return jsonify({"message": f"Plano '{plan['name']}' adicionado ao carrinho!"})

if __name__ == "__main__":
    app.run(debug=True)