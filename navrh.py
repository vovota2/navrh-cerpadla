import streamlit as st
import math

# --- FUNKCE PRO TABULKOVÉ HODNOTY A MOTOR ---
def get_eta_q(p_mpa):
    """Interpolace objemové účinnosti z tabulky"""
    p_t = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
    e_t = [0.945, 0.930, 0.913, 0.890, 0.830, 0.750]
    p_val = max(0.5, min(p_mpa, 4.0))
    for i in range(len(p_t)-1):
        if p_t[i] <= p_val <= p_t[i+1]:
            return e_t[i] + (p_val - p_t[i]) * (e_t[i+1] - e_t[i]) / (p_t[i+1] - p_t[i])
    return 0.75

def get_eta_overall(p_mpa, v_ms):
    """2D Interpolace celkové účinnosti z tabulky"""
    p_t = [0.5, 1.0, 1.5, 2.0]
    v_t = [1.0, 2.0, 3.0, 4.0]
    e_m = [
        [0.81, 0.76, 0.68, 0.62],
        [0.63, 0.77, 0.76, 0.71],
        [0.47, 0.71, 0.72, 0.73],
        [0.30, 0.55, 0.58, 0.72]
    ]
    p_val = max(0.5, min(p_mpa, 2.0))
    v_val = max(1.0, min(v_ms, 4.0))
    
    p_i = next((i for i in range(len(p_t)-1) if p_t[i] <= p_val <= p_t[i+1]), 2)
    v_i = next((j for j in range(len(v_t)-1) if v_t[j] <= v_val <= v_t[j+1]), 2)
    
    p1, p2 = p_t[p_i], p_t[p_i+1]
    v1, v2 = v_t[v_i], v_t[v_i+1]
    q11, q21 = e_m[p_i][v_i], e_m[p_i+1][v_i]
    q12, q22 = e_m[p_i][v_i+1], e_m[p_i+1][v_i+1]
    
    r1 = ((p2 - p_val)/(p2 - p1))*q11 + ((p_val - p1)/(p2 - p1))*q21
    r2 = ((p2 - p_val)/(p2 - p1))*q12 + ((p_val - p1)/(p2 - p1))*q22
    eta = ((v2 - v_val)/(v2 - v1))*r1 + ((v_val - v1)/(v2 - v1))*r2
    return eta

