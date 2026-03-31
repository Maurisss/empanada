const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { 
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    }
});

client.on('qr', (qr) => {
    console.log('ESCANEÁ ESTO CON TU WHATSAPP:');
    qrcode.generate(qr, {small: true});
});

client.on('ready', () => {
    console.log('¡Conexión exitosa! El sistema está online, Mauricio.');
});

client.on('message_create', async msg => {
    const chat = await msg.getChat();
    
    // FILTRO: Solo el chat 'Mau' y solo mensajes enviados por VOS
    if (chat.name === 'Mau' && msg.fromMe) {
        
        // 1. Buscamos el número (soporta 1500, 1.500 o 1500,50)
        const regexNumero = /\d+([\.,]\d+)?/g;
        const matches = msg.body.match(regexNumero);
        
        if (matches) {
            // Limpiamos el número para que sea un decimal válido
            let monto = parseFloat(matches[0].replace(',', '.'));
            const texto = msg.body.toLowerCase();

            // 2. LÓGICA DE MULTIPLICACIÓN: 
            if (texto.includes('mil')) {
                monto = monto * 1000;
            }

            // Separamos el detalle (el cuerpo del mensaje sin el número ni la palabra mil)
            const detalle = msg.body.replace(matches[0], '').replace(/mil/gi, '').trim();
            const fecha = new Date().toLocaleString();
            
            // 3. Definimos la RUTA ABSOLUTA (La roca del sistema)
            const rutaArchivo = '/root/empanada/mis_gastos.csv';
            
            // Preparamos la línea: Fecha, Monto, Detalle
            const linea = `${fecha},${monto},${detalle}\n`;
            
            try {
                // Guardamos usando la ruta completa
                fs.appendFileSync(rutaArchivo, linea);
                
                // Estos console.log te confirman en la terminal lo que se guardó
                console.log(`✅ REGISTRADO EN: ${rutaArchivo}`);
                console.log(`   > MONTO: $${monto}`);
                console.log(`   > CUERPO: ${detalle}`);
            } catch (err) {
                console.error('❌ Error crítico al escribir:', err);
            }
        }
    }
});

client.initialize();
