import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AGROTECH AI",
    page_icon="🚜",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #102820, #183f32);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
div.stButton > button {
    background-color: #31b779;
    color: white;
    border-radius: 12px;
    border: none;
    height: 3em;
    font-weight: bold;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🚜 AGROTECH AI")
st.subheader("Интеллектуальная диагностика сельхозтехники")

st.success("Система готова к анализу показаний")

st.markdown("### 📊 Данные датчиков")

col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input(
        "🌡️ Температура двигателя (°C)",
        min_value=0.0,
        max_value=200.0,
        value=90.0
    )

with col2:
    vibration = st.number_input(
        "〰️ Вибрация (0–10)",
        min_value=0.0,
        max_value=10.0,
        value=3.0
    )

with col3:
    pressure = st.number_input(
        "🛢️ Давление масла (бар)",
        min_value=0.0,
        max_value=20.0,
        value=3.0
    )

if st.button("🔍 ПРОВЕСТИ ДИАГНОСТИКУ"):
    problems = []

    if temperature > 102:
        problems.append(
            "🌡️ Возможен перегрев. Проверь систему охлаждения."
        )

    if vibration > 7:
        problems.append(
            "〰️ Повышенная вибрация. Проверь крепления и подшипники."
        )

    if pressure < 1.8:
        problems.append(
            "🛢️ Низкое давление масла. Проверь систему смазки."
        )

    st.markdown("---")
    st.markdown("## 📋 Результат диагностики")

    if problems:
        st.error("Обнаружены возможные отклонения")

        for problem in problems:
            st.warning(problem)
    else:
        st.success(
            "Критических отклонений по учебным порогам не обнаружено."
        )

    st.markdown("### 📈 Показания датчиков")

    chart_data = pd.DataFrame({
        "Показатель": [
            "Температура (°C)",
            "Вибрация (0–10)",
            "Давление масла (бар)"
        ],
        "Значение": [
            temperature,
            vibration,
            pressure
        ]
    }).set_index("Показатель")

    st.bar_chart(chart_data)

    st.caption(
        "Учебный прототип. Пороги условные и требуют "
        "проверки для конкретной модели техники."
    )

st.markdown("---")
st.caption("AGROTECH AI · Учебный проект")
