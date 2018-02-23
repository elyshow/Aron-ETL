$(function(){
	var b = document.getElementById("tlen").value;
	var s = b - 0;
	s = s*1;
	var b1 = document.getElementById("clen").value;
	var arr=new Array(s);
	var tb = document.getElementById("mytable");
	var rowNum=tb.rows.length;
	var m = 0;
	for (var a=0;a<=b1;a+=s){
		m++;
		var x = 0;
		for(var i=a;i<b1;i+=1) {  
		    arr[x]=document.getElementById("select").options[a+x].text;
		    x = x+1;
		}
		for(j=0;j<s;j++){
				var valueTd=document.getElementById("mytable").rows[m].cells[j];
				valueTd.innerHTML=arr[j];
		}
	}
})

$(function(){
        var $table=$('table');//获取表格对象
        var currentPage=0;//设置当前页默认值为0
        var pageSize=20;//设置每一页要显示的数目
        $table.bind('paging', function () {
            $table.find('tbody tr').hide().slice(currentPage*pageSize,(currentPage+1)*pageSize).show();
        //先将tbody中所有的行隐藏，再通过slice结合当前页数和页面显示的数目展现数据
        });
        var sumRows=$table.find('tbody tr').length;//获取数据总行数
        var sumPages=Math.ceil(sumRows/pageSize);//得到总页数
        var $pager=$('<div class="page"></div>');
        for(var pageIndex=0;pageIndex<sumPages;pageIndex++){
           $('<a href="#"><span style="font-size:18px;">'+(pageIndex+1)+'</span></a>').bind("click",{"newPage":pageIndex},function(event){
                currentPage=event.data["newPage"];
                $table.trigger("paging");
               //为每一个要显示的页数上添加触发分页函数
            }).appendTo($pager);
            $pager.append("&nbsp;&nbsp;&nbsp;&nbsp;");
        }
        $pager.insertAfter($table);
        $table.trigger("paging");
    });