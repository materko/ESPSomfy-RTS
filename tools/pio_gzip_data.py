"""Zgzipuje textove subory z data/ pred zabalenim do obrazu filesystemu.

Web.cpp siaha po <subor>.gz, ked ho na filesystéme najde, a streamFile() k nemu doplni
hlavicku Content-Encoding: gzip. Cele web UI tym spadne zo 469 kB na 121 kB.

Obrazky sa nekomprimuju - uz komprimovane su a gzip by ich len zvacsil. appversion
zostava tiez nedotknuty: ten cita samotny firmware cez LittleFS, nie cez HTTP, a
zgzipovany by hlasil verziu 0.0.0.

Adresar data/ v repozitari sa nemeni, kopia vznika v .pio/.
"""

import gzip
import shutil
from pathlib import Path

Import("env")  # noqa: F821  (dodava PlatformIO)

TEXT_SUFFIXES = {".html", ".htm", ".css", ".js", ".json", ".svg", ".xml"}


def main() -> None:
    project = Path(env["PROJECT_DIR"])  # noqa: F821
    source = project / "data"
    if not source.is_dir():
        print("pio_gzip_data: data/ neexistuje, preskakujem")
        return

    target = Path(env.subst("$BUILD_DIR")) / "data-gz"  # noqa: F821
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)

    before = after = 0
    packed = 0
    for path in sorted(target.rglob("*")):
        if not path.is_file():
            continue
        size = path.stat().st_size
        before += size
        if path.suffix.lower() in TEXT_SUFFIXES:
            with path.open("rb") as src, gzip.open(f"{path}.gz", "wb", compresslevel=9) as dst:
                shutil.copyfileobj(src, dst)
            path.unlink()
            after += Path(f"{path}.gz").stat().st_size
            packed += 1
        else:
            after += size

    print(f"pio_gzip_data: {packed} suborov zgzipovanych, {before // 1024} kB -> {after // 1024} kB")
    env.Replace(PROJECT_DATA_DIR=str(target))  # noqa: F821


main()
