/**
 * Created by pxxgogo on 2017/4/16.
 */


function search_press_key(node) {
    var key_code = event.keyCode;
    if(key_code != 13) {
        return;
    }
    var content = node.value;
    $.ajax({
            url: '/search_in_text',
            data: {"content": content},
            dataType: "json",
            type: "GET",
            beforeSend: function () {
                swal({
                    title: "Please wait for a moment.",
                    text: "operating...",
                    showConfirmButton: false
                })
            },
            success: function (response) {
                if(response.type == 'jump') {
                    window.location.href = response.url;
                }
                else if(response.type == 'none') {
                    swal("Sorry", "I can't understand what you said", "error");
                }
            },
            error: function (e) {
                swal("Failure", "Something goes wrong, try later please.", "error");
                console.log(e);
            }
        });
}