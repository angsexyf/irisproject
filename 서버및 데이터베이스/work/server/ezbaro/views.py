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
            await page.goto("https://www.gaia.go.kr/main.do")
            await page.wait_for_load_state("networkidle")
            try:
                await page.get_by_role("button", name="팝업 닫기").click()
            except:
                pass
            await page.get_by_role("link", name="로그인").click()
            await page.wait_for_load_state("networkidle")
            await page.fill('#usrId', 'mwmw7')
            await page.fill('#usrPin', '040201mM~!')
            await page.get_by_role("button", name="로그인").click()
            try:
                await page.get_by_role("button", name="팝업 닫기").click()
            except:
                pass
            print("동작중")
            if site_type == "EZBR_1":
                table_data = []
                try:
                    await page.get_by_role("link", name="공지사항").click()
                    await page.wait_for_load_state("domcontentloaded")
                    current_page_number = 1
                    while True:
                        await page.wait_for_selector("table.basic_list_table tbody tr")
                        rows = await page.query_selector_all("table.basic_list_table tbody tr")
                        for row in rows:
                            cells = await row.query_selector_all("td")
                            row_data = [await cell.inner_text() for cell in cells]
                            table_data.append(row_data)
                        next_page_number = current_page_number + 1
                        next_page_link = f'fn_bbsList({next_page_number}); return false;'
                        next_button = await page.query_selector(f'a[onclick="{next_page_link}"]')
                        if not next_button:
                            break
                        await next_button.click()
                        await page.wait_for_selector("table.basic_list_table")
                        current_page_number = next_page_number
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_1"
                new_data.save()

                await page.get_by_role("link", name="국가R&D 연구비관련 법ㆍ규정").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    tabs = await page.query_selector_all(".gaia_rnd_tab .tablinks")
                    for tab in tabs:
                        await tab.click()
                        await page.wait_for_selector(".rnd_tabcontent[style*='display: block;']")
                        content = await page.query_selector(".rnd_tabcontent[style*='display: block;']")
                        rows = await content.query_selector_all("dl .rules_box")
                        for row in rows:
                            title = await row.query_selector("dt")
                            links = await row.query_selector_all("dd a")
                            row_data = {
                                "title": await title.inner_text() if title else "",
                                "links": [await link.inner_text() for link in links]
                            }
                            table_data.append(row_data)
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type + "_2"
                new_data2.save()

                await page.get_by_role("link", name="시스템 기능개선 안내").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    current_page_number = 1
                    while True:
                        await page.wait_for_selector("table.basic_list_table tbody tr")
                        rows = await page.query_selector_all("table.basic_list_table tbody tr")
                        for row in rows:
                            cells = await row.query_selector_all("td")
                            row_data = [await cell.inner_text() for cell in cells]
                            table_data.append(row_data)

                        next_page_number = current_page_number + 1
                        next_page_link = f'fn_bbsList({next_page_number}); return false;'
                        next_button = await page.query_selector(f'a[onclick="{next_page_link}"]')
                        if not next_button:
                            break
                        await next_button.click()
                        await page.wait_for_selector("table.basic_list_table")
                        current_page_number = next_page_number
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data3 = Data()
                new_data3.content = table_data
                new_data3.content_type = site_type + "_3"
                new_data3.save()
            elif site_type == "EZBR_2":
                table_data = []
                try:
                    await page.get_by_role("link", name="회원정보수정").click()
                    await page.fill('#usrPin', '040201mM~!')
                    await page.get_by_role("link", name="확인").click()
                    await page.wait_for_load_state("domcontentloaded")
                    name = await page.query_selector('dt:has-text("이름") + dd p')
                    name_text = await name.inner_text() if name else ""
                    username = await page.query_selector('dt:has-text("아이디") + dd p')
                    username_text = await username.inner_text() if username else ""
                    birthdate = await page.query_selector('dt:has-text("생년월일") + dd p')
                    birthdate_text = await birthdate.inner_text() if birthdate else ""
                    gender = await page.query_selector('dt:has-text("성별") + dd p')
                    gender_text = await gender.inner_text() if gender else ""
                    email_part1 = await page.query_selector('#str_email01')
                    email_part2 = await page.query_selector('#str_email02')
                    email_part1_text = await email_part1.input_value() if email_part1 else ""
                    email_part2_text = await email_part2.input_value() if email_part2 else ""
                    email_domain = await page.query_selector('#selectEmail')
                    email_domain_text = await email_domain.input_value() if email_domain else ""
                    email = f"{email_part1_text}@{email_part2_text or email_domain_text}"
                    phone = await page.query_selector('#pon')
                    phone_text = await phone.input_value() if phone else ""
                    mobile_phone = await page.query_selector('#movPon')
                    mobile_phone_text = await mobile_phone.input_value() if mobile_phone else ""
                    researcher_number = await page.query_selector('#scnceEngnrRgn')
                    researcher_number_text = await researcher_number.input_value() if researcher_number else ""
                    affiliation = await page.query_selector('#ieNm')
                    affiliation_text = await affiliation.input_value() if affiliation else ""
                    employee_number = await page.query_selector('#etpIhEmplN')
                    employee_number_text = await employee_number.input_value() if employee_number else ""
                    project_team = await page.query_selector('#bstNm')
                    project_team_text = await project_team.input_value() if project_team else ""
                    specialized_agency = await page.query_selector('#spcltyIeNm')
                    specialized_agency_text = await specialized_agency.input_value() if specialized_agency else ""
                    table_data = [
                        {"name": name_text, "username": username_text, "birthdate": birthdate_text, "gender": gender_text,
                        "email": email, "phone": phone_text, "mobile_phone": mobile_phone_text,
                        "researcher_number": researcher_number_text, "affiliation": affiliation_text,
                        "employee_number": employee_number_text, "project_team": project_team_text,
                        "specialized_agency": specialized_agency_text}
                    ]
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "EZBR_3":
                table_data = []
                try:
                    await page.get_by_role("link", name="건강보험 자격득실검증").click()
                    await page.wait_for_load_state("domcontentloaded")
                    privacy_data_rows = await page.query_selector_all('table:nth-of-type(1) tbody tr')
                    for row in privacy_data_rows:
                        cells = await row.query_selector_all('td')
                        row_data = [await cell.inner_text() for cell in cells]
                        table_data.append({
                            "section": "privacy_collection_usage",
                            "data": row_data
                        })
                    r_and_d_data_rows = await page.query_selector_all('table:nth-of-type(2) tbody tr')
                    for row in r_and_d_data_rows:
                        cells = await row.query_selector_all('td')
                        row_data = [await cell.inner_text() for cell in cells]
                        table_data.append({
                            "section": "rnd_participation_status",
                            "data": row_data
                        })
                    public_data_rows = await page.query_selector_all('table:nth-of-type(3) tbody tr')
                    for row in public_data_rows:
                        cells = await row.query_selector_all('td')
                        row_data = [await cell.inner_text() for cell in cells]
                        table_data.append({
                            "section": "public_data_items",
                            "data": row_data
                        })
                    unique_info_rows = await page.query_selector_all('table:nth-of-type(4) tbody tr')
                    for row in unique_info_rows:
                        cells = await row.query_selector_all('td')
                        row_data = [await cell.inner_text() for cell in cells]
                        table_data.append({
                            "section": "unique_identification_info",
                            "data": row_data
                        })
                    third_party_data_rows = await page.query_selector_all('table:nth-of-type(5) tbody tr')
                    for row in third_party_data_rows:
                        cells = await row.query_selector_all('td')
                        row_data = [await cell.inner_text() for cell in cells]
                        table_data.append({
                            "section": "third_party_provision",
                            "data": row_data
                        })
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "EZBR_4":
                table_data = []
                try:
                    await page.get_by_role("link", name="OTP", exact=True).click()
                    await page.wait_for_load_state("domcontentloaded")
                    password_input = await page.wait_for_selector('input[name="usrPinCancel"]')
                    await password_input.fill("password")
                    confirm_button = await page.wait_for_selector('a[href="javascript:otpMain.applicateOtp();"]')
                    await confirm_button.click()
                    await page.wait_for_load_state("networkidle")
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "EZBR_5":
                table_data = []
                try:
                    await page.get_by_role("link", name="공지사항").click()
                    await page.wait_for_load_state("domcontentloaded")
                    previous_page_number = None
                    while True:
                        rows = await page.query_selector_all("table.basic_list_table tbody tr")
                        for row in rows:
                            cells = await row.query_selector_all("td")
                            row_data = [await cell.inner_text() for cell in cells]
                            table_data.append(row_data)
                        current_page_number = await page.evaluate(
                            'document.querySelector("li a.active").textContent'
                        )

                        next_button = await page.query_selector('li a[onclick*="fn_bbsList"] img[alt="다음"]')
                        if next_button:
                            await next_button.click()
                            await page.wait_for_load_state("networkidle")
                            new_page_number = await page.evaluate(
                                'document.querySelector("li a.active").textContent'
                            )
                            if previous_page_number == new_page_number:
                                break
                            previous_page_number = new_page_number
                        else:
                            break
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "EZBR_8":
                table_data = []
                try:
                    await page.get_by_role("link", name="국가R&D 연구비관련 법ㆍ규정").click()
                    await page.wait_for_load_state("domcontentloaded")
                    tab_buttons = await page.query_selector_all(".gaia_rnd_tab button")
                    for i, button in enumerate(tab_buttons):
                        await button.click()
                        tab_content_id = await button.get_attribute("onclick")
                        tab_content_id = tab_content_id.split("'")[1]
                        await page.wait_for_selector(f"#{tab_content_id}.rnd_tabcontent[style*='display: block']")
                        active_tab_content = await page.query_selector(".rnd_tabcontent:not([style*='display: none'])")
                        title = await active_tab_content.query_selector("h4.rules_title")
                        title_text = await title.inner_text() if title else ""
                        sections = await active_tab_content.query_selector_all(".rules_box")
                        for section in sections:
                            dt = await section.query_selector("dt")
                            dt_text = await dt.inner_text() if dt else ""
                            dd_links = await section.query_selector_all("dd a")
                            for link in dd_links:
                                link_text = await link.inner_text()
                                link_href = await link.get_attribute("href")
                                table_data.append([title_text, dt_text, link_text, link_href])    
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "EZBR_11":
                table_data = []
                try:
                    await page.get_by_role("link", name="시스템 기능개선 안내").click()
                    await page.wait_for_load_state("domcontentloaded")
                    while True:
                        rows = await page.query_selector_all("table.basic_list_table tbody tr")
                        for row in rows:
                            columns = await row.query_selector_all("td")
                            row_data = []
                            for column in columns:
                                if column:
                                    link = await column.query_selector("a")
                                    if link:
                                        text = await link.inner_text()
                                        href = await link.get_attribute("href")
                                        row_data.append((text, href))
                                    else:
                                        text = await column.inner_text()
                                        row_data.append(text)
                            table_data.append(row_data)
                        current_page_element = await page.query_selector(".pagination ul li .active")
                        current_page_number = int(await current_page_element.inner_text())
                        pagination_items = await page.query_selector_all(".pagination ul li a[onclick*='fn_bbsList']")
                        last_page_number = int(await pagination_items[-1].inner_text())
                        if current_page_number < last_page_number:
                            next_page_element = await page.query_selector(f".pagination ul li a[onclick*='fn_bbsList({current_page_number + 1})']")
                            await next_page_element.click()
                            await page.wait_for_load_state("networkidle")
                        else:
                            break
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "EZBR_TEST":
                otp = data['otp']
                table_data = []
                try:
                    await page.locator('a.ntb_ezbaro[title="통합 Ezbaro 새창 열림"] button').click()
                    await page.wait_for_load_state()
                    tag_exists = await page.query_selector('#otpNum') is not None
                    if tag_exists:
                        print(f"The tag exists on the page.")
                    else:
                        print(f"The tag does not exist on the page.")
                    await page.fill('#otpNum', otp)
                    await page.screenshot(path='screenshot.png')
                    async with page.expect_popup() as page1_info:
                        await page.get_by_role("link", name="확인").click()
                    page1 = await page1_info.value
                    await page1.wait_for_load_state("domcontentloaded")
                    await page1.get_by_text("닫기").click()
                except Exception as e:
                    print(f"An error occurred: {e}")
            elif site_type == "EZBR_12":
                otp = data['otp']
                table_data = []
                try:
                    await page.locator('a.ntb_ezbaro[title="통합 Ezbaro 새창 열림"] button').click()
                    await page.wait_for_load_state("domcontentloaded")
                    await page.get_by_placeholder("인증번호를 입력해주세요").fill(otp)
                    async with page.expect_popup() as page1_info:
                        await page.get_by_role("link", name="확인").click()
                    page1 = await page1_info.value
                    await page1.wait_for_load_state("domcontentloaded")
                    await page1.get_by_text("닫기").click()
                    button_selectors = [
                        "#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.frameMain\\.form\\.mainDiv\\.form\\.divTakTaskStep\\.form\\.btnTakReady",
                        "#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.frameMain\\.form\\.mainDiv\\.form\\.divTakTaskStep\\.form\\.btnTakIng",
                        "#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.frameMain\\.form\\.mainDiv\\.form\\.divTakTaskStep\\.form\\.btnTakCyrEnd",
                        "#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.frameMain\\.form\\.mainDiv\\.form\\.divTakTaskStep\\.form\\.btnTakStgEnd",
                        "#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.frameMain\\.form\\.mainDiv\\.form\\.divTakTaskStep\\.form\\.btnJungsan",
                        "#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.frameMain\\.form\\.mainDiv\\.form\\.divTakTaskStep\\.form\\.btnJungsanEnd"
                    ]
                    for selector in button_selectors:
                        try:
                            button = await page1.query_selector(selector)
                            if button:
                                await button.click()
                                try:
                                    await page1.wait_for_selector("div.GridRowControl.row.nexatransform", timeout=3000)
                                    rows = await page1.query_selector_all("div.GridRowControl.row.nexatransform")
                                    for row in rows:
                                        columns = await row.query_selector_all("div.GridCellControl.cell")
                                        row_data = []
                                        for column in columns:
                                            if column:
                                                text = await column.inner_text()
                                                row_data.append(text.strip())
                                        if row_data:
                                            table_data.append(row_data)
                                except asyncio.TimeoutError:
                                    popup = await page1.query_selector("div[id*='조회할 데이터가 없습니다.']")
                                    if popup:
                                        ok_button = await popup.query_selector("div[class*='Button'] div")
                                        if ok_button:
                                            await ok_button.click()
                                            print("조회할 데이터가 없습니다. 팝업이 나타났습니다. 다음 버튼으로 넘어갑니다.")
                        except Exception as e:
                            print(f"Error clicking button with selector {selector}: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "EZBR_17":
                print(site_type)
                table_data = []
                try:
                    async with page.expect_popup() as page1_info:
                        await page.locator('a.ntb_ezbaro[title="통합 Ezbaro 새창 열림"] button').click()
                    page1 = await page1_info.value
                    print(page1)
                    await page1.wait_for_load_state("load")
                    await page1.get_by_text("닫기").click()
                    await page1.get_by_text("소개").nth(1).click()
                    await page1.get_by_text("정보마당").click()
                    await page1.get_by_text("공지사항").click()
                    await page1.wait_for_load_state("domcontentloaded")
                    new_data = Data()
                    new_data.content = table_data
                    new_data.content_type = site_type
                    new_data.save()
                except Exception as e:
                    print(f"An error occurred: {e}")
            elif site_type == "EZBR_18":
                table_data = []
                try:
                    await page1.get_by_text("소개").nth(1).click()
                    await page1.get_by_text("정보마당").first.click()
                    await page1.get_by_text("자주묻는질문").click()
                    await page1.wait_for_load_state("domcontentloaded")
                    row_selector = '#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.framesetWork\\.winMCOM020202_0_833\\.form\\.divWork\\.form\\.divBoard\\.form\\.grdBrd\\.body > .GridRowControl'
                    rows = await page1.query_selector_all(row_selector)
                    for row in rows:
                        cells = await row.query_selector_all('.GridCellControl')
                        row_data = []
                        for cell in cells:
                            cell_text = await cell.query_selector('div').inner_text()
                            row_data.append(cell_text)
                        table_data.append(row_data)
                    new_data = Data()
                    new_data.content = table_data
                    new_data.content_type = "EZBR_18"
                    new_data.save()
                except Exception as e:
                    print(f"An error occurred: {e}")
                table_data = []
                try:
                    await page1.get_by_text("협약", exact=True).nth(1).click()
                    await page1.get_by_text("과제 관리").click()
                    await page1.get_by_text("과제관리자 관리").click()
                    await page1.get_by_text("조회", exact=True).nth(1).click()
                    await page1.wait_for_load_state("domcontentloaded")
                    row_selector = '#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.framesetWork\\.winMCNV010103_0_491\\.form\\.divWork\\.form\\.grdCnvTak\\.body > .GridRowControl'
                    rows = await page1.query_selector_all(row_selector)

                    for row in rows:
                        cells = await row.query_selector_all('.GridCellControl')
                        row_data = []
                        for cell in cells:
                            cell_text_element = await cell.query_selector('div')
                            if cell_text_element:
                                cell_text = await cell_text_element.inner_text()
                            else:
                                cell_text = ""
                            row_data.append(cell_text)
                        table_data.append(row_data)
                    new_data = Data()
                    new_data.content = table_data
                    new_data.content_type = "EZBR_24"
                    new_data.save()
                except Exception as e:
                    print(f"An error occurred: {e}")
                table_data = []
                try:
                    await page1.get_by_text("협약", exact=True).nth(1).click()
                    await page1.get_by_text("협약 과제").click()
                    await page1.get_by_text("협약과제 목록").click()
                    await page1.get_by_text("조회", exact=True).nth(1).click()
                    await page1.get_by_text("선택", exact=True).nth(1).click()
                    await page1.wait_for_load_state("domcontentloaded")
                    row_selector = '#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.framesetWork\\.winMCNV010201_0_897\\.form\\.divWork\\.form\\.cnvTakIfGrid\\.body > .GridRowControl'
                    rows = await page1.query_selector_all(row_selector)

                    for row in rows:
                        cells = await row.query_selector_all('.GridCellControl')
                        row_data = []
                        for cell in cells:
                            cell_text_element = await cell.query_selector('.nexacontentsbox')
                            if cell_text_element:
                                cell_text = await cell_text_element.inner_text()
                            else:
                                cell_text = ""
                            row_data.append(cell_text.strip())
                        table_data.append(row_data)
                    new_data = Data()
                    new_data.content = table_data
                    new_data.content_type = "EZBR_26"
                    new_data.save()
                except Exception as e:
                    print(f"An error occurred: {e}")
                table_data = []
                try:
                    await page1.get_by_text("협약", exact=True).nth(1).click()
                    await page1.get_by_text("협약 과제").click()
                    await page1.get_by_text("협약과제 상세").click()
                    await page1.wait_for_load_state("domcontentloaded")
                    async def extract_section_data(section_id):
                        section_data = []
                        rows = await page1.query_selector_all(
                            f'#{section_id} .nexacontentsbox')
                        for row in rows:
                            cells = await row.query_selector_all('div')
                            row_data = [await cell.inner_text() for cell in cells]
                            if any(row_data):
                                section_data.append(row_data)
                        return section_data
                    detail_sections = [
                        'mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV010202_0_606.form.divWork.form.TABPAGE01.form.Detail01.form',
                        'mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV010202_0_606.form.divWork.form.TABPAGE01.form.Detail02.form',
                        'mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV010202_0_606.form.divWork.form.TABPAGE01.form.Detail04.form',
                        'mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV010202_0_606.form.divWork.form.TABPAGE01.form.Detail05.form',
                        'mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV010202_0_606.form.divWork.form.TABPAGE01.form.Detail06.form'
                    ]

                    for section_id in detail_sections:
                        section_data = await extract_section_data(section_id)
                        table_data.extend(section_data)
                    new_data = Data()
                    new_data.content = table_data
                    new_data.content_type = "EZBR_27_1"
                    new_data.save()
                    table_data = []
                    await page1.get_by_text("연구비정보").click()
                    await page1.wait_for_load_state("domcontentloaded")
                    selectors = [
                        '#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.framesetWork\\.winMCNV010202_0_254\\.form\\.divWork\\.form\\.TABPAGE02\\.form\\.grdAseList\\.body',
                        '#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.framesetWork\\.winMCNV010202_0_252\\.form\\.divWork\\.form\\.TABPAGE02\\.form\\.grdBdgList\\.body'
                    ]
                    for selector in selectors:
                        rows = await page1.query_selector_all(f"{selector} .GridRowControl")

                        for row in rows:
                            cells = await row.query_selector_all('.GridCellControl')
                            row_data = [await cell.inner_text() for cell in cells]
                            table_data.append(row_data)
                    new_data = Data(content=table_data, content_type="EZBR_27_2")
                    new_data.save()

                    table_data = []
                    await page1.get_by_text("참여연구원정보").click()
                    await page1.wait_for_load_state("domcontentloaded")
                    base_selector = '#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.framesetWork\\.winMCNV010202_0_915\\.form\\.divWork\\.form\\.TABPAGE03\\.form\\.grdPaiRsrchr\\.body'

                    rows = await page1.query_selector_all(f"{base_selector} .GridRowControl")

                    for row in rows:
                        row_data = []
                        cells = await row.query_selector_all('.GridCellControl')
                        for cell in cells:
                            cell_text = await cell.inner_text()
                            row_data.append(cell_text)
                        table_data.append(row_data)

                        await row.click()
                        await page1.wait_for_load_state("domcontentloaded")

                        sub_selector = '#mainframe\\.VFrameSet\\.HFrameSet\\.VFrameSet1\\.framesetWork\\.winMCNV010202_0_8\\.form\\.divWork\\.form\\.TABPAGE03\\.form\\.grdYearMonthPai\\.body'
                        sub_rows = await page1.query_selector_all(f"{sub_selector} .GridRowControl")

                        for sub_row in sub_rows:
                            sub_row_data = []
                            sub_cells = await sub_row.query_selector_all('.GridCellControl')
                            for sub_cell in sub_cells:
                                sub_cell_text = await sub_cell.inner_text()
                                sub_row_data.append(sub_cell_text)
                            table_data.append(sub_row_data)

                    new_data = Data(content=table_data, content_type="EZBR_27_3")
                    new_data.save()

                    table_data = []
                    await page1.get_by_text("협약과제 상세").click()
                    await page1.wait_for_load_state("domcontentloaded")
                    rows = await page.query_selector_all(
                        'div[id^="mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV"][id*="form.divWork.form.TABPAGE04.form.grdBfTak.body.gridrow_"]'
                    )
                    for row in rows:
                        cells = await row.query_selector_all('div[id*=".cell_"]')
                        cell_data = []
                        for cell in cells:
                            text_div = await cell.query_selector('div[id*=":text"]')
                            if text_div:
                                text = await text_div.inner_text()
                                cell_data.append(text.strip())
                        if cell_data:
                            await row.click()
                            await page1.wait_for_load_state("domcontentloaded")
                            details = await page.query_selector_all(
                                'div[id^="mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV"][id*="form.divWork.form.TABPAGE04.form.cnvTakFmCfGrid.body.gridrow_"]'
                            )
                            detail_data = []
                            for detail in details:
                                detail_cells = await detail.query_selector_all('div[id*=".cell_"]')
                                detail_row_data = []
                                for detail_cell in detail_cells:
                                    detail_text_div = await detail_cell.query_selector('div[id*=":text"]')
                                    if detail_text_div:
                                        detail_text = await detail_text_div.inner_text()
                                        detail_row_data.append(detail_text.strip())
                                if detail_row_data:
                                    detail_data.append(detail_row_data)
                            table_data.append({
                                "main_data": cell_data,
                                "detail_data": detail_data
                            })
                    new_data = Data(content=table_data, content_type="EZBR_27_4")
                    new_data.save()

                    table_data = []        
                    await page1.get_by_text("수령계좌정보변경").click()
                    await page1.get_by_text("확인", exact=True).click()
                    await page1.wait_for_load_state("domcontentloaded")
                    detail01_data = []
                    detail01 = await page.query_selector('div[id^="mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV"][id*="form.divWork.form.Detail01.form"]')

                    if detail01:
                        detail01_cells = await detail01.query_selector_all('div[id*=".Static"], div[id*=".Combo"], div[id*=".Edit"], div[id*=".Button"]')
                        detail01_row_data = {}

                        for detail_cell in detail01_cells:
                            text_div = await detail_cell.query_selector('div[id*=":text"]')
                            input_elem = await detail_cell.query_selector('input')
                            text = ""

                            if text_div:
                                text = await text_div.inner_text()  # 셀 내의 텍스트 추출
                            elif input_elem:
                                text = await input_elem.get_attribute('value')  # 입력 필드의 값 추출

                            key = await detail_cell.get_attribute('id')
                            if key:
                                key = key.split('.')[-1].split(':')[0]
                                detail01_row_data[key] = text.strip()

                        if detail01_row_data:
                            detail01_data.append(detail01_row_data)

                    detail02_data = []
                    detail02 = await page.query_selector('div[id^="mainframe.VFrameSet.HFrameSet.VFrameSet1.framesetWork.winMCNV"][id*="form.divWork.form.Detail02.form"]')

                    if detail02:
                        detail02_cells = await detail02.query_selector_all('div[id*=".Static"], div[id*=".Combo"], div[id*=".Edit"], div[id*=".Button"]')
                        detail02_row_data = {}

                        for detail_cell in detail02_cells:
                            text_div = await detail_cell.query_selector('div[id*=":text"]')
                            input_elem = await detail_cell.query_selector('input')
                            text = ""

                            if text_div:
                                text = await text_div.inner_text()  # 셀 내의 텍스트 추출
                            elif input_elem:
                                text = await input_elem.get_attribute('value')  # 입력 필드의 값 추출

                            key = await detail_cell.get_attribute('id')
                            if key:
                                key = key.split('.')[-1].split(':')[0]
                                detail02_row_data[key] = text.strip()

                        if detail02_row_data:
                            detail02_data.append(detail02_row_data)

                    table_data.append({
                        "detail01_data": detail01_data,
                        "detail02_data": detail02_data
                    })


                except Exception as e:
                    print(f"An error occurred: {e}")

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
        "Referer": "https://www.gaia.go.kr/"
    })
    return page

def open_page(request):
    t = request.GET['type']
    html_content = Data.objects.get(content_type=t)
    if html_content:
        return HttpResponse(html_content.content)
    else:
        return HttpResponse("No HTML content available")

