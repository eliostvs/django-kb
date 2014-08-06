var main = function () {

    $(document).on('click', 'a.voter', function (event) {
        event.preventDefault();

        var $el = $(this);

        $.get($el.attr('href'), {}, function (data) {
            $('#feedback p').html(data.response);
        });

    });

};

if (typeof $ != 'undefined') {
    $(document).ready(main);
}
