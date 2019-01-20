import xdj

@xdj.Controller(
    url="",
    template="index.html"
)
class IndexController(xdj.BaseController):

    def on_get(self,model):
        """
        get view
        :param model:
        :return:
        """
        return self.render(model)