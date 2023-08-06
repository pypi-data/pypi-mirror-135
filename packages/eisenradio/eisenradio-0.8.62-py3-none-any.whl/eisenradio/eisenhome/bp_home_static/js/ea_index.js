
$(document).ready(function () {

    cookieStuff();
    // setInterval(analyser_raw_data, 2500);
    setInterval(delete_info, 2500);
    setInterval(meta_info, 5004);
    setInterval(toggle_show_select_box, 5003);
    setInterval(updateMasterprogress, 5002);
    setInterval(updateDisplay, 5001);
    var audio = document.getElementById("audio_with_controls");
    audio.volume = 0.25;
    // audio.muted = true;
    var audio_volume_control = document.getElementById("audio_volume_controller");
    audio_volume_control.addEventListener("input", setAudioVolume);

    function setAudioVolume() {
        audio.volume = audio_volume_control.value / 100;
    }
    ;

    $("button").click(function () {

        if ($(this).attr("class") === "navbar-toggle collapsed") {

            return;
        }
        ;

        let clicked = $(this).attr("name");
        console.log("send name " + clicked);
        let class_val = $(this).attr("class");  /* variable does not survive the request, this is nice */
        console.log("send button " + class_val);
        let id = $(this).attr("id");
        let dict = {
            'name': clicked,
            'class_val': class_val, /* pass it to server and get it back*/
            'button_id': id

        };
        req = $.ajax({
            type: 'POST',
            dataType: "json",
            url: "/",
            data: dict
        });
        $('#' + id).fadeOut(1).fadeIn(3);

        req.done(function (data) {

            if (data.class_val === "btn btn-primary") {
                $('#' + id).removeClass("btn btn-primary");
                $('#' + id).addClass("btn btn-danger");
            }
            ;

            if (data.class_val === "btn btn-danger") {
                $('#' + id).removeClass("btn btn-danger");
                $('#' + id).addClass("btn btn-primary");
            }
            ;

            if (data.streamer) {
                /* Del all streamer, push current in combo box */
                cookie_set_streamer();
                $('#cacheList').find('option:not(:first)').remove();
                let streamer = data.streamer.split(",");

                $.each(streamer, function (idx, val) {

                    let stream = val;
                    if (stream.length !== 0) {
                        stream = val.split("=");
                        let table_id = stream[1];
                        let title = stream[0];
                        cacheListFeed(table_id, title);

                        if (data.streamer === 'empty_json') {
                            $('#cacheList').find('option:not(:first)').remove();
                            document.getElementById('cacheList').style.color = "#696969";
                            document.getElementById('cacheList').style.textColor = "#696969";
                            cookie_del_streamer();
                        }
                        console.log('data.streamer ' + data.streamer);

                    }

                });    /*each*/

            }
            ;

            if (data.radio_table_id) {

            }
            ;

            /* current play station */

            if (data.table_ident) {

                let current_station = data.table_ident;
                console.log('table_ident ' + current_station);

                if (current_station !== 'Null') {

                    cookie_set_station(current_station, id);

                    document.getElementById('lbl_div_audio').innerText = " ► " + current_station; /*current_station.substring(0, 20)*/
                    document.getElementById('lbl_div_audio').style.cursor = "pointer";
                    document.getElementById('lbl_div_audio').style.cursor = "hand";
                    $("#lbl_div_audio").on('click', function () {
                        document.getElementById('dot_' + id).scrollIntoView({ behavior: "smooth" });
                    });

                }
                if (data.former_button_to_switch) {
                    let num = data.former_button_to_switch;
                    console.log('auto_click former_button_to_switch: ' + num);
                    $("#" + num).click();
                }
                ;
            }
            ;

            if (data.result === 'deactivate_audio') {
                console.log('deactivate_audio');

                audio_control = 'audio_with_controls';
                myAudio = document.getElementById(audio_control);
                myAudio.pause();
                myAudio.src = "";
                myAudio.load();
                document.getElementById('lbl_div_audio').innerText = '';
                cookie_del_station();

            }
            ;

            if (data.result === 'activate_audio') {
                console.log('activate_audio');

                url = data.query_url;
                console.log(url);
                audio_control = 'audio_with_controls';
                myAudio = document.getElementById(audio_control);
                myAudio.pause();
                myAudio.src = "";
                // myAudio.load()

                myAudio.src = url;
                myAudio.volume = 0.25;
                myAudio.load();
                myAudio.play = true;

                // myAudio.muted  = true;
            }
            ;

        });


    });

    function updateDisplay() {
        var req;

        req = $.ajax({
            type: 'GET',
            url: "/display_info",
            cache: false
        });

        req.done(function (data) {
            var displays = '';
            var display = '';
            var table_id = '';
            var title = '';

            displays = data.result.split(",");

            $.each(displays, function (idx, val) {
                display = val;

                if (display.length !== 0) {

                    display = val.split("=");
                    table_id = display[0];
                    title = display[1];
                    if (title !== 'Null') {
                        $('#Display_' + table_id).attr("value", title);
                    }
                    if (title === 'Null') {
                        $('#Display_' + table_id).attr("value", '');
                    }
                    // console.log(title)

                }

            });

        });


    }
    ;

    function updateMasterprogress() {
        var req;

        req = $.ajax({
            type: 'POST',
            url: "/index_posts_percent",
            cache: false,
            data: { 'percent': 'percent' }
        });

        req.done(function (data) {
            var percent = '';

            percent = data.result;
            // console.log('########### '+percent+' #########');
            if (percent === 0) {
                $('.progress-bar').css('width', 25 + '%').attr('aria-valuenow', 25).html('Timer Off');
            }
            if (percent !== 0) {
                $('.progress-bar').css('width', percent + '%').attr('aria-valuenow', percent).html('Run, Forrest! RUN!');
                if (percent >= 100) {
                    window.location.href = "/page_flash";
                }
            }

        });


    }
    ;

});


