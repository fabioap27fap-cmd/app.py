import streamlit as st
import socket

# 1. Configuração da Página
st.set_page_config(page_title="Ftek - Suporte AGF", layout="wide", page_icon="🚀")

# 2. FUNÇÃO DE MONITORAMENTO (Ping de Porta)
def check_port(ip_port):
    try:
        if ":" in ip_port:
            target_ip = ip_port.split(":")[0]
            target_port = int(ip_port.split(":")[1])
        else:
            target_ip = ip_port
            target_port = 80 # Default Port (Porta Padrão)
            
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5) # Timeout rápido para não travar o site
        result = s.connect_ex((target_ip, target_port))
        s.close()
        return result == 0
    except:
        return False

# 3. BASE DE DADOS (Recuperada e Organizada)
dados_agencias = {
    "Agf Itaberába": {
        "mcu": "00423154",
        "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.104.170:1010", "mask": "255.255.255.0", "gw": "201.6.104.1"},
        "wan2": {"op": "VIVO", "tipo": "FIXO", "ip": "177.189.223.190:1010", "mask": "255.255.255.0", "gw": "0.0.0.0"}
    },
    "Agf Cidade Dutra": {
        "mcu": "423152",
        "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.159.203", "mask": "255.255.255.0", "gw": "201.6.159.1"},
        "wan2": {"op": "Não tem", "tipo": "FIXO", "ip": "0.0.0.0", "mask": "0.0.0.0", "gw": "0.0.0.0"}
    },
    "Agf Vieira de Morais": {
        "mcu": "423153",
        "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.145.30", "mask": "255.255.255.0", "gw": "201.6.145.1"},
        "wan2": {"op": "VIVO Antiga Gvt", "tipo": "PPPoE", "user": "gvt25", "pass": "1133602736", "ip": "201.47.132.55"}
    },
    "Agf Barra Funda": {
        "mcu": "00424371",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.139.163.26"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.218", "mask": "255.255.255.0 /24", "gw": "201.6.98.1"}
    },
    "Agf Mandaqui": {
        "mcu": "00236565",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "201.69.120.142"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.216", "mask": "255.255.255.0 /24", "gw": "201.6.98.216"}
    },
    # Adicione as outras agências aqui seguindo o padrão...
}

# 4. MENU LATERAL (Sidebar) - IGUAL ANTES
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2906/2906274.png", width=100)
st.sidebar.title("Navegação Ftek")
lista_ordenada = sorted(list(dados_agencias.keys()))
agencia_sel = st.sidebar.selectbox("Selecione a Agência pelo Nome:", lista_ordenada)

# 5. CONTEÚDO PRINCIPAL
st.markdown(f"<h2 style='text-align: center;'>🚀 Painel Operacional: {agencia_sel}</h2>", unsafe_allow_html=True)
info = dados_agencias[agencia_sel]
st.sidebar.divider()
st.sidebar.info(f"🆔 MCU: {info['mcu']}")

col1, col2 = st.columns(2)

def montar_card(dados, titulo, icone, chave, cor_emoji):
    with st.container(border=True):
        # Header com Status em tempo real
        status_ok = check_port(dados.get('ip', '0.0.0.0'))
        status_txt = "✅ ONLINE" if status_ok else "❌ OFFLINE"
        st.subheader(f"{icone} {titulo} - {status_txt}")
        
        # Technical IP Address (Endereço IP)
        ip_val = st.text_input(f"Technical IP Address ({dados['op']})", value=dados.get('ip', '0.0.0.0'), key=f"ip_{chave}_{agencia_sel}")
        
        if dados.get('tipo') == "PPPoE":
            st.text_input("User (Usuário)", value=dados.get('user', ''), key=f"u_{chave}_{agencia_sel}")
            st.text_input("Password (Senha)", value=dados.get('pass', ''), type="password", key=f"p_{chave}_{agencia_sel}")
        else:
            st.text_input("Subnet Mask (Máscara)", value=dados.get('mask', '255.255.255.0'), key=f"m_{chave}_{agencia_sel}")
            st.text_input("Gateway (Gateway)", value=dados.get('gw', '0.0.0.0'), key=f"g_{chave}_{agencia_sel}")
        
        url = f"http://{ip_val}" if ip_val != "0.0.0.0" else "#"
        st.link_button(f"{cor_emoji} Abrir {dados['op']}", url, use_container_width=True)

with col1:
    montar_card(info['wan1'], "Link Primário", "🌐", "w1", "🔵")

with col2:
    if 'wan2' in info:
        montar_card(info['wan2'], "Link Secundário", "🔗", "w2", "🔴")

st.divider()
st.caption("Ftek Tecnologia - Gestão de Infraestrutura e Redes")
