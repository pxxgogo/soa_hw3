/**
 * Created by pxxgogo on 2017/4/16.
 */

$(document).ready(function () {

    Dropzone.options.myAwesomeDropzone = {

        autoProcessQueue: false,
        uploadMultiple: true,
        parallelUploads: 100,
        maxFiles: 1,
        maxFilesize: 10,
        paramName: "file",
        acceptedFiles: "image/*",
        url: "/login_with_updated_photo",


        // Dropzone settings
        init: function () {
            var myDropzone = this;

            this.element.querySelector("button[type=submit]").addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                myDropzone.processQueue();
            });
            this.on("sendingmultiple", function () {
                swal({
                    title: "Please wait for a moment.",
                    text: "operating...",
                    showConfirmButton: false
                })
            });
            this.on("successmultiple", function (files, response) {
                if (response['return_code'] == 0) {
                    window.location.href = '/';
                }
                if (response['return_code'] == 3) {
                    swal("Failure", "The face in the photo can't pass the verification.", "error");
                }
                if (response['return_code'] == 1) {
                    swal("Failure", "Please retry later.", "error");
                }
                if (response['return_code'] == 2) {
                    swal("Failure", "No faces can be detected.", "error");
                }
            });
            this.on("errormultiple", function (files, response) {
                swal("Failure", "Please retry later.", "error");
            });
            this.on("addedfile", function (file) {
                file.previewElement.addEventListener("click", function () {
                    myDropzone.removeFile(file);
                });
            });
        }

    };
});

Webcam.set({
    width: 320,
    height: 240,
    image_format: 'jpeg',
    jpeg_quality: 90
});
function setup() {
    Webcam.reset();
    Webcam.attach('#my-camera');

}

function take_snapshot() {
    // take snapshot and get image data
    Webcam.snap(function (data_uri) {
        var username = $("#username-log-in-captured-photo").val();
        $.ajax({
            url: '/login_with_captured_photo',
            data: {"img_data": data_uri, 'username': username},
            dataType: "json",
            type: "POST",
            beforeSend: function () {
                swal({
                    title: "Please wait for a moment.",
                    text: "operating...",
                    showConfirmButton: false
                })
            },
            success: function (response) {
                if (response['return_code'] == 0) {
                    window.location.href = '/';
                }
                if (response['return_code'] == 3) {
                    swal("Failure", "The face in the photo can't pass the verification.", "error");
                }
                if (response['return_code'] == 1) {
                    swal("Failure", "Please retry later.", "error");
                }
                if (response['return_code'] == 2) {
                    swal("Failure", "No faces can be detected.", "error");
                }
            },
            error: function (e) {
                swal("Failure", "Please retry later.", "error");
                console.log(e);
            }
        });
    });
}

