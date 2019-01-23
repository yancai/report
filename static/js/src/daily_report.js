const TEMPLATE_USER_REPORT = "<ul class=\"list-unstyled\">" +
    "<h4><strong>{user_name}：  </strong></h4>" +
    "<h4><strong>已完成：  </strong></h4>" +
    "{done}\n" +
    "<h4><strong>计划：  </strong></h4>" +
    "{todo}" +
    "</ul><hr>";

const TEMPLATE_LI = "<li>{task}</li>";

/**
 * 渲染任务列表
 * @param tasks
 */
function renderTask(tasks) {
    let htmlStr = "";
    for (let i = 0; i < tasks.length; i++) {
        htmlStr += TEMPLATE_LI.replace(/{task}/, (i + 1) + ". " + tasks[i]);
    }
    return htmlStr;
}

/**
 * 渲染个人的日报
 * @param report
 */
function renderPersonalReport(report) {
    let yesterdayTask = renderTask(report.yesterday);
    let todayTask = renderTask(report.today);
    return TEMPLATE_USER_REPORT.replace(/{user_name}/, report.user_name)
        .replace(/{done}/, yesterdayTask)
        .replace(/{todo}/, todayTask);
}

/**
 * 渲染每日晨报
 */
function renderDailyReport() {
    let dateStr = getDate(0);
    $.ajax({
        type: "get",
        dateType: "json",
        url: "/api/reports/" + dateStr + "/",
        success: function (data) {
            data = data.data;

            let htmlStr = "";
            for (let i = 0; i < data.length; i++) {
                htmlStr += renderPersonalReport(data[i]);
            }
            $("#div-report").html(htmlStr);
        }
    });
}

$(document).ready(function () {
    // 设置日期
    $("#date-title").html(getDate(0) + " 晨报");
    renderDailyReport();
});