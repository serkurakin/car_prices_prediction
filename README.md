
# Сервис по оценке стоимости подержанных автомобилей на основе модели машинного обучения

Сервис рассчитывает стоимость подержанного автомобиля по введенным входным характеристикам для примерной оценки его цены

# Функциональность

1. FastAPI: Предлагает API-endpoint для программного доступа к сервису по определению цены автомобилей.
2. Streamlit: Прозволяет взаимодействовать с моделью через web-интерфейс
3. Docker: Используется Docker-контейнер для контейнеризации и легкого развертывания.

# Необходимые условия запуска сервиса

Установленный на системе Docker.

# Скриншоты веб-приложения

![Streamlit Interface](https://github.com/serkurakin/car_prices_prediction/blob/main/images/screenshot_1.PNG?raw=true) 
![Streamlit Interface](https://github.com/serkurakin/car_prices_prediction/blob/main/images/screenshot_2.PNG?raw=true)
![Streamlit Interface](https://github.com/serkurakin/car_prices_prediction/blob/main/images/screenshot_3.PNG?raw=true)
![Streamlit Interface](https://github.com/serkurakin/car_prices_prediction/blob/main/images/screenshot_4.PNG?raw=true)

# Запуск сервиса

1. Убедиться, что Docker и Docker Compose установлены на сервере, а Docker Desktop запущен в системе.

2. Клонировать репозиторий

* git clone https://github.com/serkurakin/car_prices_prediction.git  
* cd car_prices_prediction

3. Запустить сервис. Для этого необходимо использовать команду:

* docker-compose up --build

4. Открыть Streamlit-приложение в браузере по адресу http://localhost:8501. Этот порт используется для frontend интерфейса. Получить доступ к FastAPI по адресу http://localhost:8001. Этот порт используется для backend-API.