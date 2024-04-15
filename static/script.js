$(document).ready(function () {

    $('.toggle-button').click(function () {
        var container = $(this).closest('.side-container');

        // Переключаем текст кнопки
        if (container.hasClass('collapsed')) {
            $(this).text('-');
            container.height(10).removeClass('collapsed');
            container.animate({
                height: 730
            }, 700);
        } else {
            $(this).text('+');
            var fullHeight = container.prop('scrollHeight');
            container.height(fullHeight).addClass('collapsed');
            setTimeout(function () {
                if (container.hasClass('collapsed')) {
                    container.height(0);
                }
            }, 700);
        }
    });


    $('#maxTokensRange').on('input', function () {
        $('#maxTokensValue').text($(this).val());
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

    function updateSubmitButtonState() {
        var isTextFilled = $('textarea[name="text"]').val().trim().length > 0;
        var isCategoryFilled = $('input[name="category"]').val().trim().length > 0;
        var isApiKeyFilled = $('#apiKey').val().trim().length > 0;
        var isFormReady = isTextFilled && isCategoryFilled && isApiKeyFilled;
        $('button[type="submit"]').prop('disabled', !isFormReady);
    }

    // Проверяем состояние кнопки при загрузке страницы
    updateSubmitButtonState();

    // Обновляем состояние кнопки при изменении любого из полей
    $('textarea[name="text"], input[name="category"], #apiKey').on('input', function () {
        updateSubmitButtonState();
    });

    $('#textForm').on('submit', function (e) {
        e.preventDefault();
        var formData = $(this).serialize() + '&apiChoice=' + encodeURIComponent($('#apiChoice').val());
        formData += '&responseFormat=' + encodeURIComponent($('#responseFormat').val());
        formData += '&modelChoice=' + encodeURIComponent($('#modelChoice').val());
        formData += '&max_tokens=' + encodeURIComponent($('#maxTokensRange').val());
        formData += '&apiKey=' + encodeURIComponent($('#apiKey').val());
        console.log('Отправляемые данные формы:', formData);

        $('#result').html('');

        $.ajax({
            url: '/process',
            method: 'POST',
            data: formData,
            success: function (response) {
                if (typeof response === 'object' && response.information) {
                    $('#result').text(JSON.stringify(response, null, 2));
                } else if (typeof response === 'object' && response.sql_queries) {
                    var resultHtml = `<strong>Итоговый запрос с новыми данными:</strong><br><br>`;
                    resultHtml += `<pre>${response.sql_queries}</pre>`;
                    $('#result').html(resultHtml);
                } else {
                    var resultHtml = '<strong></strong><br>';
                    for (var category in response) {
                        resultHtml += `<h5>${category}</h5><p>${response[category]}</p>`;
                    }
                    $('#result').html(resultHtml);
                }
            },
            error: function (xhr, status, error) {
                $('#result').html(`<strong>Ошибка:</strong> ${xhr.responseText}`);
            }
        });
    });

    var apiModels = {
        'chatgpt': ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo'],
        'gigachat': ['GigaChat', 'GigaChat-Plus', 'GigaChat-Pro']
    };

// Функция для обновления списка моделей
    function updateModelChoices() {
        var apiChoice = $('#apiChoice').val();
        var models = apiModels[apiChoice] || [];
        var modelChoice = $('#modelChoice');
        modelChoice.empty(); // Очистить текущие опции
        models.forEach(function (model) {
            modelChoice.append(new Option(model, model));
        });

    }

    updateModelChoices();

    $('#apiChoice').change(updateModelChoices);


    $('.file-upload-button').on('click', function () {
        $('#fileInput').click();
    });

    $('#fileInput').on('change', function (e) {
        var files = e.target.files;
        if (!files.length) {
            return;
        }

        var fileReaders = Array.from(files).map(function (file) {
            return new Promise((resolve) => {
                var reader = new FileReader();
                reader.onload = function (e) {
                    resolve(e.target.result);
                };
                reader.readAsText(file);
            });
        });

        Promise.all(fileReaders).then(contents => {
            var allText = contents.join("\n\n");
            $('textarea[name="text"]').val(allText);
        });
    });


    $('#saveButton').on('click', function () {
        var resultText = $('#result').text();
        var responseFormat = $('#responseFormat').val();
        var fileName, fileType;

        if (responseFormat === 'sql') {
            resultText = resultText.replace('Итоговый запрос с новыми данными:', '').trim();
            fileName = 'result.sql';
            fileType = 'text/plain;charset=utf-8';
        } else if (responseFormat === 'json') {
            fileName = 'result.json';
            fileType = 'application/json;charset=utf-8';
        } else {
            fileName = 'result.txt';
            fileType = 'text/plain;charset=utf-8';
        }

        var blob = new Blob([resultText], {type: fileType});
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});
