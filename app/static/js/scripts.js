$(".btn.btn-danger").click(function () {
    $("#delete_modal").modal('toggle');
});



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