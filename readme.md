# Add captions from a .srt to Camtasia Project as Callouts
## Edits the .tscproj file directly to add text from captions as callouts


**TL;DR** - Hacky script adds captions from a .srt file to a Camtasia project as
callouts. It's not perfect, but it's better than adding them manually.

Assuming Python 3.10 or greater is installed, you can run it like this:

``` bash 
python add_caption_callouts.py captions.srt camtasia_prj_dir.tscproj/test_project.tscproj
```

### More Info

It's a hack - normal captions can't easily be moved, animated, etc., but adding
them one by one as callouts manually is annoying. This is meant to be a quick
way to get them into the project so you can start to edit them / move them /
animate them.

I realize the overlap of people who use Camtasia and people who run Python
scripts is probably small - if you think you want to use this but don't know
how feel free to reach to out and I'll try to help. If there's enough interest
I will stand it up behind a Web UI. I'm hesitant to put much work into it because
I'm sure they'll add this feature in Camtasia soon.

This is developed with Camtasia 2023, Python 3.10 and Windows, I don't know 
what will happen on other Camtasia versions.

### Usage

This doesn't use any external libraries, so you should be able to just run it
with python 3.10 or later. It's a command line script, so you'll need to run it
from a terminal. You can run it like this to get help:

```bash
python add_captions_as_callouts.py --help
```

You have to give the script a .tscproj file and a .srt file. The .srt file is
the file that contains the captions, see the [example](example). The .tscproj
file is the Camtasia project file, which is really just JSON. Make sure you pass
the actual file path and not the directory path.

Final usage might look like:
```bash
python add_caption_callouts.py captions.srt camtasia_prj_dir.tscproj/test_project.tscproj
```

The script will add a new track to the project and add a callout for each
caption in the .srt file, and then save the project as new file (in case it
breaks).

### Example
Here's a [YouTube Video](https://youtu.be/TprEKrI0jk0) based on the example data.

### Known Issues
When the text is longer than the length of the call out, it looks truncated. It
isn't, it's just that the text past the length of the callout is super small.
Highlight it all and you can change the size and edit.

### Disclaimer
This is a script I made to make my life easier, I'm sharing because I think it
might help others out there who have the same somewhat niche problem. I'm not
sure it will work all the time, and it's not meant to produce polished captions,
just to get them in there in callouts so you can continue to edit them however
you want.

I'm running on windows and I haven't tested on other platforms.

Contributions are welcome! Open and issue or PR and I'll take a look.
