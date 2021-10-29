from django.shortcuts import render

from .models import  Asset,Area,Belong
from  .api import get_rack_rail_template,logger,json_returner,pages

from django.db.models import Q

from django.views.generic import View
from django.contrib.admin.models import LogEntry,ADDITION,DELETION,CHANGE,ContentType

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def search(request):
    key = request.GET.get('key')
    error_msg = ''
    if not key:
        error_msg = "请输入关键词"
        return render(request, 'index.html', {'error_msg': error_msg})

    elif request.user.is_authenticated: #判断是否登录
        assets = Asset.objects.filter(
                Q(hostname__icontains=keyword) |
                Q(ipadd__contains=keyword) |
                Q(sn__icontains=keyword) )

        return render(request, 'index.html', locals())
    else:
        error_msg = mark_safe('''<div class="alert alert-info">
				 <button type="button" class="close" data-dismiss="alert">×</button>
				<h4>
					提示!
				</h4> <strong>搜索失败!</strong> 请先登录 ...
			</div>''')
        return render(request, 'index.html', {'error_msg': error_msg})





@login_required
def index(request):

    """
    首页
    :param request:
    :return:
    """
    assets_list = Asset.objects.all()

    if request.user.is_superuser:
        admin = True

    return render(request, 'assets/index.html', locals())


def dashboard(request):

    """
    :param request:
    :return:
    """
    assets_list = Asset.objects.all()
    assets_bad = Asset.objects.filter(status=2)
    users = User.objects.all()



    if request.user.is_superuser:
        admin = True

    return render(request, 'assets/dashboard.html', locals())






class assets(View):
    """
    cbv 基于类视图
    """
    def get(self, request):
        server_id = request.GET.get('id','')
        keyword = request.GET.get('keyword','')


        if server_id:
            assets = Asset.objects.filter(id=server_id)


        elif keyword:
            assets = Asset.objects.filter(
                Q(hostname__icontains=keyword) |
                Q(ipadd__contains=keyword) |
                Q(sn__icontains=keyword)
            )

        else:
            assets = Asset.objects.all()
        # return render_to_response('assets/index.html', locals(),context_instance=RequestContext(request))

        assets_list, p, assets, page_range, current_page, show_first, show_end = pages(assets, request)

        if request.user.is_superuser:
            admin = True
        return render(request,'assets/index.html', locals())


class cabinet(View):
    """
    利用插件获取 机架图
    :param request:
    :param asset_id:
    :return:
    """
    # asset = get_object_or_404(Asset, id=asset_id)
    def get(self, request):
        server_id = request.GET.get('id','')
        area_id = request.GET.get('area_id','')
        keyword = request.GET.get('keyword','')
        assets = ''
        area = ''

        if server_id:
            server = Asset.objects.filter(id=server_id)
            return json_returner(server)


        # area_all = list (Area.objects.filter(needed_cabinet=True))
        _area_all = set([i.area for i in Asset.objects.filter(area__needed_cabinet=True)])
        area_all = list(_area_all)



        if area_id:

            area = Area.objects.get(id=area_id)
            if keyword :
                assets = Asset.objects.filter(
                    Q(hostname__icontains=keyword) |
                    Q(ipadd__contains=keyword) |
                    Q(sn__icontains=keyword)
                )

            # all_asset = Asset.objects.filter(area=area_id)
            # cabinets = set(list(filter(None, ([i.cabinet for i in all_asset]))))
            #

            rack_rail_template = get_rack_rail_template(area,assets)



        if request.user.is_superuser:
            admin = True
        return render(request,'assets/cabinet.html', locals())


class assetDetail(View):
    """docstring for AssetDetail"""
    def get(self, request):
        try:
            server_id = request.GET.get('id','')
            asset = Asset.objects.get(id=server_id)
            _all_asset_logs = LogEntry.objects.filter(content_type=ContentType.objects.get(model__iexact='Asset'))
            asset_logs = _all_asset_logs.filter(object_id=server_id)
            # for log in asset_logs:
                # setattr(log, )
            for log in asset_logs:
                log_dict = {}
                if log.action_flag == ADDITION: flag = "新增"
                if log.action_flag == DELETION: flag = "删除"
                if log.action_flag == CHANGE: flag = "修改"
                setattr(log, 'action_flag', flag)
        except Exception as e:
            logger.error(e)
            return HttpResponse('error')


        if request.user.is_superuser:
            admin = True
        return render(request,'assets/detail.html', locals())


class getCorp(View):
    """docstring for getCorp"""
    def get(self, request):
        try:
            corp_id = request.GET.get('corp_id','')
            corp = Belong.objects.filter(id=corp_id)
            return json_returner(corp)
        except Exception as e:
            return "faild"