var $ = jQuery.noConflict();

$.sendPost = function (location, args) {
    // отправляет POST запрос на адрес location с данными из args
    var form = $('<form></form>');
    form.attr("method", "post");
    form.attr("action", location);
    $.each(args, function (key, value) {
        var field = $('<input></input>');
        field.attr("type", "hidden");
        field.attr("name", key);
        field.attr("value", value);
        form.append(field);
    });
    $(form).appendTo('body').submit();
};

$.urlParamsDecode = function (url) {
    // анализирует url на наличие параметров и возвращает их в виде массива
    let params = {};
    let match,
        pl = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) {
            return decodeURIComponent(s.replace(pl, " "));
        },
        query = url.substring(1);
    while (match = search.exec(query)) {
        params[match[1]] = match[2];
    }
    return params;
};

// ============================= Cобытия, для html эдементов страницы view.html ===================================
(function ($) {

    $('#confirm-delete').on('show.bs.modal', function (e) {
        // После отображения модального окна
        // 1. Записать кнопке удаления ссылку, которую нужно послать серверу
        $(this).find('#btn-delete-feedback').attr('data-href', $(e.relatedTarget).data('href'));
        // 2. Показать номер записи, которую мы хоти удалить, для визуальности
        $(this).find('#feedback-id-for-delete').html($(e.relatedTarget).data('id'));
    });

    $('#btn-delete-feedback').on('click', function (e) {
        // При нажатии кнопки в модельном окне - подтверждение действия по удалению отзыва
        let url = document.createElement('a');
        url.href = $(this).data('href');
        let params = $.urlParamsDecode(url.search);
        $.sendPost(url.pathname, params);
        $('#confirm-delete').modal('hide');
    });


})(jQuery);