def get_real_motor_name(n_sync, p_kw):
    """Výběr komerčně dostupného motoru. Pokud není v DB, vrátí None."""
    if n_sync == 1500:
        if p_kw == 0.25: return "VYBO 1AL71S-4 – *1786 Kč bez DPH*"
        elif p_kw == 0.37: return "VYBO 1AL71M-4 – *1961 Kč bez DPH*"
        elif p_kw == 0.55: return "VYBO 1AL80A-4 – *1993 Kč bez DPH*"
        elif p_kw == 0.75: return "VYBO 1AL80B-4 – *2184 Kč bez DPH*"
        elif p_kw == 1.1: return "VYBO 1AL90S-4 – *2792 Kč bez DPH*"
        elif p_kw == 1.5: return "VYBO 1AL90L-4 – *2992 Kč bez DPH*"
        elif p_kw == 2.2: return "VYBO 1AL100L1-4 – *3592 Kč bez DPH*"
        elif p_kw == 3.0: return "VYBO 1AL100L2-4 – *4182 Kč bez DPH*"
        elif p_kw == 4.0: return "VYBO 1AL112M-4 – *5164 Kč bez DPH*"
        elif p_kw == 5.5: return "VYBO 1AL132S-4 – *7278 Kč bez DPH*"
        elif p_kw == 7.5: return "VYBO 1AL132M-4 – *7984 Kč bez DPH*"
        elif p_kw == 11.0: return "VYBO 1LC160M-4"
        else: return None
    elif n_sync == 1000:
        if p_kw == 0.37: return "VYBO 1AL80S-6 – *2284 Kč bez DPH*"
        elif p_kw == 0.55: return "VYBO 1AL80B-6 – *2297 Kč bez DPH*"
        elif p_kw == 0.75: return "VYBO 1AL90S-6 – *2786 Kč bez DPH*"
        elif p_kw == 1.1: return "VYBO 1AL90L-6 – *3178 Kč bez DPH*"
        elif p_kw == 1.5: return "VYBO 1AL100L-6 – *3874 Kč bez DPH*"
        elif p_kw == 2.2: return "VYBO 1AL112M-6 – *4678 Kč bez DPH*"
        elif p_kw == 3.0: return "VYBO 1AL132S-6 – *7034 Kč bez DPH*"
        elif p_kw == 4.0: return "VYBO 1AL132M-6 – *7381 Kč bez DPH*"
        elif p_kw == 5.5: return "VYBO 1AL132M-6 – *8376 Kč bez DPH*"
        elif p_kw == 7.5: return "VYBO 1AL160M-6"
        elif p_kw == 11.0: return "VYBO 1LC160L-6"
        elif p_kw == 15.0: return "VYBO 1LC180L-6"
        elif p_kw == 18.5: return "VYBO 1LC200L1-6"
        elif p_kw == 22.0: return "VYBO 1LC200L2-6"
        elif p_kw == 30.0: return "VYBO 1LC225M-6"
        else: return None
    elif n_sync == 750:
        if p_kw == 0.37: return "VYBO 1AL90S-8 – *3653 Kč bez DPH*"
        elif p_kw == 0.55: return "VYBO 1AL90L-8 – *4281 Kč bez DPH*"
        elif p_kw == 0.75: return "VYBO 1AL100L-8 – *5020 Kč bez DPH*"
        elif p_kw == 1.1: return "VYBO 1AL100L2-8 – *5314 Kč bez DPH*"
        elif p_kw == 1.5: return "VYBO 1AL112M-8 – *7086 Kč bez DPH*"
        elif p_kw == 2.2: return "VYBO 1AL132S-8 – *8820 Kč bez DPH*"
        elif p_kw == 3.0: return "VYBO 1AL132M-8 – *10481 Kč bez DPH*"
        elif p_kw == 4.0: return "VYBO 1AL160M-8"
        elif p_kw == 5.5: return "VYBO 1AL160M-8"
        elif p_kw == 7.5: return "VYBO 1AL160L-8"
        elif p_kw == 11.0: return "VYBO 1LC180L-8"
        elif p_kw == 15.0: return "VYBO 1LC200L-8"
        elif p_kw == 18.5: return "VYBO 1LC225S-8"
        elif p_kw == 22.0: return "VYBO 1LC225M-8"
        elif p_kw == 30.0: return "VYBO 1LC250M-8"
        elif p_kw == 37.0: return "VYBO 1LC280S-8"
        elif p_kw == 45.0: return "VYBO 1LC280M-8"
        else: return None
    return None

# POUZE ŘADA I z tabulky
STD_MODULES = [0.5, 0.6, 0.8, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20]
STD_MOTORS_KW = [0.12, 0.18, 0.25, 0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11.0, 15.0, 18.5, 22.0, 30.0, 37.0, 45.0, 55.0]

# --- UI APLIKACE ---
st.set_page_config(page_title="Návrh zubového čerpadla", layout="wide")
st.title("⚙️ Automatizovaný návrh zubového čerpadla")

# --- INICIALIZACE A FUNKCE PRO SESSION STATE ---
if 'q_unit' not in st.session_state: st.session_state.q_unit = 'l/min'
if 'q_num' not in st.session_state: st.session_state.q_num = 120.0
if 'q_slider' not in st.session_state: st.session_state.q_slider = 120.0
if 'p_num' not in st.session_state: st.session_state.p_num = 1.0
if 'p_slider' not in st.session_state: st.session_state.p_slider = 1.0
if 'q_tol_input' not in st.session_state: st.session_state.q_tol_input = 1.0
if 'z_init_input' not in st.session_state: st.session_state.z_init_input = 20

def update_q(): st.session_state.q_slider = st.session_state.q_num
def update_q_sl(): st.session_state.q_num = st.session_state.q_slider
def update_p(): st.session_state.p_slider = st.session_state.p_num
def update_p_sl(): st.session_state.p_num = st.session_state.p_slider

