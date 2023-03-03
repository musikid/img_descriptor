# img-descriptor

> A simple command-line image descriptor for S3 objects
> using the Rekognition API.

This is a simple command-line tool which uses the AWS Rekognition API to
describe the contents of images in an S3 bucket. It is intended to be used
as a quick way to get a sense of the contents of a bucket without having
to download the images. As it relies on the Rekognition API, it is
limited to JPEG and PNG formats.

It outputs the information as a formatted table if the output is a
terminal, or as a JSON object otherwise.

## Installation

```bash
pip install img_descriptor-23.3.3-py3-none-any.whl
```

## Usage

```sh
img_descriptor <bucket_name> [<prefix>] [--json]
```

### Output example

```sh
$ img_descriptor my-bucket folder123

                Properties of images in my-bucket with prefix folder123
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃                                       ┃          ┃ Dominant   ┃            ┃          ┃           ┃             ┃
┃ Name                                  ┃ Size     ┃ colors     ┃ Brightness ┃ Contrast ┃ Sharpness ┃ Labels      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ folder123/icon.png                    │ 5.38 kB  │ #ffffff    │ 100.00 %   │ 76.38 %  │ 43.60 %   │ Text        │
│                                       │          │ #dcdcdc    │            │          │           │             │
│                                       │          │ #2f4f4f    │            │          │           │             │
│                                       │          │ #808080    │            │          │           │             │
│ folder123/icon2020-09-27 00-09-28.png │ 5.53 kB  │ #ffffff    │ 100.00 %   │ 69.93 %  │ 40.20 %   │ Text        │
│                                       │          │ #dcdcdc    │            │          │           │             │
│                                       │          │ #000000    │            │          │           │             │
│                                       │          │ #696969    │            │          │           │             │
│ folder123/icon2020-09-27 00-09-47.png │ 4.24 kB  │ #4169e1    │ 74.84 %    │ 82.97 %  │ 48.60 %   │ Text, Logo  │
│                                       │          │ #dcdcdc    │            │          │           │             │
│                                       │          │ #00bfff    │            │          │           │             │
│                                       │          │ #6495ed    │            │          │           │             │
│ folder123/icon2020-09-27 00-10-21.png │ 6.18 kB  │ #87cefa    │ 88.39 %    │ 75.05 %  │ 29.58 %   │ Logo, Text  │
│                                       │          │ #ffffff    │            │          │           │             │
│                                       │          │ #dcdcdc    │            │          │           │             │
│                                       │          │ #afeeee    │            │          │           │             │
│ folder123/icon2020-09-27 00-10-29.png │ 5.85 kB  │ #ffffff    │ 100.00 %   │ 67.80 %  │ 43.23 %   │ Logo, Text  │
│                                       │          │ #dcdcdc    │            │          │           │             │
│                                       │          │ #2f4f4f    │            │          │           │             │
│                                       │          │ #87ceeb    │            │          │           │             │
└───────────────────────────────────────┴──────────┴────────────┴────────────┴──────────┴───────────┴─────────────┘
```

### JSON format

The JSON output is a list of objects, each of which has the following
fields:

- `Name`: the S3 key of the image
- `Size`: the size of the image in bytes
- `DominantColors`: a list of hex color codes, sorted by dominance
- `Brightness`: a number between 0 and 100, representing the average
  brightness of the image
- `Contrast`: a number between 0 and 100, representing the average
  contrast of the image
- `Sharpness`: a number between 0 and 100, representing the average
  sharpness of the image
- `Labels` : a list of labels, sorted by confidence
