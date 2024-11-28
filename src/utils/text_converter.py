import logging
import math
import re

import requests
from bs4 import BeautifulSoup, PageElement, Tag, NavigableString

from src.utils.types.AdventOfCodeDay import AdventOfCodeDay
from src.utils.types.AdventOfCodeTable import AdventOfCodeTable
from src.utils.util import day_id


def convert_url_to_day_object(base_url, year):
    response = requests.get(base_url + r"/" + str(year))
    if response is not None and response.status_code == 200:
        soup = BeautifulSoup(response.content, features="html.parser")
        table = AdventOfCodeTable(
            year=year,
            title=getTableTitle(soup),
            text=getTableText(soup),
            days=getDays(soup, base_url, year)
        )
        return table
    return None


def getTableTitle(soup: BeautifulSoup):
    return soup.title.string if soup.title else None


def getTableText(soup: BeautifulSoup):
    main: PageElement = soup.find('main')
    if main:
        p = main.find('p')
        return p.get_text() if p else None
    return None


def getDays(soup: BeautifulSoup, base_url,year) -> [AdventOfCodeDay]:
    days = []
    main: PageElement = soup.find('main')
    if main:
        spans = main.find_all('a')
        if spans is None or len(spans) == 0:
            spans = main.find_all('span', class_="calendar-day")
        for span in spans:
            day = span.find('span').get_text(strip=True) if span.find('span') else span.get_text(strip=True)
            href = span['href'] if 'href' in span.attrs else None
            title = None
            text = None
            if href is not None:
                day_response = requests.get(base_url + href)
                if day_response.status_code == 200:
                    daySoup = BeautifulSoup(day_response.content, features="html.parser")
                    title = getDaysTitle(daySoup)
                    text = getDaysText(daySoup, base_url)
                days.append(AdventOfCodeDay(day_id=day_id(year, int(day)),year=year, link=href, title=title, description=text))
    return days


def getDaysTitle(soup: BeautifulSoup) -> str:
    main: PageElement = soup.find('main')
    if main:
        h2 = main.find('h2')
        return h2.get_text() if h2 else None
    return None


def getDaysText(soup: BeautifulSoup, base_url) -> [str]:
    main: PageElement = soup.find('main')
    text = []
    if main and main.find(['p', 'pre']) is not None:
        for p in main.find_all(['p', 'pre'])[:-1]:
            tt = ""
            if p.name == 'pre':
                tt += f"```\n{p.text}\n```"
            else:
                for content in p.contents:
                    base_url = r"https://adventofcode.com"
                    tt += html_to_markdown(content, base_url)
            text.append(tt)
    return "\n".join(text)


def html_to_markdown(tag: Tag, base_url="") -> str:
    if isinstance(tag, NavigableString):
        return tag.text
    elif tag.name == 'a':
        href = tag['href']
        if href.startswith('/'):
            href = base_url + href
        return f"[{tag.text}]({href})"
    elif tag.name == 'code':
        return f"`{tag.text}`"
    return ""


