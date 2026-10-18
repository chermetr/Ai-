
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime

st.set_page_config(
    page_title="AGROTECH AI",
    page_icon="🚜",
    layout="wide"
)

# Оформление
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1713, #173b2d);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
div.stButton > button {
    background: #24b879;
    color: white;
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# История хранится в текущей сессии приложения
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🚜 AGROTECH AI")
st.caption("Интеллектуальный мониторинг сельхозтехники")

st.info(
    "Учебная система машинного обучения. "
    "Модель ищет необычные сочетания показателей; "
    "это не подтверждённая диагностика неисправностей."
)

# Демонстрационные нормальные измерения.
# Они нужны для обучения модели и не являются реальными данными трактора.
rng = np.random.default_rng(42)
training_data = pd.DataFrame({
    "temperature": rng.normal(85, 7, 500),
    "vibration": rng.normal(3, 1, 500),
    "pressure": rng.normal(3.2, 0.4, 500)
})

training_data["temperature"] = training_data["temperature"].clip(55, 105)
training_data["vibration"] = training_data["vibration"].clip(0, 7)
training_data["pressure"] = training_data["pressure"].clip(1.8, 5)

model = IsolationForest(
    n_estimators=150,
    contamination=0.05,
    random_state=42
)
model.fit(training_data)

st.subheader("📊 Показания датчиков")

col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input(
        "🌡️ Температура двигателя (°C)",
        min_value=0.0, max_value=200.0, value=90.0
    )

with col2:
    vibration = st.number_input(
        "〰️ Вибрация (0–10)",
        min_value=0.0, max_value=10.0, value=3.0
    )

with col3:
    pressure = st.number_input(
        "🛢️ Давление масла (бар)",
        min_value=0.0, max_value=20.0, value=3.0
    )

if st.button("🔍 ПРОВЕСТИ АНАЛИЗ"):
    values = pd.DataFrame([{
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure
    }])

    prediction = model.predict(values)[0]
    anomaly_score = model.decision_function(values)[0]

    # Отдельные проверочные предупреждения —
    # пороги условные, их нужно подтвердить для конкретной машины.
    warnings = []

    if temperature > 102:
        warnings.append("Высокая температура двигателя")
    if vibration > 7:
        warnings.append("Повышенная вибрация")
    if pressure < 1.8:
        warnings.append("Низкое давление масла")

    st.divider()
    st.subheader("🧠 Результат анализа")

    if warnings:
        st.error("Обнаружены показатели, требующие проверки")
        for warning in warnings:
            st.warning(warning)
    elif prediction == -1:
        st.warning(
            "Модель обнаружила необычное сочетание показателей. "
            "Это не означает, что неисправность точно есть."
        )
    else:
        st.success(
            "Модель не обнаружила выраженной аномалии "
            "в этих показаниях."
        )

    st.metric("Оценка необычности", f"{anomaly_score:.3f}")
    st.caption(
        "Чем ниже оценка, тем более необычными модель считает "
        "показания относительно учебных данных. "
        "Это не вероятность поломки."
    )

    st.session_state.history.append({
        "Время": datetime.now().strftime("%H:%M:%S"),
        "Температура (°C)": temperature,
        "Вибрация": vibration,
        "Давление масла (бар)": pressure,
        "Оценка модели": round(float(anomaly_score), 3)
    })

st.divider()
st.subheader("📈 История измерений")

if st.session_state.history:
    history = pd.DataFrame(st.session_state.history)
    st.dataframe(history, use_container_width=True)

    for column, title, color in [
        ("Температура (°C)", "🌡️ Температура", "#ff7043"),
        ("Вибрация", "〰️ Вибрация", "#42c5f5"),
        ("Давление масла (бар)", "🛢️ Давление масла", "#38d996")
    ]:
        st.markdown(f"### {title}")
        st.line_chart(history.set_index("Время")[[column]])
else:
    st.caption("Проведи первый анализ, чтобы появилась история.")

st.divider()
st.caption(
    "AGROTECH AI · Учебный ML-прототип · "
    "Результаты не заменяют диагностику механика."
        )
