import socket

HOST = '127.0.0.1' # Direccion del servidor (localhost)
PORT = 8002 # Puerto para Sistema de Alertas (UDP)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
    servidor.bind((HOST, PORT))
    print("[SISTEMA DE ALERTAS] Esperando alertas rapidas...")

    while True:
        data, addr = servidor.recvfrom(1024)
        mensaje = data.decode('utf-8')
        if mensaje == "base_segura":
            respuesta = "Modo emergencia desactivado. Mantente seguro alla arriba."
            servidor.sendto(respuesta.encode('utf-8'), addr)
            break
        respuesta = f"CONFIRMADO: {mensaje}"
        servidor.sendto(respuesta.encode('utf-8'), addr)
    print("[SISTEMA DE ALERTAS] Desconectado de la Estacion Espacial")