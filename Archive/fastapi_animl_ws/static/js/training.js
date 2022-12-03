
// var URL = 'http://localhost:8000'
// var URL_STATUS = 'http://localhost:8000/api/status/'

// Change URL from localhost to AWS Server http://52.52.143.50:8000/
// var URL = 'http://52.52.143.50:8000'
// var URL_STATUS = 'http://52.52.143.50:8000/api/status/'

var URL = 'http://13.56.94.163:9000/'
var URL_STATUS = 'http://13.56.94.163:9000/universities/task/'

// Ivan test 
// var url = "http://13.56.94.163:9000/universities/training_async";

var results = []
var status_list = []
var res = ''

// Ivan set form data form data 
var form_data = `{
    "jobs": [
        "job1"
    ]
    }`;

jQuery(document).ready(function () {
    $('#row_detail').hide()
    $("#row_results").hide();
    $('#btn-training').on('click', function () {
        // var form_data = new FormData();
        // files = $('#input_file').prop('files')
        // for (i = 0; i < files.length; i++)
        //     form_data.append('files', $('#input_file').prop('files')[i]);
        $.ajax({
            url: URL + 'universities/training_async',
            type: "post",
            data: form_data,
            enctype: 'multipart/form-data',
            // contentType: false,
            contentType: "application/json",
            // accepts: "application/json",
            processData: false,
            cache: false,
            beforeSend: function () {
                results = []
                status_list = []
                $("#table_result > tbody").html('');
                $('#row_detail').hide();
                $("#row_results").hide();
            },
        }).done(function (data, jsondata, textStatus, jqXHR) {
            console.log("Ivan is here before the for loop...")
            console.log("data",data)
            console.log("data.task_id",data.task_id)
            console.log("data.status",textStatus.status)
            console.log("data.statusText",textStatus.statusText)
            // console.log("jsondata.length". jsondata)
            console.log("textStatus", textStatus)
            // console.log("jqXHR". jqXHR)
            task_id = data.task_id
            console.log("task_id", task_id)
            status = textStatus.status
            console.log("status", status)
            status = textStatus.statusText
            console.log("statusText", status)
            result_button = `<button class="btn btn-small btn-success" style="display: none" id="btn-view-training" data='1'>View</a>`
            $("#table_result > tbody").append(`<tr><td>${task_id}</td><td id=${task_id}>${status}</td><td>${result_button}</td></tr>`);
            $("#row_results").show();


            var interval = setInterval(refresh_training, 1000);

            function refresh_training() {
                n_success = 0
                $.ajax({
                    url: URL_STATUS + task_id,
                    success: function (data) {
                        id = task_id
                        status = data['task_status']
                        console.log("status =", status)
                        $('#' + id).html(status)
                        if ((status == 'SUCCESS') || (status == 'FAILED')) {
                            $($('#' + id).siblings()[1]).children().show()
                            n_success++
                            console.log("I am here n_success= ", n_success)
                        }
                    },
                    async: false
                });


                if (n_success > 0) {
                    clearInterval(interval);
                }

                // if (n_success == status_list.length) {
                //     clearInterval(interval);
                // }
            }
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $("#row_results").hide();
        });

    })

    $(document).on('click', '#btn-view-training', function (e) {
        id = $(e.target).attr('data')
        console.log("id = ", id)
        console.log("task_id = ", task_id)
        // $.get(results[id], function (data) {

        $.ajax({
            url: URL_STATUS + task_id,
            success: function (data) {
                res = data
                if (data['task_status'] == 'SUCCESS') {
                    console.log("job data = ", data['task_result'] )
                    console.log("job data = ", data['task_result'].weights)
                    $('#row_detail').show()
                    $('#result_txt').val("weights = " + data['task_result'].weights + "\n" + "epochs = " + data['task_result'].epochs + "\n" + " save_dir = " + data['task_result'].save_dir, undefined, 4)
                } else {
                    alert('Result not ready or already consumed!')
                    $('#row_detail').hide()
                }
            },
            async: false
        });

    })


    $(document).on('click', '#btn-refresh-training', function (e) {
        for (i = 0; i < status_list.length; i++) {
            $.ajax({
                url: URL_STATUS + status_list[i],
                success: function (data) {
                    id = status_list[i]
                    // status = data['status']
                    status = data['task_status']
                    $('#' + id).html(status)
                    if (status == 'SUCCESS')
                        $($('#' + id).siblings()[1]).children().show()
                },
                async: false
            });
        }
    })

})