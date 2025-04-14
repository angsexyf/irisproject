from django.db import models

class Data(models.Model):
    content = models.TextField(verbose_name="컨텐츠")
    content_type = models.CharField(max_length=50, primary_key=True)

class Rcms_2(models.Model):
    account = models.CharField(max_length=50)
    table_type = models.CharField(max_length=50)
    title_1 = models.CharField(max_length=50)
    checke_1 = models.CharField(max_length=10)
    title_2 = models.CharField(max_length=50)
    checke_2 = models.CharField(max_length=10)
    title_3 = models.CharField(max_length=50)
    checke_3 = models.CharField(max_length=10)
    title_4 = models.CharField(max_length=50)
    checke_4 = models.CharField(max_length=10)
    title_5 = models.CharField(max_length=50)
    checke_5 = models.CharField(max_length=10)
    title_6 = models.CharField(max_length=50)
    checke_6 = models.CharField(max_length=10)

    # 주요 사용자 정보
    user_id = models.CharField(max_length=50, blank=True, null=True)  # 아이디
    name = models.CharField(max_length=50, blank=True, null=True)  # 이름
    password = models.CharField(max_length=50, blank=True, null=True)  # 비밀번호
    phone = models.CharField(max_length=50, blank=True, null=True)  # 휴대전화번호
    email = models.CharField(max_length=50, blank=True, null=True)  # 이메일
    call_num = models.CharField(max_length=50, blank=True, null=True)  # 전화번호

    # 주소 관련 필드
    zip_code = models.CharField(max_length=20, blank=True, null=True)  # 우편번호
    address = models.TextField(blank=True, null=True)  # 기본 주소
    address_detail = models.TextField(blank=True, null=True)  # 나머지 주소

    # 직장 및 기관 정보
    organization = models.CharField(max_length=255, blank=True, null=True)  # 직장
    unreg_org_name = models.CharField(max_length=255, blank=True, null=True)  # 미등록 기관명
    unreg_org_number = models.CharField(max_length=20, blank=True, null=True)  # 미등록 사업자번호
    unreg_org_type = models.CharField(max_length=255, blank=True, null=True)  # 미등록 기관분류
    unreg_org_zip_code = models.CharField(max_length=20, blank=True, null=True)  # 미등록 우편번호
    unreg_org_address = models.TextField(blank=True, null=True)  #미등록 기본 주소
    unreg_org_address_detail = models.TextField(blank=True, null=True)  #미등록  나머지 주소

    # 부서 및 직위
    department = models.CharField(max_length=255, blank=True, null=True)  # 부서
    position = models.CharField(max_length=255, blank=True, null=True)  # 직위

    # 기타 정보
    national_researcher_number = models.CharField(max_length=50, blank=True, null=True)  # 국가연구자번호
    certification = models.CharField(max_length=255, blank=True, null=True)  # 공인인증서
    class Meta:
        db_table = "RCMS_2"

class Rcms_3_1(models.Model):
    account = models.CharField(max_length=50)
    num = models.CharField(max_length=50, blank=True, null=True)  # 번호
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    title = models.CharField(max_length=100, blank=True, null=True)  # 제목
    upload_file = models.CharField(max_length=50, blank=True, null=True)  # 첨부파일 유무
    writer = models.CharField(max_length=50, blank=True, null=True)  # 작성자
    create_date = models.CharField(max_length=50, blank=True, null=True)  # 등록일
    views = models.CharField(max_length=50, blank=True, null=True)  # 조회수
    class Meta:
        db_table = "RCMS_3_1"

class Rcms_3_2(models.Model):
    account = models.CharField(max_length=50)
    num = models.CharField(max_length=50, blank=True, null=True)  # 번호
    archive_name = models.CharField(max_length=50, blank=True, null=True)  # 구분
    title = models.CharField(max_length=100, blank=True, null=True)  # 제목
    upload_file = models.CharField(max_length=50, blank=True, null=True)  # 첨부파일 유무
    writer = models.CharField(max_length=50, blank=True, null=True)  # 작성자
    create_date = models.CharField(max_length=50, blank=True, null=True)  # 등록일
    views = models.CharField(max_length=50, blank=True, null=True)  # 조회수
    class Meta:
        db_table = "RCMS_3_2"

