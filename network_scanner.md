### Descripción General del Código

Este script es un **escáner ARP** que utiliza la librería **Scapy** para enviar solicitudes de protocolo ARP (Address Resolution Protocol) a una red especificada y devolver una lista de dispositivos conectados con sus direcciones **IP** y **MAC**. Además, se utiliza el módulo **argparse** para recibir los parámetros del usuario desde la línea de comandos, permitiendo especificar el rango de IP a escanear.

### Explicación del Código

#### 1. **Importación de Módulos**

```python
import argparse
import scapy.all as scapy
```

- **`argparse`**: Este módulo permite procesar argumentos que se pasan al script desde la línea de comandos.
- **`scapy.all`**: Importa todas las funciones necesarias de la librería **Scapy**, utilizada para construir, enviar y recibir paquetes de red.

#### 2. **Función `get_arguments()`**

Esta función maneja los argumentos que se pasan desde la línea de comandos.

```python
def get_arguments():
    parser = argparse.ArgumentParser(description='ARP')
    parser.add_argument("--t", "--target", dest="target", help="IP range to scan")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please specify an IP range use --help for more info.")
    return args
```

- **`argparse.ArgumentParser()`**: Crea un nuevo objeto de parser, donde se define el propósito del script (en este caso, un escáner ARP).
- **`add_argument("--t", "--target", dest="target", help="IP range to scan")`**: Define el argumento `--t` o `--target`, que el usuario debe proporcionar para especificar el rango de IPs a escanear.
- **`if not args.target:`**: Si no se pasa ningún argumento, se muestra un mensaje de error solicitando al usuario que especifique un rango de IPs.
- **`return args`**: Devuelve los argumentos capturados.

#### 3. **Función `scan(ip)`**

Esta función se encarga de realizar el escaneo de la red utilizando ARP.

```python
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)  # Who has this IP? Using an ARP request
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Ethernet object
    arp_request_broadcast = broadcast/arp_request  # New packet
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list
```

- **`scapy.ARP(pdst=ip)`**: Crea un paquete ARP preguntando "¿Quién tiene esta IP?" en el rango especificado.
- **`scapy.Ether(dst="ff:ff:ff:ff:ff:ff")`**: Crea un paquete Ethernet con dirección de difusión, lo que significa que será enviado a todos los dispositivos en la red.
- **`broadcast/arp_request`**: Combina el paquete de difusión con la solicitud ARP para enviar una solicitud a toda la red.
- **`scapy.srp()`**: Envía y recibe paquetes a nivel de capa 2 (enlace de datos). Retorna dos listas: la primera con las respuestas recibidas y la segunda con los paquetes no respondidos. Aquí solo se usa la lista de respuestas (`answered_list`).
- **`clients_list`**: Una lista que contendrá diccionarios con las direcciones **IP** y **MAC** de los dispositivos que respondan a la solicitud ARP.
- **`element[1].psrc`**: Recupera la dirección IP del dispositivo que respondió.
- **`element[1].hwsrc`**: Recupera la dirección MAC del dispositivo que respondió.
- Finalmente, devuelve la lista `clients_list` con los dispositivos encontrados.

#### 4. **Función `print_result(results_list)`**

Esta función imprime los resultados del escaneo en un formato tabular.

```python
def print_result(results_list):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])
```

- **`print()`**: Imprime un encabezado de tabla que incluye las columnas "IP" y "MAC Address".
- **`for client in results_list:`**: Recorre la lista de clientes (dispositivos encontrados) y muestra su dirección IP y dirección MAC.

#### 5. **Ejecución del Programa**

```python
args = get_arguments()
scan_result = scan(str(args.target))
print_result(scan_result)
```

- **`get_arguments()`**: Obtiene los argumentos proporcionados por el usuario, en este caso, el rango de IPs a escanear.
- **`scan(args.target)`**: Realiza el escaneo de ARP en el rango de IPs proporcionado.
- **`print_result(scan_result)`**: Imprime los resultados del escaneo.

### Ejemplo de Ejecución

Si ejecutas este script con el comando:

```bash
python3 network_scanner.py --t 192.168.1.1/24
```

Y hay dispositivos activos en la red, obtendrás una salida como la siguiente:

```
IP                      MAC Address
------------------------------------------
192.168.1.2             00:1A:2B:3C:4D:5E
192.168.1.5             00:1A:2B:3C:4D:5F
192.168.1.10            00:1A:2B:3C:4D:60
```

### Resumen

Este script es una herramienta útil para escanear redes locales, descubrir dispositivos conectados y obtener información básica sobre ellos, como sus direcciones IP y MAC. La combinación de **argparse** y **Scapy** permite que el script sea dinámico y fácil de usar.
