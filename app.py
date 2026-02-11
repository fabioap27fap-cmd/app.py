import streamlit as st
import socket

# 1. Configuração da Página
st.set_page_config(page_title="Ftek - Suporte AGF", layout="wide", page_icon="🚀")

# 2. FUNÇÃO DE MONITORAMENTO (Checa portas específicas)
def check_port(ip_port, manual_port=None):
    try:
        if manual_port:
            target_port = manual_port
            target_ip = ip_port.split(":")[0] if ":" in ip_port else ip_port
        elif ":" in ip_port:
            target_ip, target_port = ip_port.split(":")
            target_port = int(target_port)
        else:
            target_ip, target_port = ip_port, 80 
            
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.2) 
        result = s.connect_ex((target_ip, target_port))
        s.close()
        return result == 0, target_port
    except: return False, 80

# 3. BASE DE DADOS (Mantendo suas agências)
dados_agencias = {
    "Agf Itaberába": {"mcu": "00423154", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.104.170:1010", "mask": "255.255.255.0", "gw": "201.6.104.1"}, "wan2": {"op": "VIVO", "tipo": "FIXO", "ip": "177.189.223.190:1010", "mask": "255.255.255.0", "gw": "0.0.0.0"}},
    "Agf Cidade Dutra": {"mcu": "423152", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.159.203", "mask": "255.255.255.0", "gw": "201.6.159.1"}},
    "Agf Barra Funda": {"mcu": "00424371", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.139.163.26", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.218", "mask": "255.255.255.0", "gw": "201.6.98.1"}}
} # Adicione as outras aqui seguindo o mesmo padrão

# 4. MENU LATERAL
st.sidebar.title("🚀 Navegação Ftek")
agencia_sel = st.sidebar.selectbox("Selecione a Agência:", sorted(dados_agencias.keys()))
info = dados_agencias[agencia_sel]
st.sidebar.info(f"🆔 MCU: {info['mcu']}")

# 5. CONTEÚDO PRINCIPAL
st.markdown(f"<h3 style='text-align: center;'>Painel Operacional: {agencia_sel}</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

def montar_card(dados, titulo, chave, cor):
    if not dados: return
    with st.container(border=True):
        # Ping da Porta do Link (80 ou 1010)
        status_ok, porta_teste = check_port(dados.get('ip', '0.0.0.0'))
        # Ping da Porta do Winbox (8291)
        winbox_ok, _ = check_port(dados.get('ip', '0.0.0.0'), manual_port=8291)
        
        st.subheader(f"{titulo} ({dados.get('op', 'Link')})")
        st.write(f"Link: **{'✅ ONLINE' if status_ok else '❌ OFFLINE'}** (Porta: {porta_teste})")
        st.write(f"Winbox: **{'✅ ACESSO OK' if winbox_ok else '❌ SEM ACESSO'}** (Porta: 8291)")
        
        ip_val = st.text_input(f"Technical IP Address ({titulo})", value=dados.get('ip', '0.0.0.0'), key=f"ip_{chave}_{agencia_sel}")
        
        if dados.get('tipo') == "PPPoE":
            st.text_input("User (Usuário)", value=dados.get('user', ''), key=f"u_{chave}_{agencia_sel}")
        else:
            st.text_input("Subnet Mask (Máscara)", value=dados.get('mask', '255.255.255.0'), key=f"m_{chave}_{agencia_sel}")
        
        st.link_button(f"{cor} Abrir Unidade", f"http://{ip_val}", use_container_width=True)

with col1: montar_card(info['wan1'], "Link Primário", "w1", "🔵")
with col2: montar_card(info.get('wan2'), "Link Secundário", "w2", "🔴")

st.divider()
st.caption("Ftek Tecnologia - Suporte Especializado MikroTik")
