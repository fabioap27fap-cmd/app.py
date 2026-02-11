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

# 3. BASE DE DADOS COMPLETA (Todas as 35 agências cadastradas)
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
    "Agf São Roberto": {"mcu": "00424435", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "187.122.101.223", "mask": "255.255.255.0", "gw": "187.122.101.1"}, "wan2": {"op": "Algar", "tipo": "PPPoE", "user": "09091605", "pass": "12345678", "ip": "187.72.251.252"}},
    "Agf Campo Grande": {"mcu": "0000000", "wan1": {"op": "Vivo Lp", "tipo": "FIXO", "ip": "189.109.212.18", "mask": "255.255.255.248 /29", "gw": "189.109.212.17"}, "wan2": {"op": "Algar", "tipo": "FIXO", "ip": "177.69.127.110", "mask": "255.255.255.252 /30", "gw": "177.69.127.109"}},
    "Agf Maria Candida": {"mcu": "00000000", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.118.90", "mask": "255.255.255.0", "gw": "201.6.118.90"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.68.158.15"}},
    "Agf Timotéo Penteado": {"mcu": "00424411", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.111.12", "mask": "255.255.255.0", "gw": "201.6.111.1"}, "wan2": {"op": "Não tem", "tipo": "PPPoE", "ip": "177.102.66.65"}},
    "Agf Parque Brasil": {"mcu": "00000000", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.111.12", "mask": "255.255.255.0", "gw": "201.6.111.1"}, "wan2": {"op": "Não tem", "tipo": "PPPoE", "ip": "0.0.0.0"}},
    "Agf Shopppin Campo Limpo": {"mcu": "00423129", "wan1": {"op": "America Net", "tipo": "PPPoE", "user": "A690972280003@sp.spo", "pass": "hghs11vvt7w9", "ip": "201.46.24.84:1010"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "187.35.133.110:1010"}},
    "Agf Silvio Romero": {"mcu": "000000000", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "187.11.252.169"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.126.99", "mask": "255.255.255.0", "gw": "201.6.126.1"}},
    "Agf Visconde de Inhauma": {"mcu": "000000000", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.170.30.234"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.158.90", "mask": "255.255.255.0", "gw": "201.6.158.90"}},
    "Agf Cidade Tiradentes": {"mcu": "000000000", "wan1": {"op": "Não sei", "tipo": "FIXO", "ip": "138.36.59.138", "mask": "255.255.255.252 /30", "gw": "138.36.59.137" }, "wan2": {"op": "Não sei", "tipo": "FIXO", "ip": "177.135.153.154", "mask": "255.255.255.248 /29", "gw": "177.135.153.153"}},
    "Agf Mirandopolis": {"mcu": "00000000", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.103.129", "mask": "255.255.255.0", "gw": "201.6.103.1"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.95.228.202"}},
    "Agf Parque São Jorge": {"mcu": "00424320", "wan1": {"op": "Vivo Lp", "tipo": "FIXO", "ip": "200.159.109.162", "mask": "255.255.255.248 /29", "gw": "200.159.109.161"}, "wan2": {"op": "Net", "tipo": "FIXO", "ip": "187.122.102.45", "mask": "255.255.255.252 /24", "gw": "187.122.102.1"}},
    "Agf Wluiz": {"mcu": "00424426", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.110.163", "mask": "255.255.255.0", "gw": "201.6.110.1"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "179.228.251.146"}},
    "Agf Piratininga": {"mcu": "0000000", "wan1": {"op": "Vivo", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "191.13.225.209"}, "wan2": {"op": "CLARO", "tipo": "FIXO", "ip": "187.122.106.195", "mask": "255.255.255.0", "gw": "187.122.106.195"}},
    "Agf Clodomiro Amazonas": {"mcu": "0000000", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "152.250.250.69"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.238.122", "mask": "255.255.255.0 /24", "gw": "201.6.238.1"}},
    "Agf Santa Cruz": {"mcu": "0000000", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "200.148.80.137"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.117.250", "mask": "255.255.255.0 /24", "gw": "201.6.117.1"}},
    "Agf Mandaqui": {"mcu": "00236565", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "201.69.120.142"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.216", "mask": "255.255.255.0 /24", "gw": "201.6.98.216"}},
    "Agf Britania": {"mcu": "00236543", "wan1": {"op": "Globa Tel", "tipo": "PPPoE", "user": "2630@globaltel.com.br", "pass": "cliente", "ip": "12345678"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "187.35.147.205"}},
    "Agf Geovani Gronchi": {"mcu": "00424884", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.127.82", "mask": "255.255.255.0 /24", "gw": "201.6.127.1"}},
    "Agf Engenho Novo": {"mcu": "00424438", "wan1": {"op": "Algar", "tipo": "FIXO", "ip": "177.69.251.66", "mask": "255.255.255.248 /29", "gw": "177.69.251.70"}, "wan2": {"op": "Vivo", "tipo": "FIXO", "ip": "189.44.74.226", "mask": "255.255.255.248 /29", "gw": "189.44.74.225"}},
    "Agf Vila Prell": {"mcu": "0000000", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "191.13.249.195"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.157.195", "mask": "255.255.255.0 /24", "gw": "201.6.157.195"}},
    "Agf Estados Unidos": {"mcu": "00236533", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "191.8.183.152"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.130.46", "mask": "255.255.255.252 /30", "gw": "201.6.130.45"}},
    "Agf Barra Funda": {"mcu": "00424371", "wan1": {"op": "VIVO", "tipo": "PPPoE", "user": "cliente@cliente", "pass": "cliente", "ip": "177.139.163.26"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.218", "mask": "255.255.255.0 /24", "gw": "201.6.98.1"}}
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
        montar_card(info['wan2'], "Link Sec
