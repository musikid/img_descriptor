import typer
from rich.style import Style
from rich.color import Color
from rich.console import Console
from rich.table import Table
from rich.text import Text
import boto3
from mypy_boto3_rekognition.type_defs import DominantColorTypeDef

import json

app = typer.Typer()

s3 = boto3.resource("s3")
rekognition = boto3.client("rekognition")


def stylize(color: DominantColorTypeDef) -> Style:
    color = Color.from_rgb(color["Red"], color["Green"], color["Blue"])
    return Style(color="black", bgcolor=color, bold=True)


@app.command(help="Get properties of images in a bucket.")
def main(
    bucket_name: str = typer.Argument(..., help="Bucket name"),
    prefix: str = typer.Argument("", help="Prefix to filter by"),
    json_out: bool = typer.Option(False, "--json", help="Output JSON"),
):
    bucket = s3.Bucket(bucket_name)
    console = Console()

    json_output = not console.is_terminal or json_out

    if json_output:
        output = []
    else:
        table = (
            Table(
                title=f"Properties of images in {bucket_name} {f'with prefix {prefix}' if prefix else ''}",
                show_header=True,
                header_style="bold magenta",
            )
            if console.is_terminal
            else Table.grid(show_header=True)
        )
        table.add_column("Name", style="dim", no_wrap=True)
        table.add_column("Size")
        table.add_column("Dominant colors")
        table.add_column("Brightness")
        table.add_column("Contrast")
        table.add_column("Sharpness")
        table.add_column("Labels")

    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key.endswith(("jpg", "png")):
            response = rekognition.detect_labels(
                Image={"S3Object": {"Bucket": bucket_name, "Name": obj.key}},
                Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
                MaxLabels=8,
                MinConfidence=80,
                Settings={"ImageProperties": {"MaxDominantColors": 4}},
            )
            if "ImageProperties" in response:
                props = response["ImageProperties"]

                if json_output:
                    colors = [color["HexCode"] for color in props["DominantColors"]]
                    info = {
                        "Name": obj.key,
                        "Size": obj.size,
                        "DominantColors": colors,
                        "Brightness": props["Quality"]["Brightness"],
                        "Contrast": props["Quality"]["Contrast"],
                        "Sharpness": props["Quality"]["Sharpness"],
                    }
                    if "Labels" in response:
                        info["Labels"] = [label["Name"] for label in response["Labels"]]

                    output.append(info)
                else:
                    colors = Text.assemble(
                        *[
                            Text.assemble((color["HexCode"], stylize(color)), " ")
                            for color in props["DominantColors"]
                        ]
                    )
                    info = [
                        obj.key,
                        f"{obj.size/1024:.2f} kB",
                        colors,
                        f"{props['Quality']['Brightness']:.2f} %",
                        f"{props['Quality']['Contrast']:.2f} %",
                        f"{props['Quality']['Sharpness']:.2f} %",
                    ]
                    if "Labels" in response:
                        info.append(
                            ", ".join([label["Name"] for label in response["Labels"]])
                        )

                    table.add_row(*info)

    if json_output:
        typer.echo(json.dumps(output, indent=2))
    else:
        console.print(table)


if __name__ == "__main__":
    app()
