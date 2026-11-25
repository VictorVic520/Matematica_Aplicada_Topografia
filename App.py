import math
import matplotlib.pyplot as plt
import streamlit as st

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y FUNCIONES AUXILIARES
# ==========================================
st.set_page_config(
    page_title="Matemática Aplicada - Topografía y Geodesia",
    page_icon="📐",
    layout="centered",
)


def dms_to_deg(g, m, s):
    """Convierte Grados, Minutos y Segundos a Grados Decimales."""
    signo = -1 if g < 0 else 1
    return signo * (abs(g) + m / 60.0 + s / 3600.0)


def deg_to_dms_str(deg):
    """Formatea Grados Decimales a texto GMS (° ' '')."""
    d = int(deg)
    rem = abs(deg - d) * 60
    m = int(rem)
    s = (rem - m) * 60
    return f"{d}° {m:02d}' {s:05.2f}\""


def input_angulo_topografico(label, default_deg, key_prefix):
    """Widget inteligente para ingresar ángulos en Decimal o GMS."""
    modo = st.radio(
        f"Formato para {label}:",
        ["Decimal (°)", "Sexagesimal (° ' \")"],
        horizontal=True,
        key=f"{key_prefix}_modo",
    )
    if modo == "Decimal (°)":
        return st.number_input(
            f"{label} (°)",
            min_value=0.01,
            max_value=179.99,
            value=float(default_deg),
            step=0.5,
            key=f"{key_prefix}_dec",
        )
    else:
        c1, c2, c3 = st.columns(3)
        g_def = int(default_deg)
        m_def = int((default_deg - g_def) * 60)
        s_def = round(((default_deg - g_def) * 60 - m_def) * 60, 1)
        g = c1.number_input(
            "Grados (°)", 0, 179, g_def, key=f"{key_prefix}_g"
        )
        m = c2.number_input(
            "Minutos (')", 0, 59, m_def, key=f"{key_prefix}_m"
        )
        s = c3.number_input(
            'Segundos (")', 0.0, 59.99, float(s_def), key=f"{key_prefix}_s"
        )
        return dms_to_deg(g, m, s)


def dibujar_triangulo_topografico(a, b, c, A_deg, B_deg, C_deg):
    """Genera un croquis geométrico a escala del levantamiento."""
    # Coordenadas: C en (0,0), B en (a, 0), A calculado por trigonometría
    C_rad = math.radians(C_deg)
    Ax = b * math.cos(C_rad)
    Ay = b * math.sin(C_rad)

    fig, ax = plt.subplots(figsize=(6, 4))
    xs = [0, a, Ax, 0]
    ys = [0, 0, Ay, 0]

    ax.plot(xs, ys, "o-", color="#1f77b4", linewidth=2.2, markersize=7)
    ax.fill(xs, ys, color="#1f77b4", alpha=0.12)

    # Etiquetas de vértices
    offset = max(a, b, c) * 0.04
    ax.text(
        -offset, -offset, f"Estación C\n({C_deg:.1f}°)", fontweight="bold", ha="right"
    )
    ax.text(
        a + offset, -offset, f"Estación B\n({B_deg:.1f}°)", fontweight="bold", ha="left"
    )
    ax.text(
        Ax,
        Ay + offset,
        f"Estación A\n({A_deg:.1f}°)",
        fontweight="bold",
        ha="center",
    )

    # Etiquetas de lados
    ax.text(
        a / 2,
        -offset * 1.3,
        f"a = {a:.2f} m",
        color="#d62728",
        ha="center",
        fontweight="bold",
    )
    ax.text(
        (Ax + a) / 2 + offset,
        Ay / 2,
        f"c = {c:.2f} m",
        color="#d62728",
        ha="left",
        fontweight="bold",
    )
    ax.text(
        Ax / 2 - offset,
        Ay / 2,
        f"b = {b:.2f} m",
        color="#d62728",
        ha="right",
        fontweight="bold",
    )

    ax.set_aspect("equal", adjustable="datalim")
    ax.margins(0.25)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_title("Croquis del Levantamiento Topográfico (A escala)")
    ax.set_xlabel("Este / X (metros)")
    ax.set_ylabel("Norte / Y (metros)")
    return fig


