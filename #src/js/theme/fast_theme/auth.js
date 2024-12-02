$(document).ready(function () {
    // Получение CSRF-токена из cookie
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                return cookie.substring('csrftoken='.length, cookie.length);
            }
        }
        return null;
    }

    const csrfToken = getCSRFToken();

    // Таймер для повторной отправки
    function startResendTimer(duration) {
        const endTime = Date.now() + duration * 1000; // Время окончания
        localStorage.setItem('resendTimerEnd', endTime);

        const button = $('#resendSmsButton');
        button.prop('disabled', true);

        const interval = setInterval(() => {
            const timeLeft = Math.ceil((endTime - Date.now()) / 1000);
            if (timeLeft > 0) {
                button.text(`${timeLeft} сек.`);
            } else {
                clearInterval(interval);
                button.prop('disabled', false);
                button.text('Отправить код');
                localStorage.removeItem('resendTimerEnd');
            }
        }, 1000);
    }

    // Восстановление состояния кнопки при загрузке страницы
    function restoreResendTimer() {
        const endTime = localStorage.getItem('resendTimerEnd');
        if (endTime) {
            const timeLeft = Math.ceil((endTime - Date.now()) / 1000);
            if (timeLeft > 0) {
                startResendTimer(timeLeft); // Запускаем таймер с оставшимся временем
            } else {
                localStorage.removeItem('resendTimerEnd'); // Таймер истек
                $('#resendSmsButton').prop('disabled', false).text('Отправить код');
            }
        }
    }

    // Восстанавливаем таймер при загрузке страницы
    restoreResendTimer();

    // Шаг 1: Отправка номера телефона
    $(document).on('submit', '#phoneForm', function(e) {
        e.preventDefault();
        const phone = $('#phone').val();

        $.ajax({
            url: '/api/v1/send-sms-code/',
            type: 'POST',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({ phone }),
            success: function (response) {
                // $('#message').text(response.message).css('color', 'green');
                $('#phoneForm').hide();
                $('#codeForm').show();
                startResendTimer(60); // Запускаем таймер на 60 секунд
            },
            error: function (xhr) {
                const errorResponse = JSON.parse(xhr.responseText);
                $('#message').text(errorResponse.message).css('color', 'red');

            }
        });
    });

    // Шаг 2: Проверка кода
    $(document).on('submit', '#codeForm', async function(e) {
        e.preventDefault();
        const phone = $('#phone').val();
        const code = $('#code').val();
    
        $.ajax({
            url: '/api/v1/verify-sms-code/',
            type: 'POST',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({ phone, code }),
            success: async function (response) { // Объявляем callback как async
                // Обновляем DOM и выполняем последующие функции    
                $('#phone-wrap').load(location.href + " #phone-wrap__refresh", async function () { // Объявляем этот callback как async
    
                    fetch('/api/v1/get_user/')
                        .then(response => response.json())
                        .then(data => {
                            let set_data = {
                                'cart_balls': data.cart_balls,
                                'percent_down': data.percent_down,
                                'percent_down_pickup': data.percent_down_pickup,
                                'percent_pay': data.percent_pay,
                                'percent_pay_pickup': data.percent_pay_pickup,
                                'balls_min_summ': data.balls_min_summ,
                                'exclude_combos': data.exclude_combos,
                                'exclude_sales': data.exclude_sales,
                            };
                            localStorage.setItem('loyalCart', JSON.stringify(set_data));
                            maxBallsPay();
                        })
                        .catch(error => console.error('Ошибка загрузки пользователя:', error));

                        
                });
    
            },
            error: function (xhr) {
                const errorResponse = JSON.parse(xhr.responseText);
                $("#code").css('border-color', 'red');
            }
        });
    });
    
    

    // Кнопка повторной отправки SMS
    $(document).on('click', '#resendSmsButton', function(e) {
        e.preventDefault();
        const phone = $('#phone').val();

        $.ajax({
            url: '/api/v1/send-sms-code/',
            type: 'POST',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({ phone }),
            success: function (response) {
                $('#message').text(response.message).css('color', 'green');
                startResendTimer(60); // Запускаем таймер на 60 секунд
            },
            error: function (xhr) {
                const errorResponse = JSON.parse(xhr.responseText);
                $('#message').text(errorResponse.message).css('color', 'red');
            }
        });
    });

    $(document).on('click', '#logout', function(e) {

        e.preventDefault();
        $.get("/api/v1/logout/")
        .done(function() {
            $('#phone-wrap').load(location.href + " #phone-wrap__refresh", async function () {
                fetch('/api/v1/get_user/')
                    .then(response => response.json())
                    .then(data => {
                        let set_data = {
                            'cart_balls': data.cart_balls,
                            'percent_down': data.percent_down,
                            'percent_down_pickup': data.percent_down_pickup,
                            'percent_pay': data.percent_pay,
                            'percent_pay_pickup': data.percent_pay_pickup,
                            'balls_min_summ': data.balls_min_summ,
                            'exclude_combos': data.exclude_combos,
                            'exclude_sales': data.exclude_sales,
                        };
                        localStorage.setItem('loyalCart', JSON.stringify(set_data));

                        let order = JSON.parse(localStorage.getItem('order'));
                        order.user_phone = '';
                        order.bonuses_pay = 0;
                        localStorage.setItem('order', JSON.stringify(order));
                        $('.active_balls').remove();
                        $('#balls').html('');

                        maxBallsPay();
                        updateAll();
                    })
                    .catch(error => console.error('Ошибка загрузки пользователя:', error));
                

            });
            
        });
    });


});


$(document).ready(function () {
    // Проверка наличия активной сессии
    function checkSessionAndClearStorage() {
        $.ajax({
            url: '/api/v1/check-session/', // Эндпоинт для проверки сессии
            type: 'GET',
            success: function (response) {
                if (!response.isAuthenticated) {
                    // Если пользователь не аутентифицирован, очищаем localStorage
                    order = JSON.parse(localStorage.getItem('order'));
                    // console.log(order);
                    order.phone = '';
                    localStorage.setItem('order', JSON.stringify(order));

                }
            },
            error: function () {
                // При ошибке также очищаем localStorage
                localStorage.removeItem('order');
            }
        });
    }

    // Вызов проверки сессии при загрузке страницы
    checkSessionAndClearStorage();

    // Существующий код таймера и отправки SMS...
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                return cookie.substring('csrftoken='.length, cookie.length);
            }
        }
        return null;
    }

    const csrfToken = getCSRFToken();

    function startResendTimer(duration) {
        const endTime = Date.now() + duration * 1000; // Время окончания
        localStorage.setItem('resendTimerEnd', endTime);

        const button = $('#resendSmsButton');
        button.prop('disabled', true);

        const interval = setInterval(() => {
            const timeLeft = Math.ceil((endTime - Date.now()) / 1000);
            if (timeLeft > 0) {
                button.text(`${timeLeft} сек.`);
            } else {
                clearInterval(interval);
                button.prop('disabled', false);
                button.text('Отправить код');
                localStorage.removeItem('resendTimerEnd');
            }
        }, 1000);
    }

    function restoreResendTimer() {
        const endTime = localStorage.getItem('resendTimerEnd');
        if (endTime) {
            const timeLeft = Math.ceil((endTime - Date.now()) / 1000);
            if (timeLeft > 0) {
                startResendTimer(timeLeft);
            } else {
                localStorage.removeItem('resendTimerEnd');
                $('#resendSmsButton').prop('disabled', false).text('Отправить код');
            }
        }
    }

    restoreResendTimer();
});
