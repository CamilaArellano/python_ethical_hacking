# Sniffer de Paquetes HTTP con Scapy

Este script utiliza la biblioteca Scapy para capturar y analizar paquetes HTTP que pasan por la interfaz de red especificada.

## Importación de Bibliotecas

```python
import scapy.all as scapy
from scapy.layers import http
```

- **scapy.all**: Importa todas las funcionalidades de Scapy, una poderosa biblioteca de manipulación de paquetes en Python.
- **http**: Importa las capas de HTTP para poder analizar los paquetes HTTP.

## Función `sniff(interface)`

```python
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
```

- **sniff**: Esta función inicia la captura de paquetes en la interfaz especificada.
- **iface**: El nombre de la interfaz de red (por ejemplo, `wlo1`).
- **store=False**: No almacena los paquetes en memoria.
- **prn=process_sniffed_packet**: Especifica la función a llamar para procesar cada paquete capturado.

## Función `process_sniffed_packet(packet)`

```python
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()
        print(f"[*] HTTP Request to: {url}")
        info = get_info(packet)
        if info:
            print(f"\n[*] Payload: {info}\n")
```

- **process_sniffed_packet**: Esta función se ejecuta para cada paquete capturado.
- **packet.haslayer(http.HTTPRequest)**: Verifica si el paquete contiene una capa de solicitud HTTP.
- **url**: Combina el host y la ruta de la solicitud HTTP y los decodifica.
- **print**: Imprime la URL de la solicitud HTTP.
- **get_info(packet)**: Llama a la función `get_info` para extraer información adicional del paquete.

## Función `get_info(packet)`

```python
def get_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load.decode(errors="ignore")
        return load
```

- **get_info**: Extrae el contenido del paquete si existe una carga útil (payload).
- **packet.haslayer(scapy.Raw)**: Verifica si hay datos crudos en el paquete.
- **load**: Decodifica la carga útil y la devuelve.

## Ejecución del Sniffer

```python
sniff("wlo1")
```

- **sniff("wlo1")**: Llama a la función `sniff` para comenzar a capturar paquetes en la interfaz `wlo1`.

## Uso

1. Asegúrate de tener permisos suficientes (puedes necesitar ejecutarlo como superusuario).
2. Instala Scapy si no lo tienes:
   ```bash
   pip install scapy
   ```
3. Ejecuta el script en un entorno que permita el acceso a la interfaz de red.
