$(function(){
	$("#collectNodeList").datagrid({
		url:urls['getCollectNodeList'],
		toolbar:'#collectNodeToolBar',
		method:'post',
		autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'cjdomid',title:'节点id',width:'10%',hidden:true},
			{field:'cjdomname',title:'节点名称',width:'25%', showTitle:true },
			{field: 'region', title: '所属区域', width: '25%'},
			{field:'statetype',title:'节点状态',width:'25%',},
			{field:'oper',title:'查看任务详情',width:'23%',formatter:operCollectNode},
		]],

		onLoadSuccess:function(){
			$('.detailMore').linkbutton({iconCls: 'icon-more'});
		}
	})

	search('#collectNodeList', '#collectNodeSearchBox');
})

function operCollectNode(v,r,i){
	return '<a data-hover="查看详情" title="查看详情" class="detailMore" href="javascript:collectNodeDetail('+i+');"  data-options="" style="margin:8px 5px;"></a>'
}

function collectNodeDetail(i){
	var data = getEditData(i, '#collectNodeList');
	if(data == false){
		return; 
	}
	console.log(data);
	$.get('/sjyglIndex/',{data:data.cjdomid},function(msg){
		window.open('/sjyglIndex/newSjygl/','_blank')
		$("#collectNodeList").datagrid('unselectAll')
	})
}

function addCollectNode() {
	$("#domForm").form('submit', {
		url: "/cjjdglIndex/addjdTask/",
		onSubmit: function () {
			return true
		},
		success: function (data) {
			$('#domForm').form('reset');
			$("#domDialog").dialog('close');
			$("#collectNodeList").datagrid('reload');

		}
	});
}
//增加按钮的点击提交事件
/*function addDom() {
	console.log(123);
	$('#domForm').form('submit', {
		url: "/domForm/domData/",
		onSubmit: function () {
			var isValid = $(this).form('validate');
			console.log(isValid);
			return isValid;
		},
		success: function (data) {
			$('#domDialog').dialog('close');
			$('#collectNodeList').datagrid('reload');
		}
	});
}*/

function cancelDom() {
	$('#domDialog').dialog('close');
}

function delCollectNode() {
	var data = $("#collectNodeList").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else{
	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].cjdomid + ',';
			}
			ids = ids.substr(0, ids.length -1);
			$.get('/cjjdglIndex/cjjdglDel/',{data:ids},function(msg){
				$("#collectNodeList").datagrid('reload');
			})
		}
	})
		}
}

function editCollectNode() {
	var row=$("#collectNodeList").datagrid('getSelections');
	if(row.length==0||row.length>1) {
		$.messager.confirm('警告', '请选择一条数据', 'warning');
	}
		else{
		linkbutton_click('open_dialog',{dialog:'#changeDom'});
		$('.cjdomname_change').val(row[0].cjdomname);
		$('.cjregion_change').val(row[0].region);
		$('.cjdomid_change').val(row[0].cjdomid);
	}
}

function preserved() {
	$('#change_list').form('submit', {
		url: "/cjjdglIndex/changeDom/",
		onSubmit: function () {
			return $(this).form('validate');
		},
		success: function (data) {
			$('#domDom').form('reset');
			$('#changeDom').dialog('close');
			$('#collectNodeList').datagrid('reload');
		}
	});
}
/*
function domDetail() {
	var data = $("#collectNodeList").datagrid('getSelected');
	dataid=data.cjdomid;
	console.log(dataid);

}

*/