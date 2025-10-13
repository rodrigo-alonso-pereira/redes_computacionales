import socket

HOST = '127.0.0.1' # Direccion del servidor (localhost)
PORT = 8001 # Puerto para Centro de Control (TCP)
CONNECTIONS = 1  # Numero maximo de conexiones permitidas
historial = [] # Historial de comunicaciones

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen(CONNECTIONS)
    print("[CENTRO DE CONTROL] Esperando conexiones de la Estacion Espacial...")

    conn, addr = servidor.accept()
    with conn:
        print(f"[CENTRO DE CONTROL] Conectado con {addr}")
        count = 0
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            if data.startswith("REPORTE:"):
                count += 1
                reporte = data.split("REPORTE:")[1].strip()
                historial.append(f"{count}. {reporte}")
                conn.sendall("Reporte almacenado. Todo bajo control, Estación.\n".encode('utf-8'))
            elif data.strip() == "CONSULTAR":
                respuesta = "=== HISTORIAL DE COMUNICACIONES ===\n" + "\n".join(historial)
                conn.sendall(respuesta.encode('utf-8'))
            elif data.strip() == "MISION_COMPLETA":
                conn.sendall("Comunicación finalizada. Buen trabajo, astronautas.\n".encode('utf-8'))
                break
        print("[CENTRO DE CONTROL] Desconectado de la Estacion Espacial")