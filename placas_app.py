# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 17:59:24 2025

@author: camil
"""
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# -------- Parámetros fijos --------
N      = 130        # número de "cargas" discretas por placa
sigma  = 1.7        # densidad lineal (escala visual)
length = 2.0        # longitud de las placas (m)

# Densidad y resolución fijos
DENSITY  = 1.8
GRID_PTS = 400

st.set_page_config(page_title="Campo eléctrico: placas paralelas", layout="wide")

# ---- Título más pequeño y centrado ----
st.markdown(
    "<div style='text-align: center; font-size:30px; font-weight:bold;'>"
    "Campo eléctrico - Condensador de placas paralelas"
    "</div>",
    unsafe_allow_html=True
)

# st.caption("© Domenico Sapone, Camila Montecinos")

# Panel lateral de configuración
st.sidebar.header("Configuración")
config = st.sidebar.radio(
    "Elige una configuración",
    options=["Configuración 1", "Configuración 2", "Configuración 3"],
    index=1
)
sep_options = {"Configuración 1": 0.5, "Configuración 2": 1.0, "Configuración 3": 1.5}
sep = sep_options[config]

def plot_parallel_plate(sep: float, density: float = DENSITY, grid_pts: int = GRID_PTS):
    """Calcula y dibuja el campo para placas paralelas con separación 'sep'."""
    # Distribución de cargas (placas en y = ±sep/2)
    xs = np.linspace(-length/2, length/2, N)
    q = sigma * (length / N)
    plate1 = [(x,  sep/2,  q) for x in xs]   # placa superior (+σ)
    plate2 = [(x, -sep/2, -q) for x in xs]   # placa inferior (−σ)

    # Malla para evaluar el campo
    x = np.linspace(-length, length, grid_pts)
    y = np.linspace(-length, length, grid_pts)
    X, Y = np.meshgrid(x, y)
    Ex = np.zeros_like(X, dtype=float)
    Ey = np.zeros_like(Y, dtype=float)

    # Superposición de campos de todas las "cargas" discretas
    for (cx, cy, cq) in plate1 + plate2:
        dx = X - cx
        dy = Y - cy
        r2 = dx**2 + dy**2
        inv_r3 = np.where(r2 == 0, 0.0, 1.0 / (r2 * np.sqrt(r2)))
        Ex += cq * dx * inv_r3
        Ey += cq * dy * inv_r3

    # Dibujo con matplotlib (figura más pequeña)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.streamplot(X, Y, Ex, Ey, color='k', linewidth=1, density=density, arrowsize=1)

    # Placas
    t = 0.04  # grosor visual
    ax.add_patch(plt.Rectangle((-length/2,  sep/2 - t/2),  length, t, color='crimson', zorder=3))
    ax.add_patch(plt.Rectangle((-length/2, -sep/2 - t/2),  length, t, color='navy',    zorder=3))

    # Etiquetas +σ y −σ
    ax.text(length/2 + 0.08,  sep/2, r'+$\sigma$', color='crimson', va='center', fontsize=12, weight='bold')
    ax.text(length/2 + 0.08, -sep/2, r'-$\sigma$', color='navy',    va='center', fontsize=12, weight='bold')

    ax.set_aspect('equal')
    ax.set_xlim(-length, length)
    ax.set_ylim(-length, length)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title(f'Campo eléctrico (sep = {sep:.2f} m)')

    return fig

# Generar figura
fig = plot_parallel_plate(sep, density=DENSITY, grid_pts=GRID_PTS)

# Mostrar centrado (evita ocupar todo el ancho)
col_izq, col_centro, col_der = st.columns([1, 3, 1])
with col_centro:
    st.pyplot(fig)  # sin use_container_width para no expandir

# Pie de página
st.markdown(
    "<div style='text-align:center; color:gray; font-size:12px;'>"
    "© Domenico Sapone, Camila Montecinos"
    "</div>",
    unsafe_allow_html=True
)






