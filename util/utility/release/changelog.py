import re
import xml.dom.minidom

RawRelease = tuple[str, list[str]]
RawReleases = list[RawRelease]

LIST_STARTERS = ("- ", "+ ")


def __get_raw_releases(content) -> RawReleases:
    raw_releases: RawReleases = []
    for line in content.split("\n"):
        if line.startswith("## "):
            raw_releases.append((line, []))
        elif len(raw_releases) != 0:
            raw_releases[-1][1].append(line)
    return raw_releases


def __parse_line(line: str, idx=0, in_code_block=False, illegal_link="") -> str:
    if idx == len(line):
        return ""
    this_segment = ""
    segment = line[idx]
    if segment == "`":
        if in_code_block:
            this_segment += "</code>"
            in_code_block = False
        else:
            this_segment += "<code>"
            in_code_block = True
    elif segment == "[":
        illegal_link += segment
    elif illegal_link:
        if segment == ")" and "]" in illegal_link:
            this_segment += illegal_link.split("[")[1].split("]")[0]
            illegal_link = ""
        elif segment != "(" and illegal_link[-1] == "]":
            this_segment += illegal_link
            illegal_link = ""
        else:
            illegal_link += segment
    else:
        this_segment += segment

    return (this_segment + __parse_line(
        line, idx + 1, in_code_block, illegal_link
    )).replace("<code></code>", "")


def __parse_markup(
    lines: list[str], idx: int = 0, ul_depth: int = 0,
    curr_ul_sep="", curr_line_depth=0
) -> str:
    if idx == len(lines):
        return ""
    parsed_line = ""
    line = lines[idx].lstrip()
    line_depth = len(lines[idx]) - len(line)
    if line.startswith(LIST_STARTERS):
        ul_sep = line[0:2]
        if curr_ul_sep == "":
            curr_ul_sep = ul_sep
            ul_depth += 1
            parsed_line += "<ul>"
        '''if ul_sep != curr_ul_sep:
            curr_ul_sep = ul_sep
            if line_depth >= curr_line_depth:
                ul_depth += 1
                parsed_line += "<ul>"
            else:
                ul_depth -= 1
                parsed_line += "</ul>"
            # Since Appstream does not support nested lists ind their standart, this is left out
        '''
        parsed_line += f"<li>{__parse_line(line.lstrip(ul_sep))}</li>"
    elif line_depth == curr_line_depth + 2 and curr_ul_sep != "":
        parsed_line += f"<MERGE_FORMER>{__parse_line(line)}</li>"
    else:
        line = line.lstrip("#")
        if ul_depth != 0:
            parsed_line += "</ul>" * ul_depth
            ul_depth = 0
            curr_ul_sep = ""
        if line.strip() != "":
            parsed_line += f"<p>{__parse_line(line)}</p>"

    return (
        parsed_line +
        __parse_markup(
            lines, idx + 1, ul_depth,
            curr_ul_sep, line_depth
        )
    ).replace("</li><MERGE_FORMER>", "")


def __parse_version_date(heading: str) -> tuple[str, str]:
    heading = heading.strip("##").strip()
    version_sub, date = heading.split(" - ")

    return version_sub.split("[")[1].split("]")[0].strip(), date.strip()


def __parse_release_xml(release: tuple[str, list[str]]) -> str:
    version, date = __parse_version_date(release[0])

    markup = __parse_markup(release[1])

    urgency = "medium" if version.endswith(".0") else "low"

    return f"""<release type="stable" version="{version}" date="{date}" urgency="{urgency}">
    <description>
        {markup}
    </description>
    <url>https://github.com/lxgr-linux/pokete/releases/tag/{version}</url>
</release>"""


def __get_full_releases(releases: list[str]):
    return f"""<releases>
    {"\n".join(releases)}
</releases>"""


def check_versions(tag: str, raw_releases: RawReleases):
    all_versions = [__parse_version_date(release[0])[0]
                    for release in raw_releases]
    if tag.lstrip("v") not in all_versions:
        print(f":: Warning: release tag `{tag}` has no changelog entry!")


def write_changelog(tag: str):
    with open("Changelog.md", "r") as changelog_file:
        changelog_content = changelog_file.read()
    raw_releases = __get_raw_releases(changelog_content)
    check_versions(tag, raw_releases)
    releases = [__parse_release_xml(r) for r in raw_releases]
    full_releases = __get_full_releases(releases)
    with open("assets/pokete.metainfo.xml", "r") as metainfo_file:
        content = metainfo_file.read()
    new_content = re.sub(r'<releases>.*?</releases>', full_releases,
                         content, flags=re.DOTALL)
    with open("assets/pokete.metainfo.xml", "w") as metainfo_file:
        metainfo_file.write(
            "\n".join(
                line for line in xml.dom.minidom.parseString(
                    new_content.replace("\n", "")
                )
                .toprettyxml(encoding="UTF-8")
                .decode("UTF-8")
                .split("\n")
                if line.strip()
            )
        )
