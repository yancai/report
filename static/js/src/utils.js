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