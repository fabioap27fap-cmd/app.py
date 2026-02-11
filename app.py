import streamlit as st
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

# 3. BASE DE DADOS COMPLETA (Todas as agências recuperadas)
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
    "Agf Lajeado": {
        "mcu": "00424526",
        "wan1": {"op": "Tim", "tipo": "FIXO", "ip": "177.149.87.18", "mask": "255.255.255.0", "gw": "0.0.0.0"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.247.247", "mask": "255.255.255.0", "gw": "201.6.247.247"}
    },
    "Agf Conceição": {
        "mcu": "00424406",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "191.209.82.3"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.103.146", "mask": "255.255.255.0", "gw": "201.6.103.1"}
    },
    "Agf Figueira Grande": {
        "mcu": "00424493",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "189.46.28.31"},
        "wan2": {"op": "Telion", "tipo": "FIXO", "ip": "200.155.182.26", "mask": "255.255.255.252 /30", "gw": "200.155.182.25"}
    },
    "Agf Morumbi": {
        "mcu": "00424493",
        "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.100.138", "mask": "255.255.255.0", "gw": "201.6.100.1"},
        "wan2": {"op": "Vivo Lp", "tipo": "FIXO", "ip": "187.92.219.146", "mask": "255.255.255.0 /29", "gw": "187.92.219.145"}
    },
    "Agf Bonfiglioli": {
        "mcu": "00424416",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.118.177.14"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.106.126", "mask": "255.255.255.0", "gw": "201.6.106.1"}
    },
    "Agf Perus": {
        "mcu": "00424325",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.103.179.54"},
        "wan2": {"op": "Conecta", "tipo": "PPPoE", "user": "pretacao.ltda", "pass": "Conecta01", "ip": "45.164.78.96"}
    },
    "Agf Pirituba": {
        "mcu": "0000000",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.170.55.64"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.113.34", "mask": "255.255.255.0", "gw": "201.6.113.1"}
    },
    "Agf Vila dos Remédios": {
        "mcu": "00424302",
        "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "187.122.100.70", "mask": "255.255.255.0", "gw": "187.122.100.1"},
        "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "191.8.246.181"}
    },
    "Agf São Roberto": {
        "mcu": "00424435",
        "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "187.122.101.223", "mask": "255.255.255.0", "gw": "187.122.101.1"},
        "wan2": {"op": "Algar", "tipo": "PPPoE", "user": "09091605", "pass": "12345678", "ip": "187.72.251.252"}
    },
    "Agf Maria Candida": {
        "mcu": "00000000",
        "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.118.90", "mask": "255.255.255.0", "gw": "201.6.118.90"},
        "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.68.158.15"}
    },
    "Agf Timotéo Penteado": {
        "mcu": "00424411",
        "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.111.12", "mask": "255.255.255.0", "gw": "201.6.111.1"},
        "wan2": {"op": "Não tem", "tipo": "PPPoE", "user": "nada", "pass": "nada", "ip": "177.102.66.65"}
    },
    "Agf Shopppin Campo Limpo": {
        "mcu": "00423129",
        "wan1": {"op": "America Net", "tipo": "PPPoE", "user": "A690972280003@sp.spo", "pass": "hghs11vvt7w9", "ip": "201.46.24.84:1010"},
        "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "187.35.133.110:1010"}
    },
    "Agf Mandaqui": {
        "mcu": "00236565",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "201.69.120.142"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.216", "mask": "255.255.255.0 /24", "gw": "201.6.98.216"}
    },
    "Agf Barra Funda": {
        "mcu": "00424371",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.139.163.26"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.218", "mask": "255.255.255.0 /24", "gw": "201.6.98.1"}
    },
    "Agf Estados Unidos": {
        "mcu": "00236533",
        "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "191.8.183.152"},
        "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.130.46", "mask": "255.255.255.252 /30", "gw": "201.6.130.45"}
    }
}

# 4. MENU LATERAL (Sidebar)
st.sidebar.title("🚀 Navegação Ftek")
lista_ordenada = sorted(list(dados_agencias.keys()))
agencia_sel = st.sidebar.selectbox("Selecione a Agência pelo Nome:", lista_ordenada)

# 5. CONTEÚDO PRINCIPAL
info = dados_agencias[agencia_sel]
st.markdown(f"<h2 style='text-align: center;'>Painel: {agencia_sel}</h2>", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.info(f"🆔 MCU: {info['mcu']}")

col1, col2 = st.columns(2)

def montar_card(dados, titulo, icone, chave, cor_emoji):
    with st.container(border=True):
        status_ok, porta_teste = check_port(dados.get('ip', '0.0.0.0'))
        status_txt = "✅ ONLINE" if status_ok else "❌ OFFLINE"
        st.subheader(f"{icone} {titulo}")
        st.write(f"Status: **{status_txt}** (Porta: {porta_teste})")
        
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
st.caption("Ftek Tecnologia - Suporte Especializado MikroTik")
