var UiUtils={}
function $$(v){
    function _view(view){
        this.objView=view
    }
    _view.prototype.getById=function(id){
        return sap.ui.getCore().byId(this.objView.getId()+"--"+id)
    }
    _view.prototype.setData=function(id,data){
        var x= new sap.ui.model.json.JSONModel(data)

        this.getById(id).setModel(x);
    }
    return new _view(v);
}

UiUtils.getContent=function(txt){
    var i = txt.indexOf("<script>");
    scripts = []
    while(i>-1){
        var j= txt.indexOf("</script>")
        var script = txt.substring(i+"<script>".length,j)
        scripts.push(script);
        txt =txt.substring(0,i)+txt.substring(j+"</script>".length,txt.length)
        i = txt.indexOf("<script>");
    }
    return {
        scripts:scripts,
        content:txt
    }
}
UiUtils.loadHtmlView=function(src,fn){
    $.ajax({
        url: src,
        // data: data,
        method:"GET",
        success: function(res){
            debugger;
        },
        dataType: "text/html",
        error:function(res){
            if (res.status!=200){
                debugger;
                console.log(res);
                var x=window.open();
                x.document.open().write(res.responseText);
                fn(res.responseText)
            }
            else{
                var view_name=src
                var info = UiUtils.getContent(res.responseText);
                var ctrl ={}
                
                for(var i=0;i<info.scripts.length;i++){
                    _fn=eval(info.scripts[i]);
                    var _fx = _fn();
                    var k = Object.keys(_fx)
                    for(var i=0;i<k.length;i++){
                        ctrl[k[i]]=_fx[k[i]]
                    }
                }
                var fx=sap.ui.core.mvc.Controller.extend(view_name,ctrl)
                var oView = sap.ui.view({
                    type: sap.ui.core.mvc.ViewType.XML,
                    viewContent: info.content,
                    controller: new fx()
                });
                fn(undefined,oView);
                
            }
            
        }
      });
    
}