function setDarkmode() {
    let req;

    req = $.ajax({
        type: 'POST',
        url: "/setcookiedark",
        cache: false
    });

}
;

function delDarkmode() {
    let req;

    req = $.ajax({
        type: 'POST',
        url: "/delcookiedark",
        cache: false
    });

}
;

function getDarkmode() {
    let req;

    req = $.ajax({
        type: 'GET',
        url: "/getcookiedark",
        cache: false
    });

    req.done(function (data) {
        let dark = '';

        dark = data.darkmode;
        if (dark === 'darkmode') {
            setColor('cookie_request_on_load_is_dark');
        }


    });

}
;

function cookie_set_station(station, station_id) {
    let req;

    req = $.ajax({
        type: 'POST',
        url: "/cookie_set_station",
        cache: false,
        dataType: "json",
        data: { 'station': station, 'station_id': station_id }
    });
}
;

function cookie_get_station() {
    let req;

    req = $.ajax({
        type: 'GET',
        url: "/cookie_get_station",
        cache: false
    });

    req.done(function (data) {
        let play_station = '';
        if (data.play_station !== null) {
            if (data.play_station !== ',') {
                play_station = data.play_station.split(",");
                let station = play_station[0];
                let station_id = play_station[1];

                document.getElementById('lbl_div_audio').innerText = " ► " + station; /*station.substring(0, 20)*/
                /* set from static in page to dynamic, strange! but works fire and chrome*/
                document.getElementById('lbl_div_audio').setAttribute("id", "lbl_div_audio");

                document.getElementById('lbl_div_audio').style.cursor = "pointer";
                document.getElementById('lbl_div_audio').style.cursor = "hand";
                $("#lbl_div_audio").on('click', function () {
                    document.getElementById('dot_' + station_id).scrollIntoView({ behavior: "smooth" });
                });
            }/* if */
        }

    });

}
;

function cookie_del_station() {
    let req;

    req = $.ajax({
        type: 'POST',
        url: "/cookie_del_station",
        cache: false
    });

}
;

function cookie_set_streamer() {
    let req;

    req = $.ajax({
        type: 'POST',
        url: "/cookie_set_streamer",
        cache: false
    });
}
;

function cookie_del_streamer() {
    let req;
    req = $.ajax({
        type: 'POST',
        url: "/cookie_del_streamer",
        cache: false
    });
}
;

function toggle_show_select_box() {
    if (document.getElementById('cacheList').style.color !== "rgb(219, 111, 52)") {
        document.getElementById("cacheList").style.display = "none";
    }
    if (document.getElementById('cacheList').style.color === "rgb(219, 111, 52)") {
        document.getElementById("cacheList").style.display = "block";
    }
}
;

function cookie_get_streamer() {
    let req;

    req = $.ajax({
        type: 'GET',
        url: "/cookie_get_streamer",
        cache: false,
    });

    req.done(function (data) {

        if (data.str_streamer) {
            $('#cacheList').find('option:not(:first)').remove();

            let streamer = data.str_streamer.split(",");

            $.each(streamer, function (idx, val) {
                let stream = val;

                if (stream.length !== 0) {
                    if (data.str_streamer === 'empty_json') {

                        $('#cacheList').find('option:not(:first)').remove();
                        cookie_del_streamer();
                        return;
                    }
                    stream = val.split("=");
                    let table_id = stream[1];
                    let title = stream[0];
                    cacheListFeed(table_id, title);
                }

            });

        }
        ; /*if (data.streamer)*/

    });  /*req.done*/

}
;  /*function cookie_get_streamer*/
function setTimer(val) {

    $.ajax({
        type: 'POST',
        url: "/index_posts_combo",
        cache: false,
        data: { 'time_record_select_all': val }

    });
}
;

