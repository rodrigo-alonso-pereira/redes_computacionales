# caja.py
# Cliente - Caja
import socket

HOST = '127.0.0.1'

# TCP para pedidos
tcp_port = 9001
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_tcp:
    cliente_tcp.connect((HOST, tcp_port))
    print("[CAJA] Conectado a la Cocina (TCP)")

    # Ejemplo: enviar pedidos
    cliente_tcp.sendall("PEDIDO: 2 Pizzas Napolitanas\n".encode('utf-8'))
    print("[CAJA] Respuesta:", cliente_tcp.recv(1024).decode('utf-8'))

    cliente_tcp.sendall("PEDIDO: 1 Pizza Margarita\n".encode('utf-8'))
    print("[CAJA] Respuesta:", cliente_tcp.recv(1024).decode('utf-8'))

    cliente_tcp.sendall("HISTORIAL\n".encode('utf-8'))
    print("[CAJA] Respuesta:\n", cliente_tcp.recv(1024).decode('utf-8'))

    cliente_tcp.sendall("CIERRE\n".encode('utf-8'))
    print("[CAJA] Respuesta:", cliente_tcp.recv(1024).decode('utf-8'))

# UDP para alertas rápidas
udp_port = 9002
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente_udp:
    print("[CAJA] Conectado al sistema de Entregas (UDP)")
    cliente_udp.sendto("Pedido listo para entrega".encode('utf-8'), (HOST, udp_port))
    print("[CAJA] Respuesta:", cliente_udp.recv(1024).decode('utf-8'))

    cliente_udp.sendto("Repartidor salió".encode('utf-8'), (HOST, udp_port))
    print("[CAJA] Respuesta:", cliente_udp.recv(1024).decode('utf-8'))

    cliente_udp.sendto("FIN".encode('utf-8'), (HOST, udp_port))
