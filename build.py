import jinja2
import os
import glob
import shutil
from bs4 import BeautifulSoup
from pathlib import Path
import datetime


docs_FOLDER = "./docs"
BASE = "./static/base.html"

def build():
    # Remove the docs
    shutil.rmtree("./docs")
    # Copy the static to the docs file
    shutil.copytree("./static/css", "./docs/css", dirs_exist_ok=True)
    
    # Glob all htmls
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("./static"))

    srcFiles = glob.glob("**/*.html", recursive=True, root_dir="./static")

    envVars = {
        "dateTime": datetime.datetime.now().strftime("%A, %d %b %Y | %H:%M:%S")
    }

    for f in srcFiles:
        if f.count("base.html") > 0:
            continue

        f = f.removeprefix("./static")

        t = env.get_template(f)
        raw = t.render(envVars)
        soup = BeautifulSoup(raw, "html.parser")
        pretty_html = soup.prettify()

        docsPath = Path(f"./docs/{f}")
        docsPath.parent.mkdir(exist_ok=True, parents=True)
        with docsPath.open("w") as fdocs:
            fdocs.write(pretty_html)



if __name__ == "__main__":
    build()