function setColor(val) {
    let req;
    var color;
    if (val === 'cookie_request_on_load_is_dark') {
        color = 'black'
    }
    if (val === 'view') {
        color = 'white'
    }

    req = $.ajax({
        type: 'GET',
        url: "/getcookiedark",
        cache: false
    });
    req.done(function (data) {
        let dark = '';

        dark = data.darkmode;
        if (dark !== 'darkmode') {
            color = 'black';
        }

        var bodyStyles = document.body.style;
        if (color === 'black') {
            bodyStyles.setProperty('--background-color', 'rgba(26,26,26,1)');
            bodyStyles.setProperty('--form-background', '#333333');
            bodyStyles.setProperty('--form-text', '#f1f1f1');
            bodyStyles.setProperty('--hr-color', '#777777');
            bodyStyles.setProperty('--border-color', '#202020');
            bodyStyles.setProperty('--text-color', '#bbbbbb');
            bodyStyles.setProperty('--form-edit', '#333333');
            bodyStyles.setProperty('--opacity', '0.5');
            bodyStyles.setProperty('--btn-opacity', '0.75');
            bodyStyles.setProperty('--footer-color', 'rgba(26,26,26,0.90)');
            bodyStyles.setProperty('--main-display-arrow', '#34A0DB');
            bodyStyles.setProperty('--dot-for-radio-headline', '#E74C3C');
            bodyStyles.setProperty('--lbl-div-audio', '#db6f34');
            bodyStyles.setProperty('--ghetto-measurements-bottom-color', '#FCA841');
            bodyStyles.setProperty('--radio-station-headline', '#4195fc');
            bodyStyles.setProperty('--controls-background', 'rgba(26,26,26,1)');

            setDarkmode();
        }
        if (color === 'white') {
            bodyStyles.setProperty('--background-color', '#ccc');
            bodyStyles.setProperty('--form-background', '#ddd');
            bodyStyles.setProperty('--form-text', '#565454');
            bodyStyles.setProperty('--hr-color', '#eee');
            bodyStyles.setProperty('--border-color', '#eee');
            bodyStyles.setProperty('--text-color', '#f0f0f0');
            bodyStyles.setProperty('--form-edit', '#777777');
            bodyStyles.setProperty('--opacity', '1');
            bodyStyles.setProperty('--btn-opacity', '1');
            bodyStyles.setProperty('--footer-color', 'rgba(0,63,92,0.90)');
            bodyStyles.setProperty('--main-display-arrow', '#bc5090');
            bodyStyles.setProperty('--dot-for-radio-headline', '#565454');
            bodyStyles.setProperty('--lbl-div-audio', '#FCA841');
            bodyStyles.setProperty('--ghetto-measurements-bottom-color', '#d441fc');
            bodyStyles.setProperty('--radio-station-headline', '#565454');
            bodyStyles.setProperty('--controls-background', '#565454');


            delDarkmode();
        }
    });
}
;


function cookieStuff() {
    getDarkmode();

    cookie_set_streamer();
    cookie_get_streamer();
    cookie_set_station();
    cookie_get_station();

}
;

function meta_info() {

    let req = $.ajax({
        type: 'GET',
        url: "/cache_info",
        cache: false
    });

    req.done(function (data) {
        if (data.cache_result !== "-empty-") {
            let dict_io_lists = data.cache_result
            $.each(dict_io_lists, function (idx, val) {

                let response_time = val[0];
                let suffix = val[1];
                let genre = val[2];
                let station_name = val[3];
                let station_id = val[4];
                let bit_rate = val[5];

                document.getElementById('request_time_' + station_id).innerText = "" + response_time + " ms";
                document.getElementById('request_suffix_' + station_id).innerText = "" + suffix;
                document.getElementById('request_icy_br_' + station_id).innerText = "" + bit_rate + " kB/s";
                document.getElementById('icy_name_' + station_id).innerText = "" + station_name;
                document.getElementById('request_icy_genre_' + station_id).innerText = "" + genre;
            });
        }   /*data.cache_result !== ""*/
    });
}
;

