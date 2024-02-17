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
        $('#result').html('');
        $.ajax({
            url: '/process',
            method: 'post',
            data: formData,
            success: function (response) {
                var resultHtml = '<strong>Содержание по категории:</strong><br>';
                for (var category in response) {
                    resultHtml += `<h5>${category}:</h5><p>${response[category]}</p>`;
                }
                $('#result').html(resultHtml);
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
});
