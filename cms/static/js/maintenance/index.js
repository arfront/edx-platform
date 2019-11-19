define(['jquery'], function ($) {
    return function () {
        $('.dingtalk-bottom').click(function (event) {
            $("#success_add_user_info").html('');
            $("#fail_add_user_info").html('');
            var host=window.location.host;
            var protocolStr = document.location.protocol;
            $.ajax({
                url: protocolStr+ '//' + host + "/api/v1/kh_insert_dingtalk_user/",
                type: "GET",
                success: function (result) {
                  if (result['status'] == '10001') {
                    $('.is-shown').css('display', 'block');
                    $('.result-is-shown').css('display', 'none');
                    var success_user_info = result['result']['success_user_info'];
                    var fail_user_info = result['result']['fail_user_info'];
                    if (success_user_info.length > 0) {
                      $.each(success_user_info, function (index, item) {
                        var name = item['name'];
                        $("#success_add_user_info").html($("#success_add_user_info").html() + "<li>" + "&nbsp;&nbsp;&nbsp;&nbsp;" + name + "&nbsp;&nbsp;</li>");
                      })
                    }
                    if (fail_user_info.length > 0) {
                      $.each(fail_user_info, function (index, item) {
                        var name = item['name'];
                        var msg = item['msg'];
                        $("#fail_add_user_info").html($("#fail_add_user_info").html() + "<li>" + "&nbsp;&nbsp;&nbsp;&nbsp;" + name + ":&nbsp;&nbsp;" + msg + "</li>");
                      })
                    }
                  } else {
                    alert(result['msg'])
                  }
                }

            })
        });

        $('.dingtalk-button-delete').click(function (event) {
            $(".dingtalk-delete-user-detail").html('');
            var host=window.location.host;
            var protocolStr = document.location.protocol;
            $.ajax({
              url:  protocolStr+ '//' + host + "/api/v1/kh_remove_leave_job_user/",
              type: "GET",
              success: function (result) {
                $('.is-shown').css('display', 'none');
                $('.result-is-shown').css('display', 'block');
                $('#dingtalk-delete-msg').text(result['msg']);
                if (result['detail'].length > 0) {
                  $.each(result['detail'], function (index, item) {
                    var real_name = item['real_name']
                    var username = item['username']
                    var email = item['email']
                    $('.dingtalk-delete-user-detail').html($('.dingtalk-delete-user-detail').html() +
                                                              "<li>" + "&nbsp;&nbsp;&nbsp;&nbsp;账号:&nbsp;" + username + "&nbsp;&nbsp;真实姓名:&nbsp;" + real_name
                                                                        + "&nbsp;&nbsp;邮箱:&nbsp;" + email + '</li>')
                  })
                }
              }
            })
        });
    }
})
