from bs4 import BeautifulSoup
import requests

announcement_html = '''<div class="MuiGrid-root MuiGrid-container MuiGrid-item MuiGrid-grid-xs-12" style=""><div class="MuiGrid-root jss327 jss332 MuiGrid-container MuiGrid-item MuiGrid-align-items-xs-flex-start MuiGrid-grid-xs-12"><div class="MuiGrid-root MuiGrid-container MuiGrid-item MuiGrid-justify-content-xs-space-between MuiGrid-grid-xs-12" style="margin-bottom: 16px;"><div class="MuiGrid-root MuiGrid-item"><div class="jss328 jss333"><p class="MuiTypography-root jss149 jss323 MuiTypography-body1" data-mtifont="M XiangHe Hei TC W05 Heavy" style="font-family:'mtiFont2xzpqy','M XiangHe Hei TC W05 Heavy','Helvetica','Arial','sans-serif' !important;" isrender="true">重大</p></div><div style="margin-top: 12px;"><p class="MuiTypography-root MuiTypography-body2">《特戰英豪》</p></div></div><div class="MuiGrid-root jss330 MuiGrid-container MuiGrid-item MuiGrid-align-items-xs-center MuiGrid-justify-content-xs-center"><svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 98.91 81.26" aria-label="《特戰英豪》" height="28px"><path d="M98.92 39.1V.63a.63.63 0 00-1.13-.39l-42 52.52a.64.64 0 00.5 1h30.34a2.72 2.72 0 002.11-1l9.59-12a2.73 2.73 0 00.59-1.66zM.59 40.79l31.57 39.46a2.71 2.71 0 002.11 1h30.36a.63.63 0 00.5-1l-64-80A.63.63 0 000 .63V39.1a2.73 2.73 0 00.59 1.69z"></path></svg></div></div><div class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12"><p class="MuiTypography-root jss146 jss320 MuiTypography-body1">夜市暫不開放</p><div style="margin-top: 16px;"><p class="MuiTypography-root jss329 jss334 MuiTypography-body2">公告時間： 2023年6月8日 10:08 [GMT+8]</p></div><div style="margin-top: 24px; margin-bottom: 24px;"><p class="MuiTypography-root jss331 MuiTypography-body1">由於夜市出現異常，在維修期間，我們將暫時關閉此功能。</p></div><p class="MuiTypography-root jss329 jss334 MuiTypography-body2">受影響平台： Windows, macOS, Android, iOS</p></div></div><div class="MuiGrid-root jss327 jss343 MuiGrid-container MuiGrid-item MuiGrid-align-items-xs-flex-start MuiGrid-grid-xs-12"><div class="MuiGrid-root MuiGrid-container MuiGrid-item MuiGrid-justify-content-xs-space-between MuiGrid-grid-xs-12" style="margin-bottom: 16px;"><div class="MuiGrid-root MuiGrid-item"><div class="jss328 jss344"><p class="MuiTypography-root jss149 jss339 MuiTypography-body1" data-mtifont="M XiangHe Hei TC W05 Heavy" style="font-family:'mtiFont2xzpqy','M XiangHe Hei TC W05 Heavy','Helvetica','Arial','sans-serif' !important;" isrender="true">提醒</p></div><div style="margin-top: 12px;"><p class="MuiTypography-root MuiTypography-body2">《特戰英豪》</p></div></div><div class="MuiGrid-root jss330 MuiGrid-container MuiGrid-item MuiGrid-align-items-xs-center MuiGrid-justify-content-xs-center"><svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 98.91 81.26" aria-label="《特戰英豪》" height="28px"><path d="M98.92 39.1V.63a.63.63 0 00-1.13-.39l-42 52.52a.64.64 0 00.5 1h30.34a2.72 2.72 0 002.11-1l9.59-12a2.73 2.73 0 00.59-1.66zM.59 40.79l31.57 39.46a2.71 2.71 0 002.11 1h30.36a.63.63 0 00.5-1l-64-80A.63.63 0 000 .63V39.1a2.73 2.73 0 00.59 1.69z"></path></svg></div></div><div class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12"><p class="MuiTypography-root jss146 jss336 MuiTypography-body1">付款相關問題</p><div style="margin-top: 16px;"><p class="MuiTypography-root jss329 jss345 MuiTypography-body2">公告時間： 2023年6月8日 11:05 [GMT+8]</p></div><div style="margin-top: 24px; margin-bottom: 24px;"><p class="MuiTypography-root jss331 MuiTypography-body1">Codapay付款功能正在進行例行維護，你也許會遇到連線中斷的情形。</p></div><p class="MuiTypography-root jss329 jss345 MuiTypography-body2">受影響平台： Windows</p></div></div></div>'''

announcement_html = requests.get('https://status.riotgames.com/valorant?region=ap&locale=en_US').text
print(announcement_html)
# soup = BeautifulSoup(announcement_html, 'html.parser')

# error_levels = [header.text for header in soup.select('p[data-mtifont="M XiangHe Hei TC W05 Heavy"]')]
# services = [header.text for header in soup.select('p.MuiTypography-root.MuiTypography-body2')]
# error_titles = [title.text for title in soup.select('p.MuiTypography-root.jss146.jss320.MuiTypography-body1, p.MuiTypography-root.jss146.jss336.MuiTypography-body1')]
# announcement_times = [time.text for time in soup.select('p.jss329.jss334.MuiTypography-body2, p.jss329.jss345.MuiTypography-body2')]
# announcement_contents = [content.text for content in soup.select('p.MuiTypography-root.jss331.MuiTypography-body1')]

# platforms = []
# for platform in soup.select('p.jss329.jss334.MuiTypography-body2, p.jss329.jss345.MuiTypography-body2'):
#     platforms.append(platform.text.split("：")[-1])

# result = list(zip(error_levels, services, error_titles, announcement_times, announcement_contents, platforms))

# for item in result:
#     print(f"错误等级：{item[0]}\n错误的服务：{item[1]}\n错误标题：{item[2]}\n公告时间：{item[3]}\n公告内容：{item[4]}\n受影响平台：{item[5]}\n")

soup = BeautifulSoup(announcement_html, 'html.parser')

error_levels = [header.text for header in soup.select('p.MuiTypography-root.jss76.jss114.MuiTypography-h6')]
services = [header.text for header in soup.select('p.MuiTypography-root.MuiTypography-body2')]
error_titles = [title.text for title in soup.select('p.MuiTypography-root.jss76.jss114.MuiTypography-body1')]
announcement_times = [time.text for time in soup.select('p.jss166.jss171.MuiTypography-body2')]
announcement_contents = [content.text for content in soup.select('p.MuiTypography-root.jss77.MuiTypography-body1')]

platforms = [platform.text.split("：")[-1] for platform in soup.select('p.jss166.jss171.MuiTypography-body2')]

result = list(zip(error_levels, services, error_titles, announcement_times, announcement_contents, platforms))

for item in result:
    print(f"错误等级：{item[0]}\n错误的服务：{item[1]}\n错误标题：{item[2]}\n公告时间：{item[3]}\n公告内容：{item[4]}\n受影响平台：{item[5]}\n")