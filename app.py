from flask import Flask, redirect
import sqlite3
import os

app = Flask(__name__)

# Insira os três números de WhatsApp aqui (apenas números, sem caracteres especiais)
WHATSAPP_NUMBERS = [
    '5574999728473',
    '554331423423',
]

DATABASE = 'counter.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY, value INTEGER)''')
    conn.commit()
    conn.close()

def get_and_update_counter():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT value FROM counter WHERE id=1')
    result = c.fetchone()
    
    if result:
        counter = result[0]
    else:
        counter = 0
        c.execute('INSERT INTO counter (id, value) VALUES (1, 0)')

    next_counter = (counter + 1) % len(WHATSAPP_NUMBERS)
    c.execute('UPDATE counter SET value=? WHERE id=1', (next_counter,))
    conn.commit()
    conn.close()

    return counter

@app.route('/')
def redirect_to_whatsapp():
    init_db()
    index = get_and_update_counter()
    selected_number = WHATSAPP_NUMBERS[index]
    return redirect(f'https://wa.me/{selected_number}?text=Quero%20receber%20meu%20acesso%20gratuito%20do%20Hacker%20Win', code=302)

if __name__ == '__main__':
    app.run()
