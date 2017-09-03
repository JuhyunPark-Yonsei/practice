from django.http import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView
import os
from django.conf import settings

class PostListView1(View):
    def get_template_string(self):
        return '''
                <h1>Web App</h1>
                <p>real time 실시간 {var}을 만드는 것이 목표입니다.</p>
                '''

    def get(self, request):
        title="채팅앱"
        html=self.get_template_string().format(var=title)
        return HttpResponse(html)


class PostListView2(TemplateView):
    template_name = "prac/post_list2.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["var"]="채팅앱"
        return context


class PostListView3(View):
    def get(self, request):
        return JsonResponse({
            "msg": "Django Framework",
            "items": ["chat", "web socket", "channels", "blog"],
        }, json_dumps_params={"ensure_ascii": False})


class ExcelDownloadView(View):
    def get(self, request):
        filepath = os.path.join(settings.BASE_DIR, 'SampleXLSFile_19kb.xls')
        filename = os.path.basename(filepath)
        with open(filepath, 'rb') as f:
            response = HttpResponse(f, content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "attachment"
            filename = "{}".format(filename)
            return response
