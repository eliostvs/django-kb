var main = function () {

    $("a.voter").on("click", function (event) {
        var $el = $(this);

        $.get($el.attr("href"), {}, function (data) {
            $("#feedback p").html(data.response);
        });

        return false;
    });
};

if (typeof $ !== "undefined") {
    $(document).ready(main);
}
