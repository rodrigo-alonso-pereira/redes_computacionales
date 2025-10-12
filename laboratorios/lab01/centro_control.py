import socket

HOST = '127.0.0.1'
PORT = 8001
CONNECTIONS = 1  # Numero maximo de conexiones permitidas
historial = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen(CONNECTIONS)
    print("[CENTRO DE CONTROL] Esperando conexiones de la Estacion Espacial...")

    conn, addr = servidor.accept()
    with conn:
        print(f"[CENTRO DE CONTROL] Conectado con {addr}")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            if data.startswith("REPORTE:"):
                reporte = data.split("REPORTE:")[1].strip()
                historial.append(reporte)
                conn.sendall("Centro de control: Reporte almacenado. Todo bajo control, Estación.\n".encode('utf-8'))
            elif data.strip() == "CONSULTAR":
                respuesta = "=== HISTORIAL DE COMUNICACIONES ===\n" + "\n".join(historial)
                conn.sendall(respuesta.encode('utf-8'))
            elif data.strip() == "MISION_COMPLETA":
                conn.sendall("Centro de control: Comunicación finalizada. Buen trabajo, astronautas.")
                break;