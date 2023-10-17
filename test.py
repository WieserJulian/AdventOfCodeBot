import requests

from src.message import Message

txt = """b'<!DOCTYPE html>\n<html lang="en-us">\n<head>\n<meta charset="utf-8"/>\n<title>Advent of Code 2022</title>\n<link rel="stylesheet" type="text/css" href="/static/style.css?31"/>\n<link rel="stylesheet alternate" type="text/css" href="/static/highcontrast.css?1" title="High Contrast"/>\n<link rel="shortcut icon" href="/favicon.png"/>\n<script>window.addEventListener(\'click\', function(e,s,r){if(e.target.nodeName===\'CODE\'&&e.detail===3){s=window.getSelection();s.removeAllRanges();r=document.createRange();r.selectNodeContents(e.target);s.addRange(r);}});</script>\n</head><!--\n\n\n\n\nOh, hello!  Funny seeing you here.\n\nI appreciate your enthusiasm, but you aren\'t going to find much down here.\nThere certainly aren\'t clues to any of the puzzles.  The best surprises don\'t\neven appear in the source until you unlock them for real.\n\nPlease be careful with automated requests; I\'m not a massive company, and I can\nonly take so much traffic.  Please be considerate so that everyone gets to play.\n\nIf you\'re curious about how Advent of Code works, it\'s running on some custom\nPerl code. Other than a few integrations (auth, analytics, social media), I\nbuilt the whole thing myself, including the design, animations, prose, and all\nof the puzzles.\n\nThe puzzles are most of the work; preparing a new calendar and a new set of\npuzzles each year takes all of my free time for 4-5 months. A lot of effort\nwent into building this thing - I hope you\'re enjoying playing it as much as I\nenjoyed making it for you!\n\nIf you\'d like to hang out, I\'m @ericwastl@hachyderm.io on Mastodon and\n@ericwastl on Twitter.\n\n- Eric Wastl\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n-->\n<body>\n<header><div><h1 class="title-global"><a href="/">Advent of Code</a></h1><nav><ul><li><a href="/2022/about">[About]</a></li><li><a href="/2022/events">[Events]</a></li><li><a href="https://teespring.com/stores/advent-of-code" target="_blank">[Shop]</a></li><li><a href="/2022/auth/login">[Log In]</a></li></ul></nav></div><div><h1 class="title-event">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="title-event-wrap">//</span><a href="/2022">2022</a><span class="title-event-wrap"></span></h1><nav><ul><li><a href="/2022">[Calendar]</a></li><li><a href="/2022/support">[AoC++]</a></li><li><a href="/2022/sponsors">[Sponsors]</a></li><li><a href="/2022/leaderboard">[Leaderboard]</a></li><li><a href="/2022/stats">[Stats]</a></li></ul></nav></div></header>\n\n<div id="sidebar">\n<div id="sponsor"><div class="quiet">Our <a href="/2022/sponsors">sponsors</a> help make Advent of Code possible:</div><div class="sponsor"><a href="https://www.epilog.net/en/career" target="_blank" onclick="if(ga)ga(\'send\',\'event\',\'sponsor\',\'sidebar\',this.href);" rel="noopener">EPILOG</a> - Join the SW development team conquering the world from Slovenia.</div></div>\n</div><!--/sidebar-->\n\n<main>\n<pre class="calendar calendar-beckon"><a aria-label="Day 25" href="/2022/day/25" class="calendar-day25">  - /\\ -  -        -       -     -      -    -          \n - /  \\/\\  -    -     -  -    -   -  /\\   -     -       \n@@#@@@####@@@@#@@#@#@@@#@@@@@@@##@@@#@###@@@####@  <span class="calendar-day">25</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 24" href="/2022/day/24" class="calendar-day24">#@@@@@@@@##@##@#@@@#@#@@@@@@#@#@@@@####@@@@@@@@@@  <span class="calendar-day">24</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 23" href="/2022/day/23" class="calendar-day23">@@@@@#@@@#@@@@#@@@@@#@@@@#@@@@@@@##@@@@@@@@@@@@@#  <span class="calendar-day">23</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 22" href="/2022/day/22" class="calendar-day22">@@@@@@@@@@@##@@###@#@@@#@@@@@#@@###@@@@#@@@#####@  <span class="calendar-day">22</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 21" href="/2022/day/21" class="calendar-day21">@@@@@##@@@###@#@#@@@#@@#@#@#@#@#@@@#@@#@@##@##@@@  <span class="calendar-day">21</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 20" href="/2022/day/20" class="calendar-day20">@#@#@@#@#@#@@@@@@@@##@#@@@#@#@@#@@@@@@##@##@@#@@#  <span class="calendar-day">20</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 19" href="/2022/day/19" class="calendar-day19">@@@#@@@@@#@@@@@#@#@#@@@##@@@@@@@@@@@@#@@#@@@@@@@@  <span class="calendar-day">19</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 18" href="/2022/day/18" class="calendar-day18">###@@@@@@@##@@#@#@@#@@@@##@@@@@@@#@@#@@@####@@@@@  <span class="calendar-day">18</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 17" href="/2022/day/17" class="calendar-day17">@##@@@@@#@@@@@@##@@#@##@####@@##@@##@@@@@###@@#@@  <span class="calendar-day">17</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 16" href="/2022/day/16" class="calendar-day16">#@@@#@#@#@@@@@@@@@@#@@@@@@@#@#@@@@@@@@@@@@@@#@@@@  <span class="calendar-day">16</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 15" href="/2022/day/15" class="calendar-day15">#@##@@##@@###@@@@##@@@@@#@#@@@#@@@@@@#@@#@@#@#@@@  <span class="calendar-day">15</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 14" href="/2022/day/14" class="calendar-day14">@@#@#@#@#@@@@##@@@@@@#@@@@@@@@@@@@#@@@@@@#@@@@@@#  <span class="calendar-day">14</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 13" href="/2022/day/13" class="calendar-day13">@@@@#@#@#@##@@@##@@###@#@#@##@@@@@@@@##@#@@@@##@@  <span class="calendar-day">13</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 12" href="/2022/day/12" class="calendar-day12">@@@#@@#@@@@@#@@#@@####@#@#@@#@@@#@##@@@|##@@#@@@@  <span class="calendar-day">12</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 11" href="/2022/day/11" class="calendar-day11">#@####@#@@@@@@###@@@@@@@#@#@@@##@#@@@#@#@@@@@@@@@  <span class="calendar-day">11</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 10" href="/2022/day/10" class="calendar-day10">@@####@@@@##@@@#@#@@@#@#@@@@@#@@@@@@@@##@@@#@@@#@  <span class="calendar-day">10</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 9" href="/2022/day/9" class="calendar-day9">@@#@@#@@@@@#@@@@@@@#@@##@@@@@@#@@@@#@@@@@@@##@@#@  <span class="calendar-day"> 9</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 8" href="/2022/day/8" class="calendar-day8">@@@@#@####@#@#@###@@#@#@#@#@#@@@#@@@#@#@@@@@@@@@#  <span class="calendar-day"> 8</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 7" href="/2022/day/7" class="calendar-day7">@@@###@#@##@@#@@#@@@@@@@@@@@@@#@@@#@@##@@#@@@@##@  <span class="calendar-day"> 7</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 6" href="/2022/day/6" class="calendar-day6">@@##@@#@@@#@##@@@@@#@@@@#@###@@|#@##@@@@##@@@@@#@  <span class="calendar-day"> 6</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 5" href="/2022/day/5" class="calendar-day5">@@@#@@#@@@@@@@@@@@@@@@@##@@@@#@@###@@#@@#@@#@#@@@  <span class="calendar-day"> 5</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 4" href="/2022/day/4" class="calendar-day4">@##@@##@####@@#@@@#@@##|#@#@@@#@@@@@@##@@@@@@@#@@  <span class="calendar-day"> 4</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 3" href="/2022/day/3" class="calendar-day3">@@@@@@@#@@@@@@@#@@@@@@@@@@@@@##@@@@#@@@@@@@@@@#@@  <span class="calendar-day"> 3</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 2" href="/2022/day/2" class="calendar-day2">#|@@@@#@@@@@@#@@#@@#@#@@@@@@@@@#@@@#@#@@@@@#@@@@@  <span class="calendar-day"> 2</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n<a aria-label="Day 1" href="/2022/day/1" class="calendar-day1">#@@@@@@@@@@@#@@##@##@@###@##@##@@#@#@#@#@@@#@@#@@  <span class="calendar-day"> 1</span> <span class="calendar-mark-complete">*</span><span class="calendar-mark-verycomplete">*</span></a>\n</pre>\n</main>\n\n<!-- ga -->\n<script>\n(function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){\n(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\nm=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n})(window,document,\'script\',\'//www.google-analytics.com/analytics.js\',\'ga\');\nga(\'create\', \'UA-69522494-1\', \'auto\');\nga(\'set\', \'anonymizeIp\', true);\nga(\'send\', \'pageview\');\n</script>\n<!-- /ga -->\n</body>\n</html>'"""
txt_day = """<!DOCTYPE html>\n<html lang="en-us">\n<head>\n<meta charset="utf-8"/>\n<title>Day 25 - Advent of Code 2022</title>\n<link rel="stylesheet" type="text/css" href="/static/style.css?31"/>\n<link rel="stylesheet alternate" type="text/css" href="/static/highcontrast.css?1" title="High Contrast"/>\n<link rel="shortcut icon" href="/favicon.png"/>\n<script>window.addEventListener(\'click\', function(e,s,r){if(e.target.nodeName===\'CODE\'&&e.detail===3){s=window.getSelection();s.removeAllRanges();r=document.createRange();r.selectNodeContents(e.target);s.addRange(r);}});</script>\n</head><!--\n\n\n\n\nOh, hello!  Funny seeing you here.\n\nI appreciate your enthusiasm, but you aren\'t going to find much down here.\nThere certainly aren\'t clues to any of the puzzles.  The best surprises don\'t\neven appear in the source until you unlock them for real.\n\nPlease be careful with automated requests; I\'m not a massive company, and I can\nonly take so much traffic.  Please be considerate so that everyone gets to play.\n\nIf you\'re curious about how Advent of Code works, it\'s running on some custom\nPerl code. Other than a few integrations (auth, analytics, social media), I\nbuilt the whole thing myself, including the design, animations, prose, and all\nof the puzzles.\n\nThe puzzles are most of the work; preparing a new calendar and a new set of\npuzzles each year takes all of my free time for 4-5 months. A lot of effort\nwent into building this thing - I hope you\'re enjoying playing it as much as I\nenjoyed making it for you!\n\nIf you\'d like to hang out, I\'m @ericwastl@hachyderm.io on Mastodon and\n@ericwastl on Twitter.\n\n- Eric Wastl\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n-->\n<body>\n<header><div><h1 class="title-global"><a href="/">Advent of Code</a></h1><nav><ul><li><a href="/2022/about">[About]</a></li><li><a href="/2022/events">[Events]</a></li><li><a href="https://teespring.com/stores/advent-of-code" target="_blank">[Shop]</a></li><li><a href="/2022/auth/login">[Log In]</a></li></ul></nav></div><div><h1 class="title-event">&nbsp;&nbsp;&nbsp;<span class="title-event-wrap">sub y{</span><a href="/2022">2022</a><span class="title-event-wrap">}</span></h1><nav><ul><li><a href="/2022">[Calendar]</a></li><li><a href="/2022/support">[AoC++]</a></li><li><a href="/2022/sponsors">[Sponsors]</a></li><li><a href="/2022/leaderboard">[Leaderboard]</a></li><li><a href="/2022/stats">[Stats]</a></li></ul></nav></div></header>\n\n<div id="sidebar">\n<div id="sponsor"><div class="quiet">Our <a href="/2022/sponsors">sponsors</a> help make Advent of Code possible:</div><div class="sponsor"><a href="https://careers.king.com/" target="_blank" onclick="if(ga)ga(\'send\',\'event\',\'sponsor\',\'sidebar\',this.href);" rel="noopener">King</a> - At King, we create unforgettable games (like Candy Crush) that are loved around the world. Join us to bring moments of magic to hundreds of millions of people every single day!</div></div>\n</div><!--/sidebar-->\n\n<main>\n<article class="day-desc"><h2>--- Day 25: Full of Hot Air ---</h2><p>As the expedition finally reaches the extraction point, several large <a href="https://en.wikipedia.org/wiki/Hot_air_balloon" target="_blank">hot air balloons</a> drift down to meet you. Crews quickly start unloading the equipment the balloons brought: many hot air balloon kits, some fuel tanks, and a <em>fuel heating machine</em>.</p>\n<p>The fuel heating machine is a new addition to the process. When this mountain was a volcano, the ambient temperature was more reasonable; now, it\'s so cold that the fuel won\'t work at all without being warmed up first.</p>\n<p>The Elves, seemingly in an attempt to make the new machine feel welcome, have already attached a pair of <a href="https://en.wikipedia.org/wiki/Googly_eyes" target="_blank">googly eyes</a> and started calling it "Bob".</p>\n<p>To heat the fuel, Bob needs to know the total amount of fuel that will be processed ahead of time so it can correctly calibrate heat output and flow rate. This amount is simply the <em>sum</em> of the fuel requirements of all of the hot air balloons, and those fuel requirements are even listed clearly on the side of each hot air balloon\'s burner.</p>\n<p>You assume the Elves will have no trouble adding up some numbers and are about to go back to figuring out which balloon is yours when you get a tap on the shoulder. Apparently, the fuel requirements use numbers written in a format the Elves don\'t recognize; predictably, they\'d like your help deciphering them.</p>\n<p>You make a list of all of the fuel requirements (your puzzle input), but you don\'t recognize the number format either. For example:</p>\n<pre><code>1=-0-2\n12111\n2=0=\n21\n2=01\n111\n20012\n112\n1=-1=\n1-12\n12\n1=\n122\n</code></pre>\n<p>Fortunately, Bob is labeled with a support phone number. Not to be deterred, you call and ask for help.</p>\n<p>"That\'s right, just supply the fuel amount to the-- oh, for more than one burner? No problem, you just need to add together our Special Numeral-Analogue Fuel Units. Patent pending! They\'re way better than normal numbers for--"</p>\n<p>You mention that it\'s quite cold up here and ask if they can skip ahead.</p>\n<p>"Okay, our Special Numeral-Analogue Fuel Units - SNAFU for short - are sort of like normal numbers. You know how starting on the right, normal numbers have a ones place, a tens place, a hundreds place, and so on, where the digit in each place tells you how many of that value you have?"</p>\n<p>"SNAFU works the same way, except it uses powers of five instead of ten. Starting from the right, you have a ones place, a fives place, a twenty-fives place, a one-hundred-and-twenty-fives place, and so on. It\'s that easy!"</p>\n<p>You ask why some of the digits look like <code>-</code> or <code>=</code> instead of "digits".</p>\n<p>"You know, I never did ask the engineers why they did that. Instead of using digits four through zero, the digits are <code><em>2</em></code>, <code><em>1</em></code>, <code><em>0</em></code>, <em>minus</em> (written <code>-</code>), and <em>double-minus</em> (written <code>=</code>). Minus is worth -1, and double-minus is worth -2."</p>\n<p>"So, because ten (in normal numbers) is two fives and no ones, in SNAFU it is written <code>20</code>. Since eight (in normal numbers) is two fives minus two ones, it is written <code>2=</code>."</p>\n<p>"You can do it the other direction, too. Say you have the SNAFU number <code>2=-01</code>. That\'s <code>2</code> in the 625s place, <code>=</code> (double-minus) in the 125s place, <code>-</code> (minus) in the 25s place, <code>0</code> in the 5s place, and <code>1</code> in the 1s place. (2 times 625) plus (-2 times 125) plus (-1 times 25) plus (0 times 5) plus (1 times 1). That\'s 1250 plus -250 plus -25 plus 0 plus 1. <em>976</em>!"</p>\n<p>"I see here that you\'re connected via our premium uplink service, so I\'ll transmit our handy SNAFU brochure to you now. Did you need anything else?"</p>\n<p>You ask if the fuel will even work in these temperatures.</p>\n<p>"Wait, it\'s <em>how</em> cold? There\'s no <em>way</em> the fuel - or <em>any</em> fuel - would work in those conditions! There are only a few places in the-- where did you say you are again?"</p>\n<p>Just then, you notice one of the Elves pour a few drops from a snowflake-shaped container into one of the fuel tanks, thank the support representative for their time, and disconnect the call.</p>\n<p>The SNAFU brochure contains a few more examples of decimal ("normal") numbers and their SNAFU counterparts:</p>\n<pre><code>  Decimal          SNAFU\n        1              1\n        2              2\n        3             1=\n        4             1-\n        5             10\n        6             11\n        7             12\n        8             2=\n        9             2-\n       10             20\n       15            1=0\n       20            1-0\n     2022         1=11-2\n    12345        1-0---0\n314159265  1121-1110-1=0\n</code></pre>\n<p>Based on this process, the SNAFU numbers in the example above can be converted to decimal numbers as follows:</p>\n<pre><code> SNAFU  Decimal\n1=-0-2     1747\n 12111      906\n  2=0=      198\n    21       11\n  2=01      201\n   111       31\n 20012     1257\n   112       32\n 1=-1=      353\n  1-12      107\n    12        7\n    1=        3\n   122       37\n</code></pre>\n<p>In decimal, the sum of these numbers is <code>4890</code>.</p>\n<p>As you go to input this number on Bob\'s console, you discover that some buttons you expected are missing. Instead, you are met with buttons labeled <code>=</code>, <code>-</code>, <code>0</code>, <code>1</code>, and <code>2</code>. Bob needs the input value expressed as a SNAFU number, not in decimal.</p>\n<p>Reversing the process, you can determine that for the decimal number <code>4890</code>, the SNAFU number you need to supply to Bob\'s console is <code><em>2=-1=0</em></code>.</p>\n<p>The Elves are starting to get cold. <em>What SNAFU number do you supply to Bob\'s console?</em></p>\n</article>\n<p>To play, please identify yourself via one of these services:</p>\n<p><a href="/auth/github">[GitHub]</a> <a href="/auth/google">[Google]</a> <a href="/auth/twitter">[Twitter]</a> <a href="/auth/reddit">[Reddit]</a> <span class="quiet">- <a href="/about#faq_auth">[How Does Auth Work?]</a></span></p>\n</main>\n\n<!-- ga -->\n<script>\n(function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){\n(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\nm=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n})(window,document,\'script\',\'//www.google-analytics.com/analytics.js\',\'ga\');\nga(\'create\', \'UA-69522494-1\', \'auto\');\nga(\'set\', \'anonymizeIp\', true);\nga(\'send\', \'pageview\');\n</script>\n<!-- /ga -->\n</body>\n</html>"""
base_url = "https://adventofcode.com"
main_part = str(txt).split("<main>")[1].split("</main>")[0].replace("\\n", "")
paragraphs = [i.replace("</p>", "") for i in main_part.split("<p>")]
cleaned = []
txt = txt.replace('<pre class="calendar calendar-beckon">', "").replace("</pre>", "")
txt = txt.split('<a aria-label=')[1:len(txt)]
links = []
for line in txt:
    day = line.split('"')[1].split(' ')[1]
    links.append(line.split('href="')[1].split('"')[0])
