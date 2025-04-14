import json
import time
import asyncio

from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Model
from .models import Data

from playwright.async_api import async_playwright, expect



async def getRnDPage(request):
    print("동작")
    if request.method == "POST":
        data = json.loads(request.body)
        async with async_playwright() as p:
            site_type = data['type']
            p_num = data['p_num']
            user_id = data['id']
            user_pw = data['pw']
            browser = await p.chromium.launch()
            page = await browser.new_page()
            page = await set_extra_http_headers(page)
            await page.goto("https://www.rcms.go.kr/login/rid.do?PORTAL_YN=Y")
            await page.fill('#loginId', user_id)
            await page.fill('#loginPasswd', user_pw)
            await page.get_by_role("link", name="로그인", exact=True).click()
            await asyncio.sleep(5)
            if site_type == "MAIN":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.get_by_role("link", name="전체과제").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector("#wfm_main_sbjtTab1_gen_list")
                ul_elements = await page.query_selector_all("#wfm_main_sbjtTab1_gen_list > ul")
                table_data = []
                for ul in ul_elements:
                    li_elements = await ul.query_selector_all("li")
                    row_data = []
                    for li in li_elements:
                        text = ""
                        if span := await li.query_selector("span"):
                            text = await span.inner_text()
                        elif div := await li.query_selector("div"):
                            text = await div.inner_text()
                        row_data.append(text)
                    table_data.append(row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

                await page.locator("#wfm_main_sbjtTab1_gen_list_0_row").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    nobr_elements = await page.query_selector_all('nobr')
                    table_data1 = [await nobr.inner_text() for nobr in nobr_elements]
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data1 = Data()
                new_data1.content = table_data
                new_data1.content_type = site_type + "_1"
                new_data1.save()

                await page.get_by_role("tab", name="참여연구자 현황").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    nobr_elements = await page.query_selector_all('nobr')
                    table_data2 = [await nobr.inner_text() for nobr in nobr_elements]
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type + "_2"
                new_data2.save()

                await page.get_by_role("tab", name="연구과제운영비 집행비율").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                popup_confirm = await page.query_selector('role=link[name="확인"]')

                if popup_confirm:
                    await popup_confirm.click()
                else:
                    try:
                        nobr_elements = await page.query_selector_all('nobr')
                        table_data = [await nobr.inner_text() for nobr in nobr_elements]
                    except Exception as e:
                        print(f"An error occurred: {e}")
                new_data3 = Data()
                new_data3.content = table_data
                new_data3.content_type = site_type + "_3"
                new_data3.save()

                await page.get_by_role("tab", name="직접비 집행비율").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    nobr_elements = await page.query_selector_all('nobr')
                    table_data = [await nobr.inner_text() for nobr in nobr_elements]
                except Exception as e:
                    print(f"An error occurred: {e}")
                new_data4 = Data()
                new_data4.content = table_data
                new_data4.content_type = site_type + "_4"
                new_data4.save()
            elif site_type == "RCMS_2":
                #Model = apps.get_model('rcms', 'Rcms_2_1')
                await page.locator('#wfm_header_btn_userName').click()
                async with page.expect_popup() as page_info:
                    await page.get_by_role("link", name="개인정보수정").click()
                page_1 = await page_info.value
                await page_1.frame_locator("iframe[name=\"info\"]").get_by_label("비밀번호").fill("@siab812580")
                await page_1.frame_locator("iframe[name=\"info\"]").get_by_role("link", name="확인").click()
                await page_1.wait_for_load_state("domcontentloaded")
                table_data = []
                async def extract_table_data(selector):
                    rows = await page_1.query_selector_all(f'{selector} tbody tr')
                    table = []
                    for row in rows:
                        cells = await row.query_selector_all('td')
                        row_data = [await cell.inner_text() for cell in cells]
                        table.append(row_data)
                    return table

                try:
                #    table_data.extend(await extract_table_data('table.tbl_type01'))
                    rows = await page_1.query_selector_all(f'table.tbl_type01 tbody tr')
                    table = []
                    for row in rows:
                        cells = await row.query_selector_all('td')
                        title = await cells[1].inner_text() if len(cells) > 1 else None
                        checkbox = await row.query_selector("input[name='sysCheckbox']")
                        checked = await checkbox.get_attribute('checked') is not None if checkbox else False
                        if title and title.strip() not in ["동의", "전체", ""]:
                            if not any(item['title'] == title.strip() for item in table):
                                table.append({
                                    "title": title.strip(),
                                    "checked": checked
                                })
                    print(table)

                except Exception as e:
                    print(f"An error occurred while extracting data from tbl_type01: {e}")
                try:
                    #table_data.extend(await extract_table_data('table.tbl_type02'))
                    rows = await page_1.query_selector_all(f'table.tbl_type02 tbody tr')
                    data = {}
                    for row in rows:
                        # 각 행에서 th와 td 추출
                        th = await row.query_selector('th')
                        td = await row.query_selector('td')

        # th와 td의 내용을 읽어와 데이터에 저장
                        if th and td:
                            if th:
                                key = (await th.inner_text()).strip()
                                combined_value = ""
                                #select_tags = await td.query_selector_all('select')
                                #for select in select_tags:
                                #    selected_value = await select.input_value()
                                #    if selected_value:  # 값이 있으면 추가
                                #        combined_value += f"{selected_value} "

                                # td 내부의 input 태그 처리
                                input_tags = await td.query_selector_all('input')
                                for input_tag in input_tags:
                                    input_value = await input_tag.input_value()
                                    if input_value:  # 값이 있으면 추가
                                        combined_value += f"{input_value} "
                                child_selects = await td.query_selector_all('select')
                                raw_text = (await td.inner_text()).strip()

                                # Remove text content of <select> elements from raw_text
                                for select in child_selects:
                                    selected_text = await select.inner_text()
                                    raw_text = raw_text.replace(selected_text.strip(), "")

                                # 중복 방지 및 텍스트 추가
                                if raw_text.strip() and raw_text.strip() not in combined_value:
                                    combined_value += f"{raw_text.strip()} "

                                data[key] = combined_value.strip()
                    print(data)
                except Exception as e:
                    print(f"An error occurred while extracting data from tbl_type02: {e}")
                try:
                    table_data.extend(await extract_table_data('table.tbl_type02.mgt_20.trTrg3'))
                except Exception as e:
                    print(f"An error occurred while extracting data from tbl_type02 mgt_20 trTrg3: {e}")
                try:
                    table_data.extend(await extract_table_data('table.tbl_type02.mgt_20'))
                except Exception as e:
                    print(f"An error occurred while extracting data from tbl_type02 mgt_20: {e}")
                #new_data = Data()
                #new_data.content = table_data
                #new_data.content_type = site_type + "_1"
                #new_data.save()

                await page_1.get_by_role("link", name="개인정보 이용·제공 동의/철회내역").click()
                await page_1.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    rows = await page_1.query_selector_all('div#divTab02 table.tbl_type01 tbody tr')
                    for row in rows:
                        cells = await row.query_selector_all('td')
                        row_data = [await cell.inner_text() for cell in cells]
                        table_data.append(row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                #new_data2 = Data()
                #new_data2.content = table_data
                #new_data2.content_type = site_type + "_2"
                #new_data2.save()
            
                await page_1.get_by_role("link", name="최근 접속이력").click()
                await page_1.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    rows = await page_1.query_selector_all('div#divTab03 table.tbl_type01 tbody tr')
                    for row in rows:
                        cells = await row.query_selector_all('td')
                        row_data = [await cell.inner_text() for cell in cells]
                        table_data.append(row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                #new_data3 = Data()
                #new_data3.content = table_data
                #new_data3.content_type = site_type + "_3"
                #new_data3.save()
            elif site_type == "RCMS_3":
                await page.get_by_role("link", name="고객지원").click()
                await page.get_by_role("link", name="자료실", exact=True).click()
                await page.get_by_role("link", name="이용매뉴얼").click()
                await page.wait_for_load_state("domcontentloaded")
                Model = apps.get_model('rcms', 'Rcms_3_1')
                Model.objects.filter(account=user_id).delete()
                Model2 = apps.get_model('rcms', 'Rcms_3_2')
                Model2.objects.filter(account=user_id).delete()
                has_next_page = True
                while has_next_page:
                    try:
                        rows = await page.query_selector_all('table#wfm_main_gridView_body_table tbody#wfm_main_gridView_body_tbody tr')
                        for row in rows:
                            cells = await row.query_selector_all('td.w2grid_input_table.gridBodyDefault.gridBodyDefault_data.w2grid_default_readonly')
                            Model.objects.create(
                                account = user_id,
                                num = (await cells[0].inner_text()).strip(),
                                assort = (await cells[1].inner_text()).strip(),
                                title = (await cells[2].inner_text()).strip(),
                                upload_file = (await cells[3].inner_text()).strip(),
                                writer = (await cells[4].inner_text()).strip(),
                                create_date = (await cells[5].inner_text()).strip(),
                                views = (await cells[6].inner_text()).strip(),
                            )
                        await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                        current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                        current_page_number = await current_page.inner_text() if current_page else "1"

                        next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                        if next_button and await next_button.is_enabled():
                            await next_button.click()
                            await page.wait_for_load_state("domcontentloaded")
                            new_page_number = str(int(current_page_number) + 1)
                            try:
                                await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                            except Exception as e:
                                has_next_page = False
                        else:
                            has_next_page = False
                    except Exception as e:
                        print(f"An error occurred while extracting data: {e}")
                        has_next_page = False
                await page.get_by_role("link", name="고객지원").click()
                await page.get_by_role("link", name="자료실", exact=True).click()
                await page.get_by_role("link", name="기타자료실").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                has_next_page = True
                while has_next_page:
                    try:
                        rows = await page.query_selector_all('table#wfm_main_gridView_body_table tbody#wfm_main_gridView_body_tbody tr')
                        for row in rows:
                            cells = await row.query_selector_all('td.w2grid_input_table.gridBodyDefault.gridBodyDefault_data.w2grid_default_readonly')
                            Model2.objects.create(
                                account = user_id,
                                num = (await cells[0].inner_text()).strip(),
                                archive_name = (await cells[1].inner_text()).strip(),
                                title = (await cells[2].inner_text()).strip(),
                                upload_file = (await cells[3].inner_text()).strip(),
                                writer = (await cells[4].inner_text()).strip(),
                                create_date = (await cells[5].inner_text()).strip(),
                                views = (await cells[6].inner_text()).strip(),
                            )
                        await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                        current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                        current_page_number = await current_page.inner_text() if current_page else "1"

                        next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                        if next_button and await next_button.is_enabled():
                            await next_button.click()
                            await page.wait_for_load_state("domcontentloaded")
                            new_page_number = str(int(current_page_number) + 1)
                            try:
                                await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                            except Exception as e:
                                has_next_page = False
                        else:
                            has_next_page = False
                    except Exception as e:
                        print(f"An error occurred while extracting data: {e}")
                        has_next_page = False
 
            elif site_type == "RCMS_4":
                await page.get_by_role("link", name="고객지원").click()
                await page.get_by_role("link", name="문의답변").click()
                await page.get_by_role("link", name="자주묻는질문").click()
                await page.wait_for_load_state("domcontentloaded")
                Model = apps.get_model('rcms', 'Rcms_4')
                Model.objects.filter(account=user_id).delete()
                table_data = []
                async def extract_table_data():
                    data = []
                    try:
                        rows = await page.query_selector_all('table#wfm_main_gridView_body_table tbody tr')
                        for row in rows:
                            cells = await row.query_selector_all('td')
                            row_data = [await cell.inner_text() for cell in cells]
                            data.append(row_data)
                    except Exception as e:
                        print(f"An error occurred while extracting data: {e}")
                    return data

                has_next_page = True
                while has_next_page:
                    try:
                        rows = await page.query_selector_all('table#wfm_main_gridView_body_table tbody#wfm_main_gridView_body_tbody tr')
                        for row in rows:
                            cells = await row.query_selector_all('td.w2grid_input_table.gridBodyDefault.gridBodyDefault_data.w2grid_default_readonly')
                            Model.objects.create(
                                account = user_id,
                                num = (await cells[0].inner_text()).strip(),
                                title = (await cells[2].inner_text()).strip(),
                                upload_file = "",
                                writer = (await cells[3].inner_text()).strip(),
                                create_date = (await cells[4].inner_text()).strip(),
                                views = (await cells[5].inner_text()).strip(),
                            )
                        await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                        current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                        current_page_number = await current_page.inner_text() if current_page else "1"

                        next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                        if next_button and await next_button.is_enabled():
                            await next_button.click()
                            await page.wait_for_load_state("domcontentloaded")
                            new_page_number = str(int(current_page_number) + 1)
                            try:
                                await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                            except Exception as e:
                                has_next_page = False
                        else:
                            has_next_page = False
                    except Exception as e:
                        print(f"An error occurred while extracting data: {e}")
                        has_next_page = False




                """
                new_data7 = Data()
                new_data7.content = table_data
                new_data7.content_type = site_type + "_7"
                new_data7.save()
                await page.get_by_role("tab", name="연구비정산").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                has_next_page = True
                while has_next_page:
                    table_data.extend(await extract_table_data())
                    await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                    current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                    current_page_number = await current_page.inner_text() if current_page else "1"

                    next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                    if next_button and await next_button.is_enabled():
                        await next_button.click()
                        await page.wait_for_load_state("domcontentloaded")
                        new_page_number = str(int(current_page_number) + 1)
                        try:
                            await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                        except Exception as e:
                            has_next_page = False
                    else:
                        has_next_page = False
                new_data8 = Data()
                new_data8.content = table_data
                new_data8.content_type = site_type + "_8"
                new_data8.save()
            """
            elif site_type == "RCMS_5":
                await page.get_by_role("link", name="공지사항").click()
                await page.get_by_role("link", name="일반공지").click()
                await page.wait_for_load_state("domcontentloaded")
                Model = apps.get_model('rcms', 'Rcms_5_1')
                Model.objects.filter(account=user_id).delete()
                Model2 = apps.get_model('rcms', 'Rcms_5_2')
                Model2.objects.filter(account=user_id).delete()
                has_next_page = True
                
                while has_next_page:
                    try:
                        rows = await page.query_selector_all('table#wfm_main_gridView_body_table tbody#wfm_main_gridView_body_tbody tr')
                        for row in rows:
                            cells = await row.query_selector_all('td.w2grid_input_table.gridBodyDefault.gridBodyDefault_data.w2grid_default_readonly')
                            Model.objects.create(
                                account = user_id,
                                num = (await cells[0].inner_text()).strip(),
                                assort = (await cells[1].inner_text()).strip(),
                                title = (await cells[2].inner_text()).strip(),
                                upload_file = (await cells[3].inner_text()).strip(),
                                writer = (await cells[4].inner_text()).strip(),
                                create_date = (await cells[5].inner_text()).strip(),
                                views = (await cells[6].inner_text()).strip(),
                            )
                        await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                        current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                        current_page_number = await current_page.inner_text() if current_page else "1"

                        next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                        if next_button and await next_button.is_enabled():
                            await next_button.click()
                            await page.wait_for_load_state("domcontentloaded")
                            new_page_number = str(int(current_page_number) + 1)
                            try:
                                await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                            except Exception as e:
                                has_next_page = False
                        else:
                            has_next_page = False
                    except Exception as e:
                        print(f"An error occurred while extracting data: {e}")
                        has_next_page = False


                """
                await page.get_by_role("tab", name="공통").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                has_next_page = True
                while has_next_page:
                    table_data.extend(await extract_table_data())
                    await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                    current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                    current_page_number = await current_page.inner_text() if current_page else "1"

                    next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                    if next_button and await next_button.is_enabled():
                        await next_button.click()
                        await page.wait_for_load_state("domcontentloaded")
                        new_page_number = str(int(current_page_number) + 1)
                        try:
                            await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                        except Exception as e:
                            has_next_page = False
                    else:
                        has_next_page = False
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type + "_2"
                new_data2.save()
                await page.get_by_role("tab", name="연구개발기관").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                has_next_page = True
                while has_next_page:
                    table_data.extend(await extract_table_data())
                    await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                    current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                    current_page_number = await current_page.inner_text() if current_page else "1"

                    next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                    if next_button and await next_button.is_enabled():
                        await next_button.click()
                        await page.wait_for_load_state("domcontentloaded")
                        new_page_number = str(int(current_page_number) + 1)
                        try:
                            await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                        except Exception as e:
                            has_next_page = False
                    else:
                        has_next_page = False
                new_data3 = Data()
                new_data3.content = table_data
                new_data3.content_type = site_type + "_3"
                new_data3.save()
                """
                await page.get_by_role("link", name="공지사항").click()
                await page.get_by_role("link", name="시스템공지").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector('table#wfm_main_gridView_body_table tbody#wfm_main_gridView_body_tbody tr')
                has_next_page = True
                while has_next_page:
                    try:
                        rows = await page.query_selector_all('table#wfm_main_gridView_body_table tbody#wfm_main_gridView_body_tbody tr')
                        for row in rows:
                            cells = await row.query_selector_all('td.w2grid_input_table.gridBodyDefault.gridBodyDefault_data.w2grid_default_readonly')
                            Model2.objects.create(
                                account = user_id,
                                num = (await cells[0].inner_text()).strip(),
                                assort = (await cells[1].inner_text()).strip(),
                                title = (await cells[2].inner_text()).strip(),
                                upload_file = (await cells[3].inner_text()).strip(),
                                writer = (await cells[4].inner_text()).strip(),
                                create_date = (await cells[5].inner_text()).strip(),
                                views = (await cells[6].inner_text()).strip(),
                            )
                        await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                        current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                        current_page_number = await current_page.inner_text() if current_page else "1"

                        next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                        if next_button and await next_button.is_enabled():
                            await next_button.click()
                            await page.wait_for_load_state("domcontentloaded")
                            new_page_number = str(int(current_page_number) + 1)
                            try:
                                await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                            except Exception as e:
                                has_next_page = False
                        else:
                            has_next_page = False
                    except Exception as e:
                        print(f"An error occurred while extracting data: {e}")
                        has_next_page = False
                #new_data4 = Data()
                #new_data4.content = table_data
                #new_data4.content_type = site_type + "_4"
                #new_data4.save()
                """
                await page.get_by_role("tab", name="공통").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                has_next_page = True
                while has_next_page:
                    table_data.extend(await extract_table_data())
                    await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                    current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                    current_page_number = await current_page.inner_text() if current_page else "1"

                    next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                    if next_button and await next_button.is_enabled():
                        await next_button.click()
                        await page.wait_for_load_state("domcontentloaded")
                        new_page_number = str(int(current_page_number) + 1)
                        try:
                            await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                        except Exception as e:
                            has_next_page = False
                    else:
                        has_next_page = False
                new_data5 = Data()
                new_data5.content = table_data
                new_data5.content_type = site_type + "_5"
                new_data5.save()
                await page.get_by_role("tab", name="연구개발기관").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                has_next_page = True
                while has_next_page:
                    table_data.extend(await extract_table_data())
                    await page.wait_for_selector('#wfm_main_pagelist_next_btn')
                    current_page = await page.query_selector('td.w2pageList_col_label div.w2pageList_label_selected')
                    current_page_number = await current_page.inner_text() if current_page else "1"

                    next_button = await page.query_selector('#wfm_main_pagelist_next_btn')
                    if next_button and await next_button.is_enabled():
                        await next_button.click()
                        await page.wait_for_load_state("domcontentloaded")
                        new_page_number = str(int(current_page_number) + 1)
                        try:
                            await page.wait_for_selector(f'td.w2pageList_col_label div[index="{new_page_number}"]', state="attached", timeout=5000)
                        except Exception as e:
                            has_next_page = False
                    else:
                        has_next_page = False
                new_data6 = Data()
                new_data6.content = table_data
                new_data6.content_type = site_type + "_6"
                new_data6.save()
                """
            elif site_type == "RCMS_6":
                await page.get_by_role("link", name="이용가이드").click()
                await page.get_by_role("link", name="관계법령").click()
                await page.get_by_role("link", name="국가연구개발혁신법").click()
                await page.wait_for_load_state("domcontentloaded")
                Model = apps.get_model('rcms', 'Rcms_6_1')
                Model.objects.all().delete()
                Model2 = apps.get_model('rcms', 'Rcms_6_2')
                Model2.objects.all().delete()
                Model3 = apps.get_model('rcms', 'Rcms_6_3')
                Model3.objects.all().delete()
                Model4 = apps.get_model('rcms', 'Rcms_6_4')
                Model4.objects.all().delete()
                Model5 = apps.get_model('rcms', 'Rcms_6_5')
                Model5.objects.all().delete()
                Model6 = apps.get_model('rcms', 'Rcms_6_6')
                Model6.objects.all().delete()
                await page.wait_for_selector('div.w2group.section')
                sections = await page.query_selector_all('div.w2group.linkbox.potal_lybox')
                for section in sections:
                    section_title = await section.query_selector('div.w2group.ly_column h2.w2textbox')
                    title_text = await section_title.inner_text() if section_title else "No Title"

                    links = await section.query_selector_all('a.w2anchor2, a.btn_external_link, a.btn_pdf_link')
                    for link in links:
                        Model.objects.create(
                            assort = "국가연구개발혁신법",
                            group = (title_text).strip(),
                            link_text = (await link.inner_text()).strip(),
                            external_link = "",
                        )

                await page.get_by_role("link", name="이용가이드").click()
                await page.get_by_role("link", name="관계법령").click()
                await page.get_by_role("link", name="산업기술혁신촉진법").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector('div.w2group.section')
                sections = await page.query_selector_all('div.w2group.linkbox.potal_lybox')
                for section in sections:
                    section_title = await section.query_selector('div.w2group.ly_column h2.w2textbox')
                    title_text = await section_title.inner_text() if section_title else "No Title"

                    links = await section.query_selector_all('a.w2anchor2, a.btn_external_link, a.btn_pdf_link')
                    for link in links:
                        Model2.objects.create(
                            assort = "산업기술혁신촉진법",
                            group = (title_text).strip(),
                            link_text = (await link.inner_text()).strip(),
                            external_link = "",
                        )
                await page.get_by_role("link", name="이용가이드").click()
                await page.get_by_role("link", name="관계법령").click()
                await page.get_by_role("link", name="중소기업기술혁신촉진법").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector('div.w2group.section')
                sections = await page.query_selector_all('div.w2group.linkbox.potal_lybox')
                for section in sections:
                    section_title = await section.query_selector('div.w2group.ly_column h2.w2textbox')
                    title_text = await section_title.inner_text() if section_title else "No Title"

                    links = await section.query_selector_all('a.w2anchor2, a.btn_external_link, a.btn_pdf_link')
                    for link in links:
                        Model3.objects.create(
                            assort = "중소기업기술혁신촉진법",
                            group = (title_text).strip(),
                            link_text = (await link.inner_text()).strip(),
                            external_link = "",
                        )
                await page.get_by_role("link", name="이용가이드").click()
                await page.get_by_role("link", name="관계법령").click()
                await page.get_by_role("link", name="환경기술및환경산업지원법").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector('div.w2group.section')
                sections = await page.query_selector_all('div.w2group.linkbox.potal_lybox')
                for section in sections:
                    section_title = await section.query_selector('div.w2group.ly_column h2.w2textbox')
                    title_text = await section_title.inner_text() if section_title else "No Title"

                    links = await section.query_selector_all('a.w2anchor2, a.btn_external_link, a.btn_pdf_link')
                    for link in links:
                        Model4.objects.create(
                            assort = "환경기술및환경산업지원법",
                            group = (title_text).strip(),
                            link_text = (await link.inner_text()).strip(),
                            external_link = "",
                        )
                await page.get_by_role("link", name="이용가이드").click()
                await page.get_by_role("link", name="관계법령").click()
                await page.get_by_role("link", name="해양수산과학기술육성법").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector('div.w2group.section')
                sections = await page.query_selector_all('div.w2group.linkbox.potal_lybox')
                for section in sections:
                    section_title = await section.query_selector('div.w2group.ly_column h2.w2textbox')
                    title_text = await section_title.inner_text() if section_title else "No Title"

                    links = await section.query_selector_all('a.w2anchor2, a.btn_external_link, a.btn_pdf_link')
                    for link in links:
                        Model5.objects.create(
                            assort = "해양수산과학기술육성법",
                            group = (title_text).strip(),
                            link_text = (await link.inner_text()).strip(),
                            external_link = "",
                        )
                await page.get_by_role("link", name="이용가이드").click()
                await page.get_by_role("link", name="관계법령").click()
                await page.get_by_role("link", name="방위산업기술보호법").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector('div.w2group.section')
                sections = await page.query_selector_all('div.w2group.linkbox.potal_lybox')
                for section in sections:
                    section_title = await section.query_selector('div.w2group.ly_column h2.w2textbox')
                    title_text = await section_title.inner_text() if section_title else "No Title"

                    links = await section.query_selector_all('a.w2anchor2, a.btn_external_link, a.btn_pdf_link')
                    for link in links:
                        Model6.objects.create(
                            assort = "방위산업기술보호법",
                            group = (title_text).strip(),
                            link_text = (await link.inner_text()).strip(),
                            external_link = "",
                        )
            elif site_type == "RCMS_8":
                Model = apps.get_model('rcms', 'Rcms_8_1')
                Model.objects.filter(account=user_id).delete()
                Model2 = apps.get_model('rcms', 'Rcms_8_2')
                Model2.objects.filter(account=user_id).delete()
                Model3_1 = apps.get_model('rcms', 'Rcms_8_3_1')
                Model3_1.objects.filter(account=user_id).delete()

                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="연구비 총괄 현황표").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()

                await page.get_by_role("link", name="전체과제").click()

                await page.get_by_role("gridcell", name=p_num).click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('div.w2group.section')
                flags = await page.query_selector_all('div.w2group.flag.type2 span.w2span')
                titles = await page.query_selector_all('div.w2textbox.ass_txt2')
                contents = await page.query_selector_all('span.toggle_txt')

                for title in titles:
                    Model.objects.create(
                        account= user_id,
                        p_num = p_num,
                        flag_1 = (await flags[0].inner_text()).strip(),
                        flag_2 = (await flags[1].inner_text()).strip(),
                        flag_3 = (await flags[2].inner_text()).strip(),
                        assign_name = (await title.inner_text()).strip(),
                        step_annual = (await contents[1].inner_text()).strip(),
                        organization = (await contents[2].inner_text()).strip(),
                        pro_inst = (await contents[3].inner_text()).strip(),
                        dev_period = (await contents[4].inner_text()).strip(),
                        manager = (await contents[5].inner_text()).strip(),
                        host_rnd_inst = (await contents[6].inner_text()).strip(),
                    )
                
                first_value_element = await page.query_selector('#tac_layout_contents_211A0_body_ORGN_NM_label')
                first_value = await first_value_element.inner_text()
                #table = await page.query_selector('table#tac_layout_contents_211A0_body_wq_uuid_1045')
                tables = await page.query_selector_all('table.w2group.w2tb.tb')
                target_table = None

                for table in tables:
                    td = await table.query_selector('td.w2group.w2tb_td.tac div.w2textbox.txt_box')
                    if td:
                        target_table = table
                        break
                other_elements = await target_table.query_selector_all('td.w2group.w2tb_td.tac div.w2textbox.txt_box')
                #for element in other_elements:
                #    value = await element.inner_text()
                #print(await other_elements[0].inner_text())
                
                #table = await page.query_selector('div#tac_layout_contents_211A0_body_wq_uuid_1098')
                #other_elements = await table.query_selector_all('table tbody div.w2textbox.txt_box')
                #for element in other_elements:
                #    print(await element.inner_text())
                if other_elements:
                    Model2.objects.create(
                        account= user_id,
                        p_num = p_num,
                        rnd_inst = first_value,
                        app_category = (await other_elements[0].inner_text()).strip(),
                        host_rnd_inst = (await other_elements[1].inner_text()).strip(),
                        current_dev_period = (await other_elements[2].inner_text()).strip(),
                        total_dev_period = (await other_elements[3].inner_text()).strip(),
                        pro_inst = (await other_elements[4].inner_text()).strip(),
                        agree_class = (await other_elements[5].inner_text()).strip(),
                        settle_form = (await other_elements[6].inner_text()).strip(),
                        rnd_cost_payment_assort = (await other_elements[7].inner_text()).strip(),
                        assign_agree_status = (await other_elements[8].inner_text()).strip(),
                        execute_status = (await other_elements[9].inner_text()).strip(),
                        research_fund_account = (await other_elements[10].inner_text()).strip(),
                    )
                #await page.wait_for_selector('#tac_layout_contents_211A0_body_gv_egm_body_table')
                #grid_rows = await page.query_selector_all('#tac_layout_contents_211A0_body_gv_egm_body_table tbody tr')
                #for row_index, grid_row in enumerate(grid_rows):
                #    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_211A0_body_gv_egm_cell_{row_index}_"]')
                #    grid_row_data = []
                #    for grid_cell in grid_cells:
                #        grid_cell_text = await grid_cell.inner_text()
                #        grid_row_data.append(grid_cell_text.strip())
                #    table_data.append(grid_row_data)
                #new_data = Data()
                #new_data.content = table_data
                #new_data.content_type = site_type
                #new_data.save()

                await page.locator("#tac_layout_contents_211A0_body_btn_cnIdenSttNm").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtDtlMainPopup_body_grd_agrtDtlMainPopup_body_table tbody tr')
                #grid_rows = await page.query_selector_all('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtDtlMainPopup_body_grd_agrtDtlMainPopup_body_table tbody tr')
                grid_row = await page.query_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtDtlMainPopup_body_grd_agrtDtlMainPopup_main_div')
                grid_rows = await grid_row.query_selector_all('tr.grid_body_row')
                for row in grid_rows:
                    cells = await row.query_selector_all('td nobr.w2grid_input.w2grid_input_readonly')
                    if cells:
                        Model3_1.objects.create(
                            account= user_id,
                            p_num = p_num,
                            tab_title = "연구개발비구성",
                            step = (await cells[0].inner_text()).strip(),
                            annual = (await cells[1].inner_text()).strip(),
                            part_class = (await cells[2].inner_text()).strip(),
                            rnd_inst = (await cells[3].inner_text()).strip(),
                            rnd_cost_payment_assort = (await cells[4].inner_text()).strip(),
                            total_cash_1 = (await cells[5].inner_text()).strip(),
                            total_kind_1 = (await cells[6].inner_text()).strip(),
                            gov_sup_rnd_cash = (await cells[7].inner_text()).strip(),
                            inst_rnd_cash = (await cells[8].inner_text()).strip(),
                            inst_rnd_kind = (await cells[9].inner_text()).strip(),
                            local_gov_rnd_cash = (await cells[10].inner_text()).strip(),
                            local_gov_rnd_kind = (await cells[11].inner_text()).strip(),
                            total_cash_2 = (await cells[12].inner_text()).strip(),
                            total_kind_2 = (await cells[13].inner_text()).strip(),
                            direct_cost_cash = (await cells[14].inner_text()).strip(),
                            direct_cost_kind = (await cells[15].inner_text()).strip(),
                            indirect_cost_cash = (await cells[16].inner_text()).strip(),
                            indirect_cost_kind = (await cells[17].inner_text()).strip(),
                            commission_rnd_cash = (await cells[18].inner_text()).strip(),
                            commission_rnd_kind = (await cells[19].inner_text()).strip(),
                        )

                await page.get_by_role("tab", name="연구개발기관").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_bexpCpstPopup_body_table tbody tr')
                #grid_rows = await page.query_selector_all('#tac_layout_contents_24210_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_bexpCpstPopup_body_table tbody tr')
                grid_row = await page.query_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_bexpCpstPopup_main_div')
                grid_rows = await grid_row.query_selector_all('tr.grid_body_row')
                Model3_2 = apps.get_model('rcms', 'Rcms_8_3_2')
                Model3_2.objects.filter(account=user_id).delete()
                for row in grid_rows:
                    cells = await row.query_selector_all('td nobr.w2grid_input.w2grid_input_readonly')
                    if cells:
                        Model3_2.objects.create(
                            account= user_id,
                            p_num = p_num,
                            tab_title = "연구개발기관",
                            business_reg_num = (await cells[0].inner_text()).strip(),
                            rnd_inst = (await cells[1].inner_text()).strip(),
                            rnd_cost_payment_assort = (await cells[2].inner_text()).strip(),
                            participate_assort = (await cells[3].inner_text()).strip(),
                            non_profit = (await cells[4].inner_text()).strip(),
                            bank = (await cells[5].inner_text()).strip(),
                            research_fund_account = (await cells[6].inner_text()).strip(),
                            payment_whether = (await cells[7].inner_text()).strip(),
                            pro_inst = (await cells[8].inner_text()).strip(),
                            innovation_act_whether = (await cells[9].inner_text()).strip(),
                            annual_leave_report = (await cells[10].inner_text()).strip(),
                        )
                await page.get_by_role("tab", name="참여연구자").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_ptcpMbrPopup_body_grd_ptcpMbrPopup_body_table tbody tr')
                grid_row = await page.query_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_ptcpMbrPopup_body_grd_ptcpMbrPopup_main_div')
                grid_rows = await grid_row.query_selector_all('tr.grid_body_row')
                Model3_3 = apps.get_model('rcms', 'Rcms_8_3_3')
                Model3_3.objects.filter(account=user_id).delete()
                for row in grid_rows:
                    cells = await row.query_selector_all('td nobr.w2grid_input.w2grid_input_readonly')
                    if cells:
                        Model3_3.objects.create(
                            account= user_id,
                            p_num = p_num,
                            tab_title = "참여연구자",
                            rnd_inst = (await cells[0].inner_text()).strip(),
                            participate_assort = (await cells[1].inner_text()).strip(),
                            name = (await cells[2].inner_text()).strip(),
                            birth_date = (await cells[3].inner_text()).strip(),
                            foreign_dist = (await cells[4].inner_text()).strip(),
                            labor_cost_rate = (await cells[5].inner_text()).strip(),
                            start_date = (await cells[6].inner_text()).strip(),
                            end_date = (await cells[7].inner_text()).strip(),
                            employ_type = (await cells[8].inner_text()).strip(),
                        )
                await page.get_by_role("tab", name="과제조회권한자").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtOrgnPopup_body_grd_agrtOrgnPopup_body_table tbody tr')
                grid_row = await page.query_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtOrgnPopup_body_grd_agrtOrgnPopup_main_div')
                grid_rows = await grid_row.query_selector_all('tr.grid_body_row')
                Model3_4 = apps.get_model('rcms', 'Rcms_8_3_4')
                Model3_4.objects.filter(account=user_id).delete()
                for row in grid_rows:
                    cells = await row.query_selector_all('td nobr.w2grid_input.w2grid_input_readonly')
                    if cells:
                        Model3_4.objects.create(
                            account= user_id,
                            p_num = p_num,
                            tab_title = "과제조회권한자",
                            inst = (await cells[0].inner_text()).strip(),
                            inst_role = (await cells[1].inner_text()).strip(),
                            name = (await cells[2].inner_text()).strip(),
                            position = (await cells[3].inner_text()).strip(),
                            res_fund_execute_auth = (await cells[4].inner_text()).strip(),
                        )

                #new_data4 = Data()
                #new_data4.content = table_data
                #new_data4.content_type = site_type + "_1_4"
                #new_data4.save()

                await page.get_by_role("tab", name="연구비 총괄 현황표").click()
                await page.locator("#tac_layout_contents_211A0_body_btn_tosAuthCnt").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_24230_body_gv_egm_body_table tbody tr')
                grid_row = await page.query_selector('#tac_layout_contents_24230_body_gv_egm_main_div')
                grid_rows = await grid_row.query_selector_all('tr.grid_body_row')
                
                Model4 = apps.get_model('rcms', 'Rcms_8_4')
                Model4.objects.filter(account=user_id).delete()
                for row in grid_rows:
                    cells = await row.query_selector_all('td nobr.w2grid_input.w2grid_input_readonly')
                    if cells:
                        Model4.objects.create(
                            account= user_id,
                            p_num = p_num,
                            tab_title = "사용권한 관리",
                            name = (await cells[0].inner_text()).strip(),
                            part_class = (await cells[1].inner_text()).strip(),
                            res_fund_execute_auth = (await cells[2].inner_text()).strip(),
                            whether_use = (await cells[3].inner_text()).strip(),
                            identity = (await cells[4].inner_text()).strip(),
                            birth_date = (await cells[5].inner_text()).strip(),
                            whether_receive = (await cells[6].inner_text()).strip(),
                        )
                await page.get_by_role("tab", name="연구비 총괄 현황표").click()
                await page.locator("#tac_layout_contents_211A0_body_btn_agrToagCardCnt").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_24240_body_grd_view_body_table tbody tr')
                grid_row = await page.query_selector('#tac_layout_contents_24240_body_grd_view_main_div')
                grid_rows = await grid_row.query_selector_all('tr.grid_body_row')

                Model5 = apps.get_model('rcms', 'Rcms_8_5')
                Model5.objects.filter(account=user_id).delete()
                for row in grid_rows:
                    cells = await row.query_selector_all('td nobr.w2grid_input.w2grid_input_readonly')
                    if cells:
                        Model5.objects.create(
                            account= user_id,
                            p_num = p_num,
                            tab_title = "사용카드 관리",
                            assort = (await cells[0].inner_text()).strip(),
                            card_company = (await cells[1].inner_text()).strip(),
                            card_num = (await cells[2].inner_text()).strip(),
                            validity_period = (await cells[3].inner_text()).strip(),
                            payment_bank = (await cells[4].inner_text()).strip(),
                            payment_account_num = (await cells[5].inner_text()).strip(),
                            payment_date = (await cells[6].inner_text()).strip(),
                            reg_date = (await cells[7].inner_text()).strip(),
                            reg_status = (await cells[8].inner_text()).strip(),
                            whether_reg = (await cells[9].inner_text()).strip(),
                        )

                await page.get_by_role("tab", name="연구비 총괄 현황표").click()
                await page.locator("#tac_layout_contents_211A0_body_btn_vtAcctIsutBrdc").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21140_body_grid_vtAcctIsutBrdnIqr_body_table tbody tr')
                grid_row = await page.query_selector('#tac_layout_contents_21140_body_grid_vtAcctIsutBrdnIqr_main_div')
                grid_rows = await grid_row.query_selector_all('tr.grid_body_row')

                Model6 = apps.get_model('rcms', 'Rcms_8_6')
                Model6.objects.filter(account=user_id).delete()
                for row in grid_rows:
                    cells = await row.query_selector_all('td nobr')
                    if cells:
                        Model6.objects.create(
                            account= user_id,
                            p_num = p_num,
                            tab_title = "가상계좌 발급 현황",
                            issue_date = (await cells[0].inner_text()).strip(),
                            issue_reason = (await cells[1].inner_text()).strip(),
                            req_amount = (await cells[2].inner_text()).strip(),
                            bank = (await cells[3].inner_text()).strip(),
                            virtual_account_num = (await cells[4].inner_text()).strip(),
                            depositor = (await cells[5].inner_text()).strip(),
                            process_status = (await cells[6].inner_text()).strip(),
                            deposit_date = (await cells[7].inner_text()).strip(),
                            deposit_deadline = (await cells[8].inner_text()).strip(),
                            request_reason = (await cells[9].inner_text()).strip(),
                            refusal_reason = (await cells[10].inner_text()).strip(),
                            pay_exclusion_status = (await cells[11].inner_text()).strip(),
                        )

                await page.get_by_role("tab", name="연구비 총괄 현황표").click()
                await page.locator("#tac_layout_contents_211A0_body_btn_rechctUseSitu").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21110_body_gv_egm_body_table tbody tr')
                grid_row = await page.query_selector('#tac_layout_contents_21110_body_gv_egm_main_div')
                grid_rows = await grid_row.query_selector_all('tr.grid_body_row')

                #Model7 = apps.get_model('rcms', 'Rcms_8_7')
                #Model7.objects.filter(account=user_id).delete()
                for row in grid_rows:
                    cells = await row.query_selector_all('td nobr')
                    if cells:
                        for cell in cells:
                            print((await cell.inner_text()).strip())
                        """
                        Model7.objects.create(
                            account= user_id,
                            p_num = p_num,
                            tab_title = "연구비 사용 현황",
                            issue_date = (await cells[0].inner_text()).strip(),
                            issue_reason = (await cells[1].inner_text()).strip(),
                            req_amount = (await cells[2].inner_text()).strip(),
                            bank = (await cells[3].inner_text()).strip(),
                            virtual_account_num = (await cells[4].inner_text()).strip(),
                            depositor = (await cells[5].inner_text()).strip(),
                            process_status = (await cells[6].inner_text()).strip(),
                            deposit_date = (await cells[7].inner_text()).strip(),
                            deposit_deadline = (await cells[8].inner_text()).strip(),
                            request_reason = (await cells[9].inner_text()).strip(),
                            refusal_reason = (await cells[10].inner_text()).strip(),
                            pay_exclusion_status = (await cells[11].inner_text()).strip(),
                        )
                        """
                #await page.get_by_role("tab", name="연구비 총괄 현황표").click()
                #await page.locator("#tac_layout_contents_211A0_body_btn_excc").click()
                #await page.wait_for_load_state("domcontentloaded")
                
                await page.get_by_role("tab", name="연구비 총괄 현황표").click()
                await page.locator("#tac_layout_contents_211A0_body_anc_coexDrwpMng").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngSituIqrLstCont_body_coex_drwp_annl_table_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngSituIqrLstCont_body_coex_drwp_annl_table_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngSituIqrLstCont_body_coex_drwp_annl_table_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                #new_data10 = Data()
                #new_data10.content = table_data
                #new_data10.content_type = site_type + "_2_6_1"
                #new_data10.save()
                await page.get_by_role("tab", name="계속비 편성 등록").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngRegCont_body_coex_drwp_annl_table_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngRegCont_body_coex_drwp_annl_table_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngRegCont_body_coex_drwp_annl_table_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                #new_data11 = Data()
                #new_data11.content = table_data
                #new_data11.content_type = site_type + "_2_6_2"
                #new_data11.save()
                await page.get_by_role("tab", name="계속비 편성 관리").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngLstCont_body_coex_drwp_mng_table_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngLstCont_body_coex_drwp_mng_table_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngLstCont_body_coex_drwp_mng_table_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                #new_data12 = Data()
                #new_data12.content = table_data
                #new_data12.content_type = site_type + "_2_6_3"
                #new_data12.save()
            elif site_type == "RCMS_9":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="연구비 사용 현황").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21110_body_gv_egm_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21110_body_gv_egm_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21110_body_gv_egm_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            
            elif site_type == "RCMS_10":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="연구비 사용 내역").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="전체").click()
                await page.get_by_role("link", name="조회", exact=True).click()
                await page.locator("#tac_layout_contents_21120_body_egm_btn").click()
                await page.locator("#tac_layout_contents_21120_body_grd_list_H_TOTAL_AMT").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21120_body_grd_list_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21120_body_grd_list_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21120_body_grd_list_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

                await page.locator("#tac_layout_contents_21120_body_grd_list_cell_0_1").click()
                await page.wait_for_selector('//table[contains(@id, "tac_layout_contents_21120_body__rechctUseRsltDtlPopup") and contains(@class, "w2tb")]')
                table_data = []
                rows = await page.query_selector_all('//table[contains(@id, "tac_layout_contents_21120_body__rechctUseRsltDtlPopup") and contains(@class, "w2tb")]/tbody/tr')
                for row in rows:
                    row_data = []
                    cells = await row.query_selector_all('th, td')
                    for cell in cells:
                        cell_text = await cell.inner_text()
                        row_data.append(cell_text.strip())
                    table_data.append(row_data)
                rows2 = await page.query_selector_all('//table[contains(@id, "tac_layout_contents_21120_body__rechctUseRsltDtlPopup") and contains(@class, "gridHeaderTableDefault")]/tbody/tr')
                for row in rows2:
                    row_data = []
                    cells = await row.query_selector_all('th, td')
                    for cell in cells:
                        cell_text = await cell.inner_text()
                        row_data.append(cell_text.strip())
                    table_data.append(row_data)
                new_data1 = Data()
                new_data1.content = table_data
                new_data1.content_type = site_type + "_1"
                new_data1.save()

            elif site_type == "RCMS_11":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="가상계좌 발급 현황").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="전체").click()
                await page.get_by_role("link", name="조회", exact=True).click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21140_body_grid_vtAcctIsutBrdnIqr_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21140_body_grid_vtAcctIsutBrdnIqr_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21140_body_grid_vtAcctIsutBrdnIqr_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_12":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="RCMS 이체 내역").click()
                await page.get_by_role("link", name="전체").click()
                await page.locator("#tac_layout_contents_21150_body_sel_acctInfo").click()
                await page.locator("#tac_layout_contents_21150_body_sel_acctInfo_itemTable_1").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21150_body_grd_exctBrdnLstIqr_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21150_body_grd_exctBrdnLstIqr_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21150_body_grd_exctBrdnLstIqr_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_1"
                new_data.save()
                await page.get_by_role("tab", name="정산금/이자 지급내역").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21150_body_grd_ecamIntRcpsBrdnLstIqr_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21150_body_grd_ecamIntRcpsBrdnLstIqr_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21150_body_grd_ecamIntRcpsBrdnLstIqr_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type + "_2"
                new_data2.save()

            elif site_type == "RCMS_13":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="연구비 집행 상태").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21160_body_grd_rechctExctSttIqrList_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21160_body_grd_rechctExctSttIqrList_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21160_body_grd_rechctExctSttIqrList_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_14":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="이자 발생 내역").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21170_body_grd_view_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21170_body_grd_view_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21170_body_grd_view_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()    
            elif site_type == "RCMS_15":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="연구비 사용 등록").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name=p_num).click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                await page.locator("#tac_layout_contents_21210_body_tab_regMenu_contents_content_evdcInfo_body_sel_evdcSe_button").click()
                await page.get_by_text("카드", exact=True).click()
                await page.wait_for_load_state("networkidle")
                #await page.screenshot(path='screenshot.png')
                text_to_select = '5585-2697-3839-3886'
                td_xpath = f'//td[nobr[text()="{text_to_select}"]]'
                td_element = await page.query_selector(td_xpath)
                if td_element:
                    await td_element.click()
                await page.get_by_role("link", name="전체").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("networkidle")
                await page.screenshot(path='screenshot.png')
                table_data = []
                current_page = 1

                while True:
                    await page.wait_for_selector('table[id^="tac_layout_contents_21210_body_tab_regMenu_contents_content_evdcInfo_body_cardUseBrdnIqrLayer"] tbody')
                    table_selector = 'table[id^="tac_layout_contents_21210_body_tab_regMenu_contents_content_evdcInfo_body_cardUseBrdnIqrLayer"]'
                    tbody_selector = f'{table_selector} tbody'
                    rows = await page.query_selector_all(f'{tbody_selector} tr')
                    
                    for row in rows:
                        #cells = await row.query_selector_all('td')
                        cells = await row.query_selector_all('td[id*="_wframe_gv_cardFrpcBrdnIqrRes_cell_"]')
                        row_data = []
                        for cell in cells:
                            text = await cell.inner_text()
                            row_data.append(text.strip())
                        table_data.append(row_data)

                    next_button = await page.query_selector('td[id$="_next_btn"]')
                    current_page_element = await page.query_selector(f'div[role="button"][index="{current_page}"]')
                    next_page_element = await page.query_selector(f'div[role="button"][index="{current_page + 1}"]')
                    if not next_page_element:
                        break
                    await next_page_element.click()
                    await page.wait_for_selector(tbody_selector)
                    current_page += 1
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_1"
                new_data.save()

                #await page.locator("#tac_layout_contents_21210_body_tab_regMenu_contents_content_evdcInfo_body_sel_evdcSe_button").click()
                #await page.get_by_text("전자세금계산서").click()

                #await page.screenshot(path='screenshot.png')
                #await page.get_by_role("tab", name="기간 조회").click()
                #async with page.expect_download() as download_info:
                #    await page.get_by_role("link", name="예").click()
                #download = await download_info.value
                #print(download)
                #await page.get_by_role("link", name="확인 ").click()
                #await page.screenshot(path='screenshot.png')
                #await page.wait_for_load_state()
                #await page.get_by_role("link", name="조회", exact=True).click()
                #await page.get_by_role("gridcell", name="전자세금용").click()
                #await page.fill('input[type="password"]', 'ipc@20cokr')
                #await page.get_by_role("link", name="확인").click()

                #table_data = []
                #await page.wait_for_selector('#tac_layout_contents_21170_body_grd_view_body_table tbody tr')
                #grid_rows = await page.query_selector_all('#tac_layout_contents_21170_body_grd_view_body_table tbody tr')

                #for row_index, grid_row in enumerate(grid_rows):
                #    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21170_body_grd_view_cell_{row_index}_"]')
                #    grid_row_data = []
                #    for grid_cell in grid_cells:
                #        grid_cell_text = await grid_cell.inner_text()
                #        grid_row_data.append(grid_cell_text.strip())
                #    table_data.append(grid_row_data)
                #new_data = Data()
                #new_data.content = table_data
                #new_data.content_type = site_type + "_2"
                #new_data.save()
            elif site_type == "RCMS_16":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="연구비 이체 실행").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21220_body_grd_rechctUsePrtc_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21220_body_grd_rechctUsePrtc_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21220_body_grd_rechctUsePrtc_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_17":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="연구비 이체 결과").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="전체").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                await page.wait_for_selector('#tac_layout_contents_21230_body_grd_list_body_table tbody tr')
                grid_rows = await page.query_selector_all('#tac_layout_contents_21230_body_grd_list_body_table tbody tr')
                for row_index, grid_row in enumerate(grid_rows):
                    grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21230_body_grd_list_cell_{row_index}_"]')
                    grid_row_data = []
                    for grid_cell in grid_cells:
                        grid_cell_text = await grid_cell.inner_text()
                        grid_row_data.append(grid_cell_text.strip())
                    table_data.append(grid_row_data)
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_18":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="자계좌이체 승인 요청").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_19":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="현장실태 조사 준비").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_21250_body_gv_egm_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_21250_body_gv_egm_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_21250_body_gv_egm_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_20":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="사용등록 지연사유서").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_21":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="취소/복원 가상계좌 조회").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="조회", exact=True).click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_22100_body_gv_egm_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_22100_body_gv_egm_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_22100_body_gv_egm_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_22":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="취소/복원 내역 등록").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="전체").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_22200_body_grd_view_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_22200_body_grd_view_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_22200_body_grd_view_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_1"
                new_data.save()

                await page.get_by_role("tab", name="부가세복원").click()
                await page.get_by_role("link", name="전체").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_22200_body_cnclTabMain_contents_content2_body_grd_view_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_22200_body_cnclTabMain_contents_content2_body_grd_view_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_22200_body_cnclTabMain_contents_content2_body_grd_view_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type + "_2"
                new_data2.save()

            elif site_type == "RCMS_23":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="카드 승인취소 내역").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="전체").click()
                await page.locator("#tac_layout_contents_22300_body_SEL_CARD_NO").click()
                await page.locator("#tac_layout_contents_22300_body_SEL_CARD_NO_itemTable_1").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_22300_body_grd_view_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_22300_body_grd_view_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_22300_body_grd_view_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_24":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="연구비 상시 점검").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23100_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23100_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23100_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
                await page.get_by_role("gridcell", name="정상").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="조회", exact=True).click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23100_body_grd_basic_table_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23100_body_grd_basic_table_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23100_body_grd_basic_table_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data1 = Data()
                new_data1.content = table_data
                new_data1.content_type = site_type + "_1"
                new_data1.save()

            elif site_type == "RCMS_25":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="계속비 편성").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23700_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23700_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23700_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

                await page.get_by_role("gridcell", name="정상").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngSituIqrLstCont_body_coex_drwp_annl_table_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngSituIqrLstCont_body_coex_drwp_annl_table_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngSituIqrLstCont_body_coex_drwp_annl_table_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data1 = Data()
                new_data1.content = table_data
                new_data1.content_type = site_type + "_1"
                new_data1.save()

                await page.get_by_role("tab", name="계속비 편성 등록").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngRegCont_body_coex_drwp_annl_table_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngRegCont_body_coex_drwp_annl_table_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngRegCont_body_coex_drwp_annl_table_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type + "_2"
                new_data2.save()

                await page.get_by_role("tab", name="계속비 편성 관리").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngLstCont_body_coex_drwp_mng_table_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngLstCont_body_coex_drwp_mng_table_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23700_body_basic_tab_cont_contents_coexDrwpMngLstCont_body_coex_drwp_mng_table_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data3 = Data()
                new_data3.content = table_data
                new_data3.content_type = site_type + "_3"
                new_data3.save()
            
            elif site_type == "RCMS_26":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="카드대금 선입금").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23200_body_grd_cardPstlRqsListIqr_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23200_body_grd_cardPstlRqsListIqr_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23200_body_grd_cardPstlRqsListIqr_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_1"
                new_data.save()

                await page.get_by_role("tab", name="카드선입금 처리내역").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data1 = Data()
                new_data1.content = table_data
                new_data1.content_type = site_type + "_2"
                new_data1.save()
            elif site_type == "RCMS_27":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="정산 준비").click() 
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23300_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23300_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23300_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

                await page.get_by_role("gridcell", name="정상").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('div.w2group.section')
                    sections = await page.query_selector_all('div.w2group.section')

                    for section in sections:
                        section_title = await section.query_selector('h2')
                        title_text = await section_title.inner_text() if section_title else "No Title"

                        links = await section.query_selector_all('a.w2anchor2, a.btn_external_link, a.btn_pdf_link')
                        link_texts = [await link.inner_text() for link in links]
                        table_data.append({'section': title_text, 'links': link_texts})
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data1 = Data()
                new_data1.content = table_data
                new_data1.content_type = site_type + "_1"
                new_data1.save()

                await page.get_by_role("tab", name="정산서류등록").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23300_body_tab_exccRady_contents_content2_body_excc_pps_reg_table_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23300_body_tab_exccRady_contents_content2_body_excc_pps_reg_table_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23300_body_tab_exccRady_contents_content2_body_excc_pps_reg_table_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type + "_2"
                new_data2.save()

                await page.get_by_role("tab", name="전년도편성금사용등록").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_23300_body_tab_exccRady_contents_content3_body_grd_pryyCorvUseOrgnList_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23300_body_tab_exccRady_contents_content3_body_grd_pryyCorvUseOrgnList_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23300_body_tab_exccRady_contents_content3_body_grd_pryyCorvUseOrgnList_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                try:
                    await page.wait_for_selector('#tac_layout_contents_23300_body_tab_exccRady_contents_content3_body_grd_pryyCorvUseMstList_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23300_body_tab_exccRady_contents_content3_body_grd_pryyCorvUseMstList_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23300_body_tab_exccRady_contents_content3_body_grd_pryyCorvUseMstList_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data3 = Data()
                new_data3.content = table_data
                new_data3.content_type = site_type + "_3"
                new_data3.save()

                await page.get_by_role("tab", name="수익금등록").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data4 = Data()
                new_data4.content = table_data
                new_data4.content_type = site_type + "_4"
                new_data4.save()

            elif site_type == "RCMS_28":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="사용실적보고서 제출").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.locator("#tac_layout_contents_23400_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_cell_0_2").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('div[id^="tac_layout_contents_23400_body_txt_SBJT"]')
                    grid_rows = await page.query_selector_all('tr[id^="tac_layout_contents_23400_body_wq_uuid_"]')
                    for grid_row in grid_rows:
                        grid_cells = await grid_row.query_selector_all('div[id^="tac_layout_contents_23400_body_txt_SBJT"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data 1: {e}")

                try:
                    await page.wait_for_selector('#tac_layout_contents_23400_body_grd_usePfmcRptpSbmt_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23400_body_grd_usePfmcRptpSbmt_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23400_body_grd_usePfmcRptpSbmt_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                    footer_row = await page.query_selector('table#tac_layout_contents_23400_body_grd_usePfmcRptpSbmt_foot_table tbody tr')
                    footer_cells = await footer_row.query_selector_all('td')
                    footer_data = []
                    for footer_cell in footer_cells:
                        footer_cell_text = await footer_cell.inner_text()
                        footer_data.append(footer_cell_text.strip())
                    table_data.append(footer_data)
                except Exception as e:
                    print(f"An error occurred while extracting data 2: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()

            elif site_type == "RCMS_29":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="정산 진행 현황").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.locator("#tac_layout_contents_23500_body_wframe_sbjtSelectMain_wframe_sbjtSelect_gridView_cell_0_2").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('table[id^="tac_layout_contents_23500_body_wq_uuid_"]')
                    tables = await page.query_selector_all('table[id^="tac_layout_contents_23500_body_wq_uuid_"]')
                    for table in tables:
                        grid_rows = await table.query_selector_all('tbody tr')
                        for grid_row in grid_rows:
                            grid_cells = await grid_row.query_selector_all('div[id^="tac_layout_contents_23500_body_wq_uuid_"]')
                            grid_row_data = []
                            for grid_cell in grid_cells:
                                grid_cell_text = await grid_cell.inner_text()
                                grid_row_data.append(grid_cell_text.strip())
                            table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                try:
                    await page.wait_for_selector('#tac_layout_contents_23500_body_gv_egm_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23500_body_gv_egm_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23500_body_gv_egm_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                try:
                    await page.wait_for_selector('#tac_layout_contents_23500_body_grd_bexpUsePfmcLstIqr_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_23500_body_grd_bexpUsePfmcLstIqr_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_23500_body_grd_bexpUsePfmcLstIqr_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                    footer_row = await page.query_selector('table#tac_layout_contents_23500_body_grd_bexpUsePfmcLstIqr_foot_table tbody tr')
                    footer_cells = await footer_row.query_selector_all('td')
                    footer_data = []
                    for footer_cell in footer_cells:
                        footer_cell_text = await footer_cell.inner_text()
                        footer_data.append(footer_cell_text.strip())
                    table_data.append(footer_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_30":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="정산 점검 메모").click()
                await page.get_by_role("cell", name="과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_31":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="서비스 개요").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('div[id^="tac_layout_contents_26300_body_wq_uuid_"]')
                    extra_divs = await page.query_selector_all('div[id^="tac_layout_contents_26300_body_wq_uuid_"]')
                    for extra_div in extra_divs:
                        extra_div_text = await extra_div.inner_text()
                        table_data.append([extra_div_text.strip()])
                    await page.wait_for_selector('table[id^="tac_layout_contents_26300_body_wq_uuid_"]')
                    tables = await page.query_selector_all('table[id^="tac_layout_contents_26300_body_wq_uuid_"]')
                    for table in tables:
                        grid_rows = await table.query_selector_all('tbody tr')
                        for grid_row in grid_rows:
                            grid_cells = await grid_row.query_selector_all('div[id^="tac_layout_contents_26300_body_wq_uuid_"]')
                            grid_row_data = []
                            for grid_cell in grid_cells:
                                grid_cell_text = await grid_cell.inner_text()
                                grid_row_data.append(grid_cell_text.strip())
                            table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_32":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="탐지 내역").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.locator("#tac_layout_contents_26100_body_DETCT_YN").get_by_text("전체").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                div_ids = [
                    "tac_layout_contents_26100_body_grpList_0_grpInfo_0_txtAnztItemNm",
                    "tac_layout_contents_26100_body_grpList_1_grpInfo_0_txtAnztItemNm",
                    "tac_layout_contents_26100_body_grpList_1_grpInfo_1_txtAnztItemNm"
                ]
                try:
                    for div_id in div_ids:
                        await page.click(f'div#{div_id}')
                        await page.wait_for_selector('#tac_layout_contents_26100_body_grdView_body_table tbody tr')
                        grid_rows = await page.query_selector_all('#tac_layout_contents_26100_body_grdView_body_table tbody tr')
                        for row_index, grid_row in enumerate(grid_rows):
                            grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_26100_body_grdView_cell_{row_index}_"]')
                            grid_row_data = []
                            for grid_cell in grid_cells:
                                grid_cell_text = await grid_cell.inner_text()
                                grid_row_data.append(grid_cell_text.strip())
                            table_data.append(grid_row_data)
                        footer_row = await page.query_selector('table#tac_layout_contents_26100_body_grdView_foot_table tbody tr')
                        footer_cells = await footer_row.query_selector_all('td')
                        footer_data = []
                        for footer_cell in footer_cells:
                            footer_cell_text = await footer_cell.inner_text()
                            footer_data.append(footer_cell_text.strip())
                        table_data.append(footer_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_33":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="조치확인 내역").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_34":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="기관 정보").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('table[id^="tac_layout_contents_24700_body_wq_uuid_"]')
                    tables = await page.query_selector_all('table[id^="tac_layout_contents_24700_body_wq_uuid_"]')
                    for table in tables:
                        grid_rows = await table.query_selector_all('tbody tr')
                        for grid_row in grid_rows:
                            grid_cells = await grid_row.query_selector_all('td div[class^="w2textbox"], td div[class^="w2selectbox"]')
                            grid_row_data = []
                            for grid_cell in grid_cells:
                                grid_cell_text = await grid_cell.inner_text()
                                grid_row_data.append(grid_cell_text.strip())
                            table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")

                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_35":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="세무정보 동의").click() 
                await page.locator("#tac_layout_contents_24110_body_gv_egm_cell_0_0").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_24110_body_gv_egm_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24110_body_gv_egm_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24110_body_gv_egm_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                    await page.wait_for_selector('table[id^="tac_layout_contents_"]')
                    tables = await page.query_selector_all('table[id^="tac_layout_contents_"]')
                    for table in tables:
                        grid_rows = await table.query_selector_all('tbody tr')
                        for grid_row in grid_rows:
                            grid_cells = await grid_row.query_selector_all('td div[class^="w2textbox"], td div[class^="w2selectbox"], td div[class^="layoutbox"]')
                            grid_row_data = []
                            for grid_cell in grid_cells:
                                if await grid_cell.get_attribute('type') == 'text':
                                    grid_cell_text = await grid_cell.get_attribute('value')
                                else:
                                    grid_cell_text = await grid_cell.inner_text()
                                grid_row_data.append(grid_cell_text.strip())
                            table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_36":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="펌뱅킹 이용 동의").click()
                await page.locator("#tac_layout_contents_24220_body_grd_view_cell_0_0").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                try:
                    await page.wait_for_selector('#tac_layout_contents_24220_body_grd_view_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24220_body_grd_view_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24220_body_grd_view_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                    await page.wait_for_selector('table[id^="tac_layout_contents_"]')
                    tables = await page.query_selector_all('table[id^="tac_layout_contents_"]')
                    for table in tables:
                        grid_rows = await table.query_selector_all('tbody tr')
                        for grid_row in grid_rows:
                            grid_cells = await grid_row.query_selector_all('td div[class^="w2textbox"], td div[class^="w2selectbox"], td div[class^="layoutbox"]')
                            grid_row_data = []
                            for grid_cell in grid_cells:
                                if await grid_cell.get_attribute('type') == 'text':
                                    grid_cell_text = await grid_cell.get_attribute('value')
                                else:
                                    grid_cell_text = await grid_cell.inner_text()
                                grid_row_data.append(grid_cell_text.strip())
                            table_data.append(grid_row_data)
                    h3_elements = await page.query_selector_all('h3[id^="tac_layout_contents_"]')
                    for h3_element in h3_elements:
                        h3_text = await h3_element.inner_text()
                        table_data.append([h3_text.strip()])
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_37":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="협약정보 확인").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                try:
                    table_data = []
                    await page.wait_for_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtDtlMainPopup_body_grd_agrtDtlMainPopup_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtDtlMainPopup_body_grd_agrtDtlMainPopup_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtDtlMainPopup_body_grd_agrtDtlMainPopup_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type + "_1"
                new_data.save()
                try:
                    table_data = []
                    await page.get_by_role("tab", name="연구개발기관").click()
                    await page.wait_for_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_bexpCpstPopup_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24210_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_bexpCpstPopup_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24210_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_bexpCpstPopup_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data2 = Data()
                new_data2.content = table_data
                new_data2.content_type = site_type + "_2"
                new_data2.save()
                try:
                    table_data = []
                    await page.get_by_role("tab", name="참여연구자").click()
                    await page.wait_for_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_ptcpMbrPopup_body_grd_ptcpMbrPopup_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24210_body_tab_agrt_contents_tab_ptcpMbrPopup_body_grd_ptcpMbrPopup_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24210_body_tab_agrt_contents_tab_ptcpMbrPopup_body_grd_ptcpMbrPopup_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data3 = Data()
                new_data3.content = table_data
                new_data3.content_type = site_type + "_3"
                new_data3.save()
                try:
                    table_data = []
                    await page.get_by_role("tab", name="과제조회권한자").click()
                    await page.wait_for_selector('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtOrgnPopup_body_grd_agrtOrgnPopup_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtOrgnPopup_body_grd_agrtOrgnPopup_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24210_body_tab_agrt_contents_tab_agrtOrgnPopup_body_grd_agrtOrgnPopup_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data4 = Data()
                new_data4.content = table_data
                new_data4.content_type = site_type + "_4"
                new_data4.save()
            elif site_type == "RCMS_38":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="과제권한 관리").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.get_by_role("link", name="조회").click()
                await page.wait_for_load_state("domcontentloaded")
                try:
                    table_data = []
                    await page.wait_for_selector('#tac_layout_contents_24230_body_gv_egm_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24230_body_gv_egm_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24230_body_gv_egm_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_39":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="사용카드 관리").click()
                await page.get_by_text("과제를 선택해 주시기 바랍니다").click()
                await page.get_by_role("gridcell", name="S3214725").click()
                await page.get_by_role("link", name="선택").click()
                await page.wait_for_load_state("domcontentloaded")
                try:
                    table_data = []
                    await page.wait_for_selector('#tac_layout_contents_24240_body_grd_view_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24240_body_grd_view_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24240_body_grd_view_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_40":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="거래처 정보 관리").click()
                await page.wait_for_load_state("domcontentloaded")
                try:
                    table_data = []
                    await page.wait_for_selector('#tac_layout_contents_24800_body_grd_view_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24800_body_grd_view_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24800_body_grd_view_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_41":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="자주쓰는 계좌").click()
                await page.wait_for_load_state("domcontentloaded")
                try:
                    table_data = []
                    await page.wait_for_selector('#tac_layout_contents_24180_body_grd_view_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24180_body_grd_view_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24180_body_grd_view_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_42":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="카드결제 계좌").click()
                await page.locator("#tac_layout_contents_24160_body_grd_view2_cell_0_0").click()
                await page.wait_for_load_state("domcontentloaded")
                try:
                    table_data = []
                    await page.wait_for_selector('#tac_layout_contents_24160_body_grd_view2_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24160_body_grd_view2_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24160_body_grd_view2_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                    await page.wait_for_selector('#tac_layout_contents_24160_body_grd_view_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24160_body_grd_view_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24160_body_grd_view_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_43":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="참여연구자 계좌").click()
                await page.locator("#tac_layout_contents_24150_body_grd_view2_cell_0_0").click()
                await page.wait_for_load_state("domcontentloaded")
                try:
                    table_data = []
                    await page.wait_for_selector('#tac_layout_contents_24150_body_grd_view2_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24150_body_grd_view2_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24150_body_grd_view2_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_44":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="기타계좌 관리").click()
                await page.locator("#tac_layout_contents_24120_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_view2_cell_0_0").click()
                await page.wait_for_load_state("domcontentloaded")
                try:
                    table_data = []
                    await page.wait_for_selector('#tac_layout_contents_24120_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_view2_body_table tbody tr')
                    grid_rows = await page.query_selector_all('#tac_layout_contents_24120_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_view2_body_table tbody tr')
                    for row_index, grid_row in enumerate(grid_rows):
                        grid_cells = await grid_row.query_selector_all(f'td[id^="tac_layout_contents_24120_body_tab_agrt_contents_tab_bexpCpstPopup_body_grd_view2_cell_{row_index}_"]')
                        grid_row_data = []
                        for grid_cell in grid_cells:
                            grid_cell_text = await grid_cell.inner_text()
                            grid_row_data.append(grid_cell_text.strip())
                        table_data.append(grid_row_data)
                except Exception as e:
                    print(f"An error occurred while extracting data: {e}")
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()
            elif site_type == "RCMS_45":
                await page.get_by_role("link", name="연구개발기관", exact=True).click()
                await page.locator("#wfm_header_btn_allMenu").click()
                await page.get_by_role("link", name="이체비밀번호 설정").click()
                await page.wait_for_load_state("domcontentloaded")
                table_data = []
                new_data = Data()
                new_data.content = table_data
                new_data.content_type = site_type
                new_data.save()


            await page.close()


    return HttpResponse("성공!")

async def getMainPage(request):
    print("동작")
    if request.method == "POST":
        data = json.loads(request.body)
        async with async_playwright() as p:
            site = data['site']
            site_type = data['type']
            browser = await p.chromium.launch()
            page = await browser.new_page()
            page = await set_extra_http_headers(page)
            await page.goto("https://www.rcms.go.kr/login/rid.do?PORTAL_YN=Y")
            await page.fill('#loginId', 'nextkey1')
            await page.fill('#loginPasswd', '@siab812580')
            await page.get_by_role("link", name="로그인", exact=True).click()
            await asyncio.sleep(5)
            await page.locator('#wfm_header_btn_userName').click()
            async with page.expect_popup() as page_info:
                await page.get_by_role("link", name="개인정보수정").click()
            page_1 = await page_info.value
            await page_1.frame_locator("iframe[name=\"info\"]").get_by_label("비밀번호").fill("@siab812580")
            await page_1.frame_locator("iframe[name=\"info\"]").get_by_role("link", name="확인").click()
            #await asyncio.sleep(15)
            #await page.screenshot(path="test.png", full_page= True)
            new_data = Data()
            new_data.content = await page_1.content()
            #new_data.content = new_data.content.replace("/css/","https://cims.keit.re.kr/css/").replace("/js/","https://cims.keit.re.kr/js/")
            new_data.content_type = site_type
            new_data.save()

            await page_1.get_by_role("link", name="개인정보 이용·제공 동의/철회>내역").click()
            new_data2 = Data()
            new_data2.content = await page_1.content()
            new_data2.content_type = "login_2"
            new_data2.save()

            await page_1.get_by_role("link", name="최근 접속이력").click()
            new_data3 = Data()
            new_data3.content = await page_1.content()
            new_data3.content_type = "login_3"
            new_data3.save()

            #for strong in await page.locator('strong').all():
            #    print(await strong.text_content())
            await page.close()


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
        "Referer": "https://www.iris.go.kr/"
    })
    return page

def open_page(request):
    t = request.GET['type']
    html_content = Data.objects.get(content_type=t)
    if html_content:
        return HttpResponse(html_content.content)
    else:
        return HttpResponse("No HTML content available")

def main_page(request):
    model_name = request.GET.get('type', None)

    if not model_name:
        return JsonResponse({"error": "No model name provided."}, status=400)

    try:
        ModelClass = apps.get_model('rcms', model_name)
        if not issubclass(ModelClass, Model):
            return JsonResponse({"error": "Invalid model name."}, status=400)
        records = ModelClass.objects.all()

        data = list(records.values())

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def iframe_page(request):
    return render(request, 'index.html')
