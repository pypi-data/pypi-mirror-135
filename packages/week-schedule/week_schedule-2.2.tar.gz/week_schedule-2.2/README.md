# `week_schedule`

A python little package for creating a schedule of my weekly classes from a JSON file using matplotlib.

Install it from the [python package index](https://pypi.org/project/week-schedule/):

```bash
pip install week_schedule
```

## How it works

Save your classes in a `.json` file with the structure:

```json
{
	"class name":{
		"[class days initials]":"[start time]-[end time]"
	}
}
```

`[class days initials]` can be any letter of an user-defined week abbreviations characters. For instance, you can treat your week like a piano, and put `A`,`B`,`C`,`D`,`E`,`F`,`G` as abbreviations for monday,tuesday,...,sunday. One sensible choice (and the default choice) are the labels `MTWRFSD`, **M**onday, **T**uesday, **W**ednesday, Thu**R**sday, **F**riday, **S**aturday, Sun**D**ay. Sunday is usually ommited, as it is not likely that you have some fixed thing to do that day. Days labels count from monday for that reason.

`[start time]` and `[end time]` can be hour strings such as `"11:00"`. By default, a 24-hour clock is assumed. You can specify am or pm: `"11:00pm"`. Minutes are optional `"11"`, `"3pm"`, and seconds are allowed just for fun: `"11:59:59am"`. Pretty much the only restriction is no spaces allowed, and a separating `'-'`.

You can include multiple days on the same hour. These are equivalent:

```json
{
	"my favorite class":{
		"MW":"1pm-2pm"
	}
}
```

```json
{
	"my favorite class":{
		"M":"1pm-2pm",
		"W":"1pm-2pm"
	}
}
```

This syntax allows a class with different days and hours, and you still could write the repeated days together. For examaple, let's say you have a class with two magistral sessions and one lab session. 

```json
{
	"Fungi lectures":{
		"TR":"8-9:30",    // Tuesday and Thursday cool fungi slideshows
		"S":"2pm-5:15pm"  // let's grow fungi on saturday
	}
}
```

Like everything in JSON you separate your things with commas. Here is an example of a full schedule

```json
{
	"Fungi lectures":{
		"TR":"8-9:30",
		"S":"2pm-5:15pm"
	},
	"Acquire a taste for free form jazz":{
		"MWF":"6pm-7:15pm"
	},
	"Shitpost masterclass with reddit entrepreneur":{
		"MW":"11-12:30"
	},
	"frog and toad shenaniganry II":{
		"TR":"10-11:45"
	},
	"childhood traumas with 4chan experts":{
		"TWRF":"13-15"
	}
}
```

You can found it in `./tests/test.json`. Then you go to python

```python
>>> from week_schedule import schedule_figure
>>> schedule_figure("./tests/test.json").savefig("./tests/test.png")
```

which results in

![](./tests/test.png)

### `schedule_figure` parameters

You can pass parameters to control various visual styles:

* `schedule_path`: path of the `.json` file
* `day_names`: ordered names of the weekdays. Defaults are `"MTWRFS"`
* `font_dict`: additional font tweaks; the same keyword arguments accepted by [matplotlib.pyplot.text](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html). Defaults used by this function are:
	* fontweight: bold
	* horizontalalignment: center
	* verticalalignment: center
	* fontsize: 7
	* color: white
* `text_stroke` outward black stroke for better reading of the text on all background colors. Default is `True`
* `major_minor_intervals`: interval of major and minor ticks, in hours. Defaults are 1 hour for major ticks and 15 minutes (1/4 hour) for minor ticks. Major tickss interval must be an integer number of hours, else a `ValueError` is raised.
* `cmap_name`: color palette to use on the subject backgrounds. Default is `"plasma"`. Options are in the matplotlib docs for [colormap reference](https://matplotlib.org/stable/gallery/color/colormap_reference.html).
* `cmap_range`: min and max output range of the colormap. In other words, portion of the colors to use. Default is `(0,0.9)`, almost the full range of colors (`(0,1)`).


## TODOs

- [ ] extend JSON format to allow optional hex colors and fontsizes for each subject. Currently the only two options if one of the classes names is too long are:
	1. Use abbreviations
	2. Change the global fontsize on `font_dict`
- [ ] add checks for conflicting class hours
