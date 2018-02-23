$(function(){
	$("#busList").datagrid({
		url:'/standardIndex/busCodeIndex/busCode/',
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'codename',title:'代码名称',width:'35%',},
			{field:'codetable',title:'代码表',width:'35%',},
			{field:'registertime',title:'注册时间',width:'28%',},
			// {field:'oper',title:'操作',width:'10%',formatter:func},
		]]
	})
	 $('#busSearchBox').searchbox({
        prompt:'请输入代码表搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#busList').datagrid('load', {condition:v,type:1});
			console.log(v);
			console.log('111');
        }
    })
})


// function func(v,r,i){
// 	return  '<a class="easyui-linkbutton" href="javascript:;" data-options="iconCls:\'icon-edit\'">编辑</a>'
// }

function busAdd() {
	$("#busForm").form('submit', {
		url: "/standardIndex/busCodeIndex/addBusCode/",
		onSubmit: function () {
			return $(this).form('validate');
		},
		success: function (data) {
			$("#busDialog").dialog('close');
			$("#busList").datagrid('reload');

		}
	});
}

function busDel() {
	var data = $("#busList").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else {
		$.messager.confirm('确认删除框', '是否确定删除选中记录?', function (ok) {
			if (ok) {
				var ids = '';
				for (var i in data) {
					ids += data[i].codeid + ',';
				}
				ids = ids.substr(0, ids.length - 1);
				$.post('/standardIndex/busCodeIndex/delBusCode/', {data: ids}, function (msg) {
					$("#busList").datagrid('reload');
				})
			}
		})
	}
}