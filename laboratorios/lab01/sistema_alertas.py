import socket

HOST = '127.0.0.1'
PORT = 8002

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
    servidor.bind((HOST, PORT))
    print("[SISTEMA DE ALERTAS] Esperando alertas rapidas...")

    while True:
        data, addr = servidor.recvfrom(1024)
        mensaje = data.decode('utf-8')
        if mensaje == "base_segura":
            print("Modo emergencia desactivado. Mantente seguro alla arriba.")
            break
        respuesta = f"CONFIRMADO: {mensaje}"
        servidor.sendto(respuesta.encode('utf-8'), addr)