# entrega.py
# Servidor UDP - Entregas (mensajes rápidos sin historial)
import socket

HOST = '127.0.0.1'
PORT = 9002

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
    servidor.bind((HOST, PORT))
    print("[ENTREGA] Esperando alertas rápidas...")

    while True:
        data, addr = servidor.recvfrom(1024)
        mensaje = data.decode('utf-8')
        if mensaje == "FIN":
            print("[ENTREGA] Sistema de entregas finalizado.")
            break
        respuesta = f"CONFIRMADO: {mensaje}"
        servidor.sendto(respuesta.encode('utf-8'), addr)
