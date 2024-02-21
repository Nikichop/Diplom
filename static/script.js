$(document).ready(function () {
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
        e.preventDefault();
        var formData = $(this).serialize() + '&apiChoice=' + encodeURIComponent($('#apiChoice').val());
        formData += '&responseFormat=' + encodeURIComponent($('#responseFormat').val()); // Добавленный параметр формата ответа
        $('#result').html('');
        $.ajax({
            url: '/process',
            method: 'post',
            data: formData,
            success: function (response) {
                if (typeof response === 'object' && response.information) { // Проверка на формат JSON
                    $('#result').text(JSON.stringify(response, null, 2)); // Вывод JSON в текстовом формате
                } else {
                    var resultHtml = '<strong>Содержание по категории:</strong><br>';
                    for (var category in response) {
                        resultHtml += `<h5>${category}:</h5><p>${response[category]}</p>`;
                    }
                    $('#result').html(resultHtml);
                }
            },
            error: function (xhr, status, error) {
                $('#result').html(`<strong>Ошибка:</strong> ${xhr.responseText}`);
            }
        });
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

});