def on_unit_change():
    new_u = st.session_state.unit_selector
    old_u = st.session_state.q_unit
    if old_u == 'l/min' and new_u == 'l/s':
        st.session_state.q_num = round(st.session_state.q_num / 60.0, 2)
        st.session_state.q_slider = st.session_state.q_num
    elif old_u == 'l/s' and new_u == 'l/min':
        st.session_state.q_num = round(st.session_state.q_num * 60.0, 1)
        st.session_state.q_slider = st.session_state.q_num
    st.session_state.q_unit = new_u

def reset_to_defaults():
    st.session_state.q_unit = 'l/min'
    st.session_state.unit_selector = 'l/min'
    st.session_state.q_num = 120.0
    st.session_state.q_slider = 120.0
    st.session_state.p_num = 1.0
    st.session_state.p_slider = 1.0
    st.session_state.q_tol_input = 1.0
    st.session_state.z_init_input = 20

with st.sidebar:
    st.header("Vstupní parametry")
    
    # --- PRŮTOK (PŘEPÍNAČ JEDNOTEK) ---
    unit = st.session_state.q_unit
    st.markdown(f"**Průtok Q [{unit}]**")
    st.radio("Jednotka průtoku", ['l/min', 'l/s'], key='unit_selector', on_change=on_unit_change, horizontal=True, label_visibility="collapsed")
    
    q_min = 5.0 if unit == 'l/min' else 0.1
    q_max = 300.0 if unit == 'l/min' else 5.0
    q_step = 1.0 if unit == 'l/min' else 0.1
    
    if st.session_state.q_num > q_max: st.session_state.q_num = q_max
    if st.session_state.q_num < q_min: st.session_state.q_num = q_min
    
    col_q1, col_q2 = st.columns([3, 1])
    with col_q1:
        st.slider("Q", min_value=q_min, max_value=q_max, step=q_step, key='q_slider', on_change=update_q_sl, label_visibility="collapsed")
    with col_q2:
        st.number_input("Q", min_value=q_min, max_value=q_max, step=q_step, key='q_num', on_change=update_q, label_visibility="collapsed")
        
    st.number_input("Tolerance průtoku [%]", min_value=0.0, max_value=10.0, step=0.5, key='q_tol_input')
    
    st.markdown("---")
    
    # --- TLAK ---
    st.markdown("**Tlakový rozdíl Δp [MPa]**")
    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.slider("p", min_value=0.1, max_value=10.0, step=0.1, key='p_slider', on_change=update_p_sl, label_visibility="collapsed")
    with col_p2:
        st.number_input("p", min_value=0.1, max_value=10.0, step=0.1, key='p_num', on_change=update_p, label_visibility="collapsed")

    st.markdown("---")
    
    # --- ZUBY ---
    st.number_input("Výchozí počet zubů z (Krok 1)", min_value=6, max_value=50, step=1, key='z_init_input')
    
    z_init = st.session_state.z_init_input
    if z_init < 12 or z_init > 24:
        st.warning("⚠️ Doporučený počet zubů je v rozmezí 12 až 24.")
    
    st.markdown("---")
    st.button("🔄 Restartovat na výchozí", on_click=reset_to_defaults, use_container_width=True)

# --- ALGORITMUS (BACKEND) ---
Q_input = st.session_state.q_num
p_mpa = st.session_state.p_num
q_tol = st.session_state.q_tol_input

Q_m3s = (Q_input / 60000.0) if st.session_state.q_unit == 'l/min' else (Q_input / 1000.0)

# 2. Určení objemové účinnosti
eta_q = get_eta_q(p_mpa)

# 3, 6, 7. Volba otáček
n_sync_list = [1500, 1000, 750, 600, 500, 3000] 
n_rpm = 0
v_m_s = 0
D_prime_m = 0
selected_n_sync = 1500 # Výchozí