# ==========================================
# ENCABEZADO ACADÉMICO
# ==========================================
st.title("📐 Suite de Matemática Aplicada")
st.markdown(
    "**Producto Académico — Ciclo I: Topografía y Geodesia**"
)
st.info(
    "Herramienta de cálculo para gabinete y campo: Proporcionalidad y Resolución de Triángulos Oblicuángulos."
)

# Pestañas principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ R3 Directa",
    "2️⃣ R3 Inversa",
    "3️⃣ R3 Compuesta",
    "4️⃣ Ley de Cosenos",
    "5️⃣ Ley de Senos",
])

# ==========================================
# PESTAÑA 1: REGLA DE TRES SIMPLE DIRECTA
# ==========================================
with tab1:
    st.header("Regla de Tres Simple Directa")
    st.write(
        "Se aplica cuando dos magnitudes son **directamente proporcionales** (si una aumenta, la otra también)."
    )
    st.latex(r"\frac{A}{B} = \frac{C}{X} \implies X = \frac{B \cdot C}{A}")

    with st.expander("📌 Ejemplo Topográfico: Escalas en Planos"):
        st.write(
            "En un plano, **4 cm** equivalen a **100 m** en campo. ¿Cuántos metros reales representan **14.5 cm**?"
        )

    col1, col2 = st.columns(2)
    with col1:
        a_dir = st.number_input("Dato conocido (A)", value=4.0, step=0.1, key="a_dir")
        c_dir = st.number_input("Dato a calcular (C)", value=14.5, step=0.1, key="c_dir")
    with col2:
        b_dir = st.number_input("Equivalencia (B)", value=100.0, step=1.0, key="b_dir")
        st.text_input("Incógnita (X)", value="¿Cuánto vale X?", disabled=True)

    if st.button("Calcular Directa", type="primary"):
        if a_dir == 0:
            st.error("El valor de A no puede ser cero.")
        else:
            x_dir = (b_dir * c_dir) / a_dir
            st.success(f"### Resultado: X = {x_dir:.4f}")
            st.latex(
                rf"X = \frac{{{b_dir} \times {c_dir}}}{{{a_dir}}} = {x_dir:.4f}"
            )

# ==========================================
# PESTAÑA 2: REGLA DE TRES SIMPLE INVERSA
# ==========================================
with tab2:
    st.header("Regla de Tres Simple Inversa")
    st.write(
        "Se aplica cuando dos magnitudes son **inversamente proporcionales** (si una aumenta, la otra disminuye)."
    )
    st.latex(r"A \cdot B = C \cdot X \implies X = \frac{A \cdot B}{C}")

    with st.expander("📌 Ejemplo Topográfico: Rendimiento de Brigadas"):
        st.write(
            "**3 topógrafos** levantan una poligonal en **12 días**. ¿En cuántos días lo harán **4 topógrafos**?"
        )

    col1, col2 = st.columns(2)
    with col1:
        a_inv = st.number_input("Dato conocido (A)", value=3.0, step=1.0, key="a_inv")
        c_inv = st.number_input("Nuevo valor (C)", value=4.0, step=1.0, key="c_inv")
    with col2:
        b_inv = st.number_input("Recurso inicial (B)", value=12.0, step=1.0, key="b_inv")
        st.text_input("Incógnita (X)", value="¿Cuánto vale X?", disabled=True)

    if st.button("Calcular Inversa", type="primary"):
        if c_inv == 0:
            st.error("El valor de C no puede ser cero.")
        else:
            x_inv = (a_inv * b_inv) / c_inv
            st.success(f"### Resultado: X = {x_inv:.4f}")
            st.latex(
                rf"X = \frac{{{a_inv} \times {b_inv}}}{{{c_inv}}} = {x_inv:.4f}"
            )

