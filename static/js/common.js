$(function () {
    $('.model-title').click(function () {
        var id = $(this).data("id");

        $('.model-detail-' + id).toggle();
        console.log(id);

    });
    $('.brands a').each(function () {
        var location = window.location.href;
        var link = this.href;
        if (location == link) {
            $(this).addClass('active');
        }
    });

});
