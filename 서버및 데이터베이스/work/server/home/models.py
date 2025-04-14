from django.db import models

class Data(models.Model):
    content = models.TextField(verbose_name="컨텐츠")
    content_type = models.CharField(max_length=50, primary_key=True)

class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

class Account(models.Model):
    email = models.CharField(max_length=50)
    target = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

class Iris_4_1(models.Model):
    num = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    file = models.CharField(max_length=50)
    reg_date = models.CharField(max_length=50)
    edit_date = models.CharField(max_length=50)
    views = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_4_1"

class Iris_4_2(models.Model):
    num = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    file = models.CharField(max_length=50)
    reg_date = models.CharField(max_length=50)
    edit_date = models.CharField(max_length=50)
    views = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_4_2"

class Iris_4_3(models.Model):
    num = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    file = models.CharField(max_length=50)
    reg_date = models.CharField(max_length=50)
    edit_date = models.CharField(max_length=50)
    views = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_4_3"

class Iris_6(models.Model):
    number = models.CharField(max_length=50)
    status = models.CharField(max_length=200)
    class Meta:
        db_table = "IRIS_6"

class Iris_9(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    send_work = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    send_date = models.CharField(max_length=50)
    receive_date = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_9"

class Iris_15_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    assign_class = models.CharField(max_length=50)
    res_num = models.CharField(max_length=50)
    res_name = models.CharField(max_length=200)
    res_group = models.CharField(max_length=50)
    res_manager = models.CharField(max_length=50)
    res_status = models.CharField(max_length=50)
    ass_status = models.CharField(max_length=50)
    plan_status = models.CharField(max_length=50)
    con_status = models.CharField(max_length=50)
    con_execute = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_15_1"

class Iris_15_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    app_role = models.CharField(max_length=50)
    res_name = models.CharField(max_length=200)
    manager_num = models.CharField(max_length=50)
    res_manager = models.CharField(max_length=50)
    agent = models.CharField(max_length=50)
    work_manager = models.CharField(max_length=50)
    detail = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_15_2"

class Iris_17(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    assign_class = models.CharField(max_length=50)
    res_num = models.CharField(max_length=50)
    res_name = models.CharField(max_length=200)
    res_group = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    researcher = models.CharField(max_length=50)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    agree_date = models.CharField(max_length=50)
    consent_form = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_17"

class Iris_20_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    org_name = models.CharField(max_length=50)
    org_type = models.CharField(max_length=50)
    researcher_num = models.CharField(max_length=50)
    agent = models.CharField(max_length=50)
    assign_class = models.CharField(max_length=50)
    res_num = models.CharField(max_length=50)
    res_name = models.CharField(max_length=50)
    step = models.CharField(max_length=50)
    annual = models.CharField(max_length=50)
    res_director = models.CharField(max_length=50, null=True, blank=True)
    assign_status = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_20_1"

class Iris_20_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    assign_class = models.CharField(max_length=50)
    res_num = models.CharField(max_length=50)
    res_name = models.CharField(max_length=50)
    step = models.CharField(max_length=50)
    annual = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    res_director = models.CharField(max_length=50)
    account_num = models.CharField(max_length=50)
    assign_status = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_20_2"

class Iris_20_3(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    assign_class = models.CharField(max_length=50)
    res_num = models.CharField(max_length=50)
    res_name = models.CharField(max_length=50)
    step = models.CharField(max_length=50)
    annual = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    res_director = models.CharField(max_length=50)
    account_num = models.CharField(max_length=50)
    assign_status = models.CharField(max_length=50)
    class Meta:
        db_table = "IRIS_20_3"

class Iris_21_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    pro_org_name = models.CharField(max_length=50) #전문기관
    business_year = models.CharField(max_length=50) #사업년도
    step = models.CharField(max_length=50) #단계
    annual = models.CharField(max_length=50) #연차
    res_num = models.CharField(max_length=50) #연구 과제 번호
    res_name = models.CharField(max_length=200) #연구 과제 명
    assign_status = models.CharField(max_length=50) # 과제 상태
    res_org_name = models.CharField(max_length=50, null=True, blank=True) # 주관 연구개발기관
    res_director = models.CharField(max_length=50) # 연구 책임자
    is_change_req = models.CharField(max_length=50) # 변경 신청 가능 여부
    status_1 = models.CharField(max_length=10)
    status_2 = models.CharField(max_length=10)
    status_3 = models.CharField(max_length=10)
    status_4 = models.CharField(max_length=10)
    status_5 = models.CharField(max_length=10)
    status_6 = models.CharField(max_length=10)
    status_7 = models.CharField(max_length=10)
    status_8 = models.CharField(max_length=10)
    status_9 = models.CharField(max_length=10)
    status_10 = models.CharField(max_length=10)
    status_11 = models.CharField(max_length=10)
    class Meta:
        db_table = "IRIS_21_1"

class Iris_21_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    step = models.CharField(max_length=50) #단계
    annual = models.CharField(max_length=50) #연차
    change_division = models.CharField(max_length=50) # 변경구분
    change_status = models.CharField(max_length=50) # 변경상태
    req_status = models.CharField(max_length=50) # 신청 상태
    req_result = models.CharField(max_length=50) # 신청 결과
    res_org_name = models.CharField(max_length=50) # 연구 개발 기관
    requester = models.CharField(max_length=50) # 신청자
    req_date = models.CharField(max_length=50) # 신청일
    is_change_req = models.CharField(max_length=50) # 변경 신청 가능 여부
    change_req_item = models.CharField(max_length=50) # 변경 요청 항목
    class Meta:
        db_table = "IRIS_21_2"

class Iris_22_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    pro_org_name = models.CharField(max_length=50)
    business_year = models.CharField(max_length=50) #사업년도
    step = models.CharField(max_length=50) #단계
    annual = models.CharField(max_length=50) #연차
    res_num = models.CharField(max_length=50) #연구 과제 번호
    res_name = models.CharField(max_length=200) #연구 과제 명
    res_org_name = models.CharField(max_length=50) # 주관 연구개발기관
    res_director = models.CharField(max_length=50) # 연구 책임자
    assign_status = models.CharField(max_length=50) # 과제 상태
    req_status = models.CharField(max_length=50) # 신청 상태
    class Meta:
        db_table = "IRIS_22_1"

class Iris_22_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    step = models.CharField(max_length=50) #단계
    annual = models.CharField(max_length=50) #연차
    change_division = models.CharField(max_length=50) # 변경구분
    change_type = models.CharField(max_length=50) # 변경 종류
    req_status = models.CharField(max_length=50) # 신청 상태
    req_result = models.CharField(max_length=50) # 신청 결과
    res_org_name = models.CharField(max_length=50) # 연구 개발 기관
    requester = models.CharField(max_length=50) # 신청자
    req_date = models.CharField(max_length=50) # 신청일
    detail = models.CharField(max_length=50) # 상세
    class Meta:
        db_table = "IRIS_22_2"

class Iris_23_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    pro_org_name = models.CharField(max_length=50) #전문기관
    business_year = models.CharField(max_length=50) #사업년도
    step = models.CharField(max_length=50) #단계
    annual = models.CharField(max_length=50) #연차
    res_num = models.CharField(max_length=50) #연구 과제 번호
    res_name = models.CharField(max_length=200) #연구 과제 명
    assign_status = models.CharField(max_length=50) # 과제 상태
    res_org_name = models.CharField(max_length=50) # 주관 연구개발기관
    res_director = models.CharField(max_length=50) # 연구 책임자
    is_change_req = models.CharField(max_length=50) # 변경 신청 가능 여부
    is_change_date = models.CharField(max_length=50) # 협약변경가능기한
    status_1 = models.CharField(max_length=10)
    status_2 = models.CharField(max_length=10)
    status_3 = models.CharField(max_length=10)
    status_4 = models.CharField(max_length=10)
    status_5 = models.CharField(max_length=10)
    status_6 = models.CharField(max_length=10)
    status_7 = models.CharField(max_length=10)
    status_8 = models.CharField(max_length=10)
    status_9 = models.CharField(max_length=10)
    status_10 = models.CharField(max_length=10)
    status_11 = models.CharField(max_length=10)
    class Meta:
        db_table = "IRIS_23_1"

class Iris_23_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    step = models.CharField(max_length=50) #단계
    annual = models.CharField(max_length=50) #연차
    change_division = models.CharField(max_length=50) # 변경구분
    change_status = models.CharField(max_length=50) # 변경상태
    req_status = models.CharField(max_length=50) # 신청 상태
    req_result = models.CharField(max_length=50) # 신청 결과
    res_org_name = models.CharField(max_length=50) # 연구 개발 기관
    requester = models.CharField(max_length=50) # 신청자
    req_date = models.CharField(max_length=50) # 신청일
    change_req_item = models.CharField(max_length=50) # 변경 요청 항목
    class Meta:
        db_table = "IRIS_23_2"

class In_Iris_21_0_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_name = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제명
    division = models.CharField(max_length=200, null=True, blank=True) # 구분
    res_org_name = models.CharField(max_length=200, null=True, blank=True) # 연구개발기관
    res_director = models.CharField(max_length=200, null=True, blank=True) # 연구 책임자
    change_division = models.CharField(max_length=200, null=True, blank=True) # 변경 구분
    res_status = models.CharField(max_length=200, null=True, blank=True) # 과제 상태
    request_status = models.CharField(max_length=200, null=True, blank=True) # 신청 상태
    class Meta:
        db_table = "IN_IRIS_21_0_1"

class In_Iris_21_0_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_name = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제명
    m_category = models.CharField(max_length=200, null=True, blank=True) # 대분류
    category = models.CharField(max_length=200, null=True, blank=True) # 분류
    s_category_1 = models.CharField(max_length=200, null=True, blank=True) # 소분류
    s_category_2 = models.CharField(max_length=200, null=True, blank=True) # 소분류
    class Meta:
        db_table = "IN_IRIS_21_0_2"
        
class In_Iris_21_0_3(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_name = models.CharField(max_length=100, null=True, blank=True)  # 연구개발과제명  
    project_name = models.CharField(max_length=200, null=True, blank=True)  # 사업명  
    detail_project_name = models.CharField(max_length=200, null=True, blank=True)  # 내역사업명  
    res_num = models.CharField(max_length=200, null=True, blank=True)  # 연구개발과제번호  
    res_name_2 = models.CharField(max_length=200, null=True, blank=True)  # 연구개발과제명  
    annual_1 = models.CharField(max_length=50, null=True, blank=True)  # 연차_1  
    annual_2 = models.CharField(max_length=50, null=True, blank=True)  # 연차_2  
    res_org_name = models.CharField(max_length=100, null=True, blank=True)  # 주관 연구개발 기관  
    res_manager = models.CharField(max_length=50, null=True, blank=True)  # 연구 책임자  
    requester = models.CharField(max_length=50, null=True, blank=True)  # 신청자  
    res_date = models.CharField(max_length=100, null=True, blank=True)  # 연구개발 기간  
    req_date = models.CharField(max_length=50, null=True, blank=True)  # 신청일  
    req_org_name = models.CharField(max_length=100, null=True, blank=True)  # 신청 연구개발 기관  
    req_org_type = models.CharField(max_length=100, null=True, blank=True)  # 신청 연구개발 기관 유형  
    change_before = models.CharField(max_length=400, null=True, blank=True)  # 변경 내용 (변경 전)  
    change_after = models.CharField(max_length=400, null=True, blank=True)  # 변경 내용 (변경 후)  
    change_reason = models.CharField(max_length=400, null=True, blank=True)  # 변경 사유  
    document_number = models.CharField(max_length=400, null=True, blank=True)  # 문서 번호  
    sending_institution = models.CharField(max_length=400, null=True, blank=True)  # 발송 기관명  
    official_document_title = models.CharField(max_length=400, null=True, blank=True)  # 공문 제목  

    class Meta:  
        db_table = "IN_IRIS_21_0_3"



class In_Iris_21_1_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    
    change_item = models.CharField(
        max_length=20,
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],
        default="Not Selected"
    ) # 연구개발내용(과제명)변경 상호협의/승인

    
    res_num = models.CharField(max_length=100, null=True, blank=True)  # 연구개발과제번호
    res_name_kr = models.CharField(max_length=200, null=True, blank=True)  # 연구개발과제명 국문
    res_name_en = models.CharField(max_length=200, null=True, blank=True)  # 연구개발과제명 영문

    class Meta:
        db_table = "IN_IRIS_21_1_1"


class In_Iris_21_1_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True)  # 연구개발과제번호
    division = models.CharField(max_length=50, null=True, blank=True)  # 구분
    classification = models.CharField(max_length=50, null=True, blank=True)  # 분류
    first_place = models.CharField(max_length=50, null=True, blank=True)  # 1순위
    first_weight = models.CharField(max_length=50, null=True, blank=True)  # 1순위 가중치
    second_place = models.CharField(max_length=50, null=True, blank=True)  # 2순위
    second_weight = models.CharField(max_length=50, null=True, blank=True)  # 2순위 가중치
    third_place = models.CharField(max_length=50, null=True, blank=True)  # 3순위
    third_weight = models.CharField(max_length=50, null=True, blank=True)  # 3순위 가중치
    
    class Meta:
        db_table = "IN_IRIS_21_1_2"



class In_Iris_21_1_3(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    change_item = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 연구개발내용(기술분류) 변경 (통보)  

    research_stage = models.CharField(max_length=50, null=True, blank=True)  # 연구개발단계  
    research_project_type = models.CharField(max_length=50, null=True, blank=True)  # 연구개발과제성격  
    trl_start_point = models.CharField(max_length=50, null=True, blank=True)  # 기술성숙도(TRL) 착수 시점 기준  
    trl_end_point = models.CharField(max_length=50, null=True, blank=True)  # 기술성숙도(TRL) 종료 시점 기준  

    class Meta:  
        db_table = "IN_IRIS_21_1_3"


class In_Iris_21_1_4(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50) 
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호 

    change_item = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 연구개발내용(과제보안) 변경 (상호협의/승인)  

    security_grade = models.CharField(  
        max_length=20,  
        choices=[("Security Task", "Security Task"), ("General Task", "General Task")],  
        default="General Task"  
    )  # 보안과제 또는 일반과제 선택 (기본값: 일반과제, 필수 선택)  

    security_task_release_date = models.DateField(null=True, blank=True)  # 보안과제 해제년월 (달력 형식)  

    class Meta:  
        db_table = "IN_IRIS_21_1_4"



class In_Iris_21_1_5(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True)  # 연구개발과제번호

    change_item = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 연구개발내용(키워드) 변경 (통보)

    content_1_kr = models.CharField(max_length=50, null=True, blank=True)  # 국문
    content_1_en = models.CharField(max_length=50, null=True, blank=True)  # 영문
    content_2_kr = models.CharField(max_length=50, null=True, blank=True)  
    content_2_en = models.CharField(max_length=50, null=True, blank=True)  
    content_3_kr = models.CharField(max_length=50, null=True, blank=True)  
    content_3_en = models.CharField(max_length=50, null=True, blank=True)  
    content_4_kr = models.CharField(max_length=50, null=True, blank=True)  
    content_4_en = models.CharField(max_length=50, null=True, blank=True)  
    content_5_kr = models.CharField(max_length=50, null=True, blank=True)  
    content_5_en = models.CharField(max_length=50, null=True, blank=True)  

    class Meta:
        db_table = "IN_IRIS_21_1_5"


class In_Iris_21_2_1(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True)  # 연구개발과제번호  

    change_item = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 연구개발기간 변경 (상호협의/승인)  

    step = models.CharField(max_length=50, null=True, blank=True)  # 단계  
    annual = models.CharField(max_length=50, null=True, blank=True)  # 연차  
    research_start_date = models.DateField(null=True, blank=True)  # 연구개발 시작일  
    research_end_date = models.DateField(null=True, blank=True)  # 연구개발 종료일  
    months = models.IntegerField(null=True, blank=True)  # 개월 수  
    previous_step = models.CharField(max_length=50, null=True, blank=True)  # 기존 단계  
    previous_annual = models.CharField(max_length=50, null=True, blank=True)  # 기존 연차  

    class Meta:  
        db_table = "IN_IRIS_21_2_1"



class In_Iris_21_2_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True)  # 연구개발과제번호

    change_item = models.CharField(
        max_length=20,
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],
        default="Not Selected"
    )  # 최종 목표 변경(상호협의/승인)

    research_development_content = models.TextField(max_length=1333, null=True, blank=True)  # 최종목표내용
    research_development_performance = models.TextField(max_length=1333, null=True, blank=True)  # 연구개발내용
    utilization_plan_and_expected_effect = models.TextField(max_length=1333, null=True, blank=True)  # 연구개발성과 활용계획 및 기대효과

    class Meta:
        db_table = "IN_IRIS_21_2_2"



class In_Iris_21_3_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    institution_role = models.CharField(max_length=50, null=True, blank=True)  # 기관역할
    nationality = models.CharField(max_length=50, null=True, blank=True)  # 국적
    research_development_institution_name = models.CharField(max_length=100, null=True, blank=True)  # 연구개발기관명
    business_registration_number = models.CharField(max_length=50, null=True, blank=True)  # 사업자등록번호
    establishment_classification = models.CharField(max_length=50, null=True, blank=True)  # 설립구분
    company_type = models.CharField(max_length=50, null=True, blank=True)  # 기업유형
    location = models.CharField(max_length=100, null=True, blank=True)  # 소재지
    research_development_payment_type = models.CharField(max_length=50, null=True, blank=True)  # 연구비지급유형
    class Meta:
        db_table = "IN_IRIS_21_3_1"





class In_Iris_21_3_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    institution_role = models.CharField(max_length=50, null=True, blank=True)  # 기관역할
    research_development_institution_name = models.CharField(max_length=100, null=True, blank=True)  # 연구개발기관명
    research_responsible_person = models.CharField(max_length=50, null=True, blank=True)  # 연구책임자
    representative = models.CharField(max_length=50, null=True, blank=True)  # 대표자
    practitioner = models.CharField(max_length=50, null=True, blank=True)  # 실무자

    participation_annual = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 참여연차

    participation_annual_2 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 참여연차2

    government_support = models.FileField(upload_to="uploads/", null=True, blank=True)  # 첨부파일
    execution_classification = models.CharField(max_length=50, null=True, blank=True)  # 수행구분
    class Meta:
        db_table = "IN_IRIS_21_3_2"

        

class In_Iris_21_3_3(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    institution_role = models.CharField(max_length=50, null=True, blank=True)  # 기관 역할  
    research_development_institution_name = models.CharField(max_length=100, null=True, blank=True)  # 연구개발기관명  

    participation_status = models.CharField(  
        max_length=20,  
        choices=[("Participating", "Participating"), ("Not Participating", "Not Participating")],  
        default="Not Participating"  
    )  # 참여 여부 (라디오 버튼 선택)  

    stage = models.CharField(max_length=50, null=True, blank=True)  # 단계  
    annual = models.CharField(max_length=50, null=True, blank=True)  # 연차  

    start_date = models.DateField(null=True, blank=True)  # 연구개발 시작일 (달력 선택)  
    end_date = models.DateField(null=True, blank=True)  # 연구개발 종료일 (달력 선택)  

    student_integration = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 학생 통합 여부 (라디오 버튼 선택)  

    equipment_integration = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 장비 통합 여부 (라디오 버튼 선택)  

    exception_reason_for_regulation_application = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 규정 적용 예외 사유 (라디오 버튼 선택)  

    class Meta:  
        db_table = "IN_IRIS_21_3_3"



class In_Iris_21_3_4(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    research_funding_account_change_1 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 연구개발비 지급계좌 변경(통보) 1 (라디오 버튼)  

    research_funding_account_change_2 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 연구개발비 지급계좌 변경(통보) 2 (라디오 버튼)  

    agreement_institution = models.CharField(max_length=100, null=True, blank=True)  # 협약 기관  
    bank_classification = models.CharField(max_length=50, null=True, blank=True)  # 은행 구분  
    account_number = models.CharField(max_length=50, null=True, blank=True)  # 계좌번호  
    account_holder = models.CharField(max_length=100, null=True, blank=True)  # 예금주  

    class Meta:  
        db_table = "IN_IRIS_21_3_4"




class In_Iris_21_3_5(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    role = models.CharField(max_length=50, null=True, blank=True)  # 인력 역할  
    participation_type = models.CharField(max_length=50, null=True, blank=True)  # 참여 구분  
    nationality = models.CharField(max_length=50, null=True, blank=True)  # 국적  
    name = models.CharField(max_length=50, null=True, blank=True)  # 성명  
    position = models.CharField(max_length=50, null=True, blank=True)  # 직위  
    researcher_number = models.CharField(max_length=50, null=True, blank=True)  # 국가 연구자 번호 (숫자만 입력)  
    new_recruit_type = models.CharField(max_length=50, null=True, blank=True)  # 신규 채용 구분  
    recruitment_date = models.DateField(null=True, blank=True)  # 채용 일자 (날짜 선택 가능)  

    participation_phase_1 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 참여 연차1 (라디오 선택 방식)  

    participation_phase_2 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 참여 연차2 (라디오 선택 방식)  

    position_status = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 직제 존속 (라디오 선택 방식)  

    supporting_documents = models.FileField(upload_to="uploads/documents/", null=True, blank=True)  # 증빙 서류 (파일 첨부)

    ethics_guide_provided = models.CharField(max_length=50, null=True, blank=True)  # 연구 윤리 안내 여부  

    ethics_agreement_date = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 연구 윤리 동의 일자 (라디오 선택 방식)  

    performance_type = models.CharField(max_length=50, null=True, blank=True)  # 수행 구분  

    class Meta:  
        db_table = "IN_IRIS_21_3_5"



class In_Iris_21_3_6(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    researcher_name = models.CharField(max_length=50, null=True, blank=True)  # 연구자명  
    participation_year = models.CharField(max_length=50, null=True, blank=True)  # 참여 연차  
    participation_status = models.CharField(max_length=50, null=True, blank=True)  # 참여 여부  
    highest_degree = models.CharField(max_length=50, null=True, blank=True)  # 최종 학위  
    major_field = models.CharField(max_length=50, null=True, blank=True)  # 전공 계열  
    major = models.CharField(max_length=50, null=True, blank=True)  # 전공  
    graduation_year = models.CharField(max_length=50, null=True, blank=True)  # 졸업 연도  
    role = models.CharField(max_length=50, null=True, blank=True)  # 담당 역할  
    participation_type = models.CharField(max_length=50, null=True, blank=True)  # 참여 구분  
    part_time_status = models.CharField(max_length=50, null=True, blank=True)  # 시간 선택제 구분  
    sequence_number = models.CharField(max_length=50, null=True, blank=True)  # 순번  

    participation_start_date = models.DateField(null=True, blank=True)  # 참여 시작 일자 (날짜 형식)  
    participation_end_date = models.DateField(null=True, blank=True)  # 참여 종료 일자 (날짜 형식)  

    cash_budget_rate = models.CharField(max_length=50, null=True, blank=True)  # 현금 계상률  
    in_kind_budget_rate = models.CharField(max_length=50, null=True, blank=True)  # 현물 계상률  
    unpaid_budget_rate = models.CharField(max_length=50, null=True, blank=True)  # 미지급 계상률  
    calculated_annual_salary = models.CharField(max_length=50, null=True, blank=True)  # 산출 근거 연봉 금액  

    class Meta:  
        db_table = "IN_IRIS_21_3_6"




class In_Iris_21_3_7(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    personnel_role = models.CharField(max_length=50, null=True, blank=True)  # 인력 역할  
    nationality = models.CharField(max_length=50, null=True, blank=True)  # 국적  
    personnel_name = models.CharField(max_length=50, null=True, blank=True)  # 인력명  
    representative_credit_info_consent = models.CharField(max_length=100, null=True, blank=True)  # 대표자 신용정보 수집 및 이용 동의  
    researcher_number = models.CharField(max_length=50, null=True, blank=True)  # 국가 연구자 번호  
    department = models.CharField(max_length=50, null=True, blank=True)  # 소속 부서  
    position = models.CharField(max_length=50, null=True, blank=True)  # 직위  

    support_year_1 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 지원 연차 1 (라디오 버튼 선택)  

    support_year_2 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 지원 연차 2 (라디오 버튼 선택)  

    participation_type = models.CharField(max_length=50, null=True, blank=True)  # 참여 구분  
    power_of_attorney = models.CharField(max_length=50, null=True, blank=True)  # 위임장  

    class Meta:  
        db_table = "IN_IRIS_21_3_7"






class In_Iris_21_4_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    institution_role = models.CharField(max_length=50, null=True, blank=True)  # 기관역할
    nationality = models.CharField(max_length=50, null=True, blank=True)  # 국적
    supporting_institution_name = models.CharField(max_length=100, null=True, blank=True)  # 지원기관명
    business_registration_number = models.CharField(max_length=50, null=True, blank=True)  # 사업자등록번호
    company_type = models.CharField(max_length=50, null=True, blank=True)  # 기업유형
    phone_number = models.CharField(max_length=50, null=True, blank=True)  # 전화번호
    supporting_institution_role_description = models.CharField(max_length=100, null=True, blank=True)  # 지원기관 역할설명
    
    support_year_1 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 지원 연차 1 (라디오 버튼 선택)  

    support_year_2 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 지원 연차 2 (라디오 버튼 선택)  

    execution_type = models.CharField(max_length=50, null=True, blank=True)  # 수행구분
    bank_classification = models.CharField(max_length=50, null=True, blank=True)  # 은행구분
    account_number = models.CharField(max_length=50, null=True, blank=True)  # 계좌번호
    account_holder = models.CharField(max_length=100, null=True, blank=True)  # 예금주

    class Meta:
        db_table = "IN_IRIS_21_4_1"


class In_Iris_21_4_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    personnel_role = models.CharField(max_length=50, null=True, blank=True)  # 인력역할
    nationality = models.CharField(max_length=50, null=True, blank=True)  # 국적
    personnel_name = models.CharField(max_length=50, null=True, blank=True)  # 인력명
    department = models.CharField(max_length=50, null=True, blank=True)  # 소속부서
    position = models.CharField(max_length=50, null=True, blank=True)  # 직위

    support_year_1 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 지원 연차 1 (라디오 버튼 선택)  

    support_year_2 = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 지원 연차 2 (라디오 버튼 선택)  

    participation_type = models.CharField(max_length=50, null=True, blank=True)  # 참여구분

    class Meta:
        db_table = "IN_IRIS_21_4_2"




class In_Iris_21_5_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    phase = models.CharField(max_length=50, null=True, blank=True) # 단계
    year = models.CharField(max_length=50, null=True, blank=True) # 연차
    institution_role = models.CharField(max_length=50, null=True, blank=True) # 기관역할
    research_institution_name = models.CharField(max_length=50, null=True, blank=True) # 연구개발기관명
    government_cash_funding = models.CharField(max_length=50, null=True, blank=True) # 현금
    government_funding_ratio = models.CharField(max_length=50, null=True, blank=True) # 비율
    institution_cash_contribution = models.CharField(max_length=50, null=True, blank=True) # 현금
    institution_contribution_ratio = models.CharField(max_length=50, null=True, blank=True) # 비율
    institution_in_kind_contribution = models.CharField(max_length=50, null=True, blank=True) # 현물
    institution_in_kind_ratio = models.CharField(max_length=50, null=True, blank=True) # 비율
    institution_total_contribution = models.CharField(max_length=50, null=True, blank=True) # 소계
    total_cash = models.CharField(max_length=50, null=True, blank=True) # 합계
    total_in_kind = models.CharField(max_length=50, null=True, blank=True) # 현물
    total_amount = models.CharField(max_length=50, null=True, blank=True) # 종합

    class Meta:
        db_table = "IN_IRIS_21_5_1"



class In_Iris_21_5_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    phase = models.CharField(max_length=50, null=True, blank=True) # 단계
    year = models.CharField(max_length=50, null=True, blank=True) # 연차
    institution_role = models.CharField(max_length=50, null=True, blank=True) # 기관역할
    research_institution_name = models.CharField(max_length=100, null=True, blank=True) # 연구개발기관명
    total_funding_cash = models.CharField(max_length=50, null=True, blank=True) # 재원별 연구비 합계(A)현금
    total_funding_in_kind = models.CharField(max_length=50, null=True, blank=True) # 재원별 연구비 합계(A)현물
    total_funding_subtotal = models.CharField(max_length=50, null=True, blank=True) # 재원별 연구비 합계(A)소계
    itemized_funding_cash = models.CharField(max_length=50, null=True, blank=True) # 비목별 연구비(B) 현금
    itemized_funding_in_kind = models.CharField(max_length=50, null=True, blank=True) # 비목별 연구비(B) 현물
    itemized_funding_subtotal = models.CharField(max_length=50, null=True, blank=True) # 비목별 연구비(B) 소계
    unpaid_salary_baseline = models.CharField(max_length=50, null=True, blank=True) # 비목별 연구비(B) 미지급인건비 계상기준금액
    difference_cash = models.CharField(max_length=50, null=True, blank=True) # 차액(A-B) 현금
    difference_in_kind = models.CharField(max_length=50, null=True, blank=True) # 차액(A-B) 현물
    difference_subtotal = models.CharField(max_length=50, null=True, blank=True) # 차액(A-B) 소계

    class Meta:
        db_table = "IN_IRIS_21_5_2"

class In_Iris_21_5_3(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    phase = models.CharField(max_length=50, null=True, blank=True) # 단계
    year = models.CharField(max_length=50, null=True, blank=True) # 연차
    institution_role = models.CharField(max_length=50, null=True, blank=True) # 기관역할
    research_institution_name = models.CharField(max_length=50, null=True, blank=True) # 연구개발기관명

    class Meta:
        db_table = "IN_IRIS_21_5_3"


class In_Iris_21_5_4(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    research_funds_by_item = models.CharField(max_length=50, null=True, blank=True) # 비목
    sub_item = models.CharField(max_length=50, null=True, blank=True) # 세목
    cash = models.CharField(max_length=50, null=True, blank=True) # 현금
    in_kind = models.CharField(max_length=50, null=True, blank=True) # 현물
    subtotal = models.CharField(max_length=50, null=True, blank=True) # 소계
    unpaid_salary_baseline_amount = models.CharField(max_length=50, null=True, blank=True) # 미지급인건비 계상기준금액
    ratio = models.CharField(max_length=50, null=True, blank=True) # 비율

    class Meta:
        db_table = "IN_IRIS_21_5_4"


class In_Iris_21_5_5(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    phase = models.CharField(max_length=50, null=True, blank=True)  # 단계  
    year = models.CharField(max_length=50, null=True, blank=True)  # 연차  
    institution_role = models.CharField(max_length=50, null=True, blank=True)  # 기관 역할  
    research_institution_name = models.CharField(max_length=50, null=True, blank=True)  # 연구개발기관명  

    research_start_date = models.DateField(null=True, blank=True)  # 연구개발 시작일 (날짜 선택 가능)  
    research_end_date = models.DateField(null=True, blank=True)  # 연구개발 종료일 (날짜 선택 가능)  
    planned_date = models.DateField(null=True, blank=True)  # 예정일 (날짜 선택 가능)  

    cash = models.CharField(max_length=50, null=True, blank=True)  # 현금  
    in_kind = models.CharField(max_length=50, null=True, blank=True)  # 현물  
    subtotal = models.CharField(max_length=50, null=True, blank=True)  # 소계  
    round_number = models.CharField(max_length=50, null=True, blank=True)  # 차수  
    deposit_amount = models.CharField(max_length=50, null=True, blank=True)  # 입금 금액  

    class Meta:  
        db_table = "IN_IRIS_21_5_5"


    


class In_Iris_21_6_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호
    research_institution_role = models.CharField(max_length=50, null=True, blank=True)  # 연구기관역할
    research_institution_name = models.CharField(max_length=50, null=True, blank=True)  # 연구개발기관명
    principal_researcher = models.CharField(max_length=50, null=True, blank=True)  # 연구책임자
    execution_type = models.CharField(max_length=50, null=True, blank=True)  # 수행구분

    class Meta:
        db_table = "IN_IRIS_21_6_1"



class In_Iris_21_6_2(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    owning_institution = models.CharField(max_length=50, null=True, blank=True)  # 보유 기관  
    research_facility_equipment_name = models.CharField(max_length=50, null=True, blank=True)  # 연구시설/장비명  
    specifications = models.CharField(max_length=50, null=True, blank=True)  # 규격  
    quantity = models.CharField(max_length=50, null=True, blank=True)  # 수량  
    ownership_type = models.CharField(max_length=50, null=True, blank=True)  # 보유 구분  
    usage_purpose = models.CharField(max_length=50, null=True, blank=True)  # 용도  

    utilization_period = models.DateField(null=True, blank=True)  # 활용 시기 (날짜 형식)  

    installation_location = models.CharField(max_length=50, null=True, blank=True)  # 설치 장소  

    class Meta:  
        db_table = "IN_IRIS_21_6_2"




class In_Iris_21_6_3(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    sequence_number = models.CharField(max_length=50, null=True, blank=True)  # 순번  
    research_facility_equipment_name = models.CharField(max_length=50, null=True, blank=True)  # 연구시설/장비명  
    in_kind_contribution_reflected = models.CharField(max_length=50, null=True, blank=True)  # 현물 부담 반영 여부  

    operation_start_date = models.DateField(null=True, blank=True)  # 운영 시작 일자 (날짜 형식)  
    operation_end_date = models.DateField(null=True, blank=True)  # 운영 종료 일자 (날짜 형식)  

    annual_operating_cost = models.CharField(max_length=50, null=True, blank=True)  # 연간 운영 비용  
    dedicated_personnel_count = models.CharField(max_length=50, null=True, blank=True)  # 전담 인력 수  
    utilization_plan = models.CharField(max_length=50, null=True, blank=True)  # 활용 계획  

    class Meta:  
        db_table = "IN_IRIS_21_6_3"




class In_Iris_21_6_4(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    sequence_number = models.CharField(max_length=50, null=True, blank=True)  # 순번  
    specifications = models.CharField(max_length=50, null=True, blank=True)  # 규격  
    quantity = models.CharField(max_length=50, null=True, blank=True)  # 수량  
    construction_cost_unit_kkr = models.CharField(max_length=50, null=True, blank=True)  # 구축 비용 (단위: 천원)  
    estimated_price_unit_kkr = models.CharField(max_length=50, null=True, blank=True)  # 예상 단가 (단위: 천원)  
    construction_timing = models.CharField(max_length=50, null=True, blank=True)  # 구축 시점  
    usage_purpose = models.CharField(max_length=50, null=True, blank=True)  # 용도  
    shared_usage_category = models.CharField(max_length=50, null=True, blank=True)  # 공동 활용 구분  
    manufacturer_name = models.CharField(max_length=50, null=True, blank=True)  # 제작 회사명  

    attachment_file = models.FileField(upload_to="uploads/documents/", null=True, blank=True)  # 첨부 파일 (파일 저장 가능)  

    result = models.CharField(max_length=50, null=True, blank=True)  # 결과  

    class Meta:  
        db_table = "IN_IRIS_21_6_4"



class In_Iris_21_6_5(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    sequence_number = models.CharField(max_length=50, null=True, blank=True)  # 순번  
    research_facility_equipment_name = models.CharField(max_length=50, null=True, blank=True)  # 연구시설/장비명  
    utilization_status = models.CharField(max_length=50, null=True, blank=True)  # 활용 여부  

    operation_start_date = models.DateField(null=True, blank=True)  # 운영 시작 일자 (날짜 형식)  
    operation_end_date = models.DateField(null=True, blank=True)  # 운영 종료 일자 (날짜 형식)  

    annual_operating_cost = models.CharField(max_length=50, null=True, blank=True)  # 연간 운영 비용  
    dedicated_personnel_count = models.CharField(max_length=50, null=True, blank=True)  # 전담 인력 수  
    utilization_plan = models.CharField(max_length=50, null=True, blank=True)  # 활용 계획  
    installation_location = models.CharField(max_length=50, null=True, blank=True)  # 설치 장소  
    change_category = models.CharField(max_length=50, null=True, blank=True)  # 변경 구분  
    construction_cancellation_reason = models.CharField(max_length=50, null=True, blank=True)  # 구축 포기 사유  

    class Meta:  
        db_table = "IN_IRIS_21_6_5"





class In_Iris_21_7_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    performance_indicator_name = models.CharField(max_length=50, null=True, blank=True)  # 성과지표명
    target_value = models.CharField(max_length=50, null=True, blank=True)  # 목표치
    total_value = models.CharField(max_length=50, null=True, blank=True)  # 계
    weight_percentage = models.CharField(max_length=50, null=True, blank=True)  # 가중치(%)
    mandatory_status = models.CharField(max_length=50, null=True, blank=True)  # 필수여부

    class Meta:
        db_table = "IN_IRIS_21_7_1"


class In_Iris_21_7_2(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    performance_indicator_name = models.CharField(max_length=50, null=True, blank=True)  # 성과지표명
    target_value = models.CharField(max_length=50, null=True, blank=True)  # 목표치
    weight_percentage = models.CharField(max_length=50, null=True, blank=True)  # 가중치(%)

    class Meta:
        db_table = "IN_IRIS_21_7_2"



class In_Iris_21_7_3(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    radio_selection = models.CharField(  
        max_length=20,  
        choices=[("Selected", "Selected"), ("Not Selected", "Not Selected")],  
        default="Not Selected"  
    )  # 라디오 버튼 선택 방식  

    evaluation_item_main_performance = models.CharField(max_length=50, null=True, blank=True)  # 평가항목(주요성능)
    unit = models.CharField(max_length=50, null=True, blank=True)  # 단위
    weight_percentage = models.CharField(max_length=50, null=True, blank=True)  # 비중(%)
    world_top_level_country_institution = models.CharField(max_length=50, null=True, blank=True)  # 세계 최고수준 보유국/보유기관
    world_top_level_performance = models.CharField(max_length=50, null=True, blank=True)  # 세계 최고수준성능수준
    pre_research_domestic_level = models.CharField(max_length=50, null=True, blank=True)  # 연구개발전 국내수준
    pre_research_domestic_performance_level = models.CharField(max_length=50, null=True, blank=True)  # 연구개발전 국내 성능수준
    target_achievement_basis = models.CharField(max_length=50, null=True, blank=True)  # 목표 달성근거
    target_value = models.CharField(max_length=50, null=True, blank=True)  # 목표치

    class Meta:
        db_table = "IN_IRIS_21_7_3"

class In_Iris_21_7_4(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    evaluation_item_main_performance = models.CharField(max_length=100, null=True, blank=True)  # 평가항목(주요성능)
    evaluation_method = models.CharField(max_length=100, null=True, blank=True)  # 평가방법
    evaluation_environment = models.CharField(max_length=100, null=True, blank=True)  # 평가환경

    class Meta:
        db_table = "IN_IRIS_21_7_4"




class In_Iris_21_8_1(models.Model):
    account = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    institution_name = models.CharField(max_length=50, null=True, blank=True)  # 기관명
    commercialization_performance = models.CharField(max_length=50, null=True, blank=True)  # 사업화 성과
    detailed_performance_indicator = models.CharField(max_length=50, null=True, blank=True)  # 세부 성과지표
    total = models.CharField(max_length=50, null=True, blank=True)  # 합계
    round_1 = models.CharField(max_length=50, null=True, blank=True)  # 1회차
    round_2 = models.CharField(max_length=50, null=True, blank=True)  # 2회차
    round_3 = models.CharField(max_length=50, null=True, blank=True)  # 3회차
    round_4 = models.CharField(max_length=50, null=True, blank=True)  # 4회차
    round_5 = models.CharField(max_length=50, null=True, blank=True)  # 5회차

    class Meta:
        db_table = "IN_IRIS_21_8_1"


class In_Iris_21_9_1(models.Model):  
    account = models.CharField(max_length=50)  
    group = models.CharField(max_length=50)  
    res_num = models.CharField(max_length=100, null=True, blank=True) # 연구개발과제번호

    sequence_number = models.CharField(max_length=50, null=True, blank=True)  # 순번  
    document_type = models.CharField(max_length=50, null=True, blank=True)  # 문서 유형  
    required_status = models.CharField(max_length=50, null=True, blank=True)  # 필수 여부  
    file_name = models.CharField(max_length=100, null=True, blank=True)  # 파일명  
    file_size_kb = models.CharField(max_length=50, null=True, blank=True)  # 크기(KB)  

    pdf = models.FileField(upload_to="uploads/documents/", null=True, blank=True)  # PDF 파일 저장 가능  

    registration_date = models.DateTimeField(null=True, blank=True)  # 등록 일자 (날짜 + 시간 형식)  

    class Meta:  
        db_table = "IN_IRIS_21_9_1"

