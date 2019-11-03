define(['jquery.form', 'js/index'], function() {
    'use strict';
    return function() {
        // showing/hiding creation rights UI
        $('.show-creationrights').click(function(e) {
            e.preventDefault();
            $(this)
                .closest('.wrapper-creationrights')
                    .toggleClass('is-shown')
                .find('.ui-toggle-control')
                    .toggleClass('current');
        });

        var reloadPage = function() {
            location.reload();
        };

        var showError = function() {
            $('#request-coursecreator-submit')
                .toggleClass('has-error')
                .find('.label')
                    .text('Sorry, there was error with your request');
            $('#request-coursecreator-submit')
                .find('.fa-cog')
                    .toggleClass('fa-spin');
        };

        $('#request-coursecreator').ajaxForm({
            error: showError,
            success: reloadPage
        });

        $('#request-coursecreator-submit').click(function(event) {
            $(this)
                .toggleClass('is-disabled is-submitting')
                .attr('aria-disabled', $(this).hasClass('is-disabled'))
                .find('.label')
                .text('Submitting Your Request');
        });
        $('.dingtalk-user-button').click(function (event) {
            $("#success_add_user_info").html('');
            $("#fail_add_user_info").html('');
            var host=window.location.host;
            var protocolStr = document.location.protocol;
            $.ajax({
                url: protocolStr+ '//' + host + "/api/v1/kh_insert_dingtalk_user/",
                type: "GET",
                success: function (result) {
                  if (result['status'] == '10001') {
                    $('.wrapper-insert-result').addClass('is-shown');
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
        })
    };
});
