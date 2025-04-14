import json
import time
import asyncio

from django.shortcuts import render
from django.http import HttpResponse
from .models import Data

from playwright.async_api import async_playwright, expect


async def getRnDPage(request):
    print("동작")
    if request.method == "POST":
        data = json.loads(request.body)
        async with async_playwright() as p:
            site_type = data['type']
            browser = await p.chromium.launch()
            page = await browser.new_page()
            page = await set_extra_http_headers(page)
            await page.goto("https://www.smtech.go.kr/front/log/login.do?returnUrl=%2ffront%2flog%2flogin.do")
            await page.frame_locator("iframe[name=\"member\"]").get_by_role("textbox", name="아이디 입력창").fill('nextkey1')
            await page.frame_locator("iframe[name=\"member\"]").get_by_role("textbox", name="비밀번호 입력창").fill('@siab812580')
            await page.frame_locator("iframe[name=\"member\"]").get_by_role("link", name="로그인").click()
            await asyncio.sleep(2)
            if site_type == "MAIN":
                new_data = Data()
                new_data.content = await page.content()
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE":
                await page.get_by_role("link", name="마이페이지").click()
                await asyncio.sleep(2)
                
                new_data = Data()
                new_data.content = page.content()
                new_data.content_type = site_type + "_1"
                new_data.save()
            elif site_type == "MYPAGE_NOTI":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#notiCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_RESTN":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#restnCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector("#exeSbjtTable")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_AGRE":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#agreChngCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_PAYM1":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#paym1Count").click()
                await asyncio.sleep(2)
                table = await page.query_selector("#PaymSituTable")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_PAYM2":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#paym2Count").click()
                await asyncio.sleep(2)
                table = await page.query_selector("#PaymSituTable")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_TFEE":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#tfeePlanCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_TFEE":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#tfeePlanCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_IQ":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#iqCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_QNA":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#bconsQnaCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_CHK":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#bconsCityChkCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_CHK":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#bconsCityChkCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_BNOTI":
                await page.get_by_role("link", name="마이페이지").click()
                await page.locator("#bconsNotiCount").click()
                await asyncio.sleep(2)
                table = await page.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_1":
                await page.get_by_role("link", name="마이페이지").click()
                await page.get_by_role("link", name="개인정보관리", exact=True).click()
                await asyncio.sleep(2)
                iframe_handle = await page.wait_for_selector("iframe[name=\"II_IndyInfo\"]")
                iframe = await iframe_handle.content_frame()
                table = await iframe.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_2":
                await page.get_by_role("link", name="마이페이지").click()
                await page.get_by_role("link", name="개인정보관리", exact=True).click()
                await page.get_by_role("link", name="개인정보관리(상세)").click()
                await asyncio.sleep(2)
                iframe_handle = await page.wait_for_selector("iframe[name=\"II_IndyInfo\"]")
                iframe = await iframe_handle.content_frame()
                table = await iframe.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_3":
                await page.get_by_role("link", name="마이페이지").click()
                await page.get_by_role("link", name="개인정보관리", exact=True).click()
                await page.get_by_role("link", name="비밀번호 변경").click()
                await asyncio.sleep(2)
                iframe_handle = await page.wait_for_selector("iframe[name=\"II_IndyInfo\"]")
                iframe = await iframe_handle.content_frame()
                table = await iframe.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_4":
                await page.get_by_role("link", name="마이페이지").click()
                await page.get_by_role("link", name="개인정보관리", exact=True).click()
                await page.get_by_role("link", name="인증이메일 등록").click()
                await asyncio.sleep(2)
                iframe_handle = await page.wait_for_selector("iframe[name=\"II_IndyInfo\"]")
                iframe = await iframe_handle.content_frame()
                table = await iframe.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_5":
                await page.get_by_role("link", name="마이페이지").click()
                await page.get_by_role("link", name="개인정보관리", exact=True).click()
                await page.get_by_role("link", name="인증핸드폰 등록").click()
                await asyncio.sleep(2)
                iframe_handle = await page.wait_for_selector("iframe[name=\"II_IndyInfo\"]")
                iframe = await iframe_handle.content_frame()
                table = await iframe.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MYPAGE_6":
                await page.get_by_role("link", name="마이페이지").click()
                await page.get_by_role("link", name="기관정보관리").first.click()
                await asyncio.sleep(2)
                await page.frame_locator("iframe[name=\"member\"]").get_by_role("link", name="(주)넥스트키").click()
                await asyncio.sleep(2)
                iframe_handle = await page.wait_for_selector("iframe[name=\"member\"]")
                iframe = await iframe_handle.content_frame()
                table = await iframe.query_selector(".tbl_type01")
                table_data = []
                tr_elements = await table.query_selector_all('tr')

                for tr in tr_elements:
                    td = await tr.query_selector_all('td')
                    row_data = [await t.inner_text() for t in td]
                    table_data.append(row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

    return HttpResponse("성공!")

async def set_extra_http_headers(page):
    await page.set_extra_http_headers({
        "Connection" : "keep-alive",
        "Cache-Control" : "max-age=0",
        "sec-ch-ua-mobile" : "?0",
        "DNT" : "1",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site" : "none",
        "Sec-Fetch-Mode" : "navigate",
        "Sec-Fetch-User" : "?1",
        "Sec-Fetch-Dest" : "document",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "ko-KR,ko;q=0.9",
        "Referer": "https://www.smtech.go.kr/"
    })
    return page

def open_page(request):
    t = request.GET['type']
    html_content = Data.objects.get(content_type=t)
    if html_content:
        return HttpResponse(html_content.content)
    else:
        return HttpResponse("No HTML content available")
# Create your views here.