for n_sync in n_sync_list:
    n_test_rpm = n_sync * 0.96
    n_test_rps = n_test_rpm / 60.0
    d_test = ((z_init * Q_m3s) / (1.6 * math.pi * n_test_rps * eta_q))**(1/3)
    v_test = math.pi * d_test * n_test_rps
    
    if v_test <= 4.0:
        n_rpm = n_test_rpm
        D_prime_m = d_test
        v_m_s = v_test
        selected_n_sync = n_sync
        break

if n_rpm == 0:
    st.stop()

n_rps = n_rpm / 60.0

# 8. Předběžný modul
m_prime_mm = (D_prime_m / z_init) * 1000.0

# 9. Zaokrouhlení modulu DOLŮ podle řady I
valid_modules = [m for m in STD_MODULES if m <= m_prime_mm]
m_mm = valid_modules[-1] if valid_modules else STD_MODULES[0]

z = z_init
D_mm = z * m_mm
D_m = D_mm / 1000.0
v = math.pi * D_m * n_rps

# 11. Šířka ozubení
b_m = Q_m3s / (2 * math.pi * (m_mm/1000.0) * D_m * n_rps * eta_q)
b_mm = b_m * 1000.0

# 12-14. Iterační smyčka pro kontrolu lambda
lam = b_mm / D_mm
while lam > 0.8:
    idx = STD_MODULES.index(m_mm)
    if idx + 1 < len(STD_MODULES):
        m_mm = STD_MODULES[idx + 1]
    else:
        st.warning("Nelze více zvětšovat modul, dosaženo maxima normalizované řady.")
        break
        
    z = round(D_mm / m_mm)
    if z < 12: z = 12
    
    D_mm = z * m_mm
    D_m = D_mm / 1000.0
    b_m = Q_m3s / (2 * math.pi * (m_mm/1000.0) * D_m * n_rps * eta_q)
    b_mm = b_m * 1000.0
    lam = b_mm / D_mm

# --- INTELIGENTNÍ VOLBA ŠÍŘKY (KROK 16) ---
b_floor = math.floor(b_mm)
b_ceil = math.ceil(b_mm)

Q_floor_m3s = 2 * math.pi * (b_floor/1000.0) * (m_mm/1000.0) * D_m * n_rps * eta_q
Q_ceil_m3s = 2 * math.pi * (b_ceil/1000.0) * (m_mm/1000.0) * D_m * n_rps * eta_q

dev_floor = abs(Q_floor_m3s - Q_m3s) / Q_m3s * 100
dev_ceil = abs(Q_ceil_m3s - Q_m3s) / Q_m3s * 100

if dev_floor < dev_ceil:
    b_mm_round = b_floor
    Q_skut_m3s = Q_floor_m3s
    dev_pct = ((Q_floor_m3s - Q_m3s) / Q_m3s) * 100
else:
    b_mm_round = b_ceil
    Q_skut_m3s = Q_ceil_m3s
    dev_pct = ((Q_ceil_m3s - Q_m3s) / Q_m3s) * 100

Q_skut_lmin = Q_skut_m3s * 60000.0
Q_skut_ls = Q_skut_m3s * 1000.0

# 15. Hlavová kružnice
Da_mm = D_mm + 2 * m_mm

# 17. Účinnost a příkon
eta_overall = get_eta_overall(p_mpa, v)
P_th_W = Q_skut_m3s * (p_mpa * 1e6)
P_W = P_th_W / eta_overall
P_kW = P_W / 1000.0

# 18. Návrh motoru (cca 1.4 násobek)
P_rec_kW = P_kW * 1.4
motor_kw = next((kw for kw in STD_MOTORS_KW if kw >= P_rec_kW), STD_MOTORS_KW[-1])
recommended_motor = get_real_motor_name(selected_n_sync, motor_kw)

# --- PŘÍPRAVA ZOBRAZENÍ PODLE ZVOLENÉ JEDNOTKY ---
if st.session_state.q_unit == 'l/min':
    q_primary_val = f"{Q_skut_lmin:.1f}"
    q_primary_unit = "l/min"
else:
    q_primary_val = f"{Q_skut_ls:.3f}"
    q_primary_unit = "l/s"

# --- VYKRESLENÍ VÝSLEDKŮ ---
st.header("Výsledky automatizovaného návrhu")

