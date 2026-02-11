import streamlit as st

# 1. Configuração da Página
st.set_page_config(page_title="Ftek Suporte", layout="wide", page_icon="🚀")

# 2. Título (Versão Final Limpa)
st.markdown("<h2 style='text-align: center;'>🚀 FTEK - PAINEL DE SUPORTE OPERACIONAL</h2>", unsafe_allow_html=True)

# 3. CRIAÇÃO AUTOMÁTICA DAS 40 UNIDADES (Garante o menu completo)
agencias = {f"Agf Unidade {i:02d}": {"mcu": "000000", "ip": "0.0.0.0"} for i in range(1, 41)}

# 4. DADOS REAIS (Inserindo as agências que você já tem)
# Se precisar adicionar mais, é só seguir este padrão abaixo:
agencias["Agf Itaberaba"] = {"mcu": "00423154", "ip": "201.6.104.170:1010"}
agencias["Agf Barra Funda"] = {"mcu": "00424371", "ip": "177.139.163.26"}
agencias["Agf Mandaqui"] = {"mcu": "00236565", "ip": "201.69.120.142"}

# 5. INTERFACE DE SELEÇÃO
lista_ordenada = sorted(agencias.keys())
selecao = st.selectbox("Selecione a Agência (Select Agency):", lista_ordenada)

info = agencias[selecao]
st.success(f"🆔 MCU: {info['mcu']} | {selecao}")

# 6. CAMPOS TÉCNICOS (Com tradução conforme solicitado)
col1, col2 = st.columns(2)

with col1:
    ip_val = st.text_input("Technical IP Address (Endereço IP)", value=info['ip'], key="ip_ftek")
    st.text_input("Subnet Mask (Máscara de Rede)", value="255.255.255.0", key="mask_ftek")

with col2:
    st.text_input("Gateway (Gateway)", value="0.0.0.0", key="gw_ftek")
    st.link_button(f"🌐 Abrir Unidade", f"http://{ip_val}", use_container_width=True)

st.divider()
st.caption("Ftek Tecnologia - Suporte Especializado MikroTik & Redes")
