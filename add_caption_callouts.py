import argparse
import copy
import pathlib
import json


TRACK_BLANK = {'medias': [], 'trackIndex': 0}
CAPTION_BLANK = { '_type': 'Callout',
                "def" : {
                        "kind" : "remix",
                        "shape" : "text",
                        "style" : "basic",
                        "enable-ligatures" : 1.0,
                        "height" : 125.0,
                        "line-spacing" : 0.0,
                        "width" : 1890.4347826087,
                        "word-wrap" : 1.0,
                        "horizontal-alignment" : "center",
                        "resize-behavior" : "resizeText",
                        "text" : "This is a caption that will show on the screen",
                        "vertical-alignment" : "center",
                        "font" : {
                          "color-blue" : 1.0,
                          "color-green" : 1.0,
                          "color-red" : 1.0,
                          "size" : 96.0,
                          "tracking" : 0.0,
                          "name" : "Montserrat",
                          "weight" : "Regular"
                        },
                        "textAttributes" : {
                          "type" : "textAttributeList",
                          "keyframes" : [
                            {
                              "endTime" : 0,
                              "time" : 0,
                              "value" : [{"name":"fontSize","rangeEnd":46,"rangeStart":0,"value":96.0,"valueType":"double"},{"name":"fontName","rangeEnd":46,"rangeStart":0,"value":"Montserrat","valueType":"string"},{"name":"strikethrough","rangeEnd":46,"rangeStart":0,"value":0,"valueType":"int"},{"name":"kerning","rangeEnd":46,"rangeStart":0,"value":0.0,"valueType":"double"},{"name":"fgColor","rangeEnd":46,"rangeStart":0,"value":"(255,255,255,255)","valueType":"color"},{"name":"fontWeight","rangeEnd":46,"rangeStart":0,"value":400,"valueType":"int"},{"name":"underline","rangeEnd":46,"rangeStart":0,"value":0,"valueType":"int"},{"name":"fontItalic","rangeEnd":46,"rangeStart":0,"value":0,"valueType":"int"}],
                              "duration" : 0
                            }
                          ]
                        }
                    },
                    "attributes" : {
                      "ident" : "",
                      "autoRotateText" : True
                    },
                    "parameters" : {
                      "translation0" : 14.7826086956522,
                      "translation1" : -336.413043478261,
                      "geometryCrop0" : 0.0,
                      "geometryCrop1" : 0.0,
                      "geometryCrop2" : 0.0,
                      "geometryCrop3" : 0.0
                    },
                    "effects" : [

                    ],
                    "start" : 0,
                    "duration" : 4233600000,
                    "mediaStart" : 0,
                    "mediaDuration" : 4233600000,
                    "scalar" : 1,
                    "metadata" : {
                      "audiateLinkedSession" : "",
                      "clipSpeedAttribute" : False,
                      "default-HAlign" : "center",
                      "default-LineSpace" : 0.0,
                      "default-VAlign" : "center",
                      "default-anchor0" : 0.0,
                      "default-anchor1" : 0.0,
                      "default-anchor2" : 0.0,
                      "default-height" : 250.0,
                      "default-rotation0" : 0.0,
                      "default-rotation1" : 0.0,
                      "default-rotation2" : 0.0,
                      "default-scale0" : 1.0,
                      "default-scale1" : 1.0,
                      "default-scale2" : 1.0,
                      "default-shear0" : 0.0,
                      "default-shear1" : 0.0,
                      "default-shear2" : 0.0,
                      "default-text-attributes" : "[{\"name\":\"strikethrough\",\"rangeEnd\":11,\"rangeStart\":0,\"value\":0,\"valueType\":\"int\"},{\"name\":\"fgColor\",\"rangeEnd\":11,\"rangeStart\":0,\"value\":\"(255,255,255,255)\",\"valueType\":\"color\"},{\"name\":\"fontWeight\",\"rangeEnd\":11,\"rangeStart\":0,\"value\":400,\"valueType\":\"int\"},{\"name\":\"fontSize\",\"rangeEnd\":11,\"rangeStart\":0,\"value\":96.0,\"valueType\":\"double\"},{\"name\":\"fontName\",\"rangeEnd\":11,\"rangeStart\":0,\"value\":\"Montserrat\",\"valueType\":\"string\"},{\"name\":\"kerning\",\"rangeEnd\":11,\"rangeStart\":0,\"value\":0.0,\"valueType\":\"double\"},{\"name\":\"fontItalic\",\"rangeEnd\":11,\"rangeStart\":0,\"value\":0,\"valueType\":\"int\"},{\"name\":\"underline\",\"rangeEnd\":11,\"rangeStart\":0,\"value\":0,\"valueType\":\"int\"}]",
                      "default-translation0" : 0.0,
                      "default-translation1" : 0.0,
                      "default-translation2" : 0.0,
                      "default-width" : 400.0
                    },
                    "animationTracks" : {

                    }
                  }

