import streamlit as st
import socket
from concurrent.futures import ThreadPoolExecutor

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Ftek - Suporte AGF", layout="wide", page_icon="🚀")

# 2. FUNÇÃO DE MONITORAMENTO (Inteligente para Portas)
def check_port(ip_port, manual_port=None, external_test=False):
    if not ip_port or ip_port == "0.0.0.0":
        return False, 80
    
    ip_port = "".join(ip_port.split())
    
    try:
        if external_test:
            target_ip, target_port = "8.8.8.8", 53 
        elif ":" in ip_port:
            # Se o IP já tem porta (ex: :1010), ele usa ela e ignora o manual_port
            parts = ip_port.split(":")
            target_ip = parts[0]
            target_port = int(parts[1])
        else:
            # Se não tem porta no IP, usa a manual (8291) ou padrão (80)
            target_ip = ip_port
            target_port = manual_port if manual_port else 80
    except: return False, 80

    # Lógica de tentativa (Retry)
    for i in range(3):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3.5)
            result = s.connect_ex((target_ip, target_port))
            s.close()
            if result == 0: return True, target_port
        except: continue
            
    return False, target_port

# 3. BASE DE DADOS INTEGRAL FTEK (Com Carapicuíba :1010)
dados_agencias = {
    "Agf Águia de Haia": {"mcu": "00000000", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "179.228.165.235", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.101.194", "mask": "255.255.255.0 /24", "gw": "201.6.101.1"}},
    "Agf Alto do Ipiranga": {"mcu": "0000000", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.117.13", "mask": "255.255.255.0 /24", "gw": "201.6.117.1"}, "wan2": {"op": "VIVO", "tipo": "FIXO", "ip": "201.93.94.175", "mask": "255.255.255.0", "gw": "0.0.0.0"}},
    "Agf Alto do Ipiranga Aréa Acéssoria": {"mcu": "0000000", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.255.98", "mask": "255.255.255.0 /24", "gw": "201.6.255.1"}, "wan2": {"op": "VIVO", "tipo": "FIXO", "ip": "187.11.237.212", "mask": "255.255.255.0", "gw": "0.0.0.0"}},
    "Agf Barra Funda": {"mcu": "00424371", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.139.163.26", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.218", "mask": "255.255.255.0", "gw": "201.6.98.1"}},
    "Agf Bonfiglioli": {"mcu": "00424416", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.118.177.14", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Zaap", "tipo": "FIXO", "ip": "201.6.106.126", "mask": "login:rojocorreio.1120471,senha:54972568", "gw": "201.6.106.1"}},
    "Agf Bonfiglioli Ponto Remoto": {"mcu": "00424416", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "187.11.132.189", "user": "cliente@cliente", "pass": "cliente"}},
    "Agf Britânia": {"mcu": "00236543", "wan1": {"op": "Globa Tel", "tipo": "PPPoE", "ip": "138.97.242.43", "user": "2630@globaltel.com.br", "pass": "12345678"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "187.35.147.205", "user": "cliente@cliente", "pass": "cliente"}},
    "Agf Campo Grande": {"mcu": "00424450", "wan1": {"op": "Vivo Lp", "tipo": "FIXO", "ip": "189.109.212.18", "mask": "255.255.255.248", "gw": "189.109.212.17"}, "wan2": {"op": "Algar", "tipo": "FIXO", "ip": "177.69.127.110", "mask": "255.255.255.252", "gw": "177.69.127.109"}},
    "Agf Carapicuíba": {"mcu": "00424395", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.170.50.148:", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Zap", "tipo": "PPPoE", "ip": "190.123.8.64:", "user": "rojocorreio.1120471", "pass": "54972568"}},
    "Agf Cidade Dutra": {"mcu": "423152", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.159.203", "mask": "255.255.255.0", "gw": "201.6.159.1"}},
    "Agf Cidade Tiradentes": {"mcu": "00424415", "wan1": {"op": "FIXO", "tipo": "FIXO", "ip": "138.36.59.138", "mask": "255.255.255.252", "gw": "138.36.59.137"}, "wan2": {"op": "FIXO", "tipo": "FIXO", "ip": "177.135.153.154", "mask": "255.255.255.248", "gw": "177.135.153.153"}},
    "Agf Clínicas": {"mcu": "00424368", "wan1": {"op": "Vivo", "tipo": "PPPoE", "ip": "177.26.125.184", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.119.15", "mask": "255.255.255.0", "gw": "201.6.119.1"}},
    "Agf Clodomiro Amazonas": {"mcu": "00424440", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "152.250.250.69", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.238.122", "mask": "255.255.255.0", "gw": "201.6.238.1"}},
    "Agf Conceição": {"mcu": "00424406", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "191.209.82.3", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.103.146", "mask": "255.255.255.0", "gw": "201.6.103.1"}},
    "Agf Engenho Novo": {"mcu": "00424438", "wan1": {"op": "Algar", "tipo": "FIXO", "ip": "177.69.251.66", "mask": "255.255.255.248", "gw": "177.69.251.70"}, "wan2": {"op": "Vivo", "tipo": "FIXO", "ip": "189.44.74.226", "mask": "255.255.255.248", "gw": "189.44.74.225"}},
    "Agf Estados Unidos": {"mcu": "00236533", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "191.8.183.152", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.130.46", "mask": "255.255.255.252", "gw": "201.6.130.45"}},
    "Agf Figueira Grande": {"mcu": "00424493", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "189.46.28.31", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Telion", "tipo": "FIXO", "ip": "200.155.182.26", "mask": "255.255.255.252", "gw": "200.155.182.25"}},
    "Agf Geovanni Gronchi": {"mcu": "00424884", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.127.82", "mask": "255.255.255.0", "gw": "201.6.127.1"}},
    "Agf Itaberába": {"mcu": "00423154", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.104.170:1010", "mask": "255.255.255.0", "gw": "201.6.104.1"}, "wan2": {"op": "VIVO", "tipo": "FIXO", "ip": "177.189.223.190:1010", "mask": "255.255.255.0", "gw": "0.0.0.0"}},
    "Agf Jaraguá": {"mcu": "00424335", "wan1": {"op": "Vivo", "tipo": "PPPoE", "ip": "191.13.225.209", "user": "digita.post", "pass": "cliente"}, "wan2": {"op": "CLARO", "tipo": "FIXO", "ip": "187.122.106.195", "mask": "255.255.255.0", "gw": "201.6.107.1"}},
    "Agf João Dias": {"mcu": "0000000", "wan1": {"op": "Vivo", "tipo": "PPPoE", "ip": "179.111.200.4", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "CLARO", "tipo": "FIXO", "ip": "187.122.106.195", "mask": "255.255.255.0", "gw": "187.122.106.195"}},
    "Agf Jordanésia": {"mcu": "236564", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "187.35.146.196", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Não Sei", "tipo": "PPPoE", "ip": "45.188.185.141", "user": "não sei", "pass": "não sei"}},
    "Agf Lajeado": {"mcu": "00424526", "wan1": {"op": "Tim", "tipo": "FIXO", "ip": "177.149.87.18", "mask": "255.255.255.0", "gw": "0.0.0.0"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.247.247", "mask": "255.255.255.0", "gw": "201.6.247.247"}},
    "Agf Mandaqui": {"mcu": "00236565", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "201.69.120.142", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.98.216", "mask": "255.255.255.0", "gw": "201.6.98.216"}},
    "Agf Maria Cândida": {"mcu": "00424400", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.118.90", "mask": "255.255.255.0", "gw": "201.6.118.90"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.68.158.15", "user": "cliente@cliente", "pass": "cliente"}},
    "Agf Mirandópolis": {"mcu": "00424425", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.103.129", "mask": "255.255.255.0", "gw": "201.6.103.1"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.95.228.202", "user": "cliente@cliente", "pass": "cliente"}},
    "Agf Morumbi": {"mcu": "00424493", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.100.138", "mask": "255.255.255.0", "gw": "201.6.100.1"}, "wan2": {"op": "Vivo Lp", "tipo": "FIXO", "ip": "187.92.219.146", "mask": "255.255.255.0", "gw": "187.92.219.145"}},
    "Agf Parque Brasil": {"mcu": "00424390", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.111.12", "mask": "255.255.255.0", "gw": "201.6.111.1"}},
    "Agf Perus": {"mcu": "00424325", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.103.179.54", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Conecta", "tipo": "PPPoE", "ip": "45.164.78.96", "user": "pretacao.ltda", "pass": "Conecta01"}},
    "Agf Piratininga": {"mcu": "00424430", "wan1": {"op": "Conecta", "tipo": "PPPoE", "ip": "200.201.138.141:1010", "user": "cliente@cliente", "pass": "jerimaduba372"}, "wan2": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.107.181:1010", "mask": "255.255.255.0", "gw": "187.122.106.195"}},
    "Agf Pirituba": {"mcu": "00424300", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.170.55.64", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.113.34", "mask": "255.255.255.0", "gw": "201.6.113.1"}},
    "Agf Pq. São Jorge": {"mcu": "00424320", "wan1": {"op": "Vivo Lp", "tipo": "FIXO", "ip": "200.159.109.162", "mask": "255.255.255.248", "gw": "200.159.109.161"}, "wan2": {"op": "Net", "tipo": "FIXO", "ip": "187.122.102.45", "mask": "255.255.255.252", "gw": "187.122.102.1"}},
    "Agf Santa Cruz": {"mcu": "00424360", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "200.148.80.137", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.117.250", "mask": "255.255.255.0", "gw": "201.6.117.1"}},
    "Agf São Jorge Noelita": {"mcu": "00424313", "wan1": {"op": "CLARO", "tipo": "FIXO", "ip": "201.6.119.15", "mask": "255.255.255.0", "gw": "201.6.103.1"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "191.7.157.252", "user": "correios", "pass": "123"}},
    "Agf São Jorge Noelita Ponto Remoto": {"mcu": "00424313", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "177.26.123.246", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "191.7.157.246", "user": "correios.logistica", "pass": "123"}},
    "Agf São Roberto": {"mcu": "00424435", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "187.122.101.223", "mask": "255.255.255.0", "gw": "187.122.101.1"}, "wan2": {"op": "Algar", "tipo": "PPPoE", "ip": "187.72.251.252", "user": "09091605", "pass": "12345678"}},
    "Agf Shopping C. Limpo": {"mcu": "00423129", "wan1": {"op": "America Net", "tipo": "PPPoE", "ip": "201.46.24.84:1010", "user": "A690972280003@sp.spo", "pass": "hghs11vvt7w9"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "187.35.133.110:1010", "user": "cliente@cliente", "pass": "cliente"}},
    "Agf Silvio Romero": {"mcu": "00424460", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "187.11.252.169", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.126.99", "mask": "255.255.255.0", "gw": "201.6.126.1"}},
    "Agf Vila dos Remédios": {"mcu": "00424302", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "187.122.100.70", "mask": "255.255.255.0", "gw": "187.122.100.1"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "191.8.246.181", "user": "cliente@cliente", "pass": "cliente"}},
    "Agf Vila Prell": {"mcu": "00424380", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "191.13.249.195", "user": "cliente@cliente", "pass": "cliente"}, "wan2": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.157.195", "mask": "255.255.255.0", "gw": "201.6.157.195"}},
    "Agf Vila Sônia": {"mcu": "00424435", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.100.11", "mask": "255.255.255.0", "gw": "201.6.100.1"}, "wan2": {"op": "Vivo", "tipo": "PPPoE", "ip": "187.35.124.176", "user": "Nat 192.168.15.200", "pass": "não tem"}},
    "Agf Ponto remoto Vila Sônia": {"mcu": "00424435", "wan1": {"op": "VIVO", "tipo": "PPPoE", "ip": "201.69.28.73", "user": "cliente@cliente", "pass": "cliente"}},
    "Agf Visconde Inhaúma": {"mcu": "00424405", "wan1": {"op": "Não Sei", "tipo": "FIXO", "ip": "200.171.209.218", "mask": "255.255.255.248", "gw": "189.55.192.25"}, "wan2": {"op": "Não sei", "tipo": "FIXO", "ip": "189.55.192.25", "mask": "255.255.252.0", "gw": "189.55.192.1"}},
    "Agf Vieira de Morais": {"mcu": "423153", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.145.30", "mask": "255.255.255.0", "gw": "201.6.145.1"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "201.47.132.55", "user": "gvt25", "pass": "1133602736"}},
    "Agf W. Luiz": {"mcu": "00424426", "wan1": {"op": "Claro", "tipo": "FIXO", "ip": "201.6.110.163", "mask": "255.255.255.0", "gw": "201.6.110.1"}, "wan2": {"op": "VIVO", "tipo": "PPPoE", "ip": "179.228.251.146", "user": "cliente@cliente", "pass": "cliente"}}
}

# 4. EXECUÇÃO PARALELA (Threading)
def run_checks(dados):
    if not dados: return None
    ip = dados.get('ip', '0.0.0.0')
    with ThreadPoolExecutor() as ex:
        f1 = ex.submit(check_port, ip)
        f2 = ex.submit(check_port, ip, manual_port=8291)
        f3 = ex.submit(check_port, ip, external_test=True)
    return f1.result(), f2.result(), f3.result()

# 5. SIDEBAR
st.sidebar.title("🚀 Navegação Ftek")
agencia_sel = st.sidebar.selectbox("Agência:", sorted(dados_agencias.keys()))
info = dados_agencias[agencia_sel]
st.sidebar.divider()
st.sidebar.info(f"🆔 MCU: {info['mcu']}")

# 6. PAINEL PRINCIPAL
st.markdown(f"<h3 style='text-align: center;'>Painel Ftek: {agencia_sel}</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

def montar_card(dados, titulo, chave, cor):
    if not dados: return
    res = run_checks(dados)
    (link_ok, _), (win_ok, port_usada), (int_ok, _) = res
    with st.container(border=True):
        st.subheader(f"{titulo} ({dados.get('op')})")
        st.write(f"Link Operadora: **{'✅ ONLINE' if link_ok else '❌ OFFLINE'}**")
        st.write(f"Winbox (Porta {port_usada}): **{'✅ OK' if win_ok else '❌ ERRO'}**")
        st.write(f"Internet (Google): **{'✅ OK' if int_ok else '❌ OFF'}**")
        st.text_input("IP Técnico", value=dados.get('ip').strip(), key=f"ip_{chave}_{agencia_sel}")
        if dados.get('tipo') == "PPPoE":
            st.text_input("Usuário (User)", value=dados.get('user'), key=f"u_{chave}_{agencia_sel}")
            st.text_input("Senha (Password)", value=dados.get('pass'), type="password", key=f"p_{chave}_{agencia_sel}")
        else:
            st.text_input("Máscara (Mask)", value=dados.get('mask'), key=f"m_{chave}_{agencia_sel}")
            st.text_input("Gateway (GW)", value=dados.get('gw'), key=f"g_{chave}_{agencia_sel}")
        st.link_button(f"{cor} Abrir Interface", f"http://{dados.get('ip').strip()}", use_container_width=True)

with col1: montar_card(info['wan1'], "Link Primário", "w1", "🔵")
with col2: montar_card(info.get('wan2'), "Link Secundário", "w2", "🔴")

st.divider()
st.caption("Ftek Tecnologia - v7.5 (Suporte a Porta Customizada - Carapicuíba OK)")