v_status = "✅" if v <= 4.0 else "❌"
lam_status = "✅" if lam <= 0.8 else "❌"
q_status = "✅" if abs(dev_pct) <= q_tol else "❌"

table_left = f"""
| Veličina | Značka | Hodnota | Jednotka |
| :--- | :---: | :---: | :---: |
| Objemová účinnost | $\eta_Q$ | **{eta_q:.3f}** | - |
| Celková účinnost | $\eta$ | **{eta_overall:.3f}** | - |
| Pracovní otáčky | $n$ | **{n_rpm:.0f}** | ot/min |
| Modul ozubení (Řada I) | $m$ | **{m_mm}** | mm |
| Počet zubů | $z$ | **{z}** | - |
| Roztečný průměr | $D$ | **{D_mm:.1f}** | mm |
| Hlavový průměr | $D_a$ | **{Da_mm:.1f}** | mm |
| Šířka kola (zaokrouhlená) | $b$ | **{b_mm_round}** | mm |
"""

table_right = f"""
| Kontrola / Parametr | Značka | Hodnota | Jednotka | Podmínka |
| :--- | :---: | :---: | :---: | :---: |
| Obvodová rychlost | $v$ | **{v:.2f}** | m/s | <span style="white-space: nowrap;">≤ 4.0 {v_status}</span> |
| Poměr šířka/průměr | $\lambda$ | **{lam:.2f}** | - | <span style="white-space: nowrap;">≤ 0.8 {lam_status}</span> |
| Skutečný průtok | $Q_{{skut}}$ | **{q_primary_val}** | {q_primary_unit} | - |
| Odchylka průtoku | $\Delta Q$ | **{dev_pct:+.1f}** | % | <span style="white-space: nowrap;">≤ ±{q_tol:g} % {q_status}</span> |
| Potřebný příkon | $P$ | **{P_kW:.2f}** | kW | - |
| Navržený motor | $P_{{mot}}$ | **{motor_kw}** | kW | - |
"""

col1, col2 = st.columns(2)

with col1:
    st.subheader("Provozní parametry a geometrie")
    st.markdown(table_left, unsafe_allow_html=True)

with col2:
    st.subheader("Kontroly a volba elektromotoru")
    st.markdown(table_right, unsafe_allow_html=True)
    
    # Vypsání doporučeného motoru jen pokud je v databázi (not None)
    if recommended_motor:
        if selected_n_sync == 1500:
            st.info(f"💡 **Doporučený komerční motor:**\n\n{recommended_motor} | [Vyhledat na e-shopu](https://www.elektro-motor.cz/kategoria-produktu/elektromotory-1400ot/)")
        elif selected_n_sync == 1000:
            st.info(f"💡 **Doporučený komerční motor:**\n\n{recommended_motor} | [Vyhledat na e-shopu](https://www.elektro-motor.cz/kategoria-produktu/elektromotory-900ot/)")
        elif selected_n_sync == 750:
            st.info(f"💡 **Doporučený komerční motor:**\n\n{recommended_motor} | [Vyhledat na e-shopu](https://www.elektro-motor.cz/kategoria-produktu/elektromotory-700ot/)")

# --- VLASTNÍ VIZUALIZACE PROGRESS BARU ---
st.markdown("<br>", unsafe_allow_html=True)

bar_color = "#28a745" if abs(dev_pct) <= q_tol else "#dc3545" 
fill_pct = min((abs(dev_pct) / q_tol) * 100, 100) if q_tol > 0 else 100

st.markdown(f"""
<div style="width: 100%; background-color: #31333F; border-radius: 5px; margin-top: 10px; position: relative; height: 26px;">
  <div style="width: {fill_pct}%; height: 100%; background-color: {bar_color}; border-radius: 5px; transition: width 0.3s ease;"></div>
  <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; text-align: center; color: white; font-size: 15px; font-weight: bold; line-height: 26px; pointer-events: none; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
    Využití tolerance: {abs(dev_pct):.1f} % (Limit: {q_tol:g} %)
  </div>
</div>
""", unsafe_allow_html=True)