def main_page_converter(base_url, database, year):
    content = requests.get(base_url + r"/" + str(year))
    if content.status_code == 200:
        main_part = str(content.content).split("<main>")[1].split("</main>")[0].replace("\\n", "\n").replace("\\'",
                                                                                                             "\'")
        main_part = re.sub(r'<script.*?>.*?</script>', '', main_part, flags=re.DOTALL)
        main_part = main_part.replace('<pre class="calendar calendar-beckon">', "").replace("</pre>", "")
        if main_part.count('<a aria-label=') == 0:
            messageExists = database.check_message_exists("{:04d}{:02d}".format(year, 0))

            if not messageExists:
                message = []
                message.append("<title>AdventOfCode: Will start soon")
                message.append("<author>" + base_url)

                for para in main_part.split("<p>"):
                    cleaned = ""
                    para = para.replace("</p>", "")
                    if para.count('<a href="') != 0:
                        hold = para
                        for _ in range(para.count('<a href="')):
                            splitter = hold.split('<a href="', 1)
                            cleaned += splitter[0]
                            splitter = splitter[1].split('">', 1)
                            link = splitter[0]
                            splitter = splitter[1].split("</a>", 1)
                            hold = splitter[1]
                            ref = splitter[0]
                            cleaned += '[{}]({})'.format(ref, base_url + link)
                    else:
                        cleaned = para
                    if para != "":
                        message.append(cleaned)
                return "<field>".join(message), "0"
        main_part = main_part.split('<a aria-label=')[1:len(main_part)]
        links = []
        for line in main_part:
            links.append(line.split('href="')[1].split('"')[0])
        for link in links:
            day = link.split("/")[-1]
            year = link.split("/")[1]
            messageExists = database.check_message_exists("{:04d}{:02d}".format(int(year), int(day)))
            if not messageExists:
                logging.info("[REQUEST] " + link)
                response = requests.get(base_url + link)
                if response.status_code == 200:
                    content = response.content
                    main_part = str(content).split("<main>")[1].split("</main>")[0].replace("\\n", "\n").split(
                        '<article class="day-desc">')[1].split("</article>")[0]
                    paragraphs = [i.replace("</p>", "") for i in main_part.split("<p>")]
                    cleaned_text = []
                    for para in paragraphs:
                        cleaned = ""
                        modified = False
                        if para.count("<a") != 0:
                            modified = True
                            hold = para
                            y = ""
                            for _ in range(para.count("<a")):
                                spliter = hold.split('<a href="', 1)
                                cleaned += spliter[0]
                                y = spliter[1].split('"', 1)
                                link = y[0]
                                y = y[1].split(">", 1)[1].split("</a>", 1)
                                ref = y[0]
                                cleaned += "[{}]({})".format(ref, base_url + link)
                                hold = y[1]
                            cleaned += hold
                        if para.count('<span title="') != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            new_clean = ""
                            hold = cleaned
                            for _ in range(para.count('<span title="')):
                                splitter = hold.split('<span title="', 1)
                                new_clean += splitter[0]
                                splitter = splitter[1].split("</span>", 1)
                                hold = splitter[1]
                            new_clean += hold
                            cleaned = new_clean
                        if para.count("<code><em>") != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            cleaned = cleaned.replace('<code><em>', "**`")
                            cleaned = cleaned.replace('</em></code>', "`**")
                        if para.count("<em>") != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            cleaned = cleaned.replace('</em>', "**")
                            cleaned = cleaned.replace('<em>', "**")
                        if para.count('<em class="star">') != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            cleaned = cleaned.replace('<em class="star">', "**")
                            cleaned = cleaned.replace('</em>', "**")
                        if para.count("<li>") != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            cleaned = cleaned.replace('<li>', "- ")
                            cleaned = cleaned.replace('</li>', "")
                        if para.count("<ul>") != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            cleaned = cleaned.replace('<ul>', "")
                            cleaned = cleaned.replace('</ul>', "")
                        if para.count("<pre><code>") != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            cleaned = cleaned.replace('<pre><code>', "```")
                            cleaned = cleaned.replace('</code></pre>', "```")
                            pass
                        if para.count("<code>") != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            cleaned = cleaned.replace('<code>', "`")
                            cleaned = cleaned.replace('</code>', "`")
                        if para.count("<h2>") != 0:
                            modified = True
                            if cleaned == "":
                                cleaned = para
                            cleaned = cleaned.replace('<h2>', "<title>")
                            cleaned = cleaned.replace('</h2>', "")

                        if not modified:
                            cleaned = para
                        cleaned_text.append(cleaned)
                    embed_text = []
                    for cl in cleaned_text:
                        embed_clean = ""
                        if len(cl) >= 1024:
                            t = ""
                            for c in cl[:]:
                                if len(t) + len(c) < 1024:
                                    t += c
                                else:
                                    embed_clean += t
                                    t = ""
                            embed_clean += t
                            pass
                        else:
                            embed_clean = cl
                        embed_text.append(embed_clean)
                    message = ""
                    if len(embed_text) > 25:
                        count = 0
                        for _ in range(math.floor(26 / 25)):
                            message += "<field>".join(embed_text[count * 25:(count + 1) * 25]) + "<embed>"
                            count += 1
                        message += "<field>".join(embed_text[count * 25:len(embed_text)])
                    else:
                        message = "<field>".join(cleaned_text)
                    # pass
                    return message, day
