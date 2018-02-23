
$(function(){
	$("#dataTypeList").datagrid({
		url:'/standardIndex/dataTypeIndex/typeData/',
		// rownumbers:true,
		autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'dataname',title:'信息名称',width:'20%',},
			{field:'mainword',title:'关键字',width:'17%',},
			{field:'standardcode',title:'标准代码',width:'15%',},
			{field:'classify',title:'所属分类',width:'14%',},
			{field:'userecognize',title:'使用单位',width:'14%',},
			{field:'oper',title:'操作',width:'18%',formatter:func},
		]],
		onLoadSuccess:function() {
			$('.stateEditor').linkbutton({
				iconCls: 'icon-edit',
			});
		}
	})
	 $('#dataSearchBox').searchbox({
        prompt:'请输入信息名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#dataTypeList').datagrid('load', {condition:v,type:1});
        }
    })
})

function func(v, r, i) {
	return '<a data-hover="编辑" title="编辑" class="stateEditor" href="javascript:editData(' + r.id + ');"  data-options="" style="margin:8px 5px;"></a>'


}


function editData(id) {
	    $('input[name="save_type"]').val('edit');
        linkbutton_click('open_dialog', {dialog:'#dataTypedialog'});
	    $.post('/standardIndex/dataTypeIndex/dataEdit/', {data: id}, function (ret) {
				$("#dataid").val(ret[0].id);
				$("#dataname").val(ret[0].dataname).validatebox('validate');
				$("#mainWord").val(ret[0].mainword);
				$("#standardCode").val(ret[0].standardcode);
				$("#classify").val(ret[0].classify);
				$("#useRcognize").val(ret[0].userecognize);
					})
}


function dataClose() {
	$('#dataTypedialog').dialog('close');
	$('#dataTypedialogEdit').dialog('close');
}

function AddData() {
	$('input[name="save_type"]').val('add')
	   $('#dataTypeForm').form('reset');
	    linkbutton_click('open_dialog' ,{dialog: '#dataTypedialog'});
}

function dataTypeAdd() {
	$('#dataTypeForm').form('submit', {
		url: "/standardIndex/dataTypeIndex/addInfoData/",
		onSubmit: function () {
			console.log($(this).form('validate'));
			return $(this).form('validate');
		},
		success: function (data) {
			$('#dataTypedialog').dialog('close');
			$('#dataTypeList').datagrid('reload');
		}
	});
}


function delData() {
    var data = $("#dataTypeList").datagrid('getSelections');
	if (data.length == 0) {
		$.messager.alert('警告', '请选择至少一条数据', 'warning');
	}
	else {
		$.messager.confirm('确认删除框', '是否确定删除选中记录?', function (ok) {
			if (ok) {
				var ids = '';
				for (var i in data) {
					ids += data[i].id + ',';
				}
				ids = ids.substr(0, ids.length - 1);
				console.log(ids)
				$.post('/standardIndex/dataTypeIndex/dataDel/', {data: ids}, function (msg) {
					$('#dataTypeList').datagrid('reload');
				})
			}
		})
	}
}