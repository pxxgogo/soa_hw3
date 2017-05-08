/**
 * Created by pxxgogo on 2017/4/16.
 */


function search_press_key(node) {
    var key_code = event.keyCode;
    if (key_code != 13) {
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
            if (response.type == 'jump') {
                window.location.href = response.url;
            }
            else if (response.type == 'none') {
                swal("Sorry", "I can't understand what you said", "error");
            }
        },
        error: function (e) {
            swal("Failure", "Something goes wrong, try later please.", "error");
            console.log(e);
        }
    });
}

function __log(e, data) {
    console.log(e + " " + (data || ''));
}

var audio_context;
var recorder;
var record_start_flag = false;

function start_user_media(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    __log('Media stream created.');

    // Uncomment if you want the audio to feedback directly
    //input.connect(audio_context.destination);
    //__log('Input connected to audio context destination.');

    recorder = new Recorder(input);
    __log('Recorder initialised.');
}

function recording(button) {
    if (record_start_flag) {
        recorder && recorder.stop();
        __log('Stopped recording.');
        send_to_server();
        $("#recording-btn").attr('class', 'minimalize-styl-2 btn btn-success');
        recorder.clear();
        record_start_flag = false;
    } else {
        recorder && recorder.record();
        __log('Recording...');
        record_start_flag = true;
        $("#recording-btn").attr('class', 'minimalize-styl-2 btn btn-danger');

    }
}

function send_to_server() {
    recorder && recorder.exportWAV(function (blob) {
        var fd = new FormData();
        fd.append('voice', 'voice.wav');
        fd.append('data', blob);
        $.ajax({
            type: 'POST',
            url: '/search_with_voice',
            data: fd,
            processData: false,
            contentType: false,
            beforeSend: function () {
                swal({
                    title: "Please wait for a moment.",
                    text: "operating...",
                    showConfirmButton: false
                })
            },
            success: function (response) {
                if (response.type == 'jump') {
                    window.location.href = response.url;
                }
                else if (response.type == 'none') {
                    swal("Sorry", "I can't understand what you said", "error");
                }
            },
            error: function (e) {
                swal("Failure", "Something goes wrong, try later please.", "error");
                console.log(e);
            }
        });
    });
}

window.onload = function init() {
    try {
        // webkit shim
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
        window.URL = window.URL || window.webkitURL;

        audio_context = new AudioContext;
        __log('Audio context set up.');
        __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
        alert('No web audio support in this browser!');
    }

    navigator.getUserMedia({audio: true}, start_user_media, function (e) {
        __log('No live audio input: ' + e);
    });
};