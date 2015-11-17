from flask import Blueprint, render_template

sample = Blueprint('sample', __name__, template_folder='templates')


@sample.route('/')
def index():
    return render_template('sample/index.html')


@sample.route('/app_calendar')
def app_calendar():
    return render_template('sample/app_calendar.html')


@sample.route('/app_inbox_compose')
def app_inbox_compose():
    return render_template('sample/app_inbox_compose.html')


@sample.route('/app_inbox')
def app_inbox():
    return render_template('sample/app_inbox.html')


@sample.route('/app_inbox_inbox')
def app_inbox_inbox():
    return render_template('sample/app_inbox_inbox.html')


@sample.route('/app_inbox_reply')
def app_inbox_reply():
    return render_template('sample/app_inbox_reply.html')


@sample.route('/app_inbox_view')
def app_inbox_view():
    return render_template('sample/app_inbox_view.html')


@sample.route('/app_todo_2')
def app_todo_2():
    return render_template('sample/app_todo_2.html')


@sample.route('/app_todo')
def app_todo():
    return render_template('sample/app_todo.html')


@sample.route('/charts_amcharts')
def charts_amcharts():
    return render_template('sample/charts_amcharts.html')


@sample.route('/charts_echarts')
def charts_echarts():
    return render_template('sample/charts_echarts.html')


@sample.route('/charts_flotcharts')
def charts_flotcharts():
    return render_template('sample/charts_flotcharts.html')


@sample.route('/charts_flowchart')
def charts_flowchart():
    return render_template('sample/charts_flowchart.html')


@sample.route('/charts_google')
def charts_google():
    return render_template('sample/charts_google.html')


@sample.route('/charts_highcharts')
def charts_highcharts():
    return render_template('sample/charts_highcharts.html')


@sample.route('/charts_highmaps')
def charts_highmaps():
    return render_template('sample/charts_highmaps.html')


@sample.route('/charts_highstock')
def charts_highstock():
    return render_template('sample/charts_highstock.html')


@sample.route('/charts_morris')
def charts_morris():
    return render_template('sample/charts_morris.html')
