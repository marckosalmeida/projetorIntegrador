from flask import Flask, request, render_template_string

app = Flask(__name__)

nome_loja = "CASA MARIA DO BOLO E SALGADOS"

def valor_numero(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0.0

@app.route("/", methods=["GET", "POST"])
def index():
    total = 0.0
    itens = []

    if request.method == "POST":
        dados = {
            "bolo_qtd": valor_numero(request.form.get("bolo_qtd")),
            "bolo_preco": valor_numero(request.form.get("bolo_preco")),
            "salgados_qtd": valor_numero(request.form.get("salgados_qtd")),
            "salgados_preco": valor_numero(request.form.get("salgados_preco")),
            "doces_qtd": valor_numero(request.form.get("doces_qtd")),
            "doces_preco": valor_numero(request.form.get("doces_preco")),
            "refri_qtd": valor_numero(request.form.get("refri_qtd")),
            "refri_preco": valor_numero(request.form.get("refri_preco")),
            "outro_nome": request.form.get("outro_nome", "").strip(),
            "outro_qtd": valor_numero(request.form.get("outro_qtd")),
            "outro_preco": valor_numero(request.form.get("outro_preco")),
        }

        categorias = [
            ("Bolo", dados["bolo_qtd"], dados["bolo_preco"], "kg"),
            ("Salgados", dados["salgados_qtd"], dados["salgados_preco"], "un"),
            ("Doces", dados["doces_qtd"], dados["doces_preco"], "un"),
            ("Refrigerante", dados["refri_qtd"], dados["refri_preco"], "L"),
        ]

        for nome, qtd, preco, unidade in categorias:
            if qtd > 0 and preco > 0:
                subtotal = qtd * preco
                total += subtotal
                itens.append(f"{nome}: {qtd} {unidade} x R$ {preco:.2f} = R$ {subtotal:.2f}")

        if dados["outro_nome"] and dados["outro_qtd"] > 0 and dados["outro_preco"] > 0:
            subtotal = dados["outro_qtd"] * dados["outro_preco"]
            total += subtotal
            itens.append(f"{dados['outro_nome']}: {dados['outro_qtd']} x R$ {dados['outro_preco']:.2f} = R$ {subtotal:.2f}")

    return render_template_string("""
    <!doctype html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Orçamento de Festa</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
                padding: 30px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            h1, h2 {
                text-align: center;
                color: #333;
            }
            .linha {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }
            .grupo {
                margin-top: 15px;
            }
            label {
                display: block;
                font-weight: bold;
                margin-bottom: 5px;
            }
            input {
                width: 100%;
                padding: 10px;
                box-sizing: border-box;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            button {
                background: #007bff;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background: #005ecb;
            }
            .resumo {
                margin-top: 25px;
                background: #f9f9f9;
                padding: 16px;
                border-radius: 8px;
            }
            .total {
                font-size: 24px;
                font-weight: bold;
                color: green;
                margin-top: 15px;
            }
            ul {
                padding-left: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{{ nome_loja }}</h1>
            <h2>Orçamento para Festa</h2>

            <form method="POST">
                <div class="grupo">
                    <h3>Bolo</h3>
                    <div class="linha">
                        <div><label>Quantidade (kg)</label><input type="number" step="any" name="bolo_qtd"></div>
                        <div><label>Preço por kg</label><input type="number" step="any" name="bolo_preco"></div>
                    </div>
                </div>

                <div class="grupo">
                    <h3>Salgados</h3>
                    <div class="linha">
                        <div><label>Quantidade (un)</label><input type="number" step="any" name="salgados_qtd"></div>
                        <div><label>Preço por un</label><input type="number" step="any" name="salgados_preco"></div>
                    </div>
                </div>

                <div class="grupo">
                    <h3>Doces</h3>
                    <div class="linha">
                        <div><label>Quantidade (un)</label><input type="number" step="any" name="doces_qtd"></div>
                        <div><label>Preço por un</label><input type="number" step="any" name="doces_preco"></div>
                    </div>
                </div>

                <div class="grupo">
                    <h3>Refrigerante</h3>
                    <div class="linha">
                        <div><label>Quantidade (L)</label><input type="number" step="any" name="refri_qtd"></div>
                        <div><label>Preço por litro</label><input type="number" step="any" name="refri_preco"></div>
                    </div>
                </div>

                <div class="grupo">
                    <h3>Outros</h3>
                    <div class="linha">
                        <div><label>Nome do item</label><input type="text" name="outro_nome"></div>
                        <div><label>Quantidade</label><input type="number" step="any" name="outro_qtd"></div>
                    </div>
                    <label>Preço unitário</label>
                    <input type="number" step="any" name="outro_preco">
                </div>

                <button type="submit">Calcular orçamento</button>
            </form>

            {% if itens %}
            <div class="resumo">
                <h3>Resumo do orçamento</h3>
                <ul>
                    {% for item in itens %}
                        <li>{{ item }}</li>
                    {% endfor %}
                </ul>
                <div class="total">TOTAL: R$ {{ total:.2f }}</div>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """, nome_loja=nome_loja, itens=itens, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)