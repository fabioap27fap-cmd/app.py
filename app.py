import streamlit as st
import socket

# 1. Configuração da Página
st.set_page_config(page_title="Ftek - Suporte AGF", layout="wide", page_icon="🚀")

# 2. FUNÇÃO DE MONITORAMENTO (Technical Port Check)
def check_port(ip_port):
    try:
        if ":" in ip_port:
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

# 3. BASE DE DADOS COMPLETA (Compactada para não dar erro)
lista_ftek = [
    ("Agf Itaberába", "00423154", "201.6.104.170:1010", "177.189.223.190:1010"),
    ("Agf Cidade Dutra", "423152", "201.6.159.203", "0.0.0.0"),
    ("Agf Vieira de Morais", "423153", "201.6.145.30", "201.47.132.55"),
    ("Agf Lajeado", "00424526", "177.149.87.18", "201.6.247.247"),
    ("Agf Conceição", "00424406", "191.209.82.3", "201.6.103.146"),
    ("Agf Figueira Grande", "00424493", "189.46.28.31", "200.155.182.26"),
    ("Agf Morumbi", "00424493", "201.6.100.138", "187.92.219.146"),
    ("Agf Morumbi Área", "00424493", "201.63.149.130", "0.0.0.0"),
    ("Agf Bonfiglioli", "00424416", "177.118.177.14", "201.6.106.126"),
    ("Agf Bonfiglioli Área", "00424416", "187.11.132.189", "0.0.0.0"),
    ("Agf Perus", "00424325", "177.103.179.54", "45.164.78.96"),
    ("Agf Pirituba", "0000000", "177.170.55.64", "201.6.113.34"),
    ("Agf Vila dos Remédios", "00424302", "187.122.100.70", "191.8.246.181"),
    ("Agf Carapicuiba", "00000000", "177.170.50.148", "0.0.0.0"),
    ("Agf São Roberto", "00424435", "187.122.101.223", "187.72.251.252"),
    ("Agf Campo Grande", "0000000", "189.109.212.18", "177.69.127.110"),
    ("Agf Maria Candida", "00000000", "201.6.118.90", "177.68.158.15"),
    ("Agf Timotéo Penteado", "00424411", "201.6.111.12", "177.102.66.65"),
    ("Agf Parque Brasil", "00000000", "201.6.111.12", "0.0.0.0"),
    ("Agf Shopppin C. Limpo", "00423129", "201.46.24.84:1010", "187.35.133.110:1010"),
    ("Agf Silvio Romero", "00000000", "187.11.252.169", "201.6.126.99"),
    ("Agf Visconde Inhauma", "00000000", "177.170.30.234", "201.6.158.90"),
    ("Agf Cid. Tiradentes", "00000000", "138.36.59.138", "177.135.153.154"),
    ("Agf Mirandopolis", "00000000", "201.6.103.129", "177.95.228.202"),
    ("Agf Pq. São Jorge", "00424320", "200.159.109.162", "187.122.102.45"),
    ("Agf Wluiz", "00424426", "201.6.110.163", "179.228.251.146"),
    ("Agf Piratininga", "0000000", "191.13.225.209", "187.122.106.195"),
    ("Agf Clodomiro Amazonas", "0000000", "152.250.250.69", "201.6.238.122"),
    ("Agf Santa Cruz", "0000000", "200.148.80.137", "201.6.117.250"),
    ("Agf Mandaqui", "00236565", "201.69.120.142", "201.6.98.216"),
    ("Agf Britania", "00236543", "123.45.67.89", "187.35.147.205"),
    ("Agf Geovani Gronchi", "00424884", "201.6.127.82", "0.0.0.0"),
    ("Agf Engenho Novo", "00424438", "177.69.251.66", "189.44.74.226"),
    ("Agf Vila Prell", "0000000", "191.13.249.195", "201.6.157.195"),
    ("Agf Estados Unidos", "00236533", "191.8.183.152", "201.6.130.46"),
    ("Agf Barra Funda", "00424371", "177.139.163.26", "201.6.98.218")
]

# Transformando a lista no banco de dados do app
dados_agencias = {item[0]: {"mcu": item[1], "wan1": {"ip": item[2]}, "wan2": {"ip": item[3]}} for item in lista_ftek}

# 4. MENU LATERAL (Sidebar)
st.sidebar.title("🚀 Navegação Ftek")
agencia_sel = st.sidebar.selectbox("Selecione a Agência:", sorted(dados_agencias.keys()))
info = dados_agencias[agencia_sel]
st.sidebar.info(f"🆔 MCU: {info['mcu']}")

# 5. CONTEÚDO PRINCIPAL
st.markdown(f"<h3 style='text-align: center;'>Painel Operacional: {agencia_sel}</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

def montar_card(ip, titulo, chave, cor):
    with st.container(border=True):
        status, porta = check_port(ip)
        st.subheader(f"{titulo} - {'✅' if status else '❌'}")
        st.write(f"Status: {'ONLINE' if status else 'OFFLINE'} (Porta: {porta})")
        new_ip = st.text_input(f"Technical IP Address ({chave})", value=ip, key=f"ip_{chave}_{agencia_sel}")
        st.link_button(f"{cor} Abrir Unidade", f"http://{new_ip}", use_container_width=True)

with col1: montar_card(info['wan1']['ip'], "Link Primário", "w1", "🔵")
with col2:
    if info['wan2']['ip'] != "0.0.0.0":
        montar_card(info['wan2']['ip'], "Link Secundário", "w2", "🔴")

st.divider()
st.caption("Ftek Tecnologia - Suporte Especializado")
