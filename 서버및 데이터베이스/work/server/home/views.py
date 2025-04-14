import json
import time
import asyncio

from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Model
from .models import Data

from playwright.async_api import async_playwright, expect

async def getMainPage(request):
    if request.method == "GET":
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            page = await set_extra_http_headers(page)
            await page.goto('https://www.iris.go.kr/main.do')
            await asyncio.sleep(5)
            new_data = Data()
            new_data.content = await page.content()
            new_data.content = new_data.content.replace("/resources/css","https://www.iris.go.kr/resources/css").replace("/resources/js","https://www.iris.go.kr/resources/js")
            new_data.content_type = "main"
            new_data.save()

            #for strong in await page.locator('strong').all():
            #    print(await strong.text_content())
            await page.close()

    elif request.method == "POST":
        data = json.loads(request.body)
        async with async_playwright() as p:
            site = data['site']
            site_type = data['type']
            browser = await p.chromium.launch()
            page = await browser.new_page()
            page = await set_extra_http_headers(page)
            await page.goto(site)
            await asyncio.sleep(5)
            new_data = Data()
            new_data.content = await page.content()
            new_data.content = new_data.content.replace("/resources/css","https://www.iris.go.kr/resources/css").replace("/resources/js","https://www.iris.go.kr/resources/js")
            new_data.content_type = site_type
            new_data.save()

            #for strong in await page.locator('strong').all():
            #    print(await strong.text_content())
            await page.close()


    return HttpResponse("성공!")

