const TEMPLATE_INPUT_TASK = '<div class="input-group">' +
    '<span class="input-group-addon" id="basic-addon{taskId}">{taskId}</span>' +
    '<input id="input01" type="text" class="form-control" placeholder="任务描述..." aria-describedby="basic-addon{taskId}">' +
    '</div>';

const TEMPLATE_LABEL_TASK = '<div class="input-group">' +
    '<span class="input-group-addon" id="basic-addon{taskId}">{taskId}</span>' +
    '<label id="input01" class="form-control" aria-describedby="basic-addon{taskId}">{task}</label>' +
    '</div>';

const TEMPLATE_USER = '<li><a href="#" uid="{uid}" onclick="shows($(this).text(), \'{uid}\')">{name}</a></li>';

/**
 * 格式化日期
 * @param fmt
 * @param date
 * @returns {*}
 */
function dateFtt(fmt, date) {
    let o = {
        "M+": date.getMonth() + 1,                      //月份
        "d+": date.getDate(),                           //日
        "h+": date.getHours(),                          //小时
        "m+": date.getMinutes(),                        //分
        "s+": date.getSeconds(),                        //秒
        "q+": Math.floor((date.getMonth() + 3) / 3), //季度
        "S": date.getMilliseconds()                     //毫秒
    };
    if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    for (let k in o) {
        if (new RegExp("(" + k + ")").test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        }
    }
    return fmt;
}

/**
 * 获取日期字符串
 * @param delta 与当前日期差值
 * @returns {*}
 */
function getDate(delta) {
    if (delta === undefined || delta === '') {
        delta = 0;
    }
    let ts = Math.round(new Date() / 1000 + delta * 86400);
    let d = new Date(ts * 1000);
    return dateFtt("yyyy-MM-dd", d);
}

/**
 * 渲染今日任务列表
 */
function renderTodayTask() {
    let htmlStr = "";
    for (let i = 1; i <= 3; i++) {
        htmlStr += TEMPLATE_INPUT_TASK.replace(/{taskId}/g, i);
    }
    $("#div-today-tasks").html(htmlStr);
}

/**
 * 渲染昨日已完成任务列表
 */
function renderYesterdayDoneTask() {
    let htmlStr = "";
    for (let i = 1; i <= 3; i++) {
        htmlStr += TEMPLATE_INPUT_TASK.replace(/{taskId}/g, i);
    }
    $("#div-yesterday-done-tasks").html(htmlStr);
}

/**
 * 渲染昨日计划任务列表
 */
function renderYesterdayTodoTask() {
    let htmlStr = "";
    for (let i = 1; i <= 3; i++) {
        htmlStr += TEMPLATE_LABEL_TASK.replace(/{taskId}/g, i).replace(/{task}/, "任务xxx" + i);
    }
    $("#div-yesterday-todo-tasks").html(htmlStr);
}

/**
 * 添加今天任务
 */
function addTodayTask() {
    let length = $("#div-today-tasks input").length;
    let htmlStr = TEMPLATE_INPUT_TASK.replace(/{taskId}/g, length + 1);
    $("#div-today-tasks").append(htmlStr);
}

/**
 * 添加昨日已完成任务
 */
function addYesterdayDoneTask() {
    let length = $("#div-yesterday-done-tasks input").length;
    let htmlStr = TEMPLATE_INPUT_TASK.replace(/{taskId}/g, length + 1);
    $("#div-yesterday-done-tasks").append(htmlStr);
}


/**
 * 获取页面上用户填写的日报
 */
function getDailyReport() {
    let todayTasks = [];
    let yesterdayTasks = [];

    $("#div-today input").each(function () {
        let task = $(this).val();
        if (task !== "") {
            todayTasks.push(task);
        }
    });

    $("#div-yesterday-done-tasks input").each(function () {
        let task = $(this).val();
        if (task !== "") {
            yesterdayTasks.push(task);
        }
    });

    let uid = $("#label-name").attr("uid");

    return {
        uid: uid,
        yesterday: yesterdayTasks,
        today: todayTasks
    }
}


function shows(a, uid) {
    $('#label-name').text(a).attr("uid", uid);
}


/**
 * 渲染用户列表
 */
function renderUsers() {
    $.ajax({
        type: "get",
        dateType: "json",
        url: "/api/users",
        success: function (data) {
            let htmlStr = "";
            for (let i = 0; i < data.users.length; i++) {
                htmlStr += TEMPLATE_USER.replace(/{uid}/g, data.users[i].id)
                    .replace(/{name}/g, data.users[i].name);
            }
            $("#ul-users").html(htmlStr);
        }
    });
}

function commitTask() {
    let data = getDailyReport();
    let date = getDate(0);
    let uid = data.uid;

    $.ajax({
        type: "put",
        dateType: "json",
        contentType: "application/json",
        data: JSON.stringify(data),
        url: "/api/report/" + date + "/" + uid + "/",
        success: function (data) {
            if (data.msg === "success") {
                window.location = "/report"
            }
        }
    });

}

$(document).ready(function () {
    // 设置日期
    $("#date-title").html(getDate(0) + " 晨报填写");

    // 渲染今日任务列表
    renderTodayTask();
    // 今日Add按钮事件绑定
    $("#btn-today-add").click(addTodayTask);


    // 渲染昨日已完成任务列表
    renderYesterdayDoneTask();
    // 昨日已完成
    $("#btn-yesterday-done-add").click(addYesterdayDoneTask);

    // 渲染昨日计划任务列表
    renderYesterdayTodoTask();

    // 渲染用户列表
    renderUsers();


    // 绑定提交按钮事件
    $("#btn-commit").click(commitTask);

});