#TODO Check if link exitst
messages = []
for link in links:
    # response = requests.get(base_url + link)
    # if response.status_code == 200:
    if True:
        # content = content.content
        content = txt_day
        day = link.split("/")[-1]
        year = link.split("/")[1]
        main_part = str(content).split("<main>")[1].split("</main>")[0].replace("\\n", "").split(
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
                    cleaned += "[{}]({})".format(ref, link)
                    hold = y[1]
                cleaned += hold
            if para.count("<em>"):
                modified = True
                if cleaned == "":
                    cleaned = para
                cleaned = cleaned.replace('</em>', "**")
                cleaned = cleaned.replace('<em>', "**")
            if para.count("<pre><code>"):
                modified = True
                if cleaned == "":
                    cleaned = para
                cleaned = cleaned.replace('<pre><code>', "```")
                cleaned = cleaned.replace('</code></pre>', "```")
            if para.count("<h2>"):
                modified = True
                if cleaned == "":
                    cleaned = para
                cleaned = cleaned.replace('<h2>', "<title>")
                cleaned = cleaned.replace('</h2>', "")

            if not modified:
                cleaned = para
            cleaned_text.append(cleaned)

        messages.append(Message(year + day, "<field>".join(cleaned_text)))

for mes in messages:
    print(len(mes))
