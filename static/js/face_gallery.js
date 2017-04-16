/**
 * Created by pxxgogo on 2017/4/15.
 */

$(document).ready(function () {
    $(".plus-img").click(function () {
        window.location.href = '/face_gallery/add_face';

    });
});


function delete_face(id) {
    swal({
            title: "Are you sure?",
            text: "Are you sure to delete this face from your face gallery?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, delete it!",
            closeOnConfirm: false
        },
        function () {
            console.log(id);
            $.ajax({
                url: '/face_gallery/ensure_deleting_face',
                data: {"face_id": id},
                dataType: "json",
                type: "POST",
                beforeSend: function () {
                    swal({
                        title: "Please wait for a moment.",
                        text: "operating...",
                        showConfirmButton: false
                    })
                },
                success: function (responseJSON) {
                    if (responseJSON['return_code'] == 0) {
                        swal("Good job!", "The face has been deleted from your face gallery.", "success");
                        window.location.href = '/face_gallery'
                    } else {
                        swal("Failure", "Something goes wrong, try later please.", "error");
                        console.log(responseJSON);
                    }
                },
                error: function (e) {
                    swal("Failure", "Something goes wrong, try later please.", "error");
                    console.log(e);
                }
            });

        });


}