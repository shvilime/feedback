var $ = jQuery.noConflict();

// ================================= Cобытия для html эдементов  =====================================
(function ($) {

    $(document).ready(function (e) {
        $('#region').empty().append('<option>Выберите...</option>');
        $.ajax({
            url: '/listregion',
            dataType: 'json',
            type: 'GET',
            success: function (json) {
                for (i in json) {
                    $("#region").append("<option value=" + json[i][0] + ">" + json[i][1] + "</option>");
                }
            },
            error: function (x, e) {
                console.log(e);
            }
        });
    });

    $('#region').on('change', function (e) {
        let regionid = $('#region').val();
        $('#city').empty().append('<option>Выберите...</option>');
        $.ajax({
            url: '/listcity',
            dataType: 'json',
            type: 'GET',
            data: {region: regionid},
            success: function (json) {
                for (i in json) {
                    $("#city").append("<option value=" + json[i][0] + ">" + json[i][2] + "</option>");
                }
            },
            error: function (x, e) {
                console.log(e);
            }
        });
    });


    $('#feedback_submit').on('click', function (e) {
        validateForm();
    });

    validateForm = function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    };


})(jQuery);