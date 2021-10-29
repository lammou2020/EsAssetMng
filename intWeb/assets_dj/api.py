
from django.http import HttpResponse, Http404
from django.db.models.query import QuerySet
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Asset   #,group_by,Area


from django.db.models.query import QuerySet




import logging
import json
import copy

logger = logging.getLogger("bench")


class AmpException(Exception):
    def __init__(self, msg, fault):
        self.message = str(msg)
        self.fault = str(fault)

    def __str__(self):
        return "[%s]: %s" % (self.fault, self.message)


def set_log(level, filename='Asset.log'):
    """
    return a log file object
    根据提示设置log打印
    """
    log_file = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(log_file):
        os.mknod(log_file)
        # os.chmod(log_file, 0777)
    log_level_total = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}
    logger_f = logging.getLogger('AssetMP')
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)d:%(funcName)s] - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f


# logger = set_log(LOG_LEVEL)

def json_returner(data=''):
    if isinstance(data, (QuerySet, dict)):
        ret = serializers.serialize("json", data)
        return HttpResponse(json.dumps({'status': 'success', 'message': ret}))
    return HttpResponse(json.dumps({'status': 'failed', 'message': data}))


def  rack_template(area,assets):
    """
    :param area:
    :param assets:
    :return:
    """
    #all_assets = Asset.objects.filter(area=area)
    # 当前区域所有资产
    if assets:
        all_assets = assets





def get_rack_rail_template(area, assets):
    """
    paramter: Area_
    """

    all_assets = Asset.objects.filter(area=area)

    if assets:
        all_assets = assets


    # 根据机架分组

    # cabinets = group_by(all_assets, 'cabinet')
    # area_asset = Asset.objects.filter(area=area_id)
    cabinets = set(list(filter(None, ([i.cabinet for i in all_assets]))))

    cabinets_template = ""

    logger.debug("all_assets[%s] to render", all_assets)
    for cabinet in sorted(cabinets):
        all_cab_ass = all_assets.filter(cabinet=cabinet)

        rest = []
        s = """
        <div name="{0}"  class="rack">
            <table class="data-table" id="data_table">
                <tbody>
                    <tr>
                        <td><p class="rackname">{0}</p></td>
                    </tr>
        """.format(cabinet)

        s1 = """
                    <tr>
                        <td><img src="/static/cabinetmaps/server1U.png" class="timg" id="%s" data-name="img"></td>
                    </tr>
        """
        s2 = """
                    <tr>
                        <td rowspan="2" class="u2server"><img src="/static/cabinetmaps/server.png" class="timg" id="%s" data-name="img"></td>
                    </tr>
        """
        s4 = """
                    <tr>
                        <td rowspan="4" class="u4server"><img src="/static/cabinetmaps/r930.png" class="timg" id="%s" data-name="img"></td>
                    </tr>
        """
        st = """
                    <tr>
                        <td><img src="/static/cabinetmaps/net.png" class="timg" id="%s" data-name="img"></td>
                    </tr>
        """
        sf = """
                    <tr>
                        <td><img src="/static/cabinetmaps/fw.png" class="timg" id="%s" data-name="img"></td>
                    </tr>
        """
        sm = """
                    <tr>
                        <td></td>
                    </tr>    
        """

        sb = """
                    <tr>
                        <td><img src="/static/cabinetmaps/blank.png" class="timg"></td>
                    </tr>
        """

        sn = "</tbody></table></div>"

        count_rail = 41 # 41
        # 下次用递归函数改写下
        while count_rail >= 1:
            flag = 0
            for ass in all_cab_ass:
                if count_rail == ass.railnum:
                    flag = 1
                    # if ass.railnum == 35: print ass,"=============="
                    if ass.get_asset_type_display() ==   '物理机':
                        if ass.get_uhight_display() == 1:
                            _s1 = copy.deepcopy(s1)
                            _s1 = _s1 % ass.id
                            s += _s1
                            count_rail -= 1
                        elif ass.get_uhight_display() == 2:
                            _s2 = copy.deepcopy(s2)
                            _s2 = _s2 % ass.id
                            s += _s2 + sm
                            count_rail -= 2
                        elif ass.get_uhight_display() == 4:
                            _s4 = copy.deepcopy(s4)
                            _s4 = _s4 % ass.id
                            s += _s4 + sm * 3
                            count_rail -= 4
                    elif ass.get_asset_type_display() ==  "交换机" :
                        _st = copy.deepcopy(st)
                        _st = _st % ass.id
                        s += _st
                        count_rail -= 1
                    elif ass.get_asset_type_display() in ['路由器','防火墙']:
                        _sf = copy.deepcopy(sf)
                        _sf = _sf % ass.id
                        s += _sf
                        count_rail -= 1
                    else:
                        return False
            if flag == 0:
                s += sb
                count_rail -= 1
            print (count_rail, "-----count_rail ------")

        s += sn

        cabinets_template += '\n' + s
        logger.debug(cabinets_template)
    return cabinets_template


def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total
    return range(min_page, max_page + 1)


def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """
    per_page = request.GET.get("per_page", 20)
    paginator = Paginator(post_objects, per_page)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0

    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

        # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end







