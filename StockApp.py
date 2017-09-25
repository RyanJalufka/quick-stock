import alpha_vantage, jinja2, json
from datetime import datetime
from flask import Flask, render_template, request, make_response
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.sectorperformance import SectorPerformances


app = Flask(__name__)
ts = alpha_vantage.timeseries.TimeSeries(key='NCGXWTJ1X7NQFKBC')
sp = alpha_vantage.sectorperformance.SectorPerformances(key='NCGXWTJ1X7NQFKBC')
i = datetime.now()
current_Year = i.year
current_Month = i.month
current_Day = i.day
current_Hour = i.hour
current_Min = i.min
current_Sec = '00'


# 0 is appended to front of day date if current_Day value is less than 10 to keep formatting correct
if i.day < 10 and i.month < 10:
	current_Date = ("%s-0%s-0%s" % (i.year, i.month, i.day))
elif i.month < 10 and i.day > 10:
	current_Date = ("%s-0%s-%s" % (i.year, i.month, i.day))
elif i.month > 10 and i.day < 10:
	current_Date = ("%s-%s-0%s" % (i.year, i.month, i.day))
else:
	current_Date = ("%s-%s-%s" % (i.year, i.month, i.day))


OPEN_PRICE = "1. open"
HIGH_PRICE = "2. high"
LOW_PRICE = "3. low"
CLOSE_PRICE = "4. close"


@app.route('/')
def index():
	# Get json object with the intraday data and another with  the call's metadata
	# data, meta_data = ts.get_daily('GOOGL', 'compact')
	# print data
	# print i.isoformat()
	return render_template('index.html')

@app.route('/graph')
def graph():
	import datetime
	import StringIO
	import random

	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	from matplotlib.dates import DateFormatter

	fig = Figure()
	ax = fig.add_subplot(111)
	x = []
	y = []
	now = datetime.datetime.now()
	delta = datetime.timedelta(days=1)
	for i in range(10):
		x.append(now)
		now += delta
		y.append(random.randint(0, 1000))
	ax.plot_date(x, y, '-')
	ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
	fig.autofmt_xdate()
	canvas = FigureCanvas(fig)
	png_output = StringIO.StringIO()
	canvas.print_png(png_output)
	response = make_response(png_output.getvalue())
	response.headers['Content-Type'] = 'image/png'
	return response


@app.route('/stock_price', methods=['POST', 'GET'])
def stock_price():
	if request.method == 'POST':
		result = request.form['stock_symbol']
		data, meta_data = ts.get_daily(result, 'compact')
		stock_price = float(data[current_Date][CLOSE_PRICE])

		print current_Date
		print ("%.2f" % stock_price)

		return render_template("stock_price.html", stock_price=stock_price, stock=result)


if __name__ == '__main__':
	app.run(debug=True)
