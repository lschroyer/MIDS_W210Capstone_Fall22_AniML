
// var URL = 'http://localhost:8000'
// var URL_STATUS = 'http://localhost:8000/api/status/'

// Change URL from localhost to AWS Server http://52.52.143.50:8000/
var URL = 'http://52.52.143.50:8000'
var URL_STATUS = 'http://52.52.143.50:8000/api/status/'

var results = []
var status_list = []
var res = ''

// Lucas code:
// function download(content, fileName, contentType) {
//     var a = document.createElement("a");
//     var file = new Blob([content], {type: contentType});
//     a.href = URL.createObjectURL(file);
//     a.download = fileName;
//     a.click();
// }
// end Lucas code


jQuery(document).ready(function () {
    $('#row_detail').hide()
    $("#row_results").hide();
    $('#btn-process').on('click', function () {
        var form_data = new FormData();
        files = $('#input_file').prop('files')
        for (i = 0; i < files.length; i++)
            form_data.append('files', $('#input_file').prop('files')[i]);
            // save($('#input_file').prop('files')[i], "../output_" + String(i) + ".jpg") // Lucas line

        $.ajax({
            url: URL + '/api/process',
            type: "post",
            data: form_data,
            enctype: 'multipart/form-data',
            contentType: false,
            processData: false,
            cache: false,
            beforeSend: function () {
                results = []
                status_list = []
                $("#table_result > tbody").html('');
                $('#row_detail').hide();
                $("#row_results").hide();
            },
        }).done(function (jsondata, textStatus, jqXHR) {
            for (i = 0; i < jsondata.length; i++) {
                // console.log(jsondata)
                task_id = jsondata[i]['task_id']
                status = jsondata[i]['status']
                results.push(URL + jsondata[i]['url_result'])
                // download(jsonData, jsondata[i] + '_json.txt', 'text/plain'); //Lucas code
                status_list.push(task_id)
                result_button = `<button class="btn btn-small btn-success" style="display: none" id="btn-view" data=${i}>View</a>`
                $("#table_result > tbody").append(`<tr><td>${task_id}</td><td id=${task_id}>${status}</td><td>${result_button}</td></tr>`);
                $("#row_results").show();
            }

            // Lucas test
            // https://stackoverflow.com/questions/2894946/passing-javascript-variable-to-python
            // var reply=data.reply;
            // if (reply=="success")
            // {
            //     return;
            // }
            // else
            //     {
            //     alert("some error ocured in session agent")
            //     }
            // End Lucas test


            var interval = setInterval(refresh, 1000);

            function refresh() {
                n_success = 0
                for (i = 0; i < status_list.length; i++) {
                    $.ajax({
                        url: URL_STATUS + status_list[i],
                        success: function (data) {
                            id = status_list[i]
                            status = data['status']
                            $('#' + id).html(status)
                            if ((status == 'SUCCESS') || (status == 'FAILED')) {
                                $($('#' + id).siblings()[1]).children().show()
                                n_success++
                            }
                        },
                        async: false
                    });
                }
                if (n_success == status_list.length) {
                    clearInterval(interval);
                }
            }
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $("#row_results").hide();
        });

    })

    $(document).on('click', '#btn-view', function (e) {
        id = $(e.target).attr('data')
        $.get(results[id], function (data) {
            res = data
            if (data['status'] == 'SUCCESS') {
                $('#row_detail').show()
                $('#result_txt').val(JSON.stringify(res.result['bbox'], undefined, 4))
                $('#result_img').attr('src', URL + '/' + res.result.file_name)
                $('#result_link').attr('href', URL + '/' + res.result.file_name)
            } else {
                alert('Result not ready or already consumed!')
                $('#row_detail').hide()
            }
        });
    })

            // $.post('/create_binary_file.php', res, function(retData) {
            //     $("body").append("<iframe src='" + retData.url+ "' style='display: none;' ></iframe>");
            //   });    

    $(document).on('click', '#btn-refresh', function (e) {
        for (i = 0; i < status_list.length; i++) {
            $.ajax({
                url: URL_STATUS + status_list[i],
                success: function (data) {
                    id = status_list[i]
                    status = data['status']
                    $('#' + id).html(status)
                    if (status == 'SUCCESS')
                        $($('#' + id).siblings()[1]).children().show()
                },
                async: false
            });
        }
    })

})