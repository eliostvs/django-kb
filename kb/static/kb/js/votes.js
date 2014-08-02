if (typeof $ != 'undefined'){

    $(document).ready(function(){

        $(document).on('click', 'a.voter', function(event){
            event.preventDefault();
            var el = $(this);
            var replace_target = $('#votes p');
            $.get(el.attr('href'), {}, function(data){
                replace_target.html(data.response);
            });
        });

    });

}
