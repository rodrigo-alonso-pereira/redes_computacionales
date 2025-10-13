import socket

HOST = '127.0.0.1' # Direccion del servidor (localhost)

tcp_port = 8001 # Puerto para Centro de Control (TCP)
udp_port = 8002 # Puerto para Sistema de Alertas (UDP)

# Verifica que el mensaje ingresado sea valido para TCP
def verificar_mensaje_tcp(mensaje):
    if mensaje.startswith("REPORTE:") or mensaje == "CONSULTAR" or mensaje == "MISION_COMPLETA":
        return True
    return False

while True:
    # Menu de opciones
    print("\n[ESTACION ESPACIAL] Iniciando sistema de comunicaciones...")
    print("1. Conectar con Centro de Control")
    print("2. Enviar alerta rapida")
    print("3. Abortar el envio de mensajes y salir")
    opcion = input("Seleccione una opcion (1-3): ")

    if opcion == '1': # Conexion Centro de Control [TCP]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_tcp:
            cliente_tcp.connect((HOST, tcp_port))
            print("[ESTACION ESPACIAL] Conectado con Centro de Control (TCP)")
            mensaje = ""
            while mensaje != "MISION_COMPLETA":
                mensaje = input("Astronauta> ")
                if not verificar_mensaje_tcp(mensaje):
                    print("Mensaje no permitido. Intente de nuevo con 'REPORTE:', 'CONSULTAR', 'MISION_COMPLETA'.")
                    continue
                cliente_tcp.sendall((mensaje + "\n").encode('utf-8'))
                print("Centro de control: ", cliente_tcp.recv(1024).decode('utf-8'))
            print("[ESTACION ESPACIAL] Desconectado de Centro de Control")
        break
    elif opcion == '2': # Conexion Sistema de Alertas [UDP]
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente_udp:
            print("[ESTACION ESPACIAL] Conectado con Sistema de Alertas (UDP)")
            mensaje = ""
            while mensaje != "base_segura":
                mensaje = input("Emergencia> ")
                cliente_udp.sendto(mensaje.encode('utf-8'), (HOST, udp_port))
                if mensaje == "base_segura":
                    print("Sistema: ", cliente_udp.recv(1024).decode('utf-8'))
                    break
                print("Alerta: ", cliente_udp.recv(1024).decode('utf-8'))
            print("\n[ESTACION ESPACIAL] Desconectado de Sistemas de Alertas")
        break
    elif opcion == '3': # Salir
        try: # Enviar señal de cierre a TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_shutdown:
                tcp_shutdown.connect((HOST, tcp_port))
                tcp_shutdown.sendall("MISION_COMPLETA".encode('utf-8'))
        except:
            pass
        
        try: # Enviar señal de cierre a UDP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_shutdown:
                udp_shutdown.sendto("base_segura".encode('utf-8'), (HOST, udp_port))
        except:
            pass
        
        print("\n[ESTACION ESPACIAL] Saliendo del sistema de comunicaciones. Hasta luego astronauta!")
        break
    else: # Opcion no valida
        print("Opcion no valida. Intente de nuevo.")
        continue
