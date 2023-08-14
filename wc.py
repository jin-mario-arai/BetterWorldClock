import PySimpleGUI as sg
import datetime
import pytz
import numpy as np
import logging

### Configuration
sg.theme('Black')
padding=40
pastmax=-2880
futuremax=2880
logger = logging.getLogger("BetterWorldClock")
logging.basicConfig(filename='wc.log', level=logging.INFO)
tzlist = ['US/Pacific','US/Eastern', 'Asia/Tokyo','Asia/Shanghai', 'Asia/Kolkata', 'Etc/UTC']



### Update Clock
def update_clock(roundup,diff):
	i = 0
	### TODO: read from config file
	for tzname in tzlist:
		try:
			dt = datetime.datetime.now(pytz.timezone(tzname)) + diff
			if roundup:
				dt=round_time_to_nearest_10min(dt)
			logging.info(dt)
		except pytz.exceptions.UnknownTimeZoneError:
			# Ignore unknown Timezone
			dtime = ''
			ddate = ''
			dtimezone = ''
			logging.warning('Excpetion: Unknown Timezone - ' + tzname)

		else:
			dtime = dt.strftime("%I:%M %p")
			ddate = dt.strftime("%m/%d/%Y %a")
			dtimezone = tzname + dt.strftime("    %Z %z")

		window['-time' + str(i) + '-'].update(dtime)
		window['-date' + str(i) + '-'].update(ddate)
		window['-timezone' + str(i) + '-'].update(dtimezone)
		
		i += 1
		logging.info('----')


### Round up minutes
def round_time_to_nearest_10min(dt):
	minute = dt.minute
	delta = (minute + 5) // 10 * 10 - minute
	rounded_dt = dt + datetime.timedelta(minutes=delta)
	return rounded_dt.replace(second=0, microsecond=0)


### Reset button action
def reset_click():
	window['-slider-'].update(0)


### Calculate time difference
def diff_clock(slider_value):
	update_clock(roundup=True, diff=datetime.timedelta(minutes=slider_value))



### Construct Menu
menu = sg.MenuBar(
	[
		['File',['Quit']],
		['Edit',['Add/remove clock']],
	]
)

### Construct clock layout - 2 x 3

clocklist = []

for i in range (len(tzlist)):
	col = sg.Column(
		[
			[sg.Text('', font=('Arial',40), justification='center', key='-time' + str(i) + '-')],
			[sg.Text('', font=(15), key='-date' + str(i) + '-')],
			[sg.Text('', font=(15), key='-timezone' + str(i) + '-')]
		],
		pad=padding,
	)
	clocklist.append(col)

layout = [
	[
		menu,
	],
	[
		sg.Slider(
			range=(pastmax,futuremax),
			default_value=0,
			resolution=6,
			expand_x=True,
			enable_events=True,
			disable_number_display=True,
			orientation='horizontal',
			key='-slider-'
		),
		sg.Button(
			button_text='Reset & Restart',
			disabled=True,
			key='-reset-'
		)
	]
]
layout.extend(np.array(clocklist).reshape(2,3))


window = sg.Window(
	title='Better World Clock',
	layout=layout,
)
window.finalize()
update_clock(roundup=False, diff=datetime.timedelta())

	
# GUI process
while True:

	event, values = window.read(timeout=30000, timeout_key='-timeout-')

	if event is None:
		break

	if values['-slider-'] == 0.0:
		window['-reset-'].update(disabled=True)
		update_clock(roundup=False, diff=datetime.timedelta())
	else:
		window['-reset-'].update(disabled=False)
		diff_clock(values['-slider-'])


	if event == 'Quit':
		break
	elif event == '-timeout-':
		if values['-slider-'] == 0.0:
			update_clock(False, datetime.timedelta())
		# If slider value is not 0, then do nothing
	elif event == '-reset-':
		reset_click()
		window['-reset-'].update(disabled=True)
		update_clock(roundup=False, diff=datetime.timedelta())

window.close()
