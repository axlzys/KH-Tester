var jAlert,jConfirm;

// 蒙层
var mediaCss = "opacity: 0.5; position: fixed; left: 0;top: 0;width: 100%;height: 100%;background-color: #000000; z-index: 999;";

// 弹窗盒子
var jAlertParentCSS = "position: fixed; left: 50%;top: 50%; min-width: 400px; min-height: 200px; " +
    "margin-left: -200px;margin-top: -100px; z-index: 1000; background-color: #ffffff; border-radius: 5px;";

// 弹窗抬头样式
var jAlertTitleCSS = "height: 45px; line-height: 45px; font-size: 1.5rem; padding-left: 20px;" +
    "background-color: #1F7EFE; color: #fff; border-radius: 5px 5px 0 0;";

// 弹窗内容
var jAlertContentCSS = "height: 100px; line-height: 100px; font-size: 1.3rem;" +
    "text-align: center; color: #333; word-wrap:break-word; padding: 0 30px; letter-spacing: 3px;";

// 按钮位置
var jAlertButtonPCSS = 'height: 45px; display: flex; align-items: center; justify-content: flex-end;padding: 0 20px';

// 弹窗取消按钮
var jAlertButtonCancleCSS = "height: 35px; line-height: 35px; padding: 0 20px; color: #4D4D4D;" +
    "font-size: 1.3rem; background-color: #D4D4D4; border-radius: 5px;" +
    "cursor: pointer; margin-right: 20px";

// 弹窗确定按钮
var jAlertButtonSureCSS = "height: 35px; line-height: 35px; padding: 0 20px; color: #fff;" +
    "font-size: 1.3rem; background-color: #1F7EFE; border-radius: 5px; cursor: pointer;";

$(function () {
    jAlert = function (t, c, b, cbFun) {
        $("#jAlertParent").detach();
        if(!b) {
            b = "确定";
        }
        if(typeof b == "function") {
            cbFun = b;
            b = "确定";
        }
        var alertHtml='<div id="jAlertParent" style="'+jAlertParentCSS+'">'+
                          '<div id="jAlertTitle" style="'+jAlertTitleCSS+'">'+t+'</div>'+
                          '<div id="jAlertContent" style="'+jAlertContentCSS+'">'+c+'</div>'+
                          '<div id="jAlertButton" style="'+jAlertButtonPCSS+'">' +
                              '<div id="jAlertButton" style="'+jAlertButtonSureCSS+'">'+b+'</div>'+
                          '</div>'+
                      '</div>';

        if($(".media").length == 0) {
            alertHtml += '<div class="media" style="'+mediaCss+'"></div>';
        } else {
            $(".media").show();
        }

        $("body").append(alertHtml);

        $("#jAlertButton").on("click",function () {
            $("#jAlertParent").detach();
            $(".media").hide();
            cbFun && cbFun();
        });
    };

    jConfirm = function (t, c, b, cbFun) {
        $("#jAlertParent").detach();
        if(!b) {
            b = "确定";
        }
        if(typeof b=="function"){
            cbFun = b;
            b = "确定";
        }
        var alertHtml='<div id="jAlertParent" style="'+jAlertParentCSS+'">'+
                          '<div id="jAlertTitle" style="'+jAlertTitleCSS+'">'+t+'</div>'+
                          '<div id="jAlertContent" style="'+jAlertContentCSS+'">'+c+'</div>'+
                          '<div id="jAlertButton" style="'+jAlertButtonPCSS+'">' +
                              '<div id="jAlertButton1" style="'+jAlertButtonCancleCSS+'">取消</div>'+
                              '<div id="jAlertButton2" style="'+jAlertButtonSureCSS+'">'+b+'</div>'+
                          '</div>'+
                      '</div>';

        if($(".media").length == 0) {
            alertHtml += '<div class="media" style="'+mediaCss+'"></div>';
        } else {
            $(".media").show();
        }
        $("body").append(alertHtml);

        $("#jAlertButton1").on("click",function () {
            $("#jAlertParent").detach();
            $(".media").hide();
        });

        $("#jAlertButton2").on("click",function () {
            $("#jAlertParent").detach();
            $(".media").hide();
            cbFun && cbFun();
        });
    }
});