$(function(){
		$("#comboBelongto").combobox({
		url:'/sjyglIndex/sjyglBelongto/',
		textField:'recognname',
		valueField:'recognid',
	});
	$("#comboBelongType").combobox({
		url:'/sjyglIndex/sjyglBelongType/',
		textField:'dataid',
		valueField:'dataname',
	});

	$("#sjyglList").datagrid({
		url:'/sjyglIndex/sjygl/',
		autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
			// {field:'taskid',title:'任务id',width:'10%',},
			{field:'taskname',title:'任务名称',width:'20%',},
			{field:'tasktype',title:'任务类型',width:'15%',
			formatter: function(value,row,index){
				if (value==1){
					return '普通文件本地上传';
				}
				if (value==2)
				{
					return '数据库文件';
				}
				if (value==3)
				{
					return '数据接口';
				}
				if (value==4)
				{
					return 'API接口';
				}
				if (value==5)
				{
					return '普通文件远程下载';
				}
			  }
			},
			{field:'run_state',title:'执行频率',width:'20%',},
			{field:'taskstate',title:'当前任务状态',width:'15%',
			formatter: function(value,row,index){
				if (value==0){
					return '启用';
				}
				if (value==1)
				{
					return '停用';
				}
				if (value==2)
				{
					return '正在采集';
				}
			}},
			{field:'oper',title:'操作',width:'28%',formatter:stateFunc},

         ]],
		    onLoadSuccess:function(){
                 // 图标
				$('.stateStop').linkbutton({
					iconCls: 'icon-no',
				});
				$('.stateStart').linkbutton({
					iconCls: 'icon-ok'
				});
				$('.runNow').linkbutton({
					iconCls: 'icon-tip'
				});
				stateButton()
        },
	})

//停用 启用 立即执行
function stateFunc(v,r,i){
	str = ''
	if(r.tasktype == '1' || r.tasktype =='2' || r.tasktype == '5' ){
		str = '<a class="stateStop" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;">停用</a>'+
		    '<a class="stateStart" href="javascript:;"  data-options="disabled:true" style="margin:8px 5px;">启用</a>'+
			'<a class="runNow" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;">立即执行</a>'
	}else if(r.taskstate == '0'){
		str = '<a class="stateStop" href="javascript:;" onclick="stateStop(\''+r.taskid+'\')" data-options=" " style="margin:8px 5px;">停用</a>'+
		    '<a class="stateStart" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;">启用</a>'+
			'<a class="runNow" href="javascript:;" onclick="runNow(\''+r.taskid+'\')" data-options="" style="margin:8px 5px;">立即执行</a>'
	}else if(r.taskstate == '1'){
		str = '<a class="stateStop" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;">停用</a>'+
		    '<a class="stateStart" href="javascript:;" onclick="stateStart(\''+r.taskid+'\')" data-options="" style="margin:8px 5px;">启用</a>'+
			'<a class="runNow" href="javascript:;" data-options="disabled:true" style="margin:8px 5px;">立即执行</a>'
	}else if(r.taskstate == '2'){
		str = '<a class="stateStop" href="javascript:;" onclick="stateStop(\''+r.taskid+'\')" data-options=" " style="margin:8px 5px;">停用</a>'+
		    '<a class="stateStart"  href="javascript:;" onclick="stateStart(\''+r.taskid+'\')" data-options=" " style="margin:8px 5px;">启用</a>'+
			'<a class="runNow" href="javascript:runNow();" onclick="runNow(\''+r.taskid+'\')" data-options=" " style="margin:8px 5px;">立即执行</a>'
	}
    return str;
}



function stateButton(){
    var dataAll = $('#sjyglList').datagrid('getSelected');
}

	$('#taskSearchBox').searchbox({
        	prompt:'请输入任务名称搜索',
        	height:24,
        	width:200,
        	searcher:function(v,n){
           		$('#sjyglList').datagrid('load', {condition:v,type:1});
				console.log(v);
				console.log('111');
        }
    })

})

//停用
function stateStop(dataid){
	$.get('/taskTypeDialog/stateStop/',{data:dataid},function(msg){
		$("#sjyglList").datagrid('reload');
	})
}
// 启用
function stateStart(dataid){
	$.get('/taskTypeDialog/stateStart/',{data:dataid},function(msg){
		$("#sjyglList").datagrid('reload');
	})
}
//立即执行
function runNow(dataid){
	$.get('/taskTypeDialog/xiugai/',{data:dataid},function (ret) {
		$('#sjyglList').datagrid('reload');
		console.log(ret)
		$.get('/taskTypeDialog/runNow/',{data:dataid},function(msg){
					console.log(888)
    	$("#sjyglList").datagrid('reload');
	})
	})
}


function sjyglDel() {
	var data = $("#sjyglList").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else {
		$.messager.confirm('确认删除框', '是否确定删除选中记录?', function (ok) {
			if (ok) {
				var ids = '';
				for (var i in data) {
					ids += data[i].taskid + ',';
				}
				ids = ids.substr(0, ids.length - 1);
				console.log(ids)
				$.get('/sjyglIndex/sjyglDel/', {data: ids}, function (msg) {
					$("#sjyglList").datagrid('reload');
				})
			}
		})
	}
}

function collectLogIndex() {
	console.log(111)
	window.open('/collectLogIndex/','_blank');

}