class Rcms_4(models.Model):
    account = models.CharField(max_length=50)
    num = models.CharField(max_length=50, blank=True, null=True)  # 번호
    title = models.CharField(max_length=100, blank=True, null=True)  # 제목
    upload_file = models.CharField(max_length=200, blank=True, null=True)  # 첨부파일 유무
    writer = models.CharField(max_length=50, blank=True, null=True)  # 작성자
    create_date = models.CharField(max_length=50, blank=True, null=True)  # 등록일
    views = models.CharField(max_length=50, blank=True, null=True)  # 조회수
    class Meta:
        db_table = "RCMS_4"

class Rcms_5_1(models.Model):
    account = models.CharField(max_length=50)
    num = models.CharField(max_length=50, blank=True, null=True)  # 번호
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    title = models.CharField(max_length=100, blank=True, null=True)  # 제목
    upload_file = models.CharField(max_length=50, blank=True, null=True)  # 첨부파일 유무
    writer = models.CharField(max_length=50, blank=True, null=True)  # 작성자
    create_date = models.CharField(max_length=50, blank=True, null=True)  # 등록일
    views = models.CharField(max_length=50, blank=True, null=True)  # 조회수
    class Meta:
        db_table = "RCMS_5_1"

class Rcms_5_2(models.Model):
    account = models.CharField(max_length=50)
    num = models.CharField(max_length=50, blank=True, null=True)  # 번호
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    title = models.CharField(max_length=100, blank=True, null=True)  # 제목
    upload_file = models.CharField(max_length=50, blank=True, null=True)  # 첨부파일 유무
    writer = models.CharField(max_length=50, blank=True, null=True)  # 작성자
    create_date = models.CharField(max_length=50, blank=True, null=True)  # 등록일
    views = models.CharField(max_length=50, blank=True, null=True)  # 조회수
    class Meta:
        db_table = "RCMS_5_2"

class Rcms_6_1(models.Model):
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    group = models.CharField(max_length=100, blank=True, null=True)  
    link_text = models.CharField(max_length=50, blank=True, null=True)
    external_link = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = "RCMS_6_1"
class Rcms_6_2(models.Model):
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    group = models.CharField(max_length=100, blank=True, null=True)
    link_text = models.CharField(max_length=50, blank=True, null=True)
    external_link = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = "RCMS_6_2"
class Rcms_6_3(models.Model):
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    group = models.CharField(max_length=100, blank=True, null=True)
    link_text = models.CharField(max_length=50, blank=True, null=True)
    external_link = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = "RCMS_6_3"
class Rcms_6_4(models.Model):
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    group = models.CharField(max_length=100, blank=True, null=True)
    link_text = models.CharField(max_length=50, blank=True, null=True)
    external_link = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = "RCMS_6_4"
class Rcms_6_5(models.Model):
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    group = models.CharField(max_length=100, blank=True, null=True)
    link_text = models.CharField(max_length=50, blank=True, null=True)
    external_link = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = "RCMS_6_5"
class Rcms_6_6(models.Model):
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    group = models.CharField(max_length=100, blank=True, null=True)
    link_text = models.CharField(max_length=50, blank=True, null=True)
    external_link = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = "RCMS_6_6"

