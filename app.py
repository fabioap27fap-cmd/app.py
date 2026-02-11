import streamlit as st
import socket

# 1. Configuração da Página
st.set_page_config(page_title="Ftek - Suporte AGF", layout="wide", page_icon="🚀")

# 2. FUNÇÃO DE MONITORAMENTO (Technical Port Check)
def check_port(ip_port):
    try:
        if ":" in ip_port:
            target_ip = ip_port.split(":")[0]
            target_port = int(ip_port.split(":")[1])
        else:
            target_ip = ip_port
            target_port = 80 
            
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5) 
        result = s.connect_ex((target_ip, target_port))
        s.close()
        return result == 0, target_port
    except:
        return False, 80

# 3. BASE DE DADOS COMPLETA
dados_agencias = {
    "Agf Itaberába": {"mcu": "00423154", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.104.170:1010", "mask": "255.255.255.0", "gw": "201.6.104.1"}, "wan2": {"op": "VIVO", "tipo": "FIXO", "ip": "177.189.223.190:1010", "mask": "255.255.255.0", "gw": "0.0.0.0"}},
    "Agf Cidade Dutra": {"mcu": "423152", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.159.203", "mask": "255.255.255.0", "gw": "201.6.159.1"}, "wan2": {"op": "Não tem", "tipo": "FIXO", "ip": "0.0.0.0"}},
    "Agf Vieira de Morais": {"mcu": "423153", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.145.30", "mask": "255.255.255.0", "gw": "201.6.145.1"}, "wan2": {"op": "VIVO Antiga Gvt", "tipo": "PPPoE", "user": "gvt25", "pass": "1133602736", "ip": "201.47.132.55"}},
    "Agf Lajeado": {"mcu": "00424526", "wan1": {"op": "Tim", "tipo": "FIXO", "ip": "177.149.87.18", "mask": "255.255.255.0", "gw": "0.0.0.0"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.247.247", "mask": "255.255.255.0", "gw": "201.6.247.247"}},
    "Agf Conceição": {"mcu": "00424406", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "191.209.82.3"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.103.146", "mask": "255.255.255.0", "gw": "201.6.103.1"}},
    "Agf Figueira Grande": {"mcu": "00424493", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "189.46.28.31"}, "wan2": {"op": "Telion", "tipo": "FIXO", "ip": "200.155.182.26", "mask": "255.255.255.252 /30", "gw": "200.155.182.25"}},
    "Agf Morumbi": {"mcu": "00424493", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.100.138", "mask": "255.255.255.0", "gw": "201.6.100.1"}, "wan2": {"op": "Vivo Lp", "tipo": "FIXO", "ip": "187.92.219.146", "mask": "255.255.255.0 /29", "gw": "187.92.219.145"}},
    "Agf Morumbi Área Acessória": {"mcu": "00424493", "wan1": {"op": "Não Sabe", "tipo": "FIXO", "ip": "201.63.149.130", "mask": "255.255.255.248", "gw": "201.63.149.129"}},
    "Agf Bonfiglioli": {"mcu": "00424416", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.118.177.14"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.106.126", "mask": "255.255.255.0", "gw": "201.6.106.1"}},
    "Agf Bonfiglioli Área Acessória": {"mcu": "00424416", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "187.11.132.189"}},
    "Agf Perus": {"mcu": "00424325", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.103.179.54"}, "wan2": {"op": "Conecta", "tipo": "PPPoE", "user": "pretacao.ltda", "pass": "Conecta01", "ip": "45.164.78.96"}},
    "Agf Pirituba": {"mcu": "0000000", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.170.55.64"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.113.34", "mask": "255.255.255.0", "gw": "201.6.113.1"}},
    "Agf Vila dos Remédios": {"mcu": "00424302", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "187.122.100.70", "mask": "255.255.255.0", "gw": "187.122.100.1"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "191.8.246.181"}},
    "Agf Carapicuiba": {"mcu": "000000000", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.170.50.148"}, "wan2": {"op": "Não tem", "tipo": "FIXO", "ip": "0.0.0.0"}},
    "Agf São Roberto": {"mcu": "00424435", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "187.122.101.223", "mask": "255.255.25
