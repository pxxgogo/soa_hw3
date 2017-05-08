/**
 * Created by pxxgogo on 2017/4/15.
 */

function generate_face_html(faces) {
    var html_str = "";
    for (var i = 0; i < faces.length; i++) {
        html_str += "<div style='display: inline-block' class='text-center'>" +
            "<img src='" + faces[i].face_data_src + "' class='face-img' id='f-" + faces[i].face_No + "' onclick='choose_face(this)'>" +
            "<div class='text-center'>" +
            "<div class='label label-primary' style='display:block;'><i class='fa fa-user'></i>" + faces[i].age + " years old</div>" +
            "<div class='label label-primary' style='display:block;'>" + faces[i].emotion + "</div>" +
            "</div>" +
            "</div>"
    }
    return html_str
}

$(document).ready(function () {
    Dropzone.options.myAwesomeDropzone = {

        autoProcessQueue: false,
        uploadMultiple: true,
        parallelUploads: 100,
        maxFiles: 1,
        maxFilesize: 10,
        paramName: "file",
        acceptedFiles: "image/*",
        url: "/face_gallery/send_face",


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
                // console.log(response.faces);
                if (response.return_code === 1) {
                    swal("Failure", "No faces can be detected.", "error");
                }
                else if (response.return_code === 2) {
                    swal("Failure", "Something about your photo goes wrong, maybe the photo size is too small or too big.", "error");
                } else if (response.return_code === 0) {
                    var faces = response.faces;
                    var html_str = "";
                    if (faces.length == 0) {
                        swal("Failure", "No faces can be detected.", "error");
                        return;
                    }
                    swal("Success", "You need choose one from the detected faces.", "success");
                    $("#collapse-link").click();
                    html_str = generate_face_html(faces);
                    $("#temp-faces-panel").html(html_str);
                    $("#temp-faces-container").show();
                }
            });
            this.on("errormultiple", function (files, response) {
                if (response.return_code === 1) {
                    swal("Failure", "No faces can be detected.", "error");
                }
                else if (response.return_code === 2) {
                    swal("Failure", "Something about your photo goes wrong, maybe the photo size is too small or too big.", "error");
                }
            });
            this.on("addedfile", function (file) {
                file.previewElement.addEventListener("click", function () {
                    myDropzone.removeFile(file);
                });
            });
        }

    };


});

function choose_face(node) {
    swal({
            title: "Are you sure?",
            text: "Are you sure to add this face to your face gallery?",
            type: "info",
            showCancelButton: true,
            confirmButtonColor: "#4f9add",
            confirmButtonText: "Yes, add it!",
            closeOnConfirm: false
        },
        function () {
            var faceID = node.id.substring(2);
            console.log(faceID);
            $.ajax({
                url: '/face_gallery/ensure_adding_face',
                data: {"face_id": faceID},
                dataType: "json",
                type: "POST",
                beforeSend: function () {
                    swal({
                        title: "Please wait for a moment.",
                        text: "operating...",
                        showConfirmButton: false
                    });
                },
                success: function (responseJSON) {
                    if (responseJSON['return_code'] == 0) {
                        swal("Success", "The face has been added to your face gallery.", "success");
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


Webcam.set({
    width: 320,
    height: 240,
    image_format: 'png',
    jpeg_quality: 100
});
function setup() {
    Webcam.reset();
    Webcam.attach('#my-camera');
    $(".dz-message").hide();
    $("#submit-photo-btn").hide();
    $("#close-camera-btn").show();
    $("#access-camera-btn").hide();
    $("#take-snap-shot-btn").show();
}

function close_camera() {
    $(".dz-message").show();
    $("#my-camera").html("");
    $("#submit-photo-btn").show();
    $("#close-camera-btn").hide();
    $("#access-camera-btn").show();
    $("#take-snap-shot-btn").hide();


}

function take_snapshot() {
    // take snapshot and get image data
    Webcam.snap(function (data_uri) {
        $.ajax({
            url: '/face_gallery/send_captured_photo',
            data: {"img_data": data_uri},
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
                if (response.return_code === 1) {
                    swal("Failure", "No faces can be detected.", "error");
                }
                else if (response.return_code === 2) {
                    swal("Failure", "Something about your photo goes wrong, maybe the photo size is too small or too big.", "error");
                } else if (response.return_code === 0) {
                    var faces = response.faces;
                    var html_str = "";
                    if (faces.length == 0) {
                        swal("Failure", "No faces can be detected.", "error");
                        return;
                    }
                    swal("Success", "You need choose one from the detected faces.", "success");
                    $("#collapse-link").click();
                    html_str = generate_face_html(faces);
                    $("#temp-faces-container").show();
                    $("#temp-faces-panel").html(html_str);
                }
            },
            error: function (e) {
                swal("Failure", "Something goes wrong, try later please.", "error");
                console.log(e);
            }
        });
    });
}

