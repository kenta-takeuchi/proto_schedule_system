export function getMonthInfo(year, month) {
    const day = new Date(year, month, 1);

    const weekDay = ["日", "月", "火", "水", "木", "金", "土"];

    let monthDayList = [];
    for (let i = 2; i < new Date(year, month + 1, 0).getDate() + 2; i++) {
        monthDayList.push({
            date: String(day.getDate()),
            week: weekDay[day.getDay()]
        })
        day.setDate(i)
    }
    return monthDayList
}