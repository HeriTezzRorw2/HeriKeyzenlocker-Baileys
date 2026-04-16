import { default as makeWASocket, useMultiFileAuthState } from '@whiskeysockets/baileys';

async function start() {
    const { state, saveCreds } = await useMultiFileAuthState('session');
    const sock = makeWASocket({ auth: state, printQRInTerminal: false });
    
    sock.ev.on('connection.update', ({ pairingCode }) => {
        if (pairingCode) console.log('🔐 PAIRING CODE:', pairingCode);
    });
    
    sock.ev.on('creds.update', saveCreds);
    await sock.requestPairingCode('6281278455854'); // GANTI NOMOR LO
}

start();