# ==========================================
# PESTAÑA 3: REGLA DE TRES COMPUESTA
# ==========================================
with tab3:
    st.header("Regla de Tres Compuesta")
    st.write("Relaciona **tres o más magnitudes** proporcionales simultáneamente.")

    with st.expander("📌 Ejemplo Topográfico: Levantamiento con Estación Total"):
        st.write(
            "**2 brigadas** trabajando **8 h/día** levantan **40 ha**. ¿Cuántas hectáreas levantarán **3 brigadas** trabajando **6 h/día**?"
        )

    c1, c2, c3 = st.columns(3)
    a1 = c1.number_input("Magnitud 1 Inicial (A1)", value=2.0, key="a1")
    a2 = c2.number_input("Magnitud 1 Final (A2)", value=3.0, key="a2")
    rel_a = c3.selectbox("Relación A con X", ["Directa", "Inversa"], key="rel_a")

    c4, c5, c6 = st.columns(3)
    b1 = c4.number_input("Magnitud 2 Inicial (B1)", value=8.0, key="b1")
    b2 = c5.number_input("Magnitud 2 Final (B2)", value=6.0, key="b2")
    rel_b = c6.selectbox("Relación B con X", ["Directa", "Inversa"], key="rel_b")

    x1 = st.number_input("Valor conocido de la incógnita (X1)", value=40.0, key="x1")

    if st.button("Calcular Compuesta", type="primary"):
        if (
            (rel_a == "Directa" and a1 == 0)
            or (rel_a == "Inversa" and a2 == 0)
            or (rel_b == "Directa" and b1 == 0)
            or (rel_b == "Inversa" and b2 == 0)
        ):
            st.error("Error: División entre cero no permitida.")
        else:
            factor_a = (a2 / a1) if rel_a == "Directa" else (a1 / a2)
            factor_b = (b2 / b1) if rel_b == "Directa" else (b1 / b2)
            x_comp = x1 * factor_a * factor_b
            st.success(f"### Resultado: X = {x_comp:.4f}")

