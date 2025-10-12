# cocina.py
# Servidor TCP - Cocina (recibe pedidos y guarda historial)
import socket

HOST = '127.0.0.1'
PORT = 9001
historial = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen(1)
    print("[COCINA] Esperando conexión de la Caja...")

    conn, addr = servidor.accept()
    with conn:
        print(f"[COCINA] Conectado con {addr}")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            if data.startswith("PEDIDO:"):
                pedido = data.split("PEDIDO:")[1].strip()
                historial.append(pedido)
                conn.sendall("Pedido recibido y en preparación\n".encode('utf-8'))

            elif data.strip() == "HISTORIAL":
                respuesta = "=== HISTORIAL DE PEDIDOS ===\n" + "\n".join(historial)
                conn.sendall(respuesta.encode('utf-8'))

            elif data.strip() == "CIERRE":
                conn.sendall("Cocina cerrada. ¡Hasta mañana!\n".encode('utf-8'))
                break
