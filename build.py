import jinja2
import os
import glob
import shutil
from bs4 import BeautifulSoup
from pathlib import Path


OUT_FOLDER = "./out"
BASE = "./static/base.html"



def build():
    # Remove the out
    shutil.rmtree("./out")
    # Copy the static to the out file
    shutil.copytree("./static/css", "./out/css", dirs_exist_ok=True)
    
    # Glob all htmls
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("./static"))
    srcFiles = glob.glob("**/*.html", recursive=True, root_dir="./static")
    for f in srcFiles:
        if f.count("base.html") > 0:
            continue

        f = f.removeprefix("./static")

        t = env.get_template(f)
        raw = t.render()
        soup = BeautifulSoup(raw, "html.parser")
        pretty_html = soup.prettify()

        outPath = Path(f"./out/{f}")
        outPath.parent.mkdir(exist_ok=True, parents=True)
        with outPath.open("w") as fOut:
            fOut.write(pretty_html)



if __name__ == "__main__":
    build()