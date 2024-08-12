from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# 讀取資料
data = pd.read_csv('./data/data_cleaned.csv')

# 定義週次與日期區間的對應關係
week_to_dates = {
    "Week 1": "8/5-8/11",
    "Week 2": "8/12-8/18",
    "Week 3": "8/19-8/25",
    "Week 4": "8/26-9/1",
    "Week 5": "9/2-9/8",
    "Week 6": "9/9-9/15",
    "Week 7": "9/16-9/22",
    "Week 8": "9/23-9/29",
    "Week 9": "9/30-10/6",
    "Week 10": "10/7-10/13",
    "Week 11": "10/14-10/20",
    "Week 12": "10/21-10/27",
    "Week 13": "10/28-11/3",
    "Week 14": "11/4-11/10",
    "Week 15": "11/11-11/17",
    "Week 16": "11/18-11/24",
    "Week 17": "11/25-12/1",
    "Week 18": "12/2-12/8",
    "Week 19": "12/9-12/15",
    "Week 20": "12/16-12/22",
    "Week 21": "12/23-12/29",
    "Week 22": "12/30-1/5",
    "Week 23": "1/6-1/12",
    "Week 24": "1/13-1/19",
    "Week 25": "1/20-1/26",
    "Week 26": "1/27-2/2",
    "Week 27": "2/3-2/9",
    "Week 28": "2/10-2/16",
    "Week 29": "2/17-2/23",
    "Week 30": "2/24-3/2",
    "Week 31": "3/3-3/9",
    "Week 32": "3/10-3/16",
    "Week 33": "3/17-3/23",
    "Week 34": "3/24-3/30",
    "Week 35": "3/31-4/6",
    "Week 36": "4/7-4/13",
    "Week 37": "4/14-4/20",
    "Week 38": "4/21-4/27",
    "Week 39": "4/28-5/4",
    "Week 40": "5/5-5/11"
}

# 獲取所有科別代號
all_departments = pd.unique(data.iloc[:, 3:].values.ravel())

# 找找和你同科別的同學 (原有功能)
@app.route('/', methods=['GET', 'POST'])  # 根路徑指向這個功能
@app.route('/app1', methods=['GET', 'POST'])
def app1():
    def find_department_names(name, week):
        try:
            department = data.loc[data['姓名'] == name, week].values[0]
        except IndexError:
            return "No matching records found.", [], "0人"
        
        peers = data[data[week] == department]['姓名'].tolist()
        num = len(peers)
        
        return f"科別：{department}", peers, f"{num}人"

    if request.method == 'POST':
        name = request.form['name']
        week = request.form['week']
        department, peers, count = find_department_names(name, week)
        week_date = week_to_dates.get(week, "日期未知")
        return render_template('app1.html', name=name, week=week, week_date=week_date, department=department, peers=peers, count=count)
    
    return render_template('app1.html')

# 查找同科別人員和週次 (新功能)
@app.route('/app2', methods=['GET', 'POST'])
def app2():
    def find_weekly_peers(name, department, data):
        person_row = data[data['姓名'] == name]
        if person_row.empty:
            return f"姓名 {name} 不存在於資料中。"
        
        person_weeks = person_row.drop(columns=['Unnamed: 0', '姓名', '組別'])
        result = {}
        
        for week in person_weeks.columns:
            person_department = person_weeks[week].values[0]
            if person_department == department:
                peers = data[data[week] == department]['姓名'].tolist()
                if peers:
                    result[week] = peers
        
        weeks_with_dates = [f"{week} ({week_to_dates.get(week, '日期未知')})" for week in result.keys()]
        output = "週次：" + ", ".join(weeks_with_dates) + "\n" + "人員：" + ", ".join([", ".join(peers) for peers in result.values()])
        return output

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        output = find_weekly_peers(name, department, data)
        return render_template('app2.html', name=name, department=department, output=output)
    
    return render_template('app2.html')

if __name__ == '__main__':
    app.run(debug=True)