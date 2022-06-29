$(".btn.btn-warning").click(function() {
    $("#update_modal").modal('toggle');
});

$(document).ready(function() {
    $("#update_modal").modal('show');
})

/*$(document).ready(function() {
    $('form').on('submit', function(event) {
    
        $.ajax({
            data:$("#invoice-id").val(),
            type: 'POST',
            url: '/delete'
        });

        event.preventDefault();
    });
});*/