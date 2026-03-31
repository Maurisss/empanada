from flask import Flask, render_template_string
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

@app.route('/ver_gastos')
def ver_gastos():
    filas = []
    total = 0
    try:
        with open('/root/empanada/mis_gastos.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Si la línea tiene 4 partes (Fecha, Hora, Monto, Detalle)
                if len(row) >= 4:
                    fecha_completa = f"{row[0]} {row[1]}" # Junta fecha y hora
                    monto_str = row[2]
                    detalle = row[3]
                # Si tiene el formato viejo de 3 partes
                elif len(row) == 3:
                    fecha_completa = row[0]
                    monto_str = row[1]
                    detalle = row[2]
                else:
                    continue

                try:
                    monto_valor = float(monto_str.strip())
                    total += monto_valor
                    filas.append([fecha_completa, monto_valor, detalle])
                except ValueError:
                    continue
                    
    except Exception as e:
        return f"<p style='color:red;'>Error de lectura: {e}</p>"

    # Generamos el HTML con las filas procesadas
    filas_html = "".join([
        f"<tr style='border-bottom: 1px solid #111;'>"
        f"<td style='padding:5px;'>{f[0]}</td>"
        f"<td style='padding:5px; color:yellow;'>${f[1]:,.0f}</td>"
        f"<td style='padding:5px; color:white;'>{f[2]}</td>"
        f"</tr>" for f in filas
    ])

    html = f"""
    <div style='color: #00ff00; font-family: monospace; background: #000; padding: 15px; border: 1px solid #00ff00;'>
        <h3 style='margin-top:0;'>🟢 TERMINAL MAURICIO v1.0</h3>
        <table style='width:100%; border-collapse: collapse;'>
            <tr style='border-bottom: 2px solid #00ff00; text-align: left;'>
                <th>FECHA</th><th>MONTO</th><th>DETALLE</th>
            </tr>
            {filas_html}
        </table>
        <h2 style='color: #ffff00; text-align: right; border-top: 2px solid #00ff00; padding-top: 10px;'>
            💰 TOTAL ACUMULADO: ${total:,.0f}
        </h2>
    </div>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')