# ==========================================
# PESTAÑA 4: LEY DE COSENOS (RADIACIÓN / OBSTÁCULOS)
# ==========================================
with tab4:
    st.header("Ley de Cosenos (Caso LAL / LLL)")
    st.write(
        "Fundamental en topografía para **medición indirecta de distancias** (cuando existe un obstáculo como un río, edificio o laguna entre dos vértices)."
    )
    st.latex(r"c = \sqrt{a^2 + b^2 - 2ab \cdot \cos(C)}")

    with st.expander("📌 Caso Práctico: Método de Radiación desde Estación C"):
        st.write(
            "Estacionamos el equipo en el punto **C**. Visamos el punto **B** a una distancia $a = 125.40\text{ m}$ y el punto **A** a $b = 98.60\text{ m}$, midiendo un ángulo horizontal interno $C = 64.5^\circ$. Calcula la distancia inaccesible $c$ entre **A** y **B**, los ángulos restantes y el área del predio."
        )

    caso_cos = st.selectbox(
        "Selecciona los datos conocidos en campo:",
        [
            "Caso 1: Dos lados y el ángulo comprendido (LAL) → Hallar lado opuesto",
            "Caso 2: Tres lados conocidos (LLL) → Hallar ángulos internos (Trilateración)",
        ],
    )

    if "Caso 1" in caso_cos:
        col1, col2 = st.columns(2)
        lado_a = col1.number_input(
            "Distancia CB - Lado a (m)", min_value=0.01, value=125.40, step=1.0
        )
        lado_b = col2.number_input(
            "Distancia CA - Lado b (m)", min_value=0.01, value=98.60, step=1.0
        )
        ang_C = input_angulo_topografico("Ángulo horizontal C", 64.5, "cos_c")

        if st.button("Resolver Triángulo (Cosenos)", type="primary"):
            C_rad = math.radians(ang_C)
            lado_c = math.sqrt(
                lado_a**2 + lado_b**2 - 2 * lado_a * lado_b * math.cos(C_rad)
            )

            # Cálculo de los ángulos restantes usando ley de cosenos inversa para evitar ambigüedad
            cos_A = (lado_b**2 + lado_c**2 - lado_a**2) / (2 * lado_b * lado_c)
            ang_A = math.degrees(math.acos(max(-1.0, min(1.0, cos_A))))
            ang_B = 180.0 - ang_A - ang_C
            area_m2 = 0.5 * lado_a * lado_b * math.sin(C_rad)

            st.success(f"### Distancia calculada (c): {lado_c:.4f} m")
            st.latex(
                rf"c = \sqrt{{{lado_a}^2 + {lado_b}^2 - 2({lado_a})({lado_b})\cos({ang_C:.2f}^\circ)}} = {lado_c:.4f}\text{{ m}}"
            )

            # Resumen de libreta de campo
            st.markdown("#### 📋 Resumen de Libreta Topográfica:")
            m1, m2, m3 = st.columns(3)
            m1.metric("Ángulo A", f"{ang_A:.3f}°", deg_to_dms_str(ang_A))
            m2.metric("Ángulo B", f"{ang_B:.3f}°", deg_to_dms_str(ang_B))
            m3.metric("Superficie", f"{area_m2:.2f} m²", f"{area_m2/10000:.4f} ha")

            fig = dibujar_triangulo_topografico(
                lado_a, lado_b, lado_c, ang_A, ang_B, ang_C
            )
            st.pyplot(fig)

    else:
        st.write(
            "Ideal cuando solo cuentas con cinta métrica o distanciómetro (Trilateración)."
        )
        c1, c2, c3 = st.columns(3)
        lado_a = c1.number_input("Lado a (m)", min_value=0.01, value=120.0, key="lll_a")
        lado_b = c2.number_input("Lado b (m)", min_value=0.01, value=100.0, key="lll_b")
        lado_c = c3.number_input("Lado c (m)", min_value=0.01, value=115.0, key="lll_c")

        if st.button("Calcular Ángulos (Trilateración)", type="primary"):
            # Verificar desigualdad triangular
            if (
                (lado_a + lado_b <= lado_c)
                or (lado_a + lado_c <= lado_b)
                or (lado_b + lado_c <= lado_a)
            ):
                st.error(
                    "⚠️ Error Geométrico: Los lados ingresados no pueden formar un triángulo cerrado (la suma de dos lados debe ser mayor al tercero)."
                )
            else:
                ang_A = math.degrees(
                    math.acos((lado_b**2 + lado_c**2 - lado_a**2) / (2 * lado_b * lado_c))
                )
                ang_B = math.degrees(
                    math.acos((lado_a**2 + lado_c**2 - lado_b**2) / (2 * lado_a * lado_c))
                )
                ang_C = 180.0 - ang_A - ang_B
                s_semi = (lado_a + lado_b + lado_c) / 2
                area_m2 = math.sqrt(
                    s_semi * (s_semi - lado_a) * (s_semi - lado_b) * (s_semi - lado_c)
                )

                st.success("### Triángulo cerrado correctamente")
                m1, m2, m3 = st.columns(3)
                m1.metric("Ángulo A", f"{ang_A:.3f}°", deg_to_dms_str(ang_A))
                m2.metric("Ángulo B", f"{ang_B:.3f}°", deg_to_dms_str(ang_B))
                m3.metric("Ángulo C", f"{ang_C:.3f}°", deg_to_dms_str(ang_C))
                st.info(
                    f"**Área del terreno:** {area_m2:.2f} m² ({area_m2/10000:.4f} hectáreas)"
                )

                fig = dibujar_triangulo_topografico(
                    lado_a, lado_b, lado_c, ang_A, ang_B, ang_C
                )
                st.pyplot(fig)

