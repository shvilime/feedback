var $ = jQuery.noConflict();

$.redirectPost = function (location, args) {
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

// ================================= Cобытия для html эдементов  =====================================
(function ($) {

    $('#confirm-delete').on('show.bs.modal', function (e) {
        $(this).find('#btn-delete-feedback').attr('data-href', $(e.relatedTarget).data('href'));
    });

    $('#btn-delete-feedback').on('click', function (e) {
        let url = document.createElement('a');
        url.href = $(this).data('href');
        let params = $.urlParamsDecode(url.search);
        $.redirectPost(url.pathname, params);
        $('#confirm-delete').modal('hide');
    });


})(jQuery);