function delete_info() {

    let req = $.ajax({
        type: 'GET',
        url: "/delete_info",
        cache: false
    });

    req.done(function (data) {

        if (data.stopped_result !== "-empty-") {
            let stopped_list = data.stopped_result;

            $.each(stopped_list, function (idx, val) {

                let station_id = val;
                document.getElementById('request_time_' + station_id).innerText = "";
                document.getElementById('request_suffix_' + station_id).innerText = "";
                document.getElementById('request_icy_br_' + station_id).innerText = "";
                document.getElementById('icy_name_' + station_id).innerText = "";
                document.getElementById('request_icy_genre_' + station_id).innerText = "";

            });/**/
        }
    });
}
;

function cacheListFeed(table_id, title) {

    if (title !== 'Null') {

        let cacheList = document.getElementById('cacheList');
        cacheList.style.color = "#db6f34";
        cacheList.style.textColor = "#db6f34";

        let opt = document.createElement('option');
        opt.id = 'opt_' + table_id;
        opt.value = '#dot_' + table_id;
        opt.innerHTML = title;
        cacheList.appendChild(opt);
    }
}
;
/*
const prime_button = document.querySelectorAll('.btn-primary');
prime_button.forEach(btn => btn.addEventListener('click',showId));
function showId(e){
  console.log("Using this:", this.dataset.id);
  console.log("Using e.currentTarget:", e.currentTarget.dataset.id);
  e.target.style.visibility = 'hidden';
}
*/


/* Here graphical analyser stuff */
//const prime_button_is_blue = document.querySelectorAll('.btn-primary');
// btn event continues if other buttons are clicked, attach a break for autoclicker
//prime_button_is_blue.forEach(btn => btn.addEventListener('click',getId, false));  // ,false remove must match true/false
function getId(e) {
    if (e.currentTarget.getAttribute('class') === "btn btn-danger") {
        console.log("---> return from autoclick or btn pressed to stop, table_id: ");
        return;
    }
    //console.log("Using this:", this.dataset.id);
    //console.log("Using e.currentTarget:", e.currentTarget.dataset.id + " " + e.currentTarget.getAttribute('class'));
    let radio_id = e.currentTarget.dataset.id
    analyser_raw_data(radio_id);
    // caution - analyser_raw_data runs in timer loop !!!
};

function analyser_raw_data(id_str) {
    var context;
    var soundSource;
    var soundBuffer;

    // Step 1 - Initialise the Audio Context
    // There can be only one!

    function init() {
        if (typeof AudioContext !== "undefined") {
            context = new AudioContext();
        } else if (typeof webkitAudioContext !== "undefined") {
            context = new webkitAudioContext();
        } else {
            throw new Error('AudioContext not supported.');
        }
    }

    id_str = 'listen,4';
    return new Promise((resolve, reject) => {
        let str_list = id_str.split(",");
        var table_id = str_list[1];

        let req = $.ajax({
            type: 'POST',
            dataType: 'text',   // need some content header back and fore!
            url: "/analyser",
            cache: false,
            data: { 'table_id': table_id },

            success: function (data) {
                // mp3 as base64 string from server
                resolve(data);
                if (data === '-empty-') {
                    console.log('-->data -empty-:' + data);
                }

                // console.log("### end ### resolve:" + );

                var audioContext = new AudioContext();
                let audio1 = new Audio("data:audio/x-wav;base64," + data);
                audio1.volume = 0.1;
                audio1.play();

                let audioSource = audioContext.createMediaElementSource(audio1)
                // var source = audioContext.createBufferSource();
                const canvas = document.getElementById("canvas1");
                var canvas_ctx = canvas.getContext('2d');
                let analyser = audioContext.createAnalyser();

                audioSource.connect(analyser);
                // analyser.connect(audioContext.destination);
                audioSource.connect(audioContext.destination);

                analyser.fftSize = 256;
                const bufferLength = analyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);

                const barWidth = canvas.width / bufferLength;
                let barHeight;
                let x = 0;


                function animate() {
                    requestAnimationFrame(animate);
                    x = 0;
                    canvas_ctx.clearRect(0, 0, canvas.width, canvas.height);
                    analyser.getByteFrequencyData(dataArray);
                    for (let i = 0; i < bufferLength; i++) {
                        barHeight = dataArray[i] / 2;
                        canvas_ctx.fillStyle = 'white';
                        canvas_ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
                        x += barWidth;
                    }


                }

                animate();

            },
            error: function (error) {
                reject(error);
                //console.log("## analyser_raw_data # end ### ERROR:" + error);
                // return '-Fail-'
            },

        });

    });
    // };



};

// Convert base64 string to ArrayBuffer
function _base64ToArrayBuffer(base64) {
    var binary_string = window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}
;