# ==========================================
# PESTAÑA 5: LEY DE SENOS (TRIANGULACIÓN GEODÉSICA)
# ==========================================
with tab5:
    st.header("Ley de Senos (Triangulación Topográfica)")
    st.write(
        "Base de las **redes de triangulación geodésica**: a partir de una línea base medida con precisión y dos ángulos observados con teodolito, se determinan puntos lejanos inaccesibles."
    )
    st.latex(r"\frac{a}{\sin(A)} = \frac{b}{\sin(B)} = \frac{c}{\sin(C)}")

    with st.expander("📌 Caso Práctico: Intersección Directa hacia un Hito Inaccesible"):
        st.write(
            "Se mide una línea base $c = 250.00\text{ m}$ entre las estaciones **A** y **B**. Desde **A** se mide el ángulo $A = 52^\circ$ hacia un hito **C** al otro lado de un barranco, y desde **B** se mide $B = 68^\circ$. Halla las distancias $a$ y $b$ hacia el hito."
        )

    lado_base_c = st.number_input(
        "Línea Base conocida - Lado c (m)",
        min_value=0.01,
        value=250.00,
        step=5.0,
        key="sen_c",
    )

    col1, col2 = st.columns(2)
    with col1:
        ang_A_sen = input_angulo_topografico("Ángulo en Estación A", 52.0, "sen_a")
    with col2:
        ang_B_sen = input_angulo_topografico("Ángulo en Estación B", 68.0, "sen_b")

    if st.button("Resolver Triangulación (Senos)", type="primary"):
        if ang_A_sen + ang_B_sen >= 180.0:
            st.error(
                f"⚠️ Error Geométrico: La suma de los ángulos A + B ({ang_A_sen + ang_B_sen:.2f}°) debe ser menor a 180° para que las visuales se crucen."
            )
        else:
            ang_C_sen = 180.0 - (ang_A_sen + ang_B_sen)
            sin_C = math.sin(math.radians(ang_C_sen))

            lado_a_sen = (lado_base_c * math.sin(math.radians(ang_A_sen))) / sin_C
            lado_b_sen = (lado_base_c * math.sin(math.radians(ang_B_sen))) / sin_C
            area_sen = 0.5 * lado_a_sen * lado_b_sen * sin_C

            st.success(
                f"### Resultados: Lado a = {lado_a_sen:.4f} m | Lado b = {lado_b_sen:.4f} m"
            )
            st.latex(
                rf"C = 180^\circ - ({ang_A_sen:.2f}^\circ + {ang_B_sen:.2f}^\circ) = {ang_C_sen:.2f}^\circ"
            )
            st.latex(
                rf"a = \frac{{{lado_base_c} \cdot \sin({ang_A_sen:.2f}^\circ)}}{{\sin({ang_C_sen:.2f}^\circ)}} = {lado_a_sen:.4f}\text{{ m}} \quad ; \quad b = \frac{{{lado_base_c} \cdot \sin({ang_B_sen:.2f}^\circ)}}{{\sin({ang_C_sen:.2f}^\circ)}} = {lado_b_sen:.4f}\text{{ m}}"
            )

            st.markdown("#### 📋 Resumen de Libreta Topográfica:")
            m1, m2, m3 = st.columns(3)
            m1.metric("Ángulo C (Cierre)", f"{ang_C_sen:.3f}°", deg_to_dms_str(ang_C_sen))
            m2.metric("Perímetro", f"{lado_a_sen + lado_b_sen + lado_base_c:.2f} m")
            m3.metric("Superficie", f"{area_sen:.2f} m²", f"{area_sen/10000:.4f} ha")

            fig = dibujar_triangulo_topografico(
                lado_a_sen,
                lado_b_sen,
                lado_base_c,
                ang_A_sen,
                ang_B_sen,
                ang_C_sen,
            )
            st.pyplot(fig)

# ==========================================
# PIE DE PÁGINA
# ==========================================
st.divider()
st.caption(
    "Desarrollado con Python, Streamlit y Matplotlib • Curso de Matemática Aplicada • Topografía y Geodesia"
  )
  
