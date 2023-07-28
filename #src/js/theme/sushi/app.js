$(document).ready(function() {
    function copyAndAppend() {
        // Проверяем текущее разрешение дисплея
        if ($(window).width() < 480) {
            // Получаем содержимое исходного блока
            var sourceContent = $('.header-bottom__list').html();

            // Создаем новый элемент и добавляем ему скопированное содержимое
            var newElement = $('<div></div>').html(sourceContent);

            // Добавляем нужные классы к новому элементу
            newElement.addClass('app-menu');

            // Помещаем новый элемент в блок с id=append
            $('#appendCats').append(newElement);
        } else {
            // Если разрешение дисплея больше или равно 480, удаляем добавленные элементы
            $('#appendCats').empty();
        }
    }

    // Выполняем функцию при загрузке страницы
    copyAndAppend();

    // Выполняем функцию при изменении размера окна
    $(window).resize(function() {
        $('#appendCats').empty();
        copyAndAppend();
    });
});

