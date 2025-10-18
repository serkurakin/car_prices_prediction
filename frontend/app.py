import streamlit as st
import pandas as pd
from PIL import Image
import requests
import os

# Получаем настройки из переменных окружения
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
APP_NAME = os.getenv("APP_NAME", "Car Prices Predictor")

# Настройка страницы (ТОЛЬКО ОДИН РАЗ)
st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)

# Заголовок приложения
st.title("Предсказание стоимости автомобиля на основе его характеристик")

st.header("Характеристики автомобиля")

# Категориальные признаки - выпадающие списки
vehicle_type = st.selectbox(
    "Тип автомобиля",
    options=['small', 'sedan', 'wagon', 'coupe', 'suv', 'convertible', 'bus', 'other', 'unknown']
)

gearbox = st.selectbox(
    "Коробка передач",
    options=['manual', 'auto', 'unknown']
)

fuel_type = st.selectbox(
    "Тип топлива",
    options=['petrol', 'gasoline', 'lpg', 'cng', 'hybrid', 'electric', 'other', 'unknown']
)

repaired = st.selectbox(
    "Состояние (был ли автомобиль в ремонте)",
    options=['yes', 'no', 'unknown']
)

# Числовые признаки - поля ввода
registration_year = st.number_input(
    "Год регистрации",
    min_value=1950,
    max_value=2015,
    value=2010,
    step=1
)

power = st.number_input(
    "Мощность (л.с.)",
    min_value=1,
    max_value=450,
    value=120,
    step=1
)

kilometer = st.number_input(
    "Пробег (км)",
    min_value=5000,
    max_value=150000,
    value=100000,
    step=10000
)

# Марка автомобиля
brand = st.text_input(
    "Марка автомобиля",
    value="bmw",
    placeholder="Введите марку (например: volkswagen, opel, mercedes_benz..., если название состоит из 2-х слов, введите их через нижнее подчеркивание)"
)

# Модель автомобиля
model_car = st.text_input(
    "Модель автомобиля",
    value="golf",
    placeholder="Введите модель (например: golf, polo, 3er..., если название состоит из 2-х слов, введите их через нижнее подчеркивание)"
)

# Кнопка предсказания
if st.button("Предсказать цену", type="primary"):
    try:
        # Подготовка данных для отправки
        input_data = {
            'vehicle_type': vehicle_type,
            'registration_year': registration_year,
            'gearbox': gearbox,
            'power': power,
            'model': model_car.lower().strip(),
            'kilometer': kilometer,
            'fuel_type': fuel_type,
            'brand': brand,
            'repaired': repaired
        }
        
        # Отправка POST запроса на бэкенд
        response = requests.post(f"{BACKEND_URL}/predict_model", json=input_data, timeout=30)
        
        # Проверка статуса ответа
        if response.status_code == 200:
            result = response.json()
            
            # Проверяем наличие prediction в ответе
            if 'prediction' in result:
                price = result['prediction']
                
                # Показываем результат
                st.success("### Результат предсказания")
                
                # отображение цены
                col_pred1, col_pred2, col_pred3 = st.columns([1, 2, 1])
                
                with col_pred2:
                    st.metric(
                        label="**Предсказанная цена**",
                        value=f"€{price:,.0f}"
                    )
                
                # Дополнительная информация
                st.info("""
                **Введенные параметры:**
                - Тип: {}
                - Год: {}
                - Коробка: {}
                - Мощность: {} л.с.
                - Модель: {}
                - Пробег: {} км
                - Топливо: {}
                - Марка: {}
                - Состояние: {}
                """.format(
                    vehicle_type, registration_year, gearbox, power, 
                    model_car, kilometer, fuel_type, brand, repaired
                ))
            else:
                st.error(f"Некорректный ответ от сервера: {result}")
                
        else:
            st.error(f"Ошибка сервера {response.status_code}: {response.text}")
        
    except requests.exceptions.ConnectionError:
        st.error(f"Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен на {BACKEND_URL}")

# Боковая панель с информацией
with st.sidebar:
    st.header("О приложении")
    st.markdown("""
    Это приложение предсказывает стоимость подержанного автомобиля 
    на основе модели машинного обучения.
    
    **Как использовать:**
    1. Заполните все поля
    2. Нажмите кнопку 'Предсказать цену'
    3. Получите результат
    """)

# Футер
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p> Car Price Predictor • Made with Streamlit</p>
</div>
""", unsafe_allow_html=True)