class Caption:
  """ Holds some information about a caption """

  # I don't know what this is is, but I got it by checking the durations and
  # times of the captions in a project with a single caption - eg 1 second is
  # 705600 units
  secs_to_cs_time = 705_600

  def __init__(self, start: str, end: str, text: str):
    self.start = self._string_time_to_number(start) * self.secs_to_cs_time
    self.end = self._string_time_to_number(end) * self.secs_to_cs_time
    self.duration = self.end - self.start
    self.text = text

  def _string_time_to_number(self, time_str: str) -> int:
    """ String time in the format hh:mm:ss,ms to a number of milliseconds
    """
    hhmmss, ms = time_str.strip().split(",")
    hh, mm, ss = hhmmss.strip().split(":")
    return int(hh)*3600000 + int(mm)*60000 + int(ss)*1000 + int(ms)
  
  def __repr__(self):
    return f"Caption({self.start}, {self.end}, {self.duration}, {self.text})"


def get_new_track_with_captions(
    captions: list[Caption],
    track_idx: int,
    next_media_id: int = 100,
    font_size: int = 60):
  """ Add the captions to a new blank track and return it. """
  track = copy.deepcopy(TRACK_BLANK)
  for idx, c in enumerate(captions):
    cpt = copy.deepcopy(CAPTION_BLANK)
    cpt['id'] = idx + 100
    cpt["def"]["text"] = c.text
    cpt["start"] = c.start
    cpt["duration"] = c.duration
    # set the font size for the caption text
    cpt["def"]["textAttributes"]["keyframes"][0]["value"][0]["value"] = font_size
    cpt["def"]["textAttributes"]["keyframes"][0]["value"][0]["value"] = len(c.text)
    track["medias"].append(cpt)
  track["trackIndex"] = track_idx
  return track


def parse_captions(lines: list[str]) -> list[Caption]:
  """ Parse the captions from the lines of a .srt file """
  captions = []
  while len(lines) > 0:
    if lines[0].strip() == "":
      lines.pop(0)
      continue
    _, times, caption  = lines.pop(0), lines.pop(0), lines.pop(0)
    start, end = times.split("-->")
    captions.append(
      Caption(
        start.strip(),
        end.strip(),
        caption.strip()
      )
    )
  return captions


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "captions", type=str,
    help="The filename of the .srt captions file")
  parser.add_argument(
    "project", type=str,
    help="The filename of the .tscproj project file")
  parser.add_argument(
    "--font-size", type=int, default=60,
    help="The font size to use for the captions")
  args = parser.parse_args()

  # Check the captions file exists
  captions_filename = pathlib.Path(args.captions)
  if not captions_filename.exists():
    raise FileNotFoundError(f"Could not find {captions_filename}")
  
  # Check that it's a .srt file
  if captions_filename.suffix != ".srt":
    raise ValueError(
      f"Captions file must be a .srt file, not {captions_filename.suffix}")

  prj = pathlib.Path(args.project)
  # Check the project file exists
  if not prj.exists():
    raise FileNotFoundError(f"Could not find {args.project}")

  # Check that it's a .tscproj file  
  if not prj.suffix == ".tscproj":
    raise ValueError(
      f"Project file must be a .tscproj file, not {pathlib.Path(args.project).suffix}. Make sure you are pointing at the .tscproj file, not the folder.")

  # Load the project file 
  with open(prj, 'r') as f:
    prj_json = json.load(f)

  # Get the tracks from the project file
  timeline = prj_json["timeline"]
  tracks = timeline["sceneTrack"]["scenes"][0]["csml"]["tracks"]
  ntracks = len(tracks)
  next_media_id = max([m["id"] for t in tracks for m in t["medias"]]) + 1

  # Parse the captions file
  with open(captions_filename, 'r') as f:
    captions = parse_captions(f.readlines())

  new_track_with_captions = get_new_track_with_captions(
    captions, ntracks, next_media_id)
  tracks.append(new_track_with_captions)

  # Write the new project file with the captions
  outfile = prj.parent / f"{prj.stem}_with_captions.tscproj"
  with open(outfile, 'w') as f:
    json.dump(prj_json, f, indent=2)
  print(f"Saved new project file to {outfile}")


if __name__ == '__main__':
  main()

