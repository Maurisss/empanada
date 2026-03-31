import csv
from flask import Flask, render_template_string

# ... (tu código anterior)

@app.route('/ver_gastos')
def ver_gastos():
    filas = []
    total = 0
    with open('mis_gastos.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            filas.append(row)
            total += float(row[1]) # Suma el monto
            
    # HTML simple con estilo de casillas
    html = """
    <style>
        .gasto { border: 1px solid #00ff00; margin: 5px; padding: 10px; display: inline-block; width: 200px; }
        .total { font-size: 24px; color: yellow; margin-top: 20px; }
    </style>
    {% for f in filas %}
    <div class="gasto">
        <b>{{ f[0] }}</b><br>
        ${{ f[1] }} - {{ f[2] }}
    </div>
    {% endfor %}
    <div class="total">TOTAL: ${{ total }}</div>
    """
    return render_template_string(html, filas=filas, total=total)
