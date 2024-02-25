$(document).ready(function () {

    $('.toggle-button').click(function () {
        // Находим ближайший контейнер к кнопке
        var container = $(this).closest('.side-container, .db-connection-container');

        // Переключаем класс для сворачивания/разворачивания
        container.toggleClass('collapsed');

        // Изменяем текст кнопки в зависимости от состояния контейнера
        if (container.hasClass('collapsed')) {
            $(this).text('+');
        } else {
            $(this).text('-');
        }
    });

    function setTheme(theme) {
        if (theme === 'dark-theme') {
            $('body').removeClass('light-theme').addClass('dark-theme');
        } else {
            $('body').removeClass('dark-theme').addClass('light-theme');
        }
    }

    if (localStorage.getItem('theme')) {
        setTheme(localStorage.getItem('theme'));
        $('#themeChoice').val(localStorage.getItem('theme'));
    }

    $('#themeChoice').change(function () {
        var selectedTheme = $(this).val();
        setTheme(selectedTheme);
        localStorage.setItem('theme', selectedTheme);
    });

    $('#textForm').on('submit', function (e) {
        e.preventDefault(); // Предотвращаем обычную отправку формы
        // Собираем данные из формы, включая выбранные параметры API и формат ответа
        var formData = $(this).serialize() + '&apiChoice=' + encodeURIComponent($('#apiChoice').val());
        formData += '&responseFormat=' + encodeURIComponent($('#responseFormat').val());

        // Добавляем данные о подключении к базе данных из новых полей ввода
        formData += '&dbHost=' + encodeURIComponent($('#dbHost').val());
        formData += '&dbPort=' + encodeURIComponent($('#dbPort').val());
        formData += '&dbName=' + encodeURIComponent($('#dbName').val());
        formData += '&dbUser=' + encodeURIComponent($('#dbUser').val());
        formData += '&dbPassword=' + encodeURIComponent($('#dbPassword').val());

        // Очищаем предыдущие результаты
        $('#result').html('');

        // Отправляем данные на сервер через AJAX запрос
        $.ajax({
            url: '/process', // URL обработчика на сервере
            method: 'POST', // Метод отправки данных
            data: formData, // Данные формы, включая параметры подключения к БД
            success: function (response) {
                // Обработка успешного получения ответа
                if (typeof response === 'object' && response.information) {
                    // Если ответ в формате JSON с информацией
                    $('#result').text(JSON.stringify(response, null, 2));
                } else if (typeof response === 'object' && response.success) {
                    // Обработка успешного сохранения данных в базе данных
                    $('#result').html(`<strong>Успех:</strong> ${response.success}`);
                } else {
                    // Обработка текстового ответа или ошибки
                    var resultHtml = '<strong>Содержание по категории:</strong><br>';
                    for (var category in response) {
                        resultHtml += `<h5>${category}:</h5><p>${response[category]}</p>`;
                    }
                    $('#result').html(resultHtml);
                }
            },
            error: function (xhr, status, error) {
                // Обработка ошибки выполнения запроса
                $('#result').html(`<strong>Ошибка:</strong> ${xhr.responseText}`);
            }
        });

        localStorage.setItem('dbHost', $('#dbHost').val());
        localStorage.setItem('dbPort', $('#dbPort').val());
        localStorage.setItem('dbName', $('#dbName').val());
        localStorage.setItem('dbUser', $('#dbUser').val());
        localStorage.setItem('dbPassword', $('#dbPassword').val());
    });


    $('.file-upload-button').on('click', function () {
        $('#fileInput').click();
    });

    $('#fileInput').on('change', function (e) {
        var files = e.target.files;
        if (!files.length) {
            return;
        }

        // Создаем массив промисов для чтения всех файлов
        var fileReaders = Array.from(files).map(function (file) {
            return new Promise((resolve) => {
                var reader = new FileReader();
                reader.onload = function (e) {
                    resolve(e.target.result); // Возвращаем содержимое файла как результат промиса
                };
                reader.readAsText(file);
            });
        });

        // Ожидаем завершения всех операций чтения
        Promise.all(fileReaders).then(contents => {
            // Собираем все содержимое, разделяя его двойными переносами строк
            var allText = contents.join("\n\n");
            // Добавляем в текстовое поле
            $('textarea[name="text"]').val(allText);
        });
    });

    $('#saveButton').on('click', function () {
        var resultText = $('#result').text(); // Получаем текстовое содержимое результата
        var blob = new Blob([resultText], {type: 'text/plain;charset=utf-8'}); // Создаем Blob из текста
        var url = URL.createObjectURL(blob); // Создаем URL для Blob
        var a = document.createElement('a'); // Создаем элемент ссылки
        a.href = url; // Устанавливаем URL в качестве адреса ссылки
        a.download = 'result.txt'; // Устанавливаем имя файла для скачивания
        document.body.appendChild(a); // Добавляем ссылку в документ
        a.click(); // Имитируем клик по ссылке для начала скачивания
        document.body.removeChild(a); // Удаляем ссылку из документа
        URL.revokeObjectURL(url); // Освобождаем URL
    });
    if (localStorage.getItem('dbHost')) $('#dbHost').val(localStorage.getItem('dbHost'));
    if (localStorage.getItem('dbPort')) $('#dbPort').val(localStorage.getItem('dbPort'));
    if (localStorage.getItem('dbName')) $('#dbName').val(localStorage.getItem('dbName'));
    if (localStorage.getItem('dbUser')) $('#dbUser').val(localStorage.getItem('dbUser'));
    if (localStorage.getItem('dbPassword')) $('#dbPassword').val(localStorage.getItem('dbPassword'));
});