class Rcms_8_1(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    flag_1 = models.CharField(max_length=10, blank=True, null=True)
    flag_2 = models.CharField(max_length=10, blank=True, null=True)
    flag_3 = models.CharField(max_length=10, blank=True, null=True)
    assign_name = models.CharField(max_length=50, blank=True, null=True)  # 과제명
    step_annual = models.CharField(max_length=100, blank=True, null=True) # 연차
    organization= models.CharField(max_length=50, blank=True, null=True) # 조직
    pro_inst = models.CharField(max_length=50, blank=True, null=True) # 전문기관
    dev_period = models.CharField(max_length=50, blank=True, null=True) # 협약구분
    manager = models.CharField(max_length=50, blank=True, null=True) # 정산형태
    host_rnd_inst = models.CharField(max_length=50, blank=True, null=True) # 연구개발비지급구분
    class Meta:
        db_table = "RCMS_8_1"

class Rcms_8_2(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    rnd_inst = models.CharField(max_length=50, blank=True, null=True)  # 연구개발기관
    app_category = models.CharField(max_length=100, blank=True, null=True) # 기관 유형
    host_rnd_inst = models.CharField(max_length=50, blank=True, null=True) # 주관연구개발기관
    current_dev_period = models.CharField(max_length=50, blank=True, null=True) # 현재개발기간
    total_dev_period = models.CharField(max_length=50, blank=True, null=True) # 전체개발기간
    pro_inst = models.CharField(max_length=50, blank=True, null=True) # 전문기관
    agree_class = models.CharField(max_length=50, blank=True, null=True) # 협약구분
    settle_form = models.CharField(max_length=50, blank=True, null=True) # 정산형태
    rnd_cost_payment_assort = models.CharField(max_length=50, blank=True, null=True) # 연구개발비지급구분
    assign_agree_status = models.CharField(max_length=50, blank=True, null=True) # 과제/협약상태
    execute_status = models.CharField(max_length=50, blank=True, null=True) # 집행 상태
    research_fund_account = models.CharField(max_length=50, blank=True, null=True) # 연구비계좌
    class Meta:
        db_table = "RCMS_8_2"

class Rcms_8_3_1(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    tab_title = models.CharField(max_length=50) # 탭 제목용
    step = models.CharField(max_length=100, blank=True, null=True) # 단계
    annual = models.CharField(max_length=50, blank=True, null=True) # 연차
    part_class =  models.CharField(max_length=50, blank=True, null=True) # 참여구분
    rnd_inst = models.CharField(max_length=50, blank=True, null=True)  # 연구개발기관
    rnd_cost_payment_assort = models.CharField(max_length=50, blank=True, null=True) # 연구개발비지급구분
    total_cash_1 = models.CharField(max_length=50, blank=True, null=True) # 합계 현금
    total_kind_1 = models.CharField(max_length=50, blank=True, null=True) # 합계 현물
    gov_sup_rnd_cash = models.CharField(max_length=50, blank=True, null=True) # 정부지원연구개발비 현금
    inst_rnd_cash = models.CharField(max_length=50, blank=True, null=True) # 기관부담연구개발비 현금
    inst_rnd_kind = models.CharField(max_length=50, blank=True, null=True) # 기관부담연구개발비 현물
    local_gov_rnd_cash = models.CharField(max_length=50, blank=True, null=True) # 지자체분담금 현금
    local_gov_rnd_kind = models.CharField(max_length=50, blank=True, null=True) # 지자체분담금 현물
    total_cash_2 = models.CharField(max_length=50, blank=True, null=True) # 합계 현금
    total_kind_2 = models.CharField(max_length=50, blank=True, null=True) # 합계 현물
    direct_cost_cash = models.CharField(max_length=50, blank=True, null=True) # 직접비 현금
    direct_cost_kind = models.CharField(max_length=50, blank=True, null=True) # 직접비 현물
    indirect_cost_cash = models.CharField(max_length=50, blank=True, null=True) # 간접비 현금
    indirect_cost_kind = models.CharField(max_length=50, blank=True, null=True) # 간접비 현물
    commission_rnd_cash = models.CharField(max_length=50, blank=True, null=True) # 위탁연구개발비 현금
    commission_rnd_kind = models.CharField(max_length=50, blank=True, null=True) # 위탁연구개발비 현물
    class Meta:
        db_table = "RCMS_8_3_1"
class Rcms_8_3_2(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    tab_title = models.CharField(max_length=50) # 탭 제목용
    business_reg_num = models.CharField(max_length=100, blank=True, null=True) # 사업자등록번호
    rnd_inst = models.CharField(max_length=50, blank=True, null=True)  # 연구개발기관
    rnd_cost_payment_assort = models.CharField(max_length=50, blank=True, null=True) # 연구개발비지급구분
    participate_assort = models.CharField(max_length=50, blank=True, null=True) # 참여 구분
    non_profit = models.CharField(max_length=50, blank=True, null=True) # 비영리여부
    bank = models.CharField(max_length=50, blank=True, null=True) # 은행
    research_fund_account = models.CharField(max_length=50, blank=True, null=True) # 연구비계좌번호
    payment_whether = models.CharField(max_length=50, blank=True, null=True) # 대납여부
    pro_inst = models.CharField(max_length=50, blank=True, null=True) # 전문기관
    innovation_act_whether = models.CharField(max_length=50, blank=True, null=True) # 혁신법대상여부
    annual_leave_report = models.CharField(max_length=50, blank=True, null=True) # 연차사용보고여부
    class Meta:
        db_table = "RCMS_8_3_2"
class Rcms_8_3_3(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    tab_title = models.CharField(max_length=50) # 탭 제목용
    rnd_inst = models.CharField(max_length=50, blank=True, null=True)  # 연구개발기관
    participate_assort = models.CharField(max_length=50, blank=True, null=True) # 참여 구분
    name = models.CharField(max_length=50, blank=True, null=True) # 이름
    birth_date = models.CharField(max_length=50, blank=True, null=True) # 생년월일
    foreign_dist = models.CharField(max_length=50, blank=True, null=True) # 내/외국인 구분
    labor_cost_rate = models.CharField(max_length=50, blank=True, null=True) # 인건비계상률
    start_date = models.CharField(max_length=50, blank=True, null=True) # 참여시작일
    end_date = models.CharField(max_length=50, blank=True, null=True) # 참여종료일
    employ_type = models.CharField(max_length=50, blank=True, null=True) # 채용형태
    class Meta:
        db_table = "RCMS_8_3_3"
class Rcms_8_3_4(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    tab_title = models.CharField(max_length=50) # 탭 제목용
    inst = models.CharField(max_length=50, blank=True, null=True)  # 기관
    inst_role = models.CharField(max_length=50, blank=True, null=True) # 기관 역할
    name = models.CharField(max_length=50, blank=True, null=True) # 이름
    position = models.CharField(max_length=50, blank=True, null=True) # 인력역할
    res_fund_execute_auth = models.CharField(max_length=50, blank=True, null=True) # 연구비집행권한
    class Meta:
        db_table = "RCMS_8_3_4"

class Rcms_8_4(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    tab_title = models.CharField(max_length=50) # 탭 제목용
    name = models.CharField(max_length=50, blank=True, null=True)  # 성명
    part_class =  models.CharField(max_length=50, blank=True, null=True) # 참여구분
    res_fund_execute_auth = models.CharField(max_length=50, blank=True, null=True) # 연구비집행권한
    whether_use = models.CharField(max_length=50, blank=True, null=True) # 사용여부
    identity = models.CharField(max_length=50, blank=True, null=True) # ID
    birth_date = models.CharField(max_length=50, blank=True, null=True) # 생년월일
    whether_receive = models.CharField(max_length=50, blank=True, null=True) # 수신여부
    class Meta:
        db_table = "RCMS_8_4"

class Rcms_8_5(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    tab_title = models.CharField(max_length=50) # 탭 제목용
    assort = models.CharField(max_length=50, blank=True, null=True)  # 구분
    card_company =  models.CharField(max_length=50, blank=True, null=True) # 카드사
    card_num = models.CharField(max_length=50, blank=True, null=True) # 카드번호
    validity_period = models.CharField(max_length=50, blank=True, null=True) # 유효기간
    payment_bank = models.CharField(max_length=50, blank=True, null=True) # 결제은행
    payment_account_num = models.CharField(max_length=50, blank=True, null=True) # 결제계좌번호
    payment_date = models.CharField(max_length=50, blank=True, null=True) # 결제일
    reg_date = models.CharField(max_length=50, blank=True, null=True) # 등록일자
    reg_status = models.CharField(max_length=50, blank=True, null=True) # 등록상태
    whether_reg = models.CharField(max_length=50, blank=True, null=True) # 등록여부
    class Meta:
        db_table = "RCMS_8_5"

class Rcms_8_6(models.Model):
    account = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)
    tab_title = models.CharField(max_length=50) # 탭 제목용
    issue_date = models.CharField(max_length=50, blank=True, null=True)  # 발급일시
    issue_reason =  models.CharField(max_length=50, blank=True, null=True) # 발급사유
    req_amount = models.CharField(max_length=50, blank=True, null=True) # 요청금액
    bank = models.CharField(max_length=50, blank=True, null=True) # 은행
    virtual_account_num = models.CharField(max_length=50, blank=True, null=True) # 가상계좌번호
    depositor = models.CharField(max_length=50, blank=True, null=True) # 예금주
    process_status = models.CharField(max_length=50, blank=True, null=True) # 처리상태
    deposit_date = models.CharField(max_length=50, blank=True, null=True) # 입금일시
    deposit_deadline = models.CharField(max_length=50, blank=True, null=True) # 입금마감일
    request_reason = models.CharField(max_length=50, blank=True, null=True) # 요청사유
    refusal_reason = models.CharField(max_length=50, blank=True, null=True) # 승인거부사유
    pay_exclusion_status = models.CharField(max_length=50, blank=True, null=True) # 납부제외상태
    class Meta:
        db_table = "RCMS_8_6"

