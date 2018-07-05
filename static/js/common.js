$(function () {
    $('.model-title').click(function () {
        var id = $(this).data("id");

        $('.model-detail-' + id).toggle();
        console.log(id);

    });


});
