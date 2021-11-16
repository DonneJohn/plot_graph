# -*- coding: UTF-8 -*-
from flask import Flask, render_template
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as pltoff

import os.path

import numpy as np

import datafilter


app = Flask(__name__)
 
@app.route("/hello")
def hello():
    return render_template("index.html")


@app.route('/wt')
def showWeightTimeTable():
	#count = 500
	#xScale = np.linspace(0, 100, count)
	#yScale = np.random.randn(count)
 
	# Create a trace
	orderfile = "log/2021_01_22_07_0.log"
	weightdatas = datafilter.getdata(orderfile)
	print("weightdatas:", weightdatas)

	trace = go.Scatter(
		x = [i[0] for i in weightdatas],
		y = [i[1] for i in weightdatas],
		mode = 'markers',
		name = '原始数据'
	)
	data = [trace]
	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
	#print("random data:", graphJSON)
	layout = go.Layout(title="清运重量时间表", xaxis={'title':'time'}, yaxis={'title':'weight'})
	fig = go.Figure(data=data, layout=layout)
	htmlname = "templates/"+ orderfile + ".html"
	pltoff.plot(fig, filename=htmlname)
	return render_template(orderfile + ".html")

@app.route('/showLineChart')
def line():
	#count = 500
	#xScale = np.linspace(0, 100, count)
	#yScale = np.random.randn(count)
 
	# Create a trace
	orderfile = "2021_01_22_07_0.log"
	weightdatas = datafilter.getdata(orderfile)
	print("type:", type(weightdatas))

	trace = go.Scatter(
		x = [i[0] for i in weightdatas],
		y = [i[1] for i in weightdatas],
		mode = 'markers',
		name = '原始数据'
	)
 	
	newdatas = datafilter.filter(weightdatas.copy(), 10)
	trace1 = go.Scatter(
		x = [i[0] for i in newdatas],
		y = [i[1] for i in newdatas],
        mode = 'markers',
		name = '过滤数据'
	)
	timePoints = datafilter.findCleanPoints(newdatas)

	trace2 = go.Scatter(
		x = [i[0] for i in timePoints],
		y = [i[1] for i in timePoints],
		mode = 'markers',
		name = '拖放筐时间点'
	)

	data = [trace, trace1, trace2]
	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
	#print("random data:", graphJSON)
	layout = go.Layout(title="清运重量时间表", xaxis={'title':'time'}, yaxis={'title':'weight'})
	fig = go.Figure(data=data, layout=layout)
	htmlname = "templates/"+ orderfile + ".html"
	pltoff.plot(fig, filename=htmlname)
	return render_template(orderfile + ".html")


@app.route('/showLineCharts')
def multiLines():
	#count = 500
	#xScale = np.linspace(0, 100, count)
	#yScale = np.random.randn(count)
 
	# Create a trace

	logfiles = datafilter.getlogs()

	for logfile in logfiles:
		getWeighttimeChart(logfile)
	return "hello"
	'''
	
	'''

def getWeighttimeChart(logfile):
	weightdatas = datafilter.getLogfileData(logfile)
	print("type:", type(weightdatas))

	trace = go.Scatter(
		x = [i[0] for i in weightdatas],
		y = [i[1] for i in weightdatas],
		mode = 'markers',
		name = '原始数据'
	)
 	
	newdatas = datafilter.filter(weightdatas.copy(), 10)
	trace1 = go.Scatter(
		x = [i[0] for i in newdatas],
		y = [i[1] for i in newdatas],
		name = '过滤数据'
	)
	timePoints = datafilter.findCleanPoints(newdatas)

	trace2 = go.Scatter(
		x = [i[0] for i in timePoints],
		y = [i[1] for i in timePoints],
		mode = 'markers',
		name = '拖放筐时间点'
	)

	data = [trace, trace1, trace2]
	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
	#print("random data:", graphJSON)
	layout = go.Layout(title="清运重量时间表", xaxis={'title':'time'}, yaxis={'title':'weight'})
	fig = go.Figure(data=data, layout=layout)
	logfilename = os.path.basename(logfile)
	htmlname = "templates/"+ logfilename + ".html"
	pltoff.plot(fig, filename=htmlname)
	return render_template(logfilename + ".html")


@app.route('/showMultiChart')
def multiLine():
    count = 500
    xScale = np.linspace(0, 100, count)
    y0_scale = np.random.randn(count)
    y1_scale = np.random.randn(count)
    y2_scale = np.random.randn(count)
 
    # Create traces
    trace0 = go.Scatter(
        x = xScale,
        y = y0_scale
    )
    trace1 = go.Scatter(
        x = xScale,
        y = y1_scale
    )
    trace2 = go.Scatter(
        x = xScale,
        y = y2_scale
    )
    data = [trace0, trace1, trace2]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html',
                           graphJSON=graphJSON)

if __name__ == '__main__':
   # app.run(host = '0.0.0.0')
   app.run(host = '127.0.0.1')