async def getRnDPage(request):
    print("동작")
    if request.method == "GET":
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            page = await set_extra_http_headers(page)
            new_data = Data()
            new_data.content = await page.content()
            new_data.content = new_data.content.replace("/resources/css","https://www.iris.go.kr/resources/css").replace("/resources/js","https://www.iris.go.kr/resources/js")
            new_data.content_type = "main"
            new_data.save()

            #for strong in await page.locator('strong').all():
            #    print(await strong.text_content())
            await page.close()

    elif request.method == "POST":
        data = json.loads(request.body)
        site_type = data['type']
        account = data['id']
        password = data['pw']
        return_data = []
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1920, "height": 1080})
            page = await set_extra_http_headers(page)
            await page.goto("https://www.iris.go.kr/mbrs/entr/loginForm.do")
            await page.fill('#username', account)
            await page.fill('#password', password)
            await page.get_by_role("button", name="로그인").click()
            await page.get_by_role("cell", name="주식회사 오디엔").click()
            await page.get_by_role("button", name="선택").click()
            async with page.expect_popup() as page1_info:
                await page.get_by_role("link", name="R&D 업무포털").click()
            page1 = await page1_info.value
            await page1.wait_for_load_state("domcontentloaded")
            if site_type == "MAIN_1":
                await page.get_by_role("link", name="사업관련 서식·자료", exact=True).click()
                await page.wait_for_load_state("networkidle")
                #await asyncio.sleep(2)
                table_data = []
                current_page_number = 1
                while True:
                    tbody = await page.query_selector("#listView")
                    if not tbody:
                        break
                    rows = await tbody.query_selector_all("tr")
                    for row in rows:
                        cells = await row.query_selector_all("td")
                        row_data = {}
                        for index, cell in enumerate(cells):
                            key = f"column_{index + 1}"
                            text = await cell.text_content()
                            #row_data.append(text.strip())
                            row_data[key] = text.strip()
                        table_data.append(row_data)
                    current_page = await page.query_selector(".paginate .page_now strong")
                    if not current_page:
                        break
                    current_page_number = int(await current_page.text_content())
                    next_page_number = current_page_number + 1
                    #next_page_button = await page.query_selector(f".paginate a[title='{next_page_number}페이지']")
                    next_page_button = await page.query_selector(f".paginate a[onclick='({next_page_number}); return false;']")
                    if next_page_button:
                        await next_page_button.click()
                        await page.wait_for_load_state("networkidle")
                    else:
                        break
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "MAIN_2":
                async with page.expect_popup() as page2_info:
                    await page.get_by_text("국가R&D법령·매뉴얼").click()
                page2 = await page2_info.value
                await page2.wait_for_load_state("networkidle")
                table_data = []
                current_page_number = 1

                while True:
                    tbodies = await page2.query_selector_all("table.basic_list.t_percentage tbody")
                    if not tbodies:
                        break
                    for tbody in tbodies:
                        rows = await tbody.query_selector_all("tr")
                        for row in rows:
                            cells = await row.query_selector_all("td, th")
                            row_data = {}
                            for index, cell in enumerate(cells):
                                key = f"column_{index + 1}"
                                text = await cell.text_content()
                                #row_data.append(text.strip())
                                row_data[key] = text.strip()
                            table_data.append(row_data)

                    next_page_number = current_page_number + 1
                    next_page_button = await page2.query_selector(f".pagination a[href*='pageIndex={next_page_number}']")
                    if next_page_button:
                        await next_page_button.click()
                        await page2.wait_for_load_state("networkidle")
                        current_page_number = next_page_number
                    else:
                        break
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type +  "_1"
                new_data.save()

                await page2.get_by_role("link", name="입법·행정예고").click()
                await page2.wait_for_load_state("networkidle")
                table_data = []
                current_page_number = 1

                while True:
                    tbodies = await page2.query_selector_all("table.basic_list tbody")
                    if not tbodies:
                        break
                    for tbody in tbodies:
                        rows = await tbody.query_selector_all("tr")
                        for row in rows:
                            cells = await row.query_selector_all("td, th")
                            row_data = []
                            for cell in cells:
                                text = await cell.text_content()
                                row_data.append(text.strip())
                            table_data.append(row_data)

                    next_page_number = current_page_number + 1
                    next_page_button = await page2.query_selector(f".pagination a[href*='pageIndex={next_page_number}']")
                    if next_page_button:
                        await next_page_button.click()
                        await page2.wait_for_load_state("networkidle")
                        current_page_number = next_page_number
                    else:
                        break
                new_data1 = Data()
                new_data1.content = table_data
                new_data1.content_type = site_type +  "_2"
                new_data1.save()

                await page2.get_by_role("link", name="지침·기타").click()
                await page2.wait_for_load_state("networkidle")
                table_data = []
                current_page_number = 1

                while True:
                    tbodies = await page2.query_selector_all("table.basic_list tbody")
                    if not tbodies:
                        break
                    for tbody in tbodies:
                        rows = await tbody.query_selector_all("tr")
                        for row in rows:
                            cells = await row.query_selector_all("td, th")
                            row_data = []
                            for cell in cells:
                                text = await cell.text_content()
                                row_data.append(text.strip())
                            table_data.append(row_data)

                    next_page_number = current_page_number + 1
                    next_page_button = await page2.query_selector(f".pagination a[href*='pageIndex={next_page_number}']")
                    if next_page_button:
                        await next_page_button.click()
                        await page2.wait_for_load_state("networkidle")
                        current_page_number = next_page_number
                    else:
                        break
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type +  "_3"
                new_data2.save()
            elif site_type == "IRIS_2":
                await page.click('a.btn_user')
                await page.wait_for_load_state("networkidle")

                data = {
                    "_csrf": await page.get_attribute('input[name="_csrf"]', 'value'),
                    "prhfAutcWaySe": await page.get_attribute('input[name="prhfAutcWaySe"]', 'value'),
                    "rnmAutcCiVl": await page.get_attribute('input[name="rnmAutcCiVl"]', 'value'),
                    "rnmAutcDiVl": await page.get_attribute('input[name="rnmAutcDiVl"]', 'value'),
                    "nrscrNo": await page.get_attribute('input[name="nrscrNo"]', 'value'),
                    "orgnBlngOrgnIdAsis": await page.get_attribute('input[name="orgnBlngOrgnIdAsis"]', 'value'),
                    "mbrNmAsis": await page.get_attribute('input[name="mbrNmAsis"]', 'value'),
                    "mbrSttSe": await page.get_attribute('input[name="mbrSttSe"]', 'value'),
                    "gndrSeAsis": await page.get_attribute('input[name="gndrSeAsis"]', 'value'),
                    "celNoAsis": await page.get_attribute('input[name="celNoAsis"]', 'value'),
                    "birthDeAsis": await page.get_attribute('input[name="birthDeAsis"]', 'value'),
                    "nationalAsis": await page.get_attribute('input[name="nationalAsis"]', 'value'),
                    "orgnListArr": await page.get_attribute('input[name="orgnListArr"]', 'value'),
                    "sorgnNumChk2": await page.get_attribute('input[name="sorgnNumChk2"]', 'value'),
                    "lginId": await page.get_attribute('input[name="lginId"]', 'value'),
                    "national": await page.get_attribute('select[name="national"]', 'value'),
                    "mbrNm": await page.get_attribute('input[name="mbrNm"]', 'value'),
                    "engMbrNm": await page.get_attribute('input[name="engMbrNm"]', 'value'),
                    "birthDe": await page.get_attribute('input[name="birthDe"]', 'value'),
                    "gndrSe": await page.get_attribute('input[name="gndrSe"]:checked', 'value'),
                    "celNo": await page.get_attribute('input[name="celNo"]', 'value'),
                    "emailAd": await page.get_attribute('input[name="emailAd"]', 'value'),
                    "nrsrcNo": await page.get_attribute('input[name="nrsrcNo"]', 'value'),
                    "natSe": await page.get_attribute('input[name="natSe"]', 'value'),
                    "radioNatSe": await page.get_attribute('input[name="radioNatSe"]:checked', 'value'),
                    "ctinfoZno": await page.get_attribute('input[name="ctinfoZno"]', 'value'),
                    "ctinfoZnoAd": await page.get_attribute('input[name="ctinfoZnoAd"]', 'value'),
                    "ctinfoDtlAd": await page.get_attribute('input[name="ctinfoDtlAd"]', 'value'),
                    "nttrRcvYn": await page.get_attribute('input[name="nttrRcvYn"]:checked', 'value'),
                    "nttrRcvInfo1": await page.is_checked('input[name="nttrRcvInfo1"]'),
                    "nttrRcvInfo2": await page.is_checked('input[name="nttrRcvInfo2"]'),
                    "nttrRcvInfo3": await page.is_checked('input[name="nttrRcvInfo3"]')
                }

                new_data = Data()
                new_data.content = data
                new_data.content_type = site_type + "_1"
                new_data.save()



            elif site_type == "IRIS_4":
                await page.get_by_role("link", name="알림·고객", exact=True).click()
                await page.wait_for_load_state("networkidle")

                #await asyncio.sleep(2)
                table_data = []
                while True:
                    tbody = await page.query_selector("#listView")
                    if not tbody:
                        break
                    rows = await tbody.query_selector_all("tr")
                    for row in rows:
                        cells = await row.query_selector_all("td")
                        #row_data = {}
                        #for index, cell in enumerate(cells):
                        #    key = f"column_{index + 1}"
                        #    text = await cell.text_content()
                        #    row_data[key] = text.strip() if text else ""
                        #table_data.append(row_data)
                        row_data = {
                            "num": (await cells[0].text_content()).strip(),
                            "title": (await cells[1].text_content()).strip(),
                            "file": (await cells[2].text_content()).strip(),
                            "reg_date": (await cells[3].text_content()).strip(),
                            "edit_date": (await cells[4].text_content()).strip(),
                            "views": (await cells[5].text_content()).strip(),
                        }
                        Model = apps.get_model('home', 'Iris_4_1')
                        obj, created = Model.objects.update_or_create(
                            title=row_data["title"],
                            defaults={
                                "num": row_data["num"],
                                "file": row_data["file"],
                                "reg_date": row_data["reg_date"],
                                "edit_date": row_data["edit_date"],
                                "views": row_data["views"],
                            }
                        )
                    current_page = await page.query_selector(".paginate .page_now strong")
                    if not current_page:
                        break
                    current_page_number = int(await current_page.text_content())
                    next_page_number = current_page_number + 1
                    #next_page_button = await page.query_selector(f".paginate a[title='{next_page_number}페이지']")
                    next_page_button = await page.query_selector(f".paginate a[onclick='({next_page_number}); return false;']")
                    if next_page_button:
                        await next_page_button.click()
                        await page.wait_for_load_state("networkidle")
                    else:
                        break
                #new_data = Data()
                #new_data.content = table_data
                #new_data.content_type = site_type +  "_1"
                #new_data.save()


                await page.get_by_role("link", name="R&D제도").click()
                await page.wait_for_load_state("networkidle")
                table_data = []
                while True:
                    tbody = await page.query_selector("#listView")
                    if not tbody:
                        break
                    rows = await tbody.query_selector_all("tr")
                    for row in rows:
                        cells = await row.query_selector_all("td")
                        #row_data = {}
                        #for index, cell in enumerate(cells):
                        #    key = f"column_{index + 1}"
                        #    text = await cell.text_content()
                        #    row_data[key] = text.strip() if text else ""
                        #table_data.append(row_data)
                        row_data = {
                            "num": (await cells[0].text_content()).strip(),
                            "title": (await cells[1].text_content()).strip(),
                            "file": (await cells[2].text_content()).strip(),
                            "reg_date": (await cells[3].text_content()).strip(),
                            "edit_date": (await cells[4].text_content()).strip(),
                            "views": (await cells[5].text_content()).strip(),
                        }
                        Model = apps.get_model('home', 'Iris_4_2')
                        obj, created = Model.objects.update_or_create(
                            title=row_data["title"],
                            defaults={
                                "num": row_data["num"],
                                "file": row_data["file"],
                                "reg_date": row_data["reg_date"],
                                "edit_date": row_data["edit_date"],
                                "views": row_data["views"],
                            }
                        )
                    current_page = await page.query_selector(".paginate .page_now strong")
                    if not current_page:
                        break
                    current_page_number = int(await current_page.text_content())
                    next_page_number = current_page_number + 1
                    #next_page_button = await page.query_selector(f".paginate a[title='{next_page_number}페이지']")
                    next_page_button = await page.query_selector(f".paginate a[onclick='({next_page_number}); return false;']")
                    if next_page_button:
                        await next_page_button.click()
                        await page.wait_for_load_state("networkidle")
                    else:
                        break
                #new_data1 = Data()
                #new_data1.content = table_data
                #new_data1.content_type = site_type + "_2"
                #new_data1.save()
                await page.get_by_role("link", name="시스템·서비스").click()
                await page.wait_for_load_state("networkidle")
                table_data = []
                while True:
                    tbody = await page.query_selector("#listView")
                    if not tbody:
                        print(f"Tbody error")
                        break
                    rows = await tbody.query_selector_all("tr")
                    for row in rows:
                        cells = await row.query_selector_all("td")
                        row_data = {
                            "num": (await cells[0].text_content()).strip(),
                            "title": (await cells[1].text_content()).strip(),
                            "file": (await cells[2].text_content()).strip(),
                            "reg_date": (await cells[3].text_content()).strip(),
                            "edit_date": (await cells[4].text_content()).strip(),
                            "views": (await cells[5].text_content()).strip(),
                        }
                        Model = apps.get_model('home', 'Iris_4_3')
                        obj, created = Model.objects.update_or_create(
                            title=row_data["title"],
                            defaults={
                                "num": row_data["num"],
                                "file": row_data["file"],
                                "reg_date": row_data["reg_date"],
                                "edit_date": row_data["edit_date"],
                                "views": row_data["views"],
                            }
                        )
                    current_page = await page.query_selector(".paginate .page_now strong")
                    if not current_page:
                        break
                    current_page_number = int(await current_page.text_content())
                    next_page_number = current_page_number + 1
                    #next_page_button = await page.query_selector(f".paginate a[title='{next_page_number}페이지']")
                    next_page_button = await page.query_selector(f".paginate a[onclick='({next_page_number}); return false;']")
                    if next_page_button:
                        await next_page_button.click()
                        await page.wait_for_load_state("networkidle")
                    else:
                        break
                #new_data2 = Data()
                #new_data2.content = table_data
                #new_data2.content_type = site_type + "_3"
                #new_data2.save()
            elif site_type == "IRIS_6":
                await page.get_by_role("link", name="국가연구자 번호찾기").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector("#search_result_list")
                rows = await page.query_selector_all("#search_result_list tr")
                table_data = []

                for row in rows:
                    cells = await row.query_selector_all("td")
                    #row_data = {}
                    #row_data = [await cell.inner_text() for cell in cells]
                    #for index, cell in enumerate(cells):
                    #        key = f"column_{index + 1}"
                    #        text = await cell.inner_text()
                            #row_data.append(text.strip())
                    #        row_data[key] = text.strip() if text else ""
                    #table_data.append(row_data)
                    Model = apps.get_model('home', 'Iris_6')
                    obj, created = Model.objects.update_or_create(
                        number=(await cells[0].inner_text()).strip(),
                        defaults={
                            "status": (await cells[1].inner_text()).strip(),
                        }
                    )
            elif site_type == "IRIS_8":
                await page1.get_by_role("button", name="마이R&D").click()
                await page1.get_by_role("button", name="0").first.click()
                await page1.get_by_label("검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                while True:
                    grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdBllt.body.gridrow_']"
                    await page1.wait_for_selector(grid_selector)
                    rows = await page1.query_selector_all(grid_selector)
                    for row in rows:
                        row_data = {}
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        for index, cell in enumerate(cells):
                            key = f"column_{index + 1}"
                            text = await cell.text_content()
                            #row_data.append(text.strip())
                            row_data[key] = text.strip() if text else ""
                        table_data.append(row_data)
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPaging.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_9":
                await page1.get_by_role("button", name="마이R&D").click()
                await page1.get_by_role("button", name="0").nth(1).click()
                await page1.wait_for_load_state("domcontentloaded")
                Model = apps.get_model('home', 'Iris_9')
                Model.objects.filter(account=account).delete()
                while True:
                    grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdSend.body.gridrow_']"
                    await page1.wait_for_selector(grid_selector)
                    rows = await page1.query_selector_all(grid_selector)
                    for row in rows:
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        if cells:
                            Model.objects.create(
                                account= account,
                                group= "",
                                send_work= (await cells[0].inner_text()).strip(),
                                title= (await cells[1].inner_text()).strip(),
                                send_date= (await cells[2].inner_text()).strip(),
                                receive_date= (await cells[3].inner_text()).strip(),
                            )
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPaging.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
            elif site_type == "IRIS_10":
                await page1.get_by_role("button", name="마이R&D").click()
                await page1.get_by_role("button", name="0").nth(2).click()
                time.sleep(5)
                new_data = Data()
                new_data.content = await page1.content()
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_11":
                await page1.get_by_role("button", name="마이R&D").click()
                await page1.get_by_role("button", name="0").nth(2).click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                while True:
                    grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdBllt.body.gridrow_']"
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Selector not found: {e}")
                        break
                    rows = await page1.query_selector_all(grid_selector)
                    for row in rows:
                        row_data = []
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        for index, cell in enumerate(cells):
                            key = f"column_{index + 1}"
                            text = await cell.text_content()
                            row_data[key] = text.strip() if text else ""
                        table_data.append(row_data)
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPaging.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_15":
                #await page1.get_by_text("과제수행").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
                await page1.get_by_text("(협약용)연구개발계획서제출").click()
                await page1.get_by_title("사업년도").locator("div").nth(2).click()
                await page1.get_by_text("2023년").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                Model = apps.get_model('home', 'Iris_15_1')
                Model2 = apps.get_model('home', 'Iris_15_2')
                Model.objects.filter(account=account).delete()
                Model2.objects.filter(account=account).delete()
                while True:
                    grid_selector_1 = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdAgrt.body.gridrow_']"
                    try:
                        await page1.wait_for_selector(grid_selector_1)
                    except Exception as e:
                        print(f"Grid 1 Selector not found: {e}")
                        break
                    rows = await page1.query_selector_all(grid_selector_1)
                    if not rows:
                        print("No cells found in Grid 1 on this page.")
                        break
                    rows1 = {}
                    for row in rows:
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        if cells:
                            Model.objects.create(
                                account= account,
                                group= "",
                                year= "2023년",
                                assign_class = (await cells[1].text_content()).strip(),
                                res_num = (await cells[2].text_content()).strip(),
                                res_name = (await cells[3].text_content()).strip(),
                                res_group = (await cells[4].text_content()).strip(),
                                res_manager = (await cells[5].text_content()).strip(),
                                res_status = (await cells[6].text_content()).strip(),
                                ass_status = (await cells[7].text_content()).strip(),
                                plan_status = (await cells[8].text_content()).strip(),
                                con_status = (await cells[9].text_content()).strip(),
                                con_execute = (await cells[10].text_content()).strip(),
                            )
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPage.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector_1)

                grid_selector_2 = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdAgrtOrgn.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector_2)
                    rows = await page1.query_selector_all(grid_selector_2)
                    if not rows:
                        print("No cells found in Grid 2 on this page.")
                    for row in rows:
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        if cells:
                            Model2.objects.create(
                                account= account,
                                group= "",
                                year= "2023년",
                                app_role = (await cells[0].text_content()).strip(),
                                res_name = (await cells[1].text_content()).strip(),
                                manager_num = (await cells[2].text_content()).strip(),
                                res_manager = (await cells[3].text_content()).strip(),
                                agent = (await cells[4].text_content()).strip(),
                                work_manager = (await cells[5].text_content()).strip(),
                                detail = (await cells[6].text_content()).strip(),
                            )
                except Exception as e:
                    print(f"Grid 2 Selector not found: {e}")

            elif site_type == "IRIS_17":
                #await page1.get_by_text("과제수행").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
                await page1.get_by_title("개인정보연구윤리동의").locator("div").click()
                await page1.get_by_label("전체", exact=True).click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdPrvc.body.gridrow_']"
                Model = apps.get_model('home', 'Iris_17')
                Model.objects.filter(account=account).delete()
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 1 Selector not found: {e}")
                    rows = await page1.query_selector_all(grid_selector)
                    if not rows:
                        print("No cells found in Grid 1 on this page.")
                        break
                    for row in rows:
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        if cells:
                            Model.objects.create(
                                account= account,
                                group= "",
                                assign_class = (await cells[1].text_content()).strip(),
                                res_num = (await cells[2].text_content()).strip(),
                                res_name = (await cells[3].text_content()).strip(),
                                res_group = (await cells[4].text_content()).strip(),
                                role = (await cells[5].text_content()).strip(),
                                researcher = (await cells[6].text_content()).strip(),
                                start_date = (await cells[7].text_content()).strip(),
                                end_date = (await cells[8].text_content()).strip(),
                                agree_date = (await cells[9].text_content()).strip(),
                                consent_form = (await cells[10].text_content()).strip(),
                            )
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPage.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
            elif site_type == "IRIS_18":
                #await page1.get_by_text("과제수행").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
                await page1.get_by_text("협약신청").nth(1).click()
                await page1.get_by_title("사업년도").locator("div").nth(2).click()
                await page1.get_by_text("2023년").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                table_data_1 = []
                table_data_2 = []

                while True:
                    grid1_selector_prefix = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdAgrt.body.gridrow_']"
                    await page1.wait_for_selector(grid1_selector_prefix)
                    cells1 = await page1.query_selector_all(grid1_selector_prefix)
                    if cells1:
                        rows1 = {}
                        for cell in cells1:
                            row_id = await cell.get_attribute("id")
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                        #for row_index in sorted(rows1.keys()):
                        #    table_data_1.append(rows1[row_index])
                        for row_index, row_data in sorted(rows1.items()):
                            table_data_1.append({"row_index": row_index, "row_data": row_data})

                        for row_index in sorted(rows1.keys()):
                            cell_id = f"mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdAgrt.body.gridrow_{row_index}.cell_0_0"
                            row_cell = await page1.query_selector(f"div[id='{cell_id}']")
                            if row_cell:
                                await row_cell.click()
                                await page1.wait_for_load_state("domcontentloaded")
                                grid2_selector_prefix = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdAgrtOrgn.body.gridrow_']"
                                await page1.wait_for_selector(grid2_selector_prefix)
                                cells2 = await page1.query_selector_all(grid2_selector_prefix)
                                if cells2:
                                    rows2 = {}
                                    for cell in cells2:
                                        row_id = await cell.get_attribute("id")
                                        row_index = row_id.split('_')[1]
                                        if row_index not in rows2:
                                            rows2[row_index] = []
                                        text = await cell.text_content()
                                        rows2[row_index].append(text.strip())
                                    #for row_index in sorted(rows2.keys()):
                                    #    table_data_2.append([row_index, rows2[row_index]])
                                    for row_index, row_data in sorted(rows2.items()):
                                        table_data_2.append({"row_index": row_index, "row_data": row_data})
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPage.form.divPage.form.btnNex']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        break

                    await next_page_button.click()
                    await page1.wait_for_selector(f"div[id^='{grid1_selector_prefix}.gridrow_']")
                #table_data.append(table_data_1)
                #table_data.append(table_data_2)
                table_data = {"grid_1_data": table_data_1, "grid_2_data": table_data_2}

                new_data = Data()
                #new_data.content = await page1.content()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_19":
                #await page1.get_by_text("과제수행").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
                await page1.get_by_text("부담금 납부현황").click()
                await page1.locator("[id=\"mainframe\\.baseFrame\\.form\\.divWork\\.form\\.divCenter\\.form\\.divWork\\.form\\.divSearch\\.form\\.divSearchComm\\.form\\.divSearch\\.form\\.cboSBsnsYy\\.dropbutton\"]").click()
                await page1.get_by_text("2023년").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_data = {}
                while True:
                    grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPageSbjt.form.grdSbjt.body.gridrow_']"
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 1 Selector not found: {e}")
                        #table_data.append([1, "None"])
                        table_data.append({"row_index": None, "row_data": None, "sub_grids": []})
                    cells1 = await page1.query_selector_all(grid_selector)
                    if not cells1:
                        print("No cells found in Grid 1 on this page.")
                        break
                    rows = []
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            #if row_index not in rows1:
                            #    rows1[row_index] = []
                            text = await cell.text_content()
                            #rows1[row_index].append(text.strip())
                            rows.append({"row_index": row_index, "row_text": text.strip()})
                    #for row_index in sorted(rows1.keys()):
                    #    table_data.append([row_index, rows1[row_index]])
                    for row in rows:
                        row_index = row["row_index"]

                        await cells1[int(row_index)].click()
                        #sub_grid_data = []
                        sub_grids = []
                        for sub_grid_selector in [
                            "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divOrgn.form.grdOrgn.body.gridrow_']",
                            "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPlan.form.grdPlan.body.gridrow_']",
                            "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divRcps.form.grdRcps.body.gridrow_']"
                        ]:
                            try:
                                await page1.wait_for_selector(sub_grid_selector, timeout=5000)
                                sub_cells = await page1.query_selector_all(sub_grid_selector)
                                sub_rows = []
                                for sub_cell in sub_cells:
                                    sub_row_id = await sub_cell.get_attribute("id")
                                    if ':text' not in sub_row_id:
                                        #sub_row_index = sub_row_id.split('gridrow_')[1]
                                        #if sub_row_index not in sub_rows:
                                        #    sub_rows[sub_row_index] = []
                                        col_index = sub_row_id.split('.')[-1]
                                        sub_text = await sub_cell.text_content()
                                        #sub_rows[sub_row_index].append(sub_text.strip())
                                        sub_rows.append({"column": col_index, "value": sub_text.strip()})
                                #sub_grid_data.append({sub_row_index: sub_rows[sub_row_index] for sub_row_index in sorted(sub_rows.keys(), key=int)})
                                sub_grids.append({"sub_rows": sub_rows})
                            except Exception as e:
                                print(f"Sub Grid Selector not found: {e}")
                                #sub_grid_data.append({})
                                sub_grids.append({"sub_rows": []})
                        #grid_data[row_index] = sub_grid_data
                        #table_data.append([row_index, grid_data[row_index]])
                        row["sub_grids"] = sub_grids
                        table_data.append(row)


                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPageSbjt.form.divPage.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)

                #await page.screenshot(path="test.png", full_page= True)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_20":
                #await page1.get_by_text("과제수행").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
                await page1.get_by_text("(기관일괄)협약변경신청").click()
                await page1.wait_for_load_state("domcontentloaded")
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabOrgnInfo.Tabpage1.form.grdSbjt.body.gridrow_']"
                Model = apps.get_model('home', 'Iris_20_1')
                Model.objects.filter(account=account).delete()
                Model2 = apps.get_model('home', 'Iris_20_2')
                Model2.objects.filter(account=account).delete()
                Model3 = apps.get_model('home', 'Iris_20_3')
                Model3.objects.filter(account=account).delete()
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                rows = await page1.query_selector_all(grid_selector)
                if not rows:
                    print("No cells found in Grid 1 on this page.")
                for row in rows:
                    cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                    print(cells)
                    if cells:
                        Model.objects.create(
                            account= account,
                            group= "",
                            role = (await cells[0].text_content()).strip(),
                            org_name = (await cells[1].text_content()).strip(),
                            org_type = (await cells[2].text_content()).strip(),
                            researcher_num = (await cells[3].text_content()).strip(),
                            agent = (await cells[4].text_content()).strip(),
                            assign_class = (await cells[5].text_content()).strip(),
                            res_num = (await cells[6].text_content()).strip(),
                            res_name = (await cells[7].text_content()).strip(),
                            step = (await cells[8].text_content()).strip(),
                            annual = (await cells[9].text_content()).strip(),
                            res_director = (await cells[10].text_content()).strip(),
                            assign_status = (await cells[11].text_content()).strip(),
                        )
                await page1.get_by_role("tab", name="계좌정보 변경").click()
                await page1.wait_for_load_state("domcontentloaded")
                grid_selector2 = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabOrgnInfo.Tabpage2.form.grdSbjt.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector2)
                except Exception as e:
                    print(f"Grid 2 Selector not found: {e}")
                rows = await page1.query_selector_all(grid_selector2)
                if not rows:
                    print("No cells found in Grid 2 on this page.")
                for row in rows:
                    cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                    if cells:
                        Model2.objects.create(
                            account= account,
                            group= "",
                            assign_class = (await cells[0].text_content()).strip(),
                            res_num = (await cells[1].text_content()).strip(),
                            res_name = (await cells[2].text_content()).strip(),
                            step = (await cells[3].text_content()).strip(),
                            annual = (await cells[4].text_content()).strip(),
                            role = (await cells[5].text_content()).strip(),
                            res_director = (await cells[6].text_content()).strip(),
                            account_num = (await cells[7].text_content()).strip(),
                            assign_status = (await cells[8].text_content()).strip(),
                        )
                await page1.get_by_role("tab", name="연구개발기관 과제지원담당자 변경").click()
                await page1.wait_for_load_state("domcontentloaded")
                grid_selector3 = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabOrgnInfo.Tabpage3.form.grdChrgr.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector3)
                except Exception as e:
                    print(f"Grid 3 Selector not found: {e}")
                rows = await page1.query_selector_all(grid_selector3)
                if not rows:
                    print("No cells found in Grid 3 on this page.")
                for row in rows:
                    cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                    if cells:
                        Model3.objects.create(
                            account= account,
                            group= "",
                            assign_class = (await cells[0].text_content()).strip(),
                            res_num = (await cells[1].text_content()).strip(),
                            res_name = (await cells[2].text_content()).strip(),
                            step = (await cells[3].text_content()).strip(),
                            annual = (await cells[4].text_content()).strip(),
                            role = (await cells[5].text_content()).strip(),
                            res_director = (await cells[6].text_content()).strip(),
                            account_num = (await cells[7].text_content()).strip(),
                            assign_status = (await cells[8].text_content()).strip(),
                        )
            elif site_type == "IRIS_21":
                #await page1.get_by_text("과제수행").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
                await page1.get_by_text("(승인통보)협약변경신청").click()
                await page1.locator("[id=\"mainframe\\.baseFrame\\.form\\.divWork\\.form\\.divCenter\\.form\\.divWork\\.form\\.divSearch\\.form\\.divSearchComm\\.form\\.divSearch\\.form\\.cboSBsnsYy\\.dropbutton\"]").click()
                await page1.get_by_text("2019년").click()
                await page1.get_by_label("검색 검색").click()
                time.sleep(10)
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdAgrtChngObjtList.body.gridrow_']"
                Model = apps.get_model('home', 'Iris_21_1')
                Model.objects.filter(account=account).delete()
                Model2 = apps.get_model('home', 'Iris_21_2')
                Model2.objects.filter(account=account).delete()
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                rows = await page1.query_selector_all(grid_selector)
                if not rows:
                    print("No cells found in Grid 1 on this page.")
                for row in rows:
                    cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                    if cells:
                        Model.objects.create(
                            account= account,
                            group= "",
                            year= "2019년",
                            pro_org_name = (await cells[0].text_content()).strip(),
                            business_year = (await cells[1].text_content()).strip(),
                            step = (await cells[2].text_content()).strip(),
                            annual = (await cells[3].text_content()).strip(),
                            res_num = (await cells[4].text_content()).strip(),
                            res_name = (await cells[5].text_content()).strip(),
                            assign_status = (await cells[6].text_content()).strip(),
                            res_org_name = (await cells[7].text_content()).strip(),
                            res_director = (await cells[8].text_content()).strip(),
                            is_change_req = (await cells[9].text_content()).strip(),
                            status_1 = (await cells[10].text_content()).strip(),
                            status_2 = (await cells[11].text_content()).strip(),
                            status_3 = (await cells[12].text_content()).strip(),
                            status_4 = (await cells[13].text_content()).strip(),
                            status_5 = (await cells[14].text_content()).strip(),
                            status_6 = (await cells[15].text_content()).strip(),
                            status_7 = (await cells[16].text_content()).strip(),
                            status_8 = (await cells[17].text_content()).strip(),
                            status_9 = (await cells[18].text_content()).strip(),
                            status_10 = (await cells[19].text_content()).strip(),
                            status_11 = (await cells[20].text_content()).strip(),
                        )
                grid_selector2 = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divSitu.form.grdAgrtChngPrgSituList.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector2)
                except Exception as e:
                    print(f"Grid 2 Selector not found: {e}")
                rows = await page1.query_selector_all(grid_selector2)
                if not rows:
                    print("No cells found in Grid 2 on this page.")
                for row in rows:
                    cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                    if cells:
                        Model2.objects.create(
                            account= account,
                            group= "",
                            year= "2019년",
                            step = (await cells[0].text_content()).strip(),
                            annual = (await cells[1].text_content()).strip(),
                            change_division = (await cells[2].text_content()).strip(),
                            change_status = (await cells[3].text_content()).strip(),
                            req_status = (await cells[4].text_content()).strip(),
                            req_result = (await cells[5].text_content()).strip(),
                            res_org_name = (await cells[6].text_content()).strip(),
                            requester = (await cells[7].text_content()).strip(),
                            req_date = (await cells[8].text_content()).strip(),
                            is_change_req = (await cells[9].text_content()).strip(),
                            change_req_item = (await cells[10].text_content()).strip(),
                        )

                #for i in range(0, 5):
                #    for n in range(1, 13):
                #        dynamic_div = await page1.query_selector(f'div[id="mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divSitu.form.grdAgrtChngPrgSituList.body.gridrow_{i}.cell_{i}_{n}:text"]')
                #        if dynamic_div:
                #            return_data.append([i, await dynamic_div.inner_text()])
                #        else:
                #            return_data.append([i, "None"])

            elif site_type == "IRIS_22":
                #await page1.get_by_text("과제수행").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
                #await page1.get_by_text("차년도협약변경신청").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.pdivMegaMenu\\.form\\.btnP01542\\:icontext").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdSbjtChngObjtList.body.gridrow_']"
                grid_selector2 = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divSitu.form.grdSbjtChngPrgSituList.body.gridrow_']"
                Model = apps.get_model('home', 'Iris_22_1')
                Model.objects.filter(account=account).delete()
                Model2 = apps.get_model('home', 'Iris_22_2')
                Model2.objects.filter(account=account).delete()
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 1 Selector not found: {e}")
                    rows = await page1.query_selector_all(grid_selector)
                    if not rows:
                        print("No cells found in Grid 1 on this page.")
                        break
                    for row in rows:
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        if cells:
                            Model.objects.create(
                                account= account,
                                group= "",
                                year = "2024년",
                                pro_org_name = (await cells[0].text_content()).strip(),
                                business_year = (await cells[1].text_content()).strip(),
                                step = (await cells[2].text_content()).strip(),
                                annual = (await cells[3].text_content()).strip(),
                                res_num = (await cells[4].text_content()).strip(),
                                res_name = (await cells[5].text_content()).strip(),
                                res_org_name = (await cells[6].text_content()).strip(),
                                res_director = (await cells[7].text_content()).strip(),
                                assign_status = (await cells[8].text_content()).strip(),
                                req_status = (await cells[9].text_content()).strip(),
                            )
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPage.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector2)
                    except Exception as e:
                        print(f"Grid 2 Selector not found: {e}")
                    rows = await page1.query_selector_all(grid_selector2)
                    if not rows:
                        print("No cells found in Grid 2 on this page.")
                    for row in rows:
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        if cells:
                            Model2.objects.create(
                                account= account,
                                group= "",
                                year= "2024년",
                                step = (await cells[0].text_content()).strip(),
                                annual = (await cells[1].text_content()).strip(),
                                change_division = (await cells[2].text_content()).strip(),
                                change_type = (await cells[3].text_content()).strip(),
                                req_status = (await cells[4].text_content()).strip(),
                                req_result = (await cells[5].text_content()).strip(),
                                res_org_name = (await cells[6].text_content()).strip(),
                                requester = (await cells[7].text_content()).strip(),
                                req_date = (await cells[8].text_content()).strip(),
                                detail = (await cells[9].text_content()).strip(),
                            )
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divSituPage.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector2)

            elif site_type == "IRIS_23":
                #await page1.get_by_text("과제수행").click()
                await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
                await page1.get_by_text("직전연차협약변경신청").click()
                await page1.locator("[id=\"mainframe\\.baseFrame\\.form\\.divWork\\.form\\.divCenter\\.form\\.divWork\\.form\\.DivAftrEndAgrtChng\\.form\\.divSearch\\.form\\.divSearchComm\\.form\\.divSearch\\.form\\.cboSBsnsYy\\.dropbutton\"]").click()
                await page1.get_by_text("2023년").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.DivAftrEndAgrtChng.form.grdAgrtChngObjtList.body.gridrow_']"
                grid_selector2 = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.DivAftrEndAgrtChng.form.divSitu.form.grdAgrtChngPrgSituList.body.gridrow_']"
                Model = apps.get_model('home', 'Iris_23_1')
                Model.objects.filter(account=account).delete()
                Model2 = apps.get_model('home', 'Iris_23_2')
                Model2.objects.filter(account=account).delete()
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 1 Selector not found: {e}")
                    rows = await page1.query_selector_all(grid_selector)
                    if not rows:
                        print("No cells found in Grid 1 on this page.")
                        break
                    for row in rows:
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        if cells:
                            Model.objects.create(
                                account= account,
                                group= "",
                                year= "2023년",
                                pro_org_name = (await cells[0].text_content()).strip(),
                                business_year = (await cells[1].text_content()).strip(),
                                step = (await cells[2].text_content()).strip(),
                                annual = (await cells[3].text_content()).strip(),
                                res_num = (await cells[4].text_content()).strip(),
                                res_name = (await cells[5].text_content()).strip(),
                                assign_status = (await cells[6].text_content()).strip(),
                                res_org_name = (await cells[7].text_content()).strip(),
                                res_director = (await cells[8].text_content()).strip(),
                                is_change_req = (await cells[9].text_content()).strip(),
                                is_change_date = (await cells[10].text_content()).strip(),
                                status_1 = (await cells[11].text_content()).strip(),
                                status_2 = (await cells[12].text_content()).strip(),
                                status_3 = (await cells[13].text_content()).strip(),
                                status_4 = (await cells[14].text_content()).strip(),
                                status_5 = (await cells[15].text_content()).strip(),
                                status_6 = (await cells[16].text_content()).strip(),
                                status_7 = (await cells[17].text_content()).strip(),
                                status_8 = (await cells[18].text_content()).strip(),
                                status_9 = (await cells[19].text_content()).strip(),
                                status_10 = (await cells[20].text_content()).strip(),
                                status_11 = (await cells[21].text_content()).strip(),
                            )
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.DivAftrEndAgrtChng.form.divPage.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector2)
                    except Exception as e:
                        print(f"Grid 2 Selector not found: {e}")
                    rows = await page1.query_selector_all(grid_selector2)
                    if not rows:
                        print("No cells found in Grid 2 on this page.")
                    for row in rows:
                        cells = await row.query_selector_all("div[class^='GridCellControl cell']")
                        if cells:
                            Model2.objects.create(
                                account= account,
                                group= "",
                                year= "2023년",
                                step = (await cells[0].text_content()).strip(),
                                annual = (await cells[1].text_content()).strip(),
                                change_division = (await cells[2].text_content()).strip(),
                                change_status = (await cells[3].text_content()).strip(),
                                req_status = (await cells[4].text_content()).strip(),
                                req_result = (await cells[5].text_content()).strip(),
                                res_org_name = (await cells[6].text_content()).strip(),
                                requester = (await cells[7].text_content()).strip(),
                                req_date = (await cells[8].text_content()).strip(),
                                change_req_item = (await cells[9].text_content()).strip(),
                            )
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.DivAftrEndAgrtChng.form.divSituPage.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector2)
            elif site_type == "IRIS_24":
                await page1.get_by_text("과제수행").click()
                await page1.get_by_text("연구비 지급현황").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdRechctPaySbjtInfoList.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=40000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([0, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_25":
                await page1.get_by_text("과제수행").click()
                await page1.get_by_text("단계 이월금 신청").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_26":
                await page1.get_by_text("과제수행").click()
                await page1.get_by_text("연구시설장비 진행현황").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdEtubPgstList.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=60000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                        sub_grid_data = []
                        await cells1[int(row_index)].click()
                        sub_grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdEtubMtrsList.body.gridrow_']"
                        try:
                            await page1.wait_for_selector(sub_grid_selector, timeout=5000)
                            sub_cells = await page1.query_selector_all(sub_grid_selector)
                            sub_rows = {}
                            for sub_cell in sub_cells:
                                sub_row_id = await sub_cell.get_attribute("id")
                                if ':text' not in sub_row_id and '.cell' not in sub_row_id:
                                    sub_row_index = sub_row_id.split('gridrow_')[1]
                                    if sub_row_index not in sub_rows:
                                        sub_rows[sub_row_index] = []
                                    sub_text = await sub_cell.text_content()
                                    sub_rows[sub_row_index].append(sub_text.strip())
                            sub_grid_data.append({sub_row_index: sub_rows[sub_row_index] for sub_row_index in sorted(sub_rows.keys(), key=int)})
                        except Exception as e:
                            print(f"Sub Grid Selector not found: {e}")
                            sub_grid_data.append({})
                    table_data.append([row_index, sub_grid_data])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_27":
                await page1.get_by_text("과제수행").click()
                await page1.get_by_text("성과등록").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdFrutSbjtList.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                        sub_grid_data = []
                        await cells1[int(row_index)].click()
                        sub_grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabFrutSbjtIdx.Tabpage1.form.grdFrutIdxOfSbjtList.body.gridrow_']"
                        try:
                            await page1.wait_for_selector(sub_grid_selector, timeout=5000)
                            sub_cells = await page1.query_selector_all(sub_grid_selector)
                            sub_rows = {}
                            for sub_cell in sub_cells:
                                sub_row_id = await sub_cell.get_attribute("id")
                                if ':text' not in sub_row_id and '.cell' not in sub_row_id:
                                    sub_row_index = sub_row_id.split('gridrow_')[1]
                                    if sub_row_index not in sub_rows:
                                        sub_rows[sub_row_index] = []
                                    sub_text = await sub_cell.text_content()
                                    sub_rows[sub_row_index].append(sub_text.strip())
                            sub_grid_data.append({sub_row_index: sub_rows[sub_row_index] for sub_row_index in sorted(sub_rows.keys(), key=int)})
                        except Exception as e:
                            print(f"Sub Grid Selector not found: {e}")
                            sub_grid_data.append({})
                    table_data.append([row_index, sub_grid_data])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_28":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_text("정산결과 조회").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_29":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_title("이의신청", exact=True).locator("div").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdRxmneRqsSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_30":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_text("기술실시결과 제출").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdTfeeRsltSbjtSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_31":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_text("청년고용 감면신청").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_32":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_text("청년고용 정보 및 실적제출").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_33":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_text("종료 후 성과소유기관 변경 신청").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_34":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_text("(징수)기술료 사용실적 보고서 제출").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdTfeeSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_35":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_text("(비징수)기술료 사용실적 보고서 제출").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdTfeeUsePfmcRptpNonDutySbmtSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_36":
                await page1.get_by_text("사후관리").click()
                await page1.get_by_text("성과활용보고서 등록").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdFrutSbjtList.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                        sub_grid_data = []
                        await cells1[int(row_index)].click()
                        sub_grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabFrutSbjtIdx.Tabpage1.form.grdFrutIdxOfSbjtList.body.gridrow_']"
                        try:
                            await page1.wait_for_selector(sub_grid_selector, timeout=5000)
                            sub_cells = await page1.query_selector_all(sub_grid_selector)
                            sub_rows = {}
                            for sub_cell in sub_cells:
                                sub_row_id = await sub_cell.get_attribute("id")
                                if ':text' not in sub_row_id and '.cell' not in sub_row_id:
                                    sub_row_index = sub_row_id.split('gridrow_')[1]
                                    if sub_row_index not in sub_rows:
                                        sub_rows[sub_row_index] = []
                                    sub_text = await sub_cell.text_content()
                                    sub_rows[sub_row_index].append(sub_text.strip())
                            sub_grid_data.append({sub_row_index: sub_rows[sub_row_index] for sub_row_index in sorted(sub_rows.keys(), key=int)})
                        except Exception as e:
                            print(f"Sub Grid Selector not found: {e}")
                            sub_grid_data.append({})
                    table_data.append([row_index, sub_grid_data])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_37":
                await page1.get_by_text("과제평가", exact=True).click()
                await page1.get_by_text("보고서제출(연차/단계/최종)").click()
                #await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_38":
                await page1.get_by_text("과제평가", exact=True).click()
                await page1.get_by_title("수행보고 자료제출").locator("div").click()
                await page1.get_by_label("검색 버튼 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_39":
                await page1.get_by_text("과제평가", exact=True).click()
                await page1.get_by_text("최종보고서 비공개 요청").click()
                await page1.get_by_label("검색 버튼 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_40":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("기술료 납부안내 조회").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdTfeePaymGuidInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_41":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("회수금 납부안내 조회").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdEcamPaymGuidInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_42":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("환수금 납부안내 조회").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdRdptAmtPaymGuidInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_43":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("제재부가금 납부안내 조회").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdSncamtPaymGuidInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_44":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("기술료 납부변경 신청").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdPaymChngSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=80000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_45":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("회수금 납부변경 신청").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdPaymChngSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=80000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_46":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("기술료 납부현황").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdTfeePaymSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=5000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_47":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("회수금 납부현황").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdEcamPaymSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=20000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_48":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("환수금 납부현황").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdRdptAmtPaymSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=10000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_49":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("제재부가금 납부현황").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdSncamtPaymSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=10000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_50":
                await page1.get_by_text("납부", exact=True).click()
                await page1.get_by_text("증서 현황").click()
                await page1.get_by_label("검색 검색").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdCertSituInfo.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector, timeout=80000)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_51":
                await page1.get_by_text("R&D 고객센터").click()
                await page1.get_by_text("공지사항").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdBllt.body.gridrow_']"
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 1 Selector not found: {e}")
                        table_data.append([0, "None"])
                        break
                    cells1 = await page1.query_selector_all(grid_selector)
                    if not cells1:
                        print("No cells found in Grid 1 on this page.")
                        break
                    else:
                        rows1 = {}
                        for cell in cells1:
                            row_id = await cell.get_attribute("id")
                            if ':text' not in row_id and '.cell' not in row_id:
                                row_index = row_id.split('_')[1]
                                if row_index not in rows1:
                                    rows1[row_index] = []
                                text = await cell.text_content()
                                rows1[row_index].append(text.strip())
                        for row_index in sorted(rows1.keys()):
                            table_data.append(rows1[row_index])
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPaging.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_1"
                new_data.save()

                await page1.get_by_text("R&D제도").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdBllt.body.gridrow_']"
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 2 Selector not found: {e}")
                        table_data.append([0, "None"])
                        break
                    cells1 = await page1.query_selector_all(grid_selector)
                    if not cells1:
                        print("No cells found in Grid 2 on this page.")
                        break
                    else:
                        rows1 = {}
                        for cell in cells1:
                            row_id = await cell.get_attribute("id")
                            if ':text' not in row_id and '.cell' not in row_id:
                                row_index = row_id.split('_')[1]
                                if row_index not in rows1:
                                    rows1[row_index] = []
                                text = await cell.text_content()
                                rows1[row_index].append(text.strip())
                        for row_index in sorted(rows1.keys()):
                            table_data.append(rows1[row_index])
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPaging.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_2"
                new_data.save()

                await page1.get_by_text("시스템∙서비스").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdBllt.body.gridrow_']"
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 3 Selector not found: {e}")
                        table_data.append([0, "None"])
                        break
                    cells1 = await page1.query_selector_all(grid_selector)
                    if not cells1:
                        print("No cells found in Grid 3 on this page.")
                        break
                    else:
                        rows1 = {}
                        for cell in cells1:
                            row_id = await cell.get_attribute("id")
                            if ':text' not in row_id and '.cell' not in row_id:
                                row_index = row_id.split('_')[1]
                                if row_index not in rows1:
                                    rows1[row_index] = []
                                text = await cell.text_content()
                                rows1[row_index].append(text.strip())
                        for row_index in sorted(rows1.keys()):
                            table_data.append(rows1[row_index])
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPaging.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_3"
                new_data.save()
            elif site_type == "IRIS_52":
                await page1.get_by_text("R&D 고객센터", exact=True).click()
                await page1.get_by_text("IRIS 사용 매뉴얼").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdBllt.body.gridrow_']"
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 1 Selector not found: {e}")
                        table_data.append([0, "None"])
                        break
                    cells1 = await page1.query_selector_all(grid_selector)
                    if not cells1:
                        print("No cells found in Grid 1 on this page.")
                        break
                    else:
                        rows1 = {}
                        for cell in cells1:
                            row_id = await cell.get_attribute("id")
                            if ':text' not in row_id and '.cell' not in row_id:
                                row_index = row_id.split('_')[1]
                                if row_index not in rows1:
                                    rows1[row_index] = []
                                text = await cell.text_content()
                                rows1[row_index].append(text.strip())
                        for row_index in sorted(rows1.keys()):
                            table_data.append(rows1[row_index])
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPaging.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_53":
                await page1.get_by_text("R&D 고객센터", exact=True).click()
                await page1.get_by_text("FAQ").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.TabBllt.Tabpage1.form.grdBllt.body.gridrow_']"
                while True:
                    try:
                        await page1.wait_for_selector(grid_selector)
                    except Exception as e:
                        print(f"Grid 1 Selector not found: {e}")
                        table_data.append([0, "None"])
                        break
                    cells1 = await page1.query_selector_all(grid_selector)
                    if not cells1:
                        print("No cells found in Grid 1 on this page.")
                        break
                    else:
                        rows1 = {}
                        for cell in cells1:
                            row_id = await cell.get_attribute("id")
                            if ':text' not in row_id and '.cell' not in row_id:
                                row_index = row_id.split('_')[1]
                                if row_index not in rows1:
                                    rows1[row_index] = []
                                text = await cell.text_content()
                                rows1[row_index].append(text.strip())
                        for row_index in sorted(rows1.keys()):
                            table_data.append(rows1[row_index])
                    next_page_button = await page1.query_selector("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divPaging.form.divPage.form.btnNext']")
                    next_page_button_disabled = await next_page_button.get_attribute("status") == "disabled" if next_page_button else True
                    if next_page_button_disabled:
                        print("Next page button is disabled or not found.")
                        break
                    await next_page_button.click()
                    await page1.wait_for_selector(grid_selector)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_54":
                await page1.get_by_text("R&D 고객센터", exact=True).click()
                await page1.get_by_text("기본정보").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []

                input_ids = [
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtBstpNm:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtOrgnNm:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtBsnsrRegNo:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtOdnrAtdtCt:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtLocZnoAd:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtLocDtlAd:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtBucdtNm:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtCprtRegNo:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtEngOrgnNm:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.calOrgnStpDe.calendaredit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtHmpgAd:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtTelNo:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtFaxNo:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtLocZno:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.cboLocZneSe.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.cboNatSe.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.cboOrgnTpSe.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.cboOrgnStpSe.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.cboOrgnStpPursSe.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.cboBsnesSe.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.cboOrgnTpSeF.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.div00.form.edtAgrtRprsOrgnNm:input"
                ]
                for input_id in input_ids:
                    selector = f"input[id='{input_id}']"
                    try:
                        await page1.wait_for_selector(selector, timeout=10000)
                        element = await page1.query_selector(selector)
                        if element:
                            value = await element.input_value()
                            table_data.append(value.strip() if value else "N/A")
                        else:
                            table_data.append("N/A")
                    except Exception as e:
                        print(f"Error extracting data for selector {selector}: {e}")
                        table_data.append("N/A")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_55":
                await page1.get_by_text("R&D 고객센터", exact=True).click()
                await page1.get_by_text("보유장비정보").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_56":
                await page1.get_by_text("R&D 고객센터", exact=True).click()
                await page1.get_by_text("기관 담당자정보").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd00.body.gridrow_']"
                try:
                    await page1.wait_for_selector(grid_selector)
                except Exception as e:
                    print(f"Grid 1 Selector not found: {e}")
                    table_data.append([0, "None"])
                cells1 = await page1.query_selector_all(grid_selector)
                if not cells1:
                    print("No cells found in Grid 1 on this page.")
                else:
                    rows1 = {}
                    for cell in cells1:
                        row_id = await cell.get_attribute("id")
                        if ':text' not in row_id and '.cell' not in row_id:
                            row_index = row_id.split('_')[1]
                            if row_index not in rows1:
                                rows1[row_index] = []
                            text = await cell.text_content()
                            rows1[row_index].append(text.strip())
                    for row_index in sorted(rows1.keys()):
                        table_data.append([row_index, rows1[row_index]])
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_57":
                await page1.get_by_text("R&D 고객센터", exact=True).click()
                await page1.get_by_text("보유자산정보").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_58":
                await page1.get_by_text("R&D 고객센터", exact=True).click()
                await page1.get_by_text("기관 지식재산권").click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "IRIS_59":
                await page1.get_by_text("R&D 고객센터", exact=True).click()
                await page1.get_by_text("기관 총괄 담당자 신청").click()
                await page1.get_by_label("확인", exact=True).click()
                await page1.wait_for_load_state("domcontentloaded")
                table_data = []
                input_ids = [
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01.form.edtOrgnId:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01.form.edtMbrId:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01.form.calVlidStrDt.calendaredit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01.form.calVlidEndDt.calendaredit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01.form.cboOrgnMbrRoleSe1.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01_00.form.edtBlngDeptNm:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01_00.form.calVlidStrDt.calendaredit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01_00.form.calVlidEndDt.calendaredit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01_00.form.edtRoleDsntMbrNm:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01_00.form.cboOrgnMbrRoleSe.comboedit:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01_00.form.edtOrgnId:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01_00.form.edtPstnNm:input",
                    "mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grd01_00.form.edtMbrId:input"
                ]
                for input_id in input_ids:
                    selector = f"input[id='{input_id}']"
                    try:
                        await page1.wait_for_selector(selector, timeout=10000)
                        element = await page1.query_selector(selector)
                        if element and await element.is_visible():
                            value = await element.input_value()
                            table_data.append(value.strip() if value else "N/A")
                        else:
                            table_data.append("N/A")
                    except Exception as e:
                        print(f"Error extracting data for selector {selector}: {e}")
                        table_data.append("N/A")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            await page.close()


    #return HttpResponse("성공!")
    return HttpResponse(return_data)

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
        "Referer": "https://www.iris.go.kr/"
    })
    return page


#def main_page(request):
#    t = request.GET['type']
#    html_content = Data.objects.get(content_type=t)
#    if html_content:
#        return HttpResponse(html_content.content)
#    else:
#        return HttpResponse("No HTML content available")

async def submitRequest(request):
    data = json.loads(request.body)
    site_type = data['type']
    account = data['id']
    password = data['pw']
    return_data = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-popup-blocking"])
        context = await browser.new_context()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        page = await set_extra_http_headers(page)
        await page.goto("https://www.iris.go.kr/mbrs/entr/loginForm.do")
        await page.fill('#username', account)
        await page.fill('#password', password)
        await page.screenshot(path="test.png", full_page= True)
        await page.get_by_role("button", name="로그인").click()
        #await page.get_by_role("cell", name="주식회사 오디엔").click()
        #await page.get_by_role("button", name="선택").click()
        #print(await page.content())
        time.sleep(10)
        await page.screenshot(path="test1.png", full_page= True)
        async with page.expect_popup() as page1_info:
            await page.goto("https://www.iris.go.kr/resources/nui/index.do")  # 링크 클릭 시 팝업
        #print(await page1_info)
        page1 = await page1_info.value
        print(page1)
        await page1.wait_for_load_state("domcontentloaded")
        if site_type == "IRIS_21":
            await page1.locator("div.nexacontentsbox#mainframe\\.baseFrame\\.form\\.divTop\\.form\\.divTopComp\\.form\\.divTopBtn\\.form\\.TOP_P00522\\:icontext").click()
            await page1.get_by_text("(승인통보)협약변경신청").click()
            await page1.locator("[id=\"mainframe\\.baseFrame\\.form\\.divWork\\.form\\.divCenter\\.form\\.divWork\\.form\\.divSearch\\.form\\.divSearchComm\\.form\\.divSearch\\.form\\.cboSBsnsYy\\.dropbutton\"]").click()
            await page1.get_by_text(data['year']).click()
            await page1.get_by_label("검색 검색").click()
            time.sleep(10)
            #grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdAgrtChngObjtList.body.gridrow_']"
            await page1.locator("//div[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.divSitu.form.btnAgrtChngRqst']").click()
            await page1.wait_for_selector("//div[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divInfoBox.form.btnChngItemPop']")

            # 협약변경신청 첫페이지 정보 조회

            row_0 = await page1.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdSbjt.body'][class='GridBandControl body']")
            row_0_title = await row_0.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdSbjt.body.gridrow_0.cell_0_0.celledit:input']")
            rows_0 = await row_0.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.grdSbjt.body.gridrow_'][id$=':text']")
            title = (await row_0_title.inner_text()).strip()
            Model0 = apps.get_model('home', 'In_Iris_21_0_1')
            Model0.objects.filter(res_name=title).delete()
            Model0.objects.create(
                account= account,
                group= "",
                res_name = title,
                division = (await rows_0[0].inner_text()).strip(),
                res_org_name = (await rows_0[1].inner_text()).strip(),
                res_director = (await rows_0[2].inner_text()).strip(),
                change_division = (await rows_0[3].inner_text()).strip(),
                res_status = (await rows_0[4].inner_text()).strip(),
                request_status = (await rows_0[5].inner_text()).strip(),
            )

            #for row in rows_0:
            #    print("cell : ", await row.inner_text())





            await page1.locator("//div[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divInfoBox.form.btnChngItemPop']").click()
            await page1.wait_for_selector("div[id='mainframe.baseFrame.AGRTCHNG0202_P01.form.divSbjtChngItem_W0002.form.grdSbjtChngItem.body']")
            table = await page1.query_selector("div[id='mainframe.baseFrame.AGRTCHNG0202_P01.form.divSbjtChngItem_W0002.form.grdSbjtChngItem.body:container']")
            time.sleep(5)
            pops = await table.query_selector_all("div[id^='mainframe.baseFrame.AGRTCHNG0202_P01.form.divSbjtChngItem_W0002.form.grdSbjtChngItem.body.gridrow_'][class='GridRowControl row nexatransform']")
            Model0_1 = apps.get_model('home', 'In_Iris_21_0_2')
            Model0_1.objects.filter(res_name=title).delete()
            for pop in pops:
                cell = await pop.query_selector_all("div[id^='mainframe.baseFrame.AGRTCHNG0202_P01.form.divSbjtChngItem_W0002.form.grdSbjtChngItem.body.gridrow_'][id$=':text']")
                Model0_1.objects.create(
                    account= account,
                    group= "",
                    res_name = title,
                    m_category = await get_safe_text(cell, 0),
                    category = await get_safe_text(cell, 1),
                    s_category_1 = await get_safe_text(cell, 2),
                    s_category_2 = await get_safe_text(cell, 3),
                )

            await page1.locator("//div[@id='mainframe.baseFrame.AGRTCHNG0202_P01.form.divSbjtChngItem_W0002.form.grdSbjtChngItem.body.gridrow_0.cell_0_3.cellcheckbox']").click()
            await page1.locator("//div[@id='mainframe.baseFrame.AGRTCHNG0202_P01.form.divBtn.form.btnSave']").click()
            """
            table = await page1.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divSbjtChngRqstInfo_W0001'][class='Div div_WF_Detail']")
            rows = await table.query_selector_all("input.nexainput")
            Model0_2 = apps.get_model('home', 'In_Iris_21_0_3')
            Model0_2.objects.filter(res_name=title).delete()
            Model0_2.objects.create(
                account= account,
                group= "",
                res_name = title,
                project_name = (await rows[0].input_value()).strip(),
                detail_project_name = (await rows[1].input_value()).strip(),
                res_num = (await rows[2].input_value()).strip(),
                res_name_2 = (await rows[3].input_value()).strip(),
                annual_1 = (await rows[4].input_value()).strip(),
                annual_2 = (await rows[5].input_value()).strip(),
                res_org_name = (await rows[6].input_value()).strip(),
                res_manager = (await rows[7].input_value()).strip(),
                requester = (await rows[8].input_value()).strip(),
                req_res_org_name = (await rows[9].input_value()).strip(),
                res_date = (await rows[10].input_value()).strip(),
            )
            """
            #for row in rows:
            #    print(await row.input_value())


            await page1.locator("//textarea[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divChngRqstCn_W0001.form.txaBfcnCn:textarea']").click()
            await page1.locator("//textarea[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divChngRqstCn_W0001.form.txaBfcnCn:textarea']").fill(data['before_data'])

            await page1.locator("//textarea[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divChngRqstCn_W0001.form.taxAfchCn:textarea']").click()
            await page1.locator("//textarea[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divChngRqstCn_W0001.form.taxAfchCn:textarea']").fill(data['after_data'])

            await page1.locator("//textarea[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divChngRqstCn_W0001.form.taxChngRqstRsn:textarea']").click()
            await page1.locator("//textarea[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divChngRqstCn_W0001.form.taxChngRqstRsn:textarea']").fill(data['reason_data'])

            await page1.locator("//input[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divOcdoc_W0001.form.edtRqstOcdocNo:input']").click()
            await page1.locator("//input[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divOcdoc_W0001.form.edtRqstOcdocNo:input']").fill("0000")

            await page1.locator("//input[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divOcdoc_W0001.form.edtOcdocSendOrgnNm:input']").click()
            await page1.locator("//input[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divOcdoc_W0001.form.edtOcdocSendOrgnNm:input']").fill("test")

            await page1.locator("//input[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divOcdoc_W0001.form.edtRqstOcdocTl:input']").click()
            await page1.locator("//input[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divOcdoc_W0001.form.edtRqstOcdocTl:input']").fill("test")

            await page1.locator("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divAtchFile_W0001.form.divAtchFile.form.grdDutyDocLst.body.gridrow_1.cell_1_7.cellbutton']").click()

            #file_input = page1.locator("input[type='file']")
            #await file_input.set_input_files("/work/test.pdf")

            try:
                await page1.wait_for_selector("input[type='file']", timeout=5000)  # 5초 대기
                print("파일 업로드 필드가 생성되었습니다.")
                file_input = page1.locator("input[type='file']")
                await file_input.set_input_files("/work/test.pdf")
            except Exception as e:
                print("파일 업로드 필드가 생성되지 않았습니다.")
                print(f"오류: {e}")

            #await page1.screenshot(path="test1.png", full_page= True)

            await page1.wait_for_selector("//div[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divBtn.form.btnSave']")
            await page1.locator("//div[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divBtn.form.btnSave']").click()
            time.sleep(10)
            #await page1.screenshot(path="test1.png", full_page= True)
            await page1.wait_for_selector("//div[@id='mainframe.baseFrame.AgrtChngRqst207.form.btnOk']")
            #await page1.screenshot(path="test1.png", full_page= True)
            button = page1.locator("//div[@id='mainframe.baseFrame.AgrtChngRqst207.form.btnOk']")
            if await button.is_visible() and await button.is_enabled():
                await button.click()
            else:
                print("버튼이 비활성화 상태입니다.")
            time.sleep(10)

            table = await page1.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divSbjtChngRqstInfo_W0001'][class='Div div_WF_Detail']")
            rows = await table.query_selector_all("input.nexainput")
            for row in rows:
                print(await row.input_value())
            print(len(rows))

            Model0_2 = apps.get_model('home', 'In_Iris_21_0_3')
            Model0_2.objects.filter(res_name=title).delete()
            Model0_2.objects.create(
                account=account,
                group="",
                res_name=title,
                project_name=(await rows[0].input_value()).strip(),
                detail_project_name=(await rows[1].input_value()).strip(),
                res_num=(await rows[2].input_value()).strip(),
                res_name_2=(await rows[3].input_value()).strip(),
                annual_1=(await rows[4].input_value()).strip(),
                annual_2=(await rows[5].input_value()).strip(),
                res_org_name=(await rows[6].input_value()).strip(),
                res_manager=(await rows[7].input_value()).strip(),
                requester=(await rows[8].input_value()).strip(),
                res_date=(await rows[9].input_value()).strip(),
                req_date=(await rows[10].input_value()).strip(),
                req_org_name=(await rows[11].input_value()).strip(),
                req_org_type=(await rows[12].input_value()).strip(),
                change_before=(await rows[13].input_value()).strip(),  # 변경내용 변경전
                change_after=(await rows[14].input_value()).strip(),  # 변경내용 변경후
                change_reason=(await rows[15].input_value()).strip(),  # 변경사유
                document_number=(await rows[16].input_value()).strip(),  #문서번호
                sending_institution=(await rows[17].input_value()).strip(),  #발송 기관정보
                official_document_title=(await rows[18].input_value()).strip(), #공문 제목
            )


            # 페이지 이동 및 요소 확인
            await page1.locator("//div[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divBtn.form.btnNext']").click()

            grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0104.form']"

            try:
                await page1.wait_for_selector(grid_selector)
            except Exception as e:
                print(f"Grid 1 Selector not found: {e}")

            try:
                await page1.wait_for_selector(container_selector)
            except Exception as e:
                print(f"Container not found: {e}")

            # 연구개발 과제 번호 가져오기
            row_1 = await page1.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0102.form']")
            rows_1 = await row_1.query_selector_all("div[class*='Edit']")
            res_number = await rows_1[0].get_attribute("title")
            print(res_number)

            Model = apps.get_model('home', 'In_Iris_21_1_1')

            # 사용자가 선택한 값 가져오기
            selected_item = request.POST.get("change_item", "Not Selected")  # 기본값을 "Not Selected"로 설정

            # 기존 데이터 삭제
            Model.objects.filter(res_num=res_number.strip()).delete()

            # 새 데이터 생성
            Model.objects.create(
                account=account,
                group="",  # 그룹은 빈 문자열로 설정
                change_item=selected_item,  # 사용자가 선택한 값 반영
                res_num=res_number.strip(),
                res_name_kr=(await rows_1[1].get_attribute("title")).strip(),
                res_name_en=(await rows_1[2].get_attribute("title")).strip(),
            )


            row_1 = await page1.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0104.form.divDetail.form.grdTecl.body:container']")
            grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0104.form.divDetail.form.grdTecl.body.gridrow_']"
            await row_1.wait_for_selector(grid_selector)
            rows = await row_1.query_selector_all(grid_selector)

            # 저장 코드 추가
            Model2 = apps.get_model('home', 'In_Iris_21_1_2')
            Model2.objects.filter(res_num=res_number.strip()).delete()
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0104.form.divDetail.form.grdTecl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model2.objects.create(
                            account=account,
                            group="",
                            res_num=res_number.strip(),
                            division=await get_safe_text(cells, 0),
                            classification=await get_safe_text(cells, 1),
                            first_place=await get_safe_text(cells, 2),
                            first_weight=await get_safe_text(cells, 3),
                            second_place=await get_safe_text(cells, 4),
                            second_weight=await get_safe_text(cells, 5),
                            third_place=await get_safe_text(cells, 6),
                            third_weight=await get_safe_text(cells, 7),
                        )
                except:
                    pass

            row_2 = await page1.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body:container']")
            grid_selector_2 = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][class='GridRowControl row nexatransform']"
            await row_2.wait_for_selector(grid_selector_2)
            rows_2 = await row_2.query_selector_all(grid_selector_2)
            Model3 = apps.get_model('home', 'In_Iris_21_1_3')
            Model3.objects.filter(res_num=res_number.strip()).delete()
            for row in rows_2:
                titles = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$='cellcombo.comboedit:input'][class='nexacontentsbox']")

                Model3.objects.create(
                    account=account,
                    group="",
                    res_num=res_number.strip(),
                    change_item=request.POST.get("change_item", "Not Selected"),  # 사용자가 선택한 값 저장
                    research_stage=await get_safe_text(cells, 0),
                    research_project_type=await get_safe_text(cells, 1),
                    trl_start_point=await get_safe_text(cells, 2),
                    trl_end_point=await get_safe_text(cells, 3),
                )



                Model4 = apps.get_model('home', 'In_Iris_21_1_4')

                # 기존 데이터 삭제
                Model4.objects.filter(res_num=res_number.strip()).delete()

                # 새로운 데이터 생성
                for row in rows_2:
                    cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                    try:
                        if len(cells) > 1:
                            Model4.objects.create(
                                account=account,
                                group="",
                                res_num=res_number.strip(),  # 연구개발과제번호 추가
                                change_item=request.POST.get("change_item", "Not Selected"),  # 사용자가 선택한 값 저장
                                security_grade=request.POST.get("security_grade", "General Task"),  # 보안 등급 반영
                                security_task_release_date=await get_safe_text(cells, 0),  # 보안과제 해제년월 추가
                            )
                    except:
                        pass  # 예외 발생 시 그대로 유지


            row_3 = await page1.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0107.form']")
            radio_selector = await row_3.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0107.form.divDetail.form.rdoScurDtlSe']")
            radio_items = await radio_selector.query_selector_all("div[class*='RadioItemControl']")

            for item in radio_items:
                img = await item.query_selector("img.nexaiconitem")
                if img:
                    src = await img.get_attribute("src")
                    if src == "https://www.iris.go.kr/resources/nui/_resource_/_theme_/portal/images/rdo_WF_Radio_DS.png":
                        text_div = await item.query_selector("div.nexatextitem")
                        if text_div:
                            selected_text = await text_div.inner_text()
                            print(f"Selected Radio Button: {selected_text}")

            Model5 = apps.get_model('home', 'In_Iris_21_1_5')

            # 기존 데이터 삭제
            Model5.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                # 연구개발내용 변경 여부 체크박스 가져오기
                chk_change_item = await row.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0106.form.divChngItem.form.chkAI4121']")
                
                # 국문 키워드
                kor_kwd = [
                    await row.query_selector(f"div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0106.form.divDetail.form.edtKorKwdNm{i}']")
                    for i in range(1, 6)
                ]
                
                # 영문 키워드
                eng_kwd = [
                    await row.query_selector(f"div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0106.form.divDetail.form.edtEngKwdNm{i}']")
                    for i in range(1, 6)
                ]

                try:
                    if any(kor_kwd) and any(eng_kwd):  # 국문 및 영문 데이터가 있는 경우만 저장
                        Model5.objects.create(
                            account=account,
                            group="",
                            res_num=res_number.strip(),
                            change_item="Selected" if await get_safe_text(chk_change_item) else "Not Selected",  # 연구개발내용 변경 여부
                            content_1_kr=await get_safe_text(kor_kwd[0]),  # 국문 1
                            content_1_en=await get_safe_text(eng_kwd[0]),  # 영문 1
                            content_2_kr=await get_safe_text(kor_kwd[1]),  # 국문 2
                            content_2_en=await get_safe_text(eng_kwd[1]),  # 영문 2
                            content_3_kr=await get_safe_text(kor_kwd[2]),  # 국문 3
                            content_3_en=await get_safe_text(eng_kwd[2]),  # 영문 3
                            content_4_kr=await get_safe_text(kor_kwd[3]),  # 국문 4
                            content_4_en=await get_safe_text(eng_kwd[3]),  # 영문 4
                            content_5_kr=await get_safe_text(kor_kwd[4]),  # 국문 5
                            content_5_en=await get_safe_text(eng_kwd[4]),  # 영문 5
                        )
                except:
                    pass

                # 페이지 이동 및 요소 확인
            await page1.locator("//div[@id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.divBtn.form.btnNext']").click()

            grid_selector = "div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0104.form']"

            try:
                await page1.wait_for_selector(grid_selector)
            except Exception as e:
                print(f"Grid 1 Selector not found: {e}")

            try:
                await page1.wait_for_selector(container_selector)
            except Exception as e:
                print(f"Container not found: {e}")

            # 연구개발 과제 번호 가져오기
            row_1 = await page1.query_selector("div[id='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0102.form']")
            rows_1 = await row_1.query_selector_all("div[class*='Edit']")
            res_number = await rows_1[0].get_attribute("title")
            print(res_number)



            Model6 = apps.get_model('home', 'In_Iris_21_2_1')

            # 기존 데이터 삭제
            Model6.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0104.form.divDetail.form.grdTecl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model6.objects.create(
                            account=account,
                            group="",
                            res_num=res_number.strip(),
                            change_item=request.POST.get("change_item", "Not Selected"),  # 사용자가 선택한 값 저장
                            change_reason=await get_safe_text(cells, 0),  # 변경사유 선택
                            step_selection=await get_safe_text(cells, 1),  # 단계선택
                            announcement_period=await get_safe_text(cells, 2),  # 공고 연구기간
                            research_start_date=await get_safe_text(cells, 3),  # 연구개발 시작일
                            research_end_date=await get_safe_text(cells, 4),  # 연구개발 종료일
                        )
                except:
                    pass

            Model7 = apps.get_model('home', 'In_Iris_21_2_2')

            # 기존 데이터 삭제
            Model7.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model7.objects.create(
                            account=account,
                            group="",
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            step=await get_safe_text(cells, 2),  # 단계
                            annual=await get_safe_text(cells, 3),  # 연차
                            research_development_start_date=await get_safe_text(cells, 4),  # 연구개발 시작일
                            research_development_end_date=await get_safe_text(cells, 5),  # 연구개발 종료일
                            months=await get_safe_text(cells, 6),  # 개월 수
                            previous_step=await get_safe_text(cells, 7),  # 기존 단계
                            previous_annual=await get_safe_text(cells, 8),  # 기존 연차
                        )
                except:
                    pass


            Model8 = apps.get_model('home', 'In_Iris_21_2_3')

            # 기존 데이터 삭제
            Model8.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model8.objects.create(
                            account=account,
                            group="",
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            change_item=request.POST.get("change_item", "Not Selected"),  # 사용자가 선택한 값 저장
                            research_development_content=await get_safe_text(cells, 1),  # 최종목표내용
                            research_development_performance=await get_safe_text(cells, 2),  # 연구개발내용
                            utilization_plan_and_expected_effect=await get_safe_text(cells, 3),  # 연구개발성과
                        )
                except:
                    pass
 



                
            Model10 = apps.get_model('home', 'In_Iris_21_3_2')

            # 기존 데이터 삭제
            Model10.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model10.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            institution_role=await get_safe_text(cells, 0),  # 기관 역할
                            nationality=await get_safe_text(cells, 1),  # 국적
                            research_development_institution_name=await get_safe_text(cells, 2),  # 연구개발기관명
                            business_registration_number=await get_safe_text(cells, 3),  # 사업자등록번호
                            establishment_classification=await get_safe_text(cells, 4),  # 설립구분
                            company_type=await get_safe_text(cells, 5),  # 기업유형
                            location=await get_safe_text(cells, 6),  # 소재지
                            research_development_payment_type=await get_safe_text(cells, 7),  # 연구비지급유형
                        )
                except:
                    pass



            Model11 = apps.get_model('home', 'In_Iris_21_3_3')

            # 기존 데이터 삭제
            Model11.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model11.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            institution_role=await get_safe_text(cells, 0),  # 기관 역할
                            research_development_institution_name=await get_safe_text(cells, 1),  # 연구개발기관명
                            research_responsible_person=await get_safe_text(cells, 2),  # 연구책임자
                            representative=await get_safe_text(cells, 3),  # 대표자
                            practitioner=await get_safe_text(cells, 4),  # 실무자
                            participation_annual=request.POST.get("participation_annual", "Not Selected"),  # 참여연차
                            participation_annual_2=request.POST.get("participation_annual_2", "Not Selected"),  # 참여연차2
                            execution_classification=await get_safe_text(cells, 5),  # 수행구분
                        )
                except:
                    pass


            Model12 = apps.get_model('home', 'In_Iris_21_3_4')

            # 기존 데이터 삭제
            Model12.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model12.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            institution_role=await get_safe_text(cells, 0),  # 기관 역할
                            research_development_institution_name=await get_safe_text(cells, 1),  # 연구개발기관명
                            participation_status=request.POST.get("participation_status", "Not Participating"),  # 참여 여부
                            stage=await get_safe_text(cells, 2),  # 단계
                            annual=await get_safe_text(cells, 3),  # 연차
                            start_date=await get_safe_text(cells, 4),  # 연구개발 시작일
                            end_date=await get_safe_text(cells, 5),  # 연구개발 종료일
                            student_integration=request.POST.get("student_integration", "Not Selected"),  # 학생 통합 여부
                            equipment_integration=request.POST.get("equipment_integration", "Not Selected"),  # 장비 통합 여부
                            exception_reason_for_regulation_application=request.POST.get("exception_reason_for_regulation_application", "Not Selected"),  # 규정 적용 예외 사유
                        )
                except:
                    pass


            Model13 = apps.get_model('home', 'In_Iris_21_3_5')

            # 기존 데이터 삭제
            Model13.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model13.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            research_funding_account_change_1=request.POST.get("research_funding_account_change_1", "Not Selected"),  # 연구개발비 지급계좌 변경(통보) 1
                            research_funding_account_change_2=request.POST.get("research_funding_account_change_2", "Not Selected"),  # 연구개발비 지급계좌 변경(통보) 2
                            agreement_institution=await get_safe_text(cells, 0),  # 협약 기관
                            bank_classification=await get_safe_text(cells, 1),  # 은행 구분
                            account_number=await get_safe_text(cells, 2),  # 계좌번호
                            account_holder=await get_safe_text(cells, 3),  # 예금주
                        )
                except:
                    pass



            Model14 = apps.get_model('home', 'In_Iris_21_3_6')

            # 기존 데이터 삭제
            Model14.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model14.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            main_research_institution_leader=request.POST.get("main_research_institution_leader", "Not Selected"),  # 주관연구개발기관 책임자 (상호협의/승인)
                            joint_research_institution_leader=request.POST.get("joint_research_institution_leader", "Not Selected"),  # 공동연구개발기관 책임자 (상호협의/승인)
                            entrusted_research_institution_leader=request.POST.get("entrusted_research_institution_leader", "Not Selected"),  # 위탁연구개발기관 책임자 (상호협의/승인)
                            joint_research_institution_leader_notice=request.POST.get("joint_research_institution_leader_notice", "Not Selected"),  # 공동연구개발기관 책임자 (통보)
                            research_support_personnel_change=request.POST.get("research_support_personnel_change", "Not Selected"),  # 연구지원인력 (직계존속변경) (상호협의/승인)
                            researcher_change_notice=request.POST.get("researcher_change_notice", "Not Selected"),  # 연구원 변경 (통보)
                            research_support_staff_change_notice=request.POST.get("research_support_staff_change_notice", "Not Selected"),  # 연구지원인력 (지원인력 변경) (통보)
                        )
                except:
                    pass


            Model15 = apps.get_model('home', 'In_Iris_21_3_7')

            # 기존 데이터 삭제
            Model15.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model15.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            role=await get_safe_text(cells, 0),  # 인력 역할
                            participation_type=await get_safe_text(cells, 1),  # 참여 구분
                            nationality=await get_safe_text(cells, 2),  # 국적
                            name=await get_safe_text(cells, 3),  # 성명
                            position=await get_safe_text(cells, 4),  # 직위
                            researcher_number=await get_safe_text(cells, 5),  # 국가 연구자 번호
                            new_recruit_type=await get_safe_text(cells, 6),  # 신규 채용 구분
                            recruitment_date=await get_safe_text(cells, 7),  # 채용 일자
                            participation_phase_1=request.POST.get("participation_phase_1", "Not Selected"),  # 참여 연차1
                            participation_phase_2=request.POST.get("participation_phase_2", "Not Selected"),  # 참여 연차2
                            position_status=request.POST.get("position_status", "Not Selected"),  # 직제 존속 여부
                            ethics_guide_provided=await get_safe_text(cells, 8),  # 연구 윤리 안내 여부
                            ethics_agreement_date=request.POST.get("ethics_agreement_date", "Not Selected"),  # 연구 윤리 동의 일자
                            performance_type=await get_safe_text(cells, 9),  # 수행 구분
                        )
                except:
                    pass


            Model16 = apps.get_model('home', 'In_Iris_21_3_8')

            # 기존 데이터 삭제
            Model16.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model16.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            researcher_name=await get_safe_text(cells, 0),  # 연구자명
                            participation_year=await get_safe_text(cells, 1),  # 참여 연차
                            participation_status=await get_safe_text(cells, 2),  # 참여 여부
                            highest_degree=await get_safe_text(cells, 3),  # 최종 학위
                            major_field=await get_safe_text(cells, 4),  # 전공 계열
                            major=await get_safe_text(cells, 5),  # 전공
                            graduation_year=await get_safe_text(cells, 6),  # 졸업 연도
                            role=await get_safe_text(cells, 7),  # 담당 역할
                            participation_type=await get_safe_text(cells, 8),  # 참여 구분
                            part_time_status=await get_safe_text(cells, 9),  # 시간 선택제 구분
                            sequence_number=await get_safe_text(cells, 10),  # 순번
                            participation_start_date=await get_safe_text(cells, 11),  # 참여 시작 일자
                            participation_end_date=await get_safe_text(cells, 12),  # 참여 종료 일자
                            cash_budget_rate=await get_safe_text(cells, 13),  # 현금 계상률
                            in_kind_budget_rate=await get_safe_text(cells, 14),  # 현물 계상률
                            unpaid_budget_rate=await get_safe_text(cells, 15),  # 미지급 계상률
                            calculated_annual_salary=await get_safe_text(cells, 16),  # 산출 근거 연봉 금액
                        )
                except:
                    pass


            Model17 = apps.get_model('home', 'In_Iris_21_3_9')

            # 기존 데이터 삭제
            Model17.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model17.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            representative_change_1=request.POST.get("representative_change_1", "Not Selected"),  # 대표자 변경(통보) _1
                            research_project_practical_manager_change_1=request.POST.get("research_project_practical_manager_change_1", "Not Selected"),  # 연구개발과제 실무 담당자 변경(통보) _1
                            research_project_support_manager_change=request.POST.get("research_project_support_manager_change", "Not Selected"),  # 연구개발과제 지원 담당자 변경(통보)
                            representative_change_2=request.POST.get("representative_change_2", "Not Selected"),  # 대표자 변경(통보) _2
                            research_project_practical_manager_change_2=request.POST.get("research_project_practical_manager_change_2", "Not Selected"),  # 연구개발과제 실무 담당자 변경(통보) _2
                        )
                except:
                    pass

            Model18 = apps.get_model('home', 'In_Iris_21_3_10')

            # 기존 데이터 삭제
            Model18.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model18.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            personnel_role=await get_safe_text(cells, 0),  # 인력 역할
                            nationality=await get_safe_text(cells, 1),  # 국적
                            personnel_name=await get_safe_text(cells, 2),  # 인력명
                            representative_credit_info_consent=await get_safe_text(cells, 3),  # 대표자 신용정보 수집 및 이용 동의
                            researcher_number=await get_safe_text(cells, 4),  # 국가 연구자 번호
                            department=await get_safe_text(cells, 5),  # 소속 부서
                            position=await get_safe_text(cells, 6),  # 직위
                            support_year_1=request.POST.get("support_year_1", "Not Selected"),  # 지원 연차 1
                            support_year_2=request.POST.get("support_year_2", "Not Selected"),  # 지원 연차 2
                            participation_type=await get_safe_text(cells, 7),  # 참여 구분
                            power_of_attorney=await get_safe_text(cells, 8),  # 위임장
                        )
                except:
                    pass





            Model19 = apps.get_model('home', 'In_Iris_21_4_1')

            # 기존 데이터 삭제
            Model19.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model19.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            related_institution_change=request.POST.get("related_institution_change", "Not Selected"),  # 관계 기관 변경 (통보)
                            support_institution_removal=request.POST.get("support_institution_removal", "Not Selected"),  # 지원 기관 삭제 (통보)
                        )
                except:
                    pass


            Model20 = apps.get_model('home', 'In_Iris_21_4_2')

            # 기존 데이터 삭제
            Model20.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model20.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            institution_role=await get_safe_text(cells, 0),  # 기관 역할
                            nationality=await get_safe_text(cells, 1),  # 국적
                            supporting_institution_name=await get_safe_text(cells, 2),  # 지원기관명
                            business_registration_number=await get_safe_text(cells, 3),  # 사업자등록번호
                            company_type=await get_safe_text(cells, 4),  # 기업유형
                            phone_number=await get_safe_text(cells, 5),  # 전화번호
                            supporting_institution_role_description=await get_safe_text(cells, 6),  # 지원기관 역할설명
                            support_year_1=request.POST.get("support_year_1", "Not Selected"),  # 지원 연차 1
                            support_year_2=request.POST.get("support_year_2", "Not Selected"),  # 지원 연차 2
                            execution_type=await get_safe_text(cells, 7),  # 수행구분
                            bank_classification=await get_safe_text(cells, 8),  # 은행구분
                            account_number=await get_safe_text(cells, 9),  # 계좌번호
                            account_holder=await get_safe_text(cells, 10),  # 예금주
                        )
                except:
                    pass


            Model21 = apps.get_model('home', 'In_Iris_21_4_3')

            # 기존 데이터 삭제
            Model21.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model21.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            related_selection=request.POST.get("related_selection", "Not Selected"),  # 관계기관 인력변경(통보)
                        )
                except:
                    pass


            Model22 = apps.get_model('home', 'In_Iris_21_4_4')

            # 기존 데이터 삭제
            Model22.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model22.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            personnel_role=await get_safe_text(cells, 0),  # 인력 역할
                            nationality=await get_safe_text(cells, 1),  # 국적
                            personnel_name=await get_safe_text(cells, 2),  # 인력명
                            department=await get_safe_text(cells, 3),  # 소속 부서
                            position=await get_safe_text(cells, 4),  # 직위
                            support_year_1=request.POST.get("support_year_1", "Not Selected"),  # 지원 연차 1
                            support_year_2=request.POST.get("support_year_2", "Not Selected"),  # 지원 연차 2
                            participation_type=await get_safe_text(cells, 5),  # 참여 구분
                        )
                except:
                    pass





            Model23 = apps.get_model('home', 'In_Iris_21_5_1')

            # 기존 데이터 삭제
            Model23.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model23.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            task_phase=await get_safe_text(cells, 0),  # 과제 단계
                            task_year=await get_safe_text(cells, 1),  # 과제 연차
                            participating_institution=await get_safe_text(cells, 2),  # 참여 기관
                        )
                except:
                    pass



            Model24 = apps.get_model('home', 'In_Iris_21_5_2')

            # 기존 데이터 삭제
            Model24.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model24.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            total_research_budget_change=request.POST.get("total_research_budget_change", "Not Selected"),  # 연구개발비 총액 변경 (상호협의/승인)
                            research_institution_funding_change=request.POST.get("research_institution_funding_change", "Not Selected"),  # 연구개발기관 부담금 변경 (상호협의/승인)
                            project_budget_transfer=request.POST.get("project_budget_transfer", "Not Selected"),  # 사업비 이전 및 양도양수 (상호협의/승인)
                        )
                except:
                    pass




                    
            Model25 = apps.get_model('home', 'In_Iris_21_5_3')

            # 기존 데이터 삭제
            Model25.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model25.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            phase=await get_safe_text(cells, 0),  # 단계
                            year=await get_safe_text(cells, 1),  # 연차
                            institution_role=await get_safe_text(cells, 2),  # 기관 역할
                            research_institution_name=await get_safe_text(cells, 3),  # 연구개발기관명
                            government_cash_funding=await get_safe_text(cells, 4),  # 현금
                            government_funding_ratio=await get_safe_text(cells, 5),  # 비율
                            institution_cash_contribution=await get_safe_text(cells, 6),  # 현금
                            institution_contribution_ratio=await get_safe_text(cells, 7),  # 비율
                            institution_in_kind_contribution=await get_safe_text(cells, 8),  # 현물
                            institution_in_kind_ratio=await get_safe_text(cells, 9),  # 비율
                            institution_total_contribution=await get_safe_text(cells, 10),  # 소계
                            total_cash=await get_safe_text(cells, 11),  # 합계
                            total_in_kind=await get_safe_text(cells, 12),  # 현물
                            total_amount=await get_safe_text(cells, 13),  # 종합
                        )
                except:
                    pass



            Model26 = apps.get_model('home', 'In_Iris_21_5_4')

            # 기존 데이터 삭제
            Model26.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model26.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            labor_cost_cash_change=request.POST.get("labor_cost_cash_change", "Not Selected"),  # 인건비(현금, 영리기관 변경) 
                            subcontracted_research_budget_increase=request.POST.get("subcontracted_research_budget_increase", "Not Selected"),  # 위탁연구개발비 증가
                            international_research_budget_change=request.POST.get("international_research_budget_change", "Not Selected"),  # 국제공동연구비 변경
                            indirect_cost_increase=request.POST.get("indirect_cost_increase", "Not Selected"),  # 간접비 증액
                            research_facility_equipment_cost_high=request.POST.get("research_facility_equipment_cost_high", "Not Selected"),  # 연구시설 장비비 (차액 3천만원 이상)
                            research_lab_operation_plan_change=request.POST.get("research_lab_operation_plan_change", "Not Selected"),  # 연구실 운영 변경
                            integrated_research_facility_equipment=request.POST.get("integrated_research_facility_equipment", "Not Selected"),  # 통합 연구시설 장비비
                            research_allowance_increase=request.POST.get("research_allowance_increase", "Not Selected"),  # 연구수당 증액
                            overseas_researcher_support_fund_increase=request.POST.get("overseas_researcher_support_fund_increase", "Not Selected"),  # 해외 연구자 유지 지원비 증액
                            research_allowance_decrease=request.POST.get("research_allowance_decrease", "Not Selected"),  # 연구수당 감액
                            other_budget_items_change=request.POST.get("other_budget_items_change", "Not Selected"),  # 그 외 세목 변경
                            labor_cost_nonprofit_change=request.POST.get("labor_cost_nonprofit_change", "Not Selected"),  # 인건비(비영리기관 변경)
                            indirect_cost_decrease=request.POST.get("indirect_cost_decrease", "Not Selected"),  # 간접비 감액
                            labor_cost_in_kind_change=request.POST.get("labor_cost_in_kind_change", "Not Selected"),  # 인건비(현물, 영리기관 변경)
                            research_facility_equipment_cost_low=request.POST.get("research_facility_equipment_cost_low", "Not Selected"),  # 연구시설 장비비 (차액 3천만원 미만)
                            security_allowance_change=request.POST.get("security_allowance_change", "Not Selected"),  # 보안수당 변경
                            international_research_budget_exchange_rate=request.POST.get("international_research_budget_exchange_rate", "Not Selected"),  # 국제공동연구비 (환율 변동)
                        )
                except:
                    pass


            Model27 = apps.get_model('home', 'In_Iris_21_5_5')

            # 기존 데이터 삭제
            Model27.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model27.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            phase=await get_safe_text(cells, 0),  # 단계
                            year=await get_safe_text(cells, 1),  # 연차
                            institution_role=await get_safe_text(cells, 2),  # 기관 역할
                            research_institution_name=await get_safe_text(cells, 3),  # 연구개발기관명
                            total_funding_cash=await get_safe_text(cells, 4),  # 재원별 연구비 합계(A) 현금
                            total_funding_in_kind=await get_safe_text(cells, 5),  # 재원별 연구비 합계(A) 현물
                            total_funding_subtotal=await get_safe_text(cells, 6),  # 재원별 연구비 합계(A) 소계
                            itemized_funding_cash=await get_safe_text(cells, 7),  # 비목별 연구비(B) 현금
                            itemized_funding_in_kind=await get_safe_text(cells, 8),  # 비목별 연구비(B) 현물
                            itemized_funding_subtotal=await get_safe_text(cells, 9),  # 비목별 연구비(B) 소계
                            unpaid_salary_baseline=await get_safe_text(cells, 10),  # 비목별 연구비(B) 미지급인건비 계상 기준 금액
                            difference_cash=await get_safe_text(cells, 11),  # 차액(A-B) 현금
                            difference_in_kind=await get_safe_text(cells, 12),  # 차액(A-B) 현물
                            difference_subtotal=await get_safe_text(cells, 13),  # 차액(A-B) 소계
                        )
                except:
                    pass



            Model28 = apps.get_model('home', 'In_Iris_21_5_6')

            # 기존 데이터 삭제
            Model28.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model28.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            phase=await get_safe_text(cells, 0),  # 단계
                            year=await get_safe_text(cells, 1),  # 연차
                            institution_role=await get_safe_text(cells, 2),  # 기관 역할
                            research_institution_name=await get_safe_text(cells, 3),  # 연구개발기관명
                        )
                except:
                    pass


            Model29 = apps.get_model('home', 'In_Iris_21_5_7')

            # 기존 데이터 삭제
            Model29.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model29.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            research_funds_by_item=await get_safe_text(cells, 0),  # 비목
                            sub_item=await get_safe_text(cells, 1),  # 세목
                            cash=await get_safe_text(cells, 2),  # 현금
                            in_kind=await get_safe_text(cells, 3),  # 현물
                            subtotal=await get_safe_text(cells, 4),  # 소계
                            unpaid_salary_baseline_amount=await get_safe_text(cells, 5),  # 미지급 인건비 계상 기준 금액
                            ratio=await get_safe_text(cells, 6),  # 비율
                        )
                except:
                    pass


            Model30 = apps.get_model('home', 'In_Iris_21_5_8')

            # 기존 데이터 삭제
            Model30.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model30.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            phase=await get_safe_text(cells, 0),  # 단계
                            year=await get_safe_text(cells, 1),  # 연차
                            institution_role=await get_safe_text(cells, 2),  # 기관 역할
                            research_institution_name=await get_safe_text(cells, 3),  # 연구개발기관명
                            research_start_date=await get_safe_text(cells, 4),  # 연구개발 시작일
                            research_end_date=await get_safe_text(cells, 5),  # 연구개발 종료일
                            planned_date=await get_safe_text(cells, 6),  # 예정일
                            cash=await get_safe_text(cells, 7),  # 현금
                            in_kind=await get_safe_text(cells, 8),  # 현물
                            subtotal=await get_safe_text(cells, 9),  # 소계
                            round_number=await get_safe_text(cells, 10),  # 차수
                            deposit_amount=await get_safe_text(cells, 11),  # 입금 금액
                        )
                except:
                    pass




            Model31 = apps.get_model('home', 'In_Iris_21_6_1')

            # 기존 데이터 삭제
            Model31.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model31.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            research_institution_role=await get_safe_text(cells, 0),  # 연구기관 역할
                            research_institution_name=await get_safe_text(cells, 1),  # 연구개발기관명
                            principal_researcher=await get_safe_text(cells, 2),  # 연구책임자
                            execution_type=await get_safe_text(cells, 3),  # 수행구분
                        )
                except:
                    pass



            Model32 = apps.get_model('home', 'In_Iris_21_6_2')

            # 기존 데이터 삭제
            Model32.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model32.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            installation_location_change=request.POST.get("installation_location_change", "Not Selected"),  # 설치 운영 장소 변경
                            research_facility_equipment_status_change=request.POST.get("research_facility_equipment_status_change", "Not Selected"),  # 연구시설 장비 보유 현황 변경
                        )
                except:
                    pass


            Model33 = apps.get_model('home', 'In_Iris_21_6_3')

            # 기존 데이터 삭제
            Model33.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model33.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            owning_institution=await get_safe_text(cells, 0),  # 보유 기관
                            research_facility_equipment_name=await get_safe_text(cells, 1),  # 연구시설/장비명
                            specifications=await get_safe_text(cells, 2),  # 규격
                            quantity=await get_safe_text(cells, 3),  # 수량
                            ownership_type=await get_safe_text(cells, 4),  # 보유 구분
                            usage_purpose=await get_safe_text(cells, 5),  # 용도
                            utilization_period=await get_safe_text(cells, 6),  # 활용 시기
                            installation_location=await get_safe_text(cells, 7),  # 설치 장소
                        )
                except:
                    pass



            Model34 = apps.get_model('home', 'In_Iris_21_6_4')

            # 기존 데이터 삭제
            Model34.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model34.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            sequence_number=await get_safe_text(cells, 0),  # 순번
                            research_facility_equipment_name=await get_safe_text(cells, 1),  # 연구시설/장비명
                            in_kind_contribution_reflected=await get_safe_text(cells, 2),  # 현물 부담 반영 여부
                            operation_start_date=await get_safe_text(cells, 3),  # 운영 시작 일자
                            operation_end_date=await get_safe_text(cells, 4),  # 운영 종료 일자
                            annual_operating_cost=await get_safe_text(cells, 5),  # 연간 운영 비용
                            dedicated_personnel_count=await get_safe_text(cells, 6),  # 전담 인력 수
                            utilization_plan=await get_safe_text(cells, 7),  # 활용 계획
                        )
                except:
                    pass


            Model35 = apps.get_model('home', 'In_Iris_21_6_5')

            # 기존 데이터 삭제
            Model35.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model35.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            facility_equipment_plan_change_above_30M=request.POST.get("facility_equipment_plan_change_above_30M", "Not Selected"),  # 연구시설장비 구축계획 변경 (3000만원 이상)
                            installation_location_change_new_plan=request.POST.get("installation_location_change_new_plan", "Not Selected"),  # 설치 운영 장소 변경 (구축 계획 신규)
                            facility_equipment_plan_change_below_30M=request.POST.get("facility_equipment_plan_change_below_30M", "Not Selected"),  # 연구시설장비 구축계획 변경 (3000만원 미만)
                            facility_equipment_plan_change_within_20_percent=request.POST.get("facility_equipment_plan_change_within_20_percent", "Not Selected"),  # 연구시설장비 구축계획 변경 (원래 계획 20% 이내)
                        )
                except:
                    pass



            Model36 = apps.get_model('home', 'In_Iris_21_6_6')

            # 기존 데이터 삭제
            Model36.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model36.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            sequence_number=await get_safe_text(cells, 0),  # 순번
                            specifications=await get_safe_text(cells, 1),  # 규격
                            quantity=await get_safe_text(cells, 2),  # 수량
                            construction_cost_unit_kkr=await get_safe_text(cells, 3),  # 구축 비용 (천원 단위)
                            estimated_price_unit_kkr=await get_safe_text(cells, 4),  # 예상 단가 (천원 단위)
                            construction_timing=await get_safe_text(cells, 5),  # 구축 시점
                            usage_purpose=await get_safe_text(cells, 6),  # 용도
                            shared_usage_category=await get_safe_text(cells, 7),  # 공동 활용 구분
                            manufacturer_name=await get_safe_text(cells, 8),  # 제작 회사명
                            result=await get_safe_text(cells, 9),  # 결과
                        )
                except:
                    pass

            Model37 = apps.get_model('home', 'In_Iris_21_6_7')

            # 기존 데이터 삭제
            Model37.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model37.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            sequence_number=await get_safe_text(cells, 0),  # 순번
                            research_facility_equipment_name=await get_safe_text(cells, 1),  # 연구시설/장비명
                            utilization_status=await get_safe_text(cells, 2),  # 활용 여부
                            operation_start_date=await get_safe_text(cells, 3),  # 운영 시작 일자
                            operation_end_date=await get_safe_text(cells, 4),  # 운영 종료 일자
                            annual_operating_cost=await get_safe_text(cells, 5),  # 연간 운영 비용
                            dedicated_personnel_count=await get_safe_text(cells, 6),  # 전담 인력 수
                            utilization_plan=await get_safe_text(cells, 7),  # 활용 계획
                            installation_location=await get_safe_text(cells, 8),  # 설치 장소
                            change_category=await get_safe_text(cells, 9),  # 변경 구분
                            construction_cancellation_reason=await get_safe_text(cells, 10),  # 구축 포기 사유
                        )
                except:
                    pass


            Model38 = apps.get_model('home', 'In_Iris_21_7_1')

            # 기존 데이터 삭제
            Model38.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model38.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            performance_target_indicator=request.POST.get("performance_target_indicator", "Not Selected"),  # 성과 및 성능 목표 (성과 지표) (상호협의/승인)
                        )
                except:
                    pass



            Model39 = apps.get_model('home', 'In_Iris_21_7_2')

            # 기존 데이터 삭제
            Model39.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model39.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            performance_indicator_name=await get_safe_text(cells, 0),  # 성과지표명
                            target_value=await get_safe_text(cells, 1),  # 목표치
                            total_value=await get_safe_text(cells, 2),  # 계
                            weight_percentage=await get_safe_text(cells, 3),  # 가중치(%)
                            mandatory_status=await get_safe_text(cells, 4),  # 필수 여부
                        )
                except:
                    pass



            Model40 = apps.get_model('home', 'In_Iris_21_7_3')

            # 기존 데이터 삭제
            Model40.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model40.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            performance_indicator_name=await get_safe_text(cells, 0),  # 성과지표명
                            target_value=await get_safe_text(cells, 1),  # 목표치
                            weight_percentage=await get_safe_text(cells, 2),  # 가중치(%)
                        )
                except:
                    pass



            Model41 = apps.get_model('home', 'In_Iris_21_7_4')

            # 기존 데이터 삭제
            Model41.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model41.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            performance_target_metric=request.POST.get("performance_target_metric", "Not Selected"),  # 성과 및 성능 목표 (성능 지표) (상호협의/승인)
                        )
                except:
                    pass

            Model42 = apps.get_model('home', 'In_Iris_21_7_5')

            # 기존 데이터 삭제
            Model42.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model42.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            radio_selection=request.POST.get("radio_selection", "Not Selected"),  # 라디오 버튼 선택 방식
                            evaluation_item_main_performance=await get_safe_text(cells, 0),  # 평가항목(주요성능)
                            unit=await get_safe_text(cells, 1),  # 단위
                            weight_percentage=await get_safe_text(cells, 2),  # 비중(%)
                            world_top_level_country_institution=await get_safe_text(cells, 3),  # 세계 최고수준 보유국/보유기관
                            world_top_level_performance=await get_safe_text(cells, 4),  # 세계 최고수준 성능수준
                            pre_research_domestic_level=await get_safe_text(cells, 5),  # 연구개발전 국내수준
                            pre_research_domestic_performance_level=await get_safe_text(cells, 6),  # 연구개발전 국내 성능수준
                            target_achievement_basis=await get_safe_text(cells, 7),  # 목표 달성근거
                            target_value=await get_safe_text(cells, 8),  # 목표치
                        )
                except:
                    pass

            Model43 = apps.get_model('home', 'In_Iris_21_7_6')

            # 기존 데이터 삭제
            Model43.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model43.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            evaluation_item_main_performance=await get_safe_text(cells, 0),  # 평가항목(주요성능)
                            evaluation_method=await get_safe_text(cells, 1),  # 평가방법
                            evaluation_environment=await get_safe_text(cells, 2),  # 평가환경
                        )
                except:
                    pass




            Model44 = apps.get_model('home', 'In_Iris_21_8_1')

            # 기존 데이터 삭제
            Model44.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model44.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            revenue_commitment_share_change=request.POST.get("revenue_commitment_share_change", "Not Selected"),  # 매출 약정 점유 비율 변경 (상호협의/승인)
                        )
                except:
                    pass


            Model45 = apps.get_model('home', 'In_Iris_21_8_2')

            # 기존 데이터 삭제
            Model45.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model45.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            institution_name=await get_safe_text(cells, 0),  # 기관명
                            commercialization_performance=await get_safe_text(cells, 1),  # 사업화 성과
                            detailed_performance_indicator=await get_safe_text(cells, 2),  # 세부 성과지표
                            total=await get_safe_text(cells, 3),  # 합계
                            round_1=await get_safe_text(cells, 4),  # 1회차
                            round_2=await get_safe_text(cells, 5),  # 2회차
                            round_3=await get_safe_text(cells, 6),  # 3회차
                            round_4=await get_safe_text(cells, 7),  # 4회차
                            round_5=await get_safe_text(cells, 8),  # 5회차
                        )
                except:
                    pass




            Model46 = apps.get_model('home', 'In_Iris_21_9_1')

            # 기존 데이터 삭제
            Model46.objects.filter(res_num=res_number.strip()).delete()

            # 새로운 데이터 생성
            for row in rows:
                cells = await row.query_selector_all("div[id^='mainframe.baseFrame.form.divWork.form.divCenter.form.divWork.form.tabLink.form.div_W0105.form.divDetail.form.grdGnl.body.gridrow_'][id$=':text']")
                try:
                    if len(cells) > 1:
                        Model46.objects.create(
                            account=account,
                            group="",  # 그룹
                            res_num=res_number.strip(),  # 연구개발과제번호 필드 반영
                            sequence_number=await get_safe_text(cells, 0),  # 순번
                            document_type=await get_safe_text(cells, 1),  # 문서 유형
                            required_status=await get_safe_text(cells, 2),  # 필수 여부
                            file_name=await get_safe_text(cells, 3),  # 파일명
                            file_size_kb=await get_safe_text(cells, 4),  # 크기(KB)
                            registration_date=await get_safe_text(cells, 5),  # 등록 일자
                        )
                except:
                    pass




                




            await browser.close()







    return HttpResponse(return_data)

async def get_safe_text(cells, index, default=""):
    try:
        return (await cells[index].inner_text()).strip()
    except:
        return default

def main_page(request):
    model_name = request.GET.get('type', None)

    if not model_name:
        return JsonResponse({"error": "No model name provided."}, status=400)

    try:
        ModelClass = apps.get_model('home', model_name)
        if not issubclass(ModelClass, Model):
            return JsonResponse({"error": "Invalid model name."}, status=400)
        records = ModelClass.objects.all()

        data = list(records.values())

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

async def test_page(request):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        page = await set_extra_http_headers(page)
        await page.goto("https://www.iris.go.kr/index.do")
        content = await page.content()
        await context.close()
        await browser.close()
    return HttpResponse(content)
    #return redirect("https://www.iris.go.